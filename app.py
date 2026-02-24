"""
Sistema de Monitoreo de Red - Instituto Tecnológico de Oaxaca
=============================================================

Aplicación Flask que proporciona:
- Croquis de topología: Core -> Switches -> Teléfonos (VLAN 23)
- Estado de ping (verde/rojo) para teléfonos y switches
- Mapa del campus con edificios y teléfonos
- CRUD de teléfonos, edificios y usuarios
- Dashboard con extensión por edificio
- Login con roles: admin (CRUD completo) y monitor (solo lectura)

Modo demo: Si MySQL no está disponible, usa datos de prueba (IPs públicas
como 8.8.8.8 para probar ping). Usuarios demo: admin/admin, operador/operador.
"""
import os
import subprocess
import platform
from datetime import datetime
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from conexion_db import get_conexion

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambiar-en-produccion-clave-secreta-redes")

# Usuarios demo: usuario -> (nombre, contraseña_plana, rol)
DEMO_USUARIOS = {
    "admin": ("Administrador", "admin", "admin"),
    "operador": ("Operador", "operador", "monitor"),
}

# --- Modo DEMO (cuando no hay MySQL): datos de prueba para ver croquis y ping ---
DEMO_CORE = [{"id": 1, "nombre": "Core Principal (demo)", "ip_management": "192.168.1.1"}]
# Coordenadas en campus Tecnológico de Oaxaca (Av. Víctor Bravo Ahuja)
DEMO_SWITCHES = [
    {"id": 1, "core_id": 1, "nombre": "Switch Demo A", "ip_management": "192.168.1.10", "ubicacion": "Edificio A", "lat": 17.0698, "lng": -96.7256},
    {"id": 2, "core_id": 1, "nombre": "Switch Demo B", "ip_management": "192.168.1.11", "ubicacion": "Edificio B", "lat": 17.0690, "lng": -96.7250},
]
DEMO_EDIFICIOS = [
    {"id": 1, "nombre": "Edificio A", "ubicacion": "Edificio A", "lat": 17.0698, "lng": -96.7256, "switch_id": 1},
    {"id": 2, "nombre": "Edificio B", "ubicacion": "Edificio B", "lat": 17.0690, "lng": -96.7250, "switch_id": 2},
]
# Teléfonos de prueba (VLAN 23); edificio_id para mapa
DEMO_TELEFONOS = [
    {"id": 1, "switch_id": 1, "edificio_id": 1, "extension": "1001", "ip": "8.8.8.8", "ubicacion": "Prueba Google DNS", "modelo": "Demo IP", "vlan_id": 23, "lat": 17.0778, "lng": -96.7442},
    {"id": 2, "switch_id": 1, "edificio_id": 1, "extension": "1002", "ip": "8.8.4.4", "ubicacion": "Prueba Google DNS 2", "modelo": "Demo IP", "vlan_id": 23, "lat": 17.0776, "lng": -96.7440},
    {"id": 3, "switch_id": 2, "edificio_id": 2, "extension": "2001", "ip": "1.1.1.1", "ubicacion": "Prueba Cloudflare", "modelo": "Demo IP", "vlan_id": 23, "lat": None, "lng": None},
    {"id": 4, "switch_id": 2, "edificio_id": 2, "extension": "2002", "ip": "10.255.255.254", "ubicacion": "Prueba sin respuesta", "modelo": "Demo IP", "vlan_id": 23, "lat": None, "lng": None},
]
# Estado del ping en demo (id -> ok); se actualiza al pulsar "Actualizar ping a todos"
demo_ping_state = {}  # telefonos: id -> ok
demo_ping_at = {}     # telefonos: id -> datetime
demo_switch_ping_state = {}  # switches: id -> ok
demo_switch_ping_at = {}     # switches: id -> datetime


def asegurar_admin_si_vacio():
    """Si hay MySQL y no hay usuarios, crea admin/admin con rol admin."""
    if usar_demo():
        return
    count = ejecutar_sql("SELECT COUNT(*) AS n FROM usuarios")
    if not count or count[0]["n"] == 0:
        conn = get_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO usuarios (usuario, password_hash, nombre, rol, activo) VALUES (%s, %s, %s, 'admin', 1)",
                    ("admin", generate_password_hash("admin"), "Administrador"),
                )
                conn.commit()
                cursor.close()
            except Exception as e:
                print(f"Crear admin: ejecuta ALTER TABLE usuarios ADD COLUMN rol VARCHAR(20) DEFAULT 'admin'; y reintenta. {e}")
            finally:
                conn.close()


def usar_demo():
    """True si no hay MySQL disponible: usamos datos de prueba."""
    conn = get_conexion()
    if conn:
        conn.close()
        return False
    return True


def ejecutar_sql(query, params=None, fetch=True):
    """
    Ejecuta una consulta SQL contra MySQL.
    Args:
        query: Consulta SQL (placeholders %s).
        params: Tupla de parámetros (opcional).
        fetch: True=devuelve fetchall(), False=commit y devuelve lastrowid.
    Returns:
        Lista de dicts si fetch=True, lastrowid si fetch=False, None si error.
    """
    conn = get_conexion()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            out = cursor.fetchall()
        else:
            conn.commit()
            out = cursor.lastrowid
        cursor.close()
        return out
    except Exception as e:
        print(f"SQL error: {e}")
        return None
    finally:
        conn.close()


def hacer_ping(ip, timeout=2):
    """
    Ejecuta ping a una IP usando subprocess.
    Args:
        ip: Dirección IP a probar.
        timeout: Segundos de espera (default 2).
    Returns:
        True si el host responde, False en caso contrario.
    """
    is_windows = platform.system().lower() == "windows"
    if is_windows:
        # Windows: -n número de paquetes, -w timeout en ms
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), ip]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout), ip]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 2)
        return r.returncode == 0
    except Exception:
        return False


def usuario_logueado():
    """True si hay un usuario autenticado en la sesión."""
    return session.get("user_id") is not None


def es_admin():
    """True si el usuario actual tiene rol admin."""
    return session.get("user_rol") == "admin"


def requerir_admin():
    """
    Comprueba si el usuario actual es administrador.
    Returns:
        (response, status) si no es admin (403); None si sí es admin.
    """
    if not es_admin():
        return jsonify({"error": "Sin permisos. Solo administradores pueden realizar esta acción."}), 403
    return None


# =============================================================================
# Autenticación y rutas principales
# =============================================================================

@app.before_request
def requerir_login():
    if request.path == url_for("login") or request.path.startswith("/static"):
        return None
    if usuario_logueado():
        return None
    # API: devolver 401 para que el frontend redirija a login
    if request.path.startswith("/api/"):
        return jsonify({"error": "No autorizado. Inicia sesión."}), 401
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect(url_for("index"))
        return render_template("login.html")

    usuario = (request.form.get("usuario") or "").strip()
    password = request.form.get("password") or ""

    if not usuario:
        return redirect(url_for("login", error=1))

    if usar_demo():
        if usuario in DEMO_USUARIOS:
            dato = DEMO_USUARIOS[usuario]
            nombre, contra_plana, rol = dato[0], dato[1], dato[2] if len(dato) > 2 else "admin"
            if password == contra_plana:
                session["user_id"] = usuario
                session["user_name"] = nombre
                session["user_login"] = usuario
                session["user_rol"] = rol
                return redirect(url_for("index"))
        return redirect(url_for("login", error=1))

    asegurar_admin_si_vacio()
    row = ejecutar_sql(
        "SELECT id, usuario, password_hash, nombre, COALESCE(rol, 'admin') AS rol FROM usuarios WHERE usuario = %s AND activo = 1",
        (usuario,),
    )
    if not row:
        return redirect(url_for("login", error=1))
    if not check_password_hash(row[0]["password_hash"], password):
        return redirect(url_for("login", error=1))
    session["user_id"] = row[0]["id"]
    session["user_name"] = row[0].get("nombre") or row[0]["usuario"]
    session["user_login"] = row[0]["usuario"]
    session["user_rol"] = row[0].get("rol") or "admin"
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    return render_template("index.html", user_name=session.get("user_name"), user_login=session.get("user_login"), user_rol=session.get("user_rol", "monitor"), is_admin=es_admin())


# =============================================================================
# API: Topología y datos
# =============================================================================

@app.route("/api/topologia")
def api_topologia():
    """
    Devuelve core, switches, teléfonos y edificios para el croquis y el mapa.
    Solo incluye switches que tengan al menos un teléfono activo.
    """
    if usar_demo():
        telefonos = []
        for t in DEMO_TELEFONOS:
            t2 = dict(t)
            t2["ultimo_ping_ok"] = demo_ping_state.get(t["id"])
            t2["ultimo_ping_at"] = demo_ping_at.get(t["id"])
            telefonos.append(t2)
        # Solo switches que tengan al menos un teléfono (para la topología)
        switch_ids_con_telefonos = {t["switch_id"] for t in DEMO_TELEFONOS}
        switches = []
        for s in DEMO_SWITCHES:
            if s["id"] not in switch_ids_con_telefonos:
                continue
            s2 = dict(s)
            s2["ultimo_ping_ok"] = demo_switch_ping_state.get(s["id"])
            s2["ultimo_ping_at"] = demo_switch_ping_at.get(s["id"])
            switches.append(s2)
        edificios = []
        for e in DEMO_EDIFICIOS:
            tels = [t for t in telefonos if t.get("edificio_id") == e["id"]]
            edificios.append({"id": e["id"], "nombre": e["nombre"], "ubicacion": e.get("ubicacion"), "lat": e["lat"], "lng": e["lng"], "telefonos": tels})
        return jsonify({
            "core": DEMO_CORE,
            "switches": switches,
            "telefonos": telefonos,
            "edificios": edificios,
            "demo": True,
        })

    core_list = ejecutar_sql("SELECT id, nombre, ip_management FROM core")
    if not core_list:
        return jsonify({"core": [], "switches": [], "telefonos": [], "edificios": []})

    # Solo switches que tengan al menos un teléfono activo (para la topología)
    switches_list = ejecutar_sql("""
        SELECT DISTINCT s.id, s.core_id, s.nombre, s.ip_management, s.ubicacion, s.lat, s.lng, s.ultimo_ping_ok, s.ultimo_ping_at
        FROM switches s
        INNER JOIN telefonos t ON t.switch_id = s.id AND t.activo = 1
        ORDER BY s.nombre
    """)
    telefonos_list = ejecutar_sql(
        "SELECT id, switch_id, edificio_id, extension, ip, ubicacion, lat, lng, ultimo_ping_ok, ultimo_ping_at FROM telefonos WHERE activo = 1 ORDER BY switch_id, extension"
    )
    # Edificios con sus teléfonos para el mapa
    edificios_list = ejecutar_sql("SELECT id, nombre, ubicacion, lat, lng FROM edificios ORDER BY nombre")
    edificios_con_tels = []
    for e in edificios_list or []:
        tels = [t for t in (telefonos_list or []) if t.get("edificio_id") == e["id"]]
        edificios_con_tels.append({"id": e["id"], "nombre": e["nombre"], "ubicacion": e.get("ubicacion"), "lat": e.get("lat"), "lng": e.get("lng"), "telefonos": tels})
    return jsonify({
        "core": core_list or [],
        "switches": switches_list or [],
        "telefonos": telefonos_list or [],
        "edificios": edificios_con_tels,
    })


@app.route("/api/telefonos_tabla")
def api_telefonos_tabla():
    """Lista teléfonos activos con switch_nombre y edificio_nombre (para Gestión de Teléfonos)."""
    if usar_demo():
        rows = []
        for t in DEMO_TELEFONOS:
            sw = next((s for s in DEMO_SWITCHES if s["id"] == t["switch_id"]), {})
            ed = next((e for e in DEMO_EDIFICIOS if e["id"] == t.get("edificio_id")), {})
            rows.append({
                "id": t["id"],
                "extension": t["extension"],
                "ip": t["ip"],
                "ubicacion": t.get("ubicacion", ""),
                "modelo": t.get("modelo", ""),
                "vlan_id": t.get("vlan_id", 23),
                "switch_id": t["switch_id"],
                "edificio_id": t.get("edificio_id"),
                "lat": t.get("lat"),
                "lng": t.get("lng"),
                "ultimo_ping_ok": demo_ping_state.get(t["id"]),
                "ultimo_ping_at": demo_ping_at.get(t["id"]),
                "switch_nombre": sw.get("nombre", ""),
                "switch_ubicacion": sw.get("ubicacion", ""),
                "edificio_nombre": ed.get("nombre", ""),
            })
        return jsonify({"telefonos": rows, "demo": True})

    query = """
        SELECT t.id, t.extension, t.ip, t.ubicacion, t.modelo, t.vlan_id, t.switch_id, t.edificio_id, t.lat, t.lng,
               t.ultimo_ping_ok, t.ultimo_ping_at,
               s.nombre AS switch_nombre, s.ubicacion AS switch_ubicacion,
               e.nombre AS edificio_nombre
        FROM telefonos t
        JOIN switches s ON t.switch_id = s.id
        LEFT JOIN edificios e ON t.edificio_id = e.id
        WHERE t.activo = 1
        ORDER BY t.extension ASC
    """
    rows = ejecutar_sql(query)
    return jsonify({"telefonos": rows or []})


@app.route("/api/switches")
def api_switches():
    """Lista switches para selectores (crear/editar teléfonos y edificios)."""
    if usar_demo():
        return jsonify({"switches": [{"id": s["id"], "nombre": s["nombre"], "ubicacion": s.get("ubicacion", "")} for s in DEMO_SWITCHES]})
    rows = ejecutar_sql("SELECT id, nombre, ubicacion FROM switches ORDER BY nombre")
    return jsonify({"switches": rows or []})


@app.route("/api/edificios")
def api_edificios_list():
    """Lista edificios con switch_nombre (para mapa, dashboard y Gestión de Edificios)."""
    if usar_demo():
        out = []
        for e in DEMO_EDIFICIOS:
            sw = next((s for s in DEMO_SWITCHES if s["id"] == e.get("switch_id")), {})
            out.append({"id": e["id"], "nombre": e["nombre"], "ubicacion": e.get("ubicacion", ""), "lat": e.get("lat"), "lng": e.get("lng"), "switch_id": e.get("switch_id"), "switch_nombre": sw.get("nombre", "")})
        return jsonify({"edificios": out, "demo": True})
    query = """
        SELECT e.id, e.nombre, e.ubicacion, e.lat, e.lng, e.switch_id, s.nombre AS switch_nombre
        FROM edificios e
        LEFT JOIN switches s ON e.switch_id = s.id
        ORDER BY e.nombre
    """
    rows = ejecutar_sql(query)
    return jsonify({"edificios": rows or []})


# =============================================================================
# API: Edificios (CRUD, requiere admin)
# =============================================================================

@app.route("/api/edificios", methods=["POST"])
def api_edificio_crear():
    """Crea edificio: nombre, ubicacion, lat, lng, switch_id (opcional)."""
    r = requerir_admin()
    if r:
        return r
    data = request.get_json(force=True, silent=True) or {}
    nombre = (data.get("nombre") or "").strip()
    ubicacion = (data.get("ubicacion") or "").strip()
    lat = data.get("lat")
    lng = data.get("lng")
    switch_id = data.get("switch_id")
    if not nombre:
        return jsonify({"ok": False, "error": "Nombre es obligatorio"}), 400
    if usar_demo():
        if any(x["nombre"] == nombre for x in DEMO_EDIFICIOS):
            return jsonify({"ok": False, "error": "Ya existe un edificio con ese nombre"}), 400
        new_id = max([x["id"] for x in DEMO_EDIFICIOS], default=0) + 1
        lat_val = float(lat) if lat is not None and str(lat).strip() != "" else None
        lng_val = float(lng) if lng is not None and str(lng).strip() != "" else None
        e = {"id": new_id, "nombre": nombre, "ubicacion": ubicacion, "lat": lat_val, "lng": lng_val, "switch_id": int(switch_id) if switch_id is not None else None}
        DEMO_EDIFICIOS.append(e)
        return jsonify({"ok": True, "id": new_id, "edificio": e})
    if switch_id is not None:
        sw = ejecutar_sql("SELECT id FROM switches WHERE id = %s", (switch_id,))
        if not sw:
            return jsonify({"ok": False, "error": "Switch no válido"}), 400
    lat_val = float(lat) if lat is not None and str(lat).strip() != "" else None
    lng_val = float(lng) if lng is not None and str(lng).strip() != "" else None
    conn = get_conexion()
    if not conn:
        return jsonify({"ok": False, "error": "Error de conexión"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO edificios (nombre, ubicacion, lat, lng, switch_id) VALUES (%s, %s, %s, %s, %s)",
            (nombre, ubicacion or None, lat_val, lng_val, switch_id if switch_id is not None else None),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return jsonify({"ok": True, "id": new_id})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    finally:
        conn.close()


@app.route("/api/edificios/<int:edificio_id>", methods=["PUT"])
def api_edificio_actualizar(edificio_id):
    """Actualiza un edificio. Requiere admin."""
    r = requerir_admin()
    if r:
        return r
    data = request.get_json(force=True, silent=True) or {}
    nombre = (data.get("nombre") or "").strip()
    ubicacion = (data.get("ubicacion") or "").strip()
    lat = data.get("lat")
    lng = data.get("lng")
    switch_id = data.get("switch_id")
    if not nombre:
        return jsonify({"ok": False, "error": "Nombre es obligatorio"}), 400
    if usar_demo():
        ed = next((x for x in DEMO_EDIFICIOS if x["id"] == edificio_id), None)
        if not ed:
            return jsonify({"ok": False, "error": "Edificio no encontrado"}), 404
        nuevo_switch = int(switch_id) if switch_id is not None else None
        ed["nombre"] = nombre
        ed["ubicacion"] = ubicacion
        ed["lat"] = float(lat) if lat is not None and str(lat).strip() != "" else None
        ed["lng"] = float(lng) if lng is not None and str(lng).strip() != "" else None
        ed["switch_id"] = nuevo_switch
        if nuevo_switch is not None:
            for t in DEMO_TELEFONOS:
                if t.get("edificio_id") == edificio_id:
                    t["switch_id"] = nuevo_switch
        return jsonify({"ok": True})
    row = ejecutar_sql("SELECT id FROM edificios WHERE id = %s", (edificio_id,))
    if not row:
        return jsonify({"ok": False, "error": "Edificio no encontrado"}), 404
    if switch_id is not None:
        sw = ejecutar_sql("SELECT id FROM switches WHERE id = %s", (switch_id,))
        if not sw:
            return jsonify({"ok": False, "error": "Switch no válido"}), 400
    lat_val = float(lat) if lat is not None and str(lat).strip() != "" else None
    lng_val = float(lng) if lng is not None and str(lng).strip() != "" else None
    ejecutar_sql(
        "UPDATE edificios SET nombre = %s, ubicacion = %s, lat = %s, lng = %s, switch_id = %s WHERE id = %s",
        (nombre, ubicacion or None, lat_val, lng_val, switch_id if switch_id is not None else None, edificio_id),
        fetch=False,
    )
    if switch_id is not None:
        ejecutar_sql(
            "UPDATE telefonos SET switch_id = %s WHERE edificio_id = %s",
            (switch_id, edificio_id),
            fetch=False,
        )
    return jsonify({"ok": True})


@app.route("/api/edificios/<int:edificio_id>", methods=["DELETE"])
def api_edificio_eliminar(edificio_id):
    """Elimina un edificio solo si NO tiene teléfonos. Requiere admin."""
    r = requerir_admin()
    if r:
        return r
    if usar_demo():
        count = sum(1 for t in DEMO_TELEFONOS if t.get("edificio_id") == edificio_id)
        if count > 0:
            return jsonify({
                "ok": False,
                "error": "No se puede eliminar: este edificio tiene " + str(count) + " teléfono(s) asignado(s). Primero mueve los teléfonos a otro edificio o elimínalos en Gestión de Teléfonos."
            }), 400
        for i, e in enumerate(DEMO_EDIFICIOS):
            if e["id"] == edificio_id:
                DEMO_EDIFICIOS.pop(i)
                return jsonify({"ok": True})
        return jsonify({"ok": False, "error": "Edificio no encontrado"}), 404
    row = ejecutar_sql("SELECT id FROM edificios WHERE id = %s", (edificio_id,))
    if not row:
        return jsonify({"ok": False, "error": "Edificio no encontrado"}), 404
    count = ejecutar_sql("SELECT COUNT(*) AS n FROM telefonos WHERE edificio_id = %s", (edificio_id,))
    if count and count[0]["n"] > 0:
        n = count[0]["n"]
        return jsonify({
            "ok": False,
            "error": "No se puede eliminar: este edificio tiene " + str(n) + " teléfono(s) asignado(s). Primero mueve los teléfonos a otro edificio o elimínalos en Gestión de Teléfonos."
        }), 400
    ejecutar_sql("DELETE FROM edificios WHERE id = %s", (edificio_id,), fetch=False)
    return jsonify({"ok": True})


def _switch_id_desde_edificio(edificio_id):
    """
    Obtiene el switch_id asociado a un edificio.
    Args:
        edificio_id: ID del edificio.
    Returns:
        switch_id o None si el edificio no tiene switch.
    """
    if edificio_id is None:
        return None
    row = ejecutar_sql("SELECT switch_id FROM edificios WHERE id = %s", (edificio_id,))
    if not row or row[0].get("switch_id") is None:
        return None
    return row[0]["switch_id"]


# =============================================================================
# API: Teléfonos (CRUD, requiere admin)
# =============================================================================

@app.route("/api/telefonos", methods=["POST"])
def api_telefono_crear():
    """Crea teléfono: extension, ip, edificio_id (obligatorio), ubicacion, modelo, lat, lng."""
    r = requerir_admin()
    if r:
        return r
    data = request.get_json(force=True, silent=True) or {}
    extension = (data.get("extension") or "").strip()
    ip = (data.get("ip") or "").strip()
    ubicacion = (data.get("ubicacion") or "").strip()
    modelo = (data.get("modelo") or "").strip()
    edificio_id = data.get("edificio_id")
    switch_id = data.get("switch_id")
    lat = data.get("lat")
    lng = data.get("lng")

    if not ip:
        return jsonify({"ok": False, "error": "IP es obligatoria"}), 400
    if not extension:
        return jsonify({"ok": False, "error": "Extensión es obligatoria"}), 400
    if edificio_id is None and switch_id is None:
        return jsonify({"ok": False, "error": "Edificio es obligatorio"}), 400

    if usar_demo():
        if any(x["extension"] == extension for x in DEMO_TELEFONOS):
            return jsonify({"ok": False, "error": "Ya existe un teléfono con esa extensión"}), 400
        sid = switch_id
        if edificio_id is not None:
            ed = next((e for e in DEMO_EDIFICIOS if e["id"] == edificio_id), None)
            if not ed:
                return jsonify({"ok": False, "error": "Edificio no válido"}), 400
            sid = ed.get("switch_id")
        if sid is None:
            return jsonify({"ok": False, "error": "El edificio no tiene switch asignado"}), 400
        sw = next((s for s in DEMO_SWITCHES if s["id"] == sid), None)
        if not sw:
            return jsonify({"ok": False, "error": "Edificio/Switch no válido"}), 400
        new_id = max([x["id"] for x in DEMO_TELEFONOS], default=0) + 1
        lat_val = float(lat) if lat is not None and str(lat).strip() != "" else None
        lng_val = float(lng) if lng is not None and str(lng).strip() != "" else None
        t = {"id": new_id, "switch_id": int(sid), "edificio_id": int(edificio_id) if edificio_id is not None else None, "extension": extension, "ip": ip, "ubicacion": ubicacion, "modelo": modelo, "vlan_id": 23, "lat": lat_val, "lng": lng_val}
        DEMO_TELEFONOS.append(t)
        return jsonify({"ok": True, "telefono": t, "id": new_id})

    if edificio_id is not None:
        switch_id = _switch_id_desde_edificio(edificio_id)
        if switch_id is None:
            return jsonify({"ok": False, "error": "El edificio no tiene switch asignado"}), 400
    ed_row = ejecutar_sql("SELECT id FROM edificios WHERE id = %s", (edificio_id,)) if edificio_id is not None else None
    if edificio_id is not None and not ed_row:
        return jsonify({"ok": False, "error": "Edificio no válido"}), 400
    sw = ejecutar_sql("SELECT id FROM switches WHERE id = %s", (switch_id,))
    if not sw:
        return jsonify({"ok": False, "error": "Switch no válido"}), 400
    lat_val = float(lat) if lat is not None and str(lat).strip() != "" else None
    lng_val = float(lng) if lng is not None and str(lng).strip() != "" else None
    conn = get_conexion()
    if not conn:
        return jsonify({"ok": False, "error": "Error de conexión"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO telefonos (switch_id, edificio_id, extension, ip, ubicacion, modelo, lat, lng, activo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)",
            (switch_id, edificio_id, extension, ip, ubicacion, modelo, lat_val, lng_val),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return jsonify({"ok": True, "id": new_id})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    finally:
        conn.close()


@app.route("/api/telefonos/<int:telefono_id>", methods=["PUT"])
def api_telefono_actualizar(telefono_id):
    """Actualiza un teléfono. Requiere admin."""
    r = requerir_admin()
    if r:
        return r
    data = request.get_json(force=True, silent=True) or {}
    extension = (data.get("extension") or "").strip()
    ip = (data.get("ip") or "").strip()
    ubicacion = (data.get("ubicacion") or "").strip()
    modelo = (data.get("modelo") or "").strip()
    edificio_id = data.get("edificio_id")
    switch_id = data.get("switch_id")
    lat = data.get("lat")
    lng = data.get("lng")

    if not ip:
        return jsonify({"ok": False, "error": "IP es obligatoria"}), 400

    if usar_demo():
        t = next((x for x in DEMO_TELEFONOS if x["id"] == telefono_id), None)
        if not t:
            return jsonify({"ok": False, "error": "Teléfono no encontrado"}), 404
        sid = switch_id
        if edificio_id is not None:
            ed = next((e for e in DEMO_EDIFICIOS if e["id"] == edificio_id), None)
            if not ed:
                return jsonify({"ok": False, "error": "Edificio no válido"}), 400
            sid = ed.get("switch_id")
        if edificio_id is not None and sid is None:
            return jsonify({"ok": False, "error": "El edificio no tiene switch asignado"}), 400
        if sid is not None and next((s for s in DEMO_SWITCHES if s["id"] == sid), None) is None:
            return jsonify({"ok": False, "error": "Switch no válido"}), 400
        t["ip"] = ip
        if extension:
            t["extension"] = extension
        t["ubicacion"] = ubicacion
        t["modelo"] = modelo
        if edificio_id is not None:
            t["edificio_id"] = int(edificio_id)
            t["switch_id"] = int(sid)
        elif switch_id is not None:
            t["switch_id"] = int(switch_id)
        t["lat"] = float(lat) if lat is not None and str(lat).strip() != "" else None
        t["lng"] = float(lng) if lng is not None and str(lng).strip() != "" else None
        return jsonify({"ok": True, "telefono": t})

    row = ejecutar_sql("SELECT id FROM telefonos WHERE id = %s", (telefono_id,))
    if not row:
        return jsonify({"ok": False, "error": "Teléfono no encontrado"}), 404
    if edificio_id is not None:
        switch_id = _switch_id_desde_edificio(edificio_id)
        if switch_id is None:
            return jsonify({"ok": False, "error": "El edificio no tiene switch asignado"}), 400
    if switch_id is not None:
        sw = ejecutar_sql("SELECT id FROM switches WHERE id = %s", (switch_id,))
        if not sw:
            return jsonify({"ok": False, "error": "Switch no válido"}), 400
    sets = ["ip = %s", "ubicacion = %s", "modelo = %s"]
    params = [ip, ubicacion, modelo]
    if extension:
        sets.append("extension = %s")
        params.append(extension)
    if edificio_id is not None:
        sets.append("edificio_id = %s")
        params.append(edificio_id)
    if switch_id is not None:
        sets.append("switch_id = %s")
        params.append(switch_id)
    lat_val = float(lat) if lat is not None and str(lat).strip() != "" else None
    lng_val = float(lng) if lng is not None and str(lng).strip() != "" else None
    sets.append("lat = %s")
    sets.append("lng = %s")
    params.extend([lat_val, lng_val])
    params.append(telefono_id)
    query = "UPDATE telefonos SET " + ", ".join(sets) + " WHERE id = %s"
    ejecutar_sql(query, tuple(params), fetch=False)
    return jsonify({"ok": True})


@app.route("/api/telefonos/<int:telefono_id>", methods=["DELETE"])
def api_telefono_eliminar(telefono_id):
    """Elimina el teléfono. Requiere admin."""
    r = requerir_admin()
    if r:
        return r
    if usar_demo():
        for i, t in enumerate(DEMO_TELEFONOS):
            if t["id"] == telefono_id:
                DEMO_TELEFONOS.pop(i)
                demo_ping_state.pop(telefono_id, None)
                demo_ping_at.pop(telefono_id, None)
                return jsonify({"ok": True})
        return jsonify({"ok": False, "error": "Teléfono no encontrado"}), 404

    row = ejecutar_sql("SELECT id FROM telefonos WHERE id = %s", (telefono_id,))
    if not row:
        return jsonify({"ok": False, "error": "Teléfono no encontrado"}), 404
    ejecutar_sql("DELETE FROM telefonos WHERE id = %s", (telefono_id,), fetch=False)
    return jsonify({"ok": True})


# =============================================================================
# API: Ping (monitoreo de conectividad)
# =============================================================================

@app.route("/api/ping/<int:telefono_id>")
def api_ping_uno(telefono_id):
    """Ping a un teléfono; actualiza ultimo_ping_ok/ultimo_ping_at y devuelve conectado."""
    if usar_demo():
        t = next((x for x in DEMO_TELEFONOS if x["id"] == telefono_id), None)
        if not t:
            return jsonify({"ok": False, "error": "Teléfono no encontrado"}), 404
        ip = t["ip"]
        ok = hacer_ping(ip)
        demo_ping_state[telefono_id] = ok
        demo_ping_at[telefono_id] = datetime.now().isoformat()
        return jsonify({"id": telefono_id, "ip": ip, "conectado": ok})

    row = ejecutar_sql("SELECT id, ip FROM telefonos WHERE id = %s", (telefono_id,))
    if not row:
        return jsonify({"ok": False, "error": "Teléfono no encontrado"}), 404
    ip = row[0]["ip"]
    ok = hacer_ping(ip)
    ejecutar_sql(
        "UPDATE telefonos SET ultimo_ping_ok = %s, ultimo_ping_at = NOW() WHERE id = %s",
        (1 if ok else 0, telefono_id),
        fetch=False,
    )
    return jsonify({"id": telefono_id, "ip": ip, "conectado": ok})


@app.route("/api/ping_todos")
def api_ping_todos():
    """Hace ping a todos los teléfonos y solo a los switches que tengan al menos un teléfono (evita ping a 190+ switches)."""
    if usar_demo():
        resultados = []
        now = datetime.now().isoformat()
        for t in DEMO_TELEFONOS:
            ok = hacer_ping(t["ip"])
            demo_ping_state[t["id"]] = ok
            demo_ping_at[t["id"]] = now
            resultados.append({"id": t["id"], "ip": t["ip"], "conectado": ok, "tipo": "telefono"})
        switch_ids_con_telefonos = {t["switch_id"] for t in DEMO_TELEFONOS}
        for s in DEMO_SWITCHES:
            if s["id"] not in switch_ids_con_telefonos:
                continue
            ip = s.get("ip_management")
            if ip:
                ok = hacer_ping(ip)
            else:
                ok = None
            demo_switch_ping_state[s["id"]] = ok
            demo_switch_ping_at[s["id"]] = now
            resultados.append({"id": s["id"], "ip": ip, "conectado": ok, "tipo": "switch"})
        return jsonify({"actualizados": len(resultados), "resultados": resultados, "demo": True})

    resultados = []
    telefonos = ejecutar_sql("SELECT id, ip FROM telefonos WHERE activo = 1")
    for t in telefonos or []:
        ok = hacer_ping(t["ip"])
        ejecutar_sql(
            "UPDATE telefonos SET ultimo_ping_ok = %s, ultimo_ping_at = NOW() WHERE id = %s",
            (1 if ok else 0, t["id"]),
            fetch=False,
        )
        resultados.append({"id": t["id"], "ip": t["ip"], "conectado": ok, "tipo": "telefono"})

    # Solo switches que tengan al menos un teléfono activo (no ping a los 190+)
    switches = ejecutar_sql("""
        SELECT DISTINCT s.id, s.ip_management
        FROM switches s
        INNER JOIN telefonos t ON t.switch_id = s.id AND t.activo = 1
        WHERE s.ip_management IS NOT NULL AND s.ip_management != ''
    """)
    for s in switches or []:
        ok = hacer_ping(s["ip_management"])
        ejecutar_sql(
            "UPDATE switches SET ultimo_ping_ok = %s, ultimo_ping_at = NOW() WHERE id = %s",
            (1 if ok else 0, s["id"]),
            fetch=False,
        )
        resultados.append({"id": s["id"], "ip": s["ip_management"], "conectado": ok, "tipo": "switch"})

    return jsonify({"actualizados": len(resultados), "resultados": resultados})


# =============================================================================
# API: Usuarios (solo admin)
# =============================================================================
# Usuarios extra en modo demo (creados por admin en la sesión actual)
DEMO_EXTRA_USUARIOS = {}  # usuario -> (nombre, password_hash_simulado, rol)


@app.route("/api/usuarios")
def api_usuarios_list():
    """Lista usuarios. Solo admin."""
    r = requerir_admin()
    if r:
        return r
    if usar_demo():
        out = [{"id": "admin", "usuario": "admin", "nombre": "Administrador", "rol": "admin"}, {"id": "operador", "usuario": "operador", "nombre": "Operador", "rol": "monitor"}]
        for u, d in DEMO_EXTRA_USUARIOS.items():
            out.append({"id": u, "usuario": u, "nombre": d[0], "rol": d[2]})
        return jsonify({"usuarios": out})
    rows = ejecutar_sql("SELECT id, usuario, nombre, COALESCE(rol, 'monitor') AS rol FROM usuarios WHERE activo = 1 ORDER BY usuario")
    return jsonify({"usuarios": rows or []})


@app.route("/api/usuarios", methods=["POST"])
def api_usuario_crear():
    """Crea un usuario (solo rol monitor). Solo admin."""
    r = requerir_admin()
    if r:
        return r
    data = request.get_json(force=True, silent=True) or {}
    usuario = (data.get("usuario") or "").strip().lower()
    password = data.get("password") or ""
    nombre = (data.get("nombre") or "").strip()
    rol = (data.get("rol") or "monitor").lower()
    if rol not in ("admin", "monitor"):
        rol = "monitor"
    if not usuario:
        return jsonify({"ok": False, "error": "Usuario es obligatorio"}), 400
    if len(password) < 4:
        return jsonify({"ok": False, "error": "Contraseña mínimo 4 caracteres"}), 400
    if usar_demo():
        if usuario in DEMO_USUARIOS or usuario in DEMO_EXTRA_USUARIOS:
            return jsonify({"ok": False, "error": "Ya existe ese usuario"}), 400
        DEMO_EXTRA_USUARIOS[usuario] = (nombre or usuario, "hashed", rol)
        return jsonify({"ok": True, "id": usuario})
    existing = ejecutar_sql("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
    if existing:
        return jsonify({"ok": False, "error": "Ya existe ese usuario"}), 400
    conn = get_conexion()
    if not conn:
        return jsonify({"ok": False, "error": "Error de conexión"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (usuario, password_hash, nombre, rol, activo) VALUES (%s, %s, %s, %s, 1)",
            (usuario, generate_password_hash(password), nombre or usuario, rol),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return jsonify({"ok": True, "id": new_id})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    finally:
        conn.close()


@app.route("/api/usuarios/<usuario_id>", methods=["PUT"])
def api_usuario_actualizar(usuario_id):
    """Actualiza nombre, rol y opcionalmente contraseña. Solo admin."""
    r = requerir_admin()
    if r:
        return r
    data = request.get_json(force=True, silent=True) or {}
    nombre = (data.get("nombre") or "").strip()
    rol = (data.get("rol") or "monitor").lower()
    password = data.get("password")
    if rol not in ("admin", "monitor"):
        rol = "monitor"
    if usar_demo():
        u_from_extra = str(usuario_id) in DEMO_EXTRA_USUARIOS
        if u_from_extra:
            key = str(usuario_id)
            old = DEMO_EXTRA_USUARIOS[key]
            DEMO_EXTRA_USUARIOS[key] = (nombre or old[0], old[1], rol)
            return jsonify({"ok": True})
        return jsonify({"ok": False, "error": "Solo se pueden editar usuarios creados en esta sesión (admin/operador son fijos)"}), 400
    try:
        uid = int(usuario_id)
    except (ValueError, TypeError):
        return jsonify({"ok": False, "error": "ID no válido"}), 400
    row = ejecutar_sql("SELECT id, usuario FROM usuarios WHERE id = %s", (uid,))
    if not row:
        return jsonify({"ok": False, "error": "Usuario no encontrado"}), 404
    sets = ["nombre = %s", "rol = %s"]
    params = [nombre or row[0]["usuario"], rol]
    if password and len(password) >= 4:
        sets.append("password_hash = %s")
        params.append(generate_password_hash(password))
    params.append(uid)
    ejecutar_sql("UPDATE usuarios SET " + ", ".join(sets) + " WHERE id = %s", tuple(params), fetch=False)
    return jsonify({"ok": True})


@app.route("/api/usuarios/<usuario_id>", methods=["DELETE"])
def api_usuario_eliminar(usuario_id):
    """Elimina físicamente el usuario de la BD. Solo admin. No se puede eliminar a sí mismo."""
    r = requerir_admin()
    if r:
        return r
    try:
        uid = int(usuario_id)
    except (ValueError, TypeError):
        uid = None
    if str(session.get("user_id", "")) == str(usuario_id):
        return jsonify({"ok": False, "error": "No puedes eliminar tu propio usuario"}), 400
    if usar_demo():
        if str(usuario_id) in ("admin", "operador"):
            return jsonify({"ok": False, "error": "No se pueden eliminar los usuarios demo base"}), 400
        DEMO_EXTRA_USUARIOS.pop(str(usuario_id), None)
        return jsonify({"ok": True})
    if uid is None:
        return jsonify({"ok": False, "error": "ID no válido"}), 400
    row = ejecutar_sql("SELECT id, COALESCE(rol, 'admin') AS rol FROM usuarios WHERE id = %s", (uid,))
    if not row:
        return jsonify({"ok": False, "error": "Usuario no encontrado"}), 404
    # Solo impedir si estamos eliminando a un admin y sería el último
    if row[0]["rol"] == "admin":
        admins = ejecutar_sql("SELECT COUNT(*) AS n FROM usuarios WHERE activo = 1 AND COALESCE(rol, 'admin') = 'admin'")
        if admins and admins[0]["n"] <= 1:
            return jsonify({"ok": False, "error": "No se puede eliminar el último administrador"}), 400
    ejecutar_sql("DELETE FROM usuarios WHERE id = %s", (uid,), fetch=False)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

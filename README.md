# Redes - Topología y monitoreo de teléfonos

Aplicación para visualizar la topología del tecnológico (Core → Switches → Teléfonos), con ping para ver estado **verde** (conectado) o **rojo** (sin respuesta) y tabla de datos desde MySQL.

## Requisitos

- Python 3.8+
- MySQL (servidor local o remoto)
- Red con los teléfonos alcanzables por ping desde el equipo donde corre la app

## Instalación

1. **Crear entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar MySQL:**
   - Crea el usuario y la base de datos si hace falta.
   - Ejecuta el script SQL para crear tablas y datos de ejemplo:
     ```bash
     mysql -u root -p < schema.sql
     ```
     O abre `schema.sql` en MySQL Workbench / HeidiSQL y ejecútalo.

4. **Configurar conexión en Python:**
   - Edita las variables en `conexion_db.py` (host, user, password, database), **o**
   - Define variables de entorno: `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_PORT`.

## Uso

1. **Probar conexión a MySQL:**
   ```bash
   python conexion_db.py
   ```
   Debe mostrar: "Conexión a MySQL correcta."

2. **Iniciar la aplicación:**
   ```bash
   python app.py
   ```

3. Abre en el navegador: **http://localhost:5000** (serás redirigido al **login** si no has iniciado sesión).

4. **Login:**
   - **Con MySQL:** La primera vez que no haya usuarios en la tabla `usuarios`, se crea uno por defecto: **usuario:** `admin`, **contraseña:** `admin`. Cámbiala después.
   - **Modo demo (sin MySQL):** Usa **admin** / **admin** u **operador** / **operador**.

5. **Pestañas:**
   - **Croquis:** Muestra Core → Switches → Teléfonos. Verde = responde al ping, rojo = no responde. Usa "Actualizar ping a todos" para refrescar.
   - **Mapa (Tec Oaxaca):** Mapa del campus del Instituto Tecnológico de Oaxaca. Cada edificio (switch) tiene un marcador en **verde** si todos los teléfonos responden, **rojo** si alguno falla, **gris** si no se ha hecho ping. Al hacer clic en un marcador ves la lista de teléfonos y su estado.
   - **Tabla de teléfonos:** Listado con extensión, IP, switch, ubicación, VLAN y estado de ping.

## Documentación

- **schema.sql:** Comentarios detallados por tabla y columna.
- **docs/DIAGRAMA_BD.md:** Diagrama ER (Mermaid) y flujo de topología. Visualiza en [mermaid.live](https://mermaid.live).
- **app.py, conexion_db.py:** Docstrings en funciones y secciones documentadas.

## Estructura de la base de datos

- **core:** Equipo central (uno en el croquis).
- **switches:** Conectados al core (`core_id`). Opcionales `lat`, `lng` para ubicar el edificio en el mapa del campus.
- **telefonos:** Conectados a cada switch (`switch_id`), con IP, extensión, ubicación, modelo, opcionales `lat`/`lng` (para que aparezcan en el mapa), y `ultimo_ping_ok`/`ultimo_ping_at`. Desde Gestión (CRUD) puedes **agregar**, **editar** y **eliminar** teléfonos.
- **usuarios:** Login (usuario, password_hash, nombre). La app crea un usuario `admin` si la tabla está vacía.

Puedes añadir más core/switches/teléfonos desde MySQL o desde la interfaz (Agregar teléfono). Si ya tenías la base de datos sin columnas `lat`/`lng` en `switches`, ejecuta: `ALTER TABLE switches ADD COLUMN lat DECIMAL(10,7) NULL, ADD COLUMN lng DECIMAL(10,7) NULL;` Para que los teléfonos tengan posición en el mapa, la tabla `telefonos` debe tener `lat` y `lng`: `ALTER TABLE telefonos ADD COLUMN lat DECIMAL(10,7) NULL, ADD COLUMN lng DECIMAL(10,7) NULL;` Para producción, define `SECRET_KEY` en variables de entorno (clave secreta para las sesiones).

## Notas

- El ping se ejecuta desde el servidor (el equipo donde corre `app.py`). Para que los teléfonos aparezcan en verde, deben ser alcanzables por red desde ese equipo.
- Si usas VLAN exclusiva para teléfonos, asegúrate de que el servidor pueda hacer ping a esa VLAN (ruteo o interfaz en la misma VLAN).

"""
Módulo de conexión a MySQL - Sistema de Monitoreo de Red
========================================================

Proporciona la conexión a la base de datos MySQL (redes_tecnologico).
Si la conexión falla, app.py usa modo demo con datos en memoria.

Configuración:
- Edita DB_CONFIG o usa variables de entorno: MYSQL_HOST, MYSQL_PORT,
  MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE.
- Ejecuta este archivo directamente para probar la conexión.
"""
import os

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    mysql = None
    Error = Exception


# -----------------------------------------------------------------------------
# Configuración de la base de datos
# Variables de entorno: MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
# -----------------------------------------------------------------------------
DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", "3306")),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", "pato123"),
    "database": os.environ.get("MYSQL_DATABASE", "redes_tecnologico"),
    "charset": "utf8mb4",
    "autocommit": True,
}


def get_conexion():
    """
    Crea y devuelve una conexión a MySQL.
    Returns:
        Objeto conexión si OK; None si falla (ej. servidor apagado).
    Raises:
        ImportError: Si mysql-connector-python no está instalado.
    """
    if mysql is None:
        raise ImportError("Instala el conector: pip install mysql-connector-python")
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None


def probar_conexion():
    """
    Prueba la conexión ejecutando SELECT 1.
    Returns:
        True si la conexión es correcta; False si falla.
    """
    conn = get_conexion()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        return True
    except Error as e:
        print(f"Error al probar: {e}")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    if probar_conexion():
        print("Conexión a MySQL correcta.")
    else:
        print("No se pudo conectar. Revisa host, usuario, contraseña y que la BD exista.")

-- =============================================================================
-- SCHEMA: Sistema de Monitoreo de Red - Instituto Tecnológico de Oaxaca
-- =============================================================================
-- Base de datos para topología: Core -> Switches -> Teléfonos (VLAN 23)
-- Incluye edificios para mapa del campus y usuarios para autenticación.
-- Ejecuta este script en MySQL para crear la BD y las tablas.
-- =============================================================================

CREATE DATABASE IF NOT EXISTS redes_tecnologico
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE redes_tecnologico;

-- -----------------------------------------------------------------------------
-- TABLA: core
-- Equipo central de la red. Punto de origen de la topología.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS core (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  ip_management VARCHAR(45),      -- IP de gestión del equipo
  descripcion VARCHAR(255),
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- TABLA: switches
-- Switches conectados al core. Cada uno puede tener múltiples teléfonos.
-- lat/lng: coordenadas para ubicar en mapa si no hay edificio asociado.
-- ultimo_ping_ok: 1=responde, 0=no responde, NULL=sin probar.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS switches (
  id INT AUTO_INCREMENT PRIMARY KEY,
  core_id INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  ip_management VARCHAR(45),
  ubicacion VARCHAR(255),
  lat DECIMAL(10, 7) NULL,
  lng DECIMAL(10, 7) NULL,
  ultimo_ping_ok TINYINT(1) NULL,
  ultimo_ping_at TIMESTAMP NULL,
  FOREIGN KEY (core_id) REFERENCES core(id) ON DELETE CASCADE,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- TABLA: edificios
-- Ubicaciones del campus para el mapa. Cada edificio puede tener un switch.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS edificios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  ubicacion VARCHAR(255),
  lat DECIMAL(10, 7) NULL,
  lng DECIMAL(10, 7) NULL,
  switch_id INT NULL,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (switch_id) REFERENCES switches(id) ON DELETE SET NULL,
  UNIQUE KEY uq_edificio_nombre (nombre)
);

-- -----------------------------------------------------------------------------
-- TABLA: telefonos
-- Teléfonos IP conectados a switches. VLAN 23 por defecto.
-- edificio_id: para agrupar en mapa por edificio.
-- extension: única en todo el sistema.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS telefonos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  switch_id INT NOT NULL,
  edificio_id INT NULL,
  extension VARCHAR(20) NOT NULL,
  ip VARCHAR(45) NOT NULL,
  mac VARCHAR(17),
  vlan_id INT DEFAULT 23,
  ubicacion VARCHAR(255),
  modelo VARCHAR(100),
  lat DECIMAL(10, 7) NULL,
  lng DECIMAL(10, 7) NULL,
  activo TINYINT(1) DEFAULT 1,
  ultimo_ping_ok TINYINT(1) NULL,
  ultimo_ping_at TIMESTAMP NULL,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (switch_id) REFERENCES switches(id) ON DELETE CASCADE,
  FOREIGN KEY (edificio_id) REFERENCES edificios(id) ON DELETE SET NULL,
  UNIQUE KEY uq_extension (extension)
);

-- -----------------------------------------------------------------------------
-- TABLA: usuarios
-- Autenticación. Roles: 'admin' (CRUD completo) o 'monitor' (solo lectura).
-- activo: 1= puede iniciar sesión, 0= deshabilitado.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  nombre VARCHAR(100),
  rol VARCHAR(20) DEFAULT 'monitor',
  activo TINYINT(1) DEFAULT 1,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- Índices para consultas frecuentes
-- -----------------------------------------------------------------------------
CREATE INDEX idx_telefonos_switch ON telefonos(switch_id);
CREATE INDEX idx_telefonos_edificio ON telefonos(edificio_id);
CREATE INDEX idx_telefonos_ip ON telefonos(ip);
CREATE INDEX idx_switches_core ON switches(core_id);

-- -----------------------------------------------------------------------------
-- Datos de ejemplo: 1 core, 2 switches, varios teléfonos
-- Coordenadas: campus Tecnológico de Oaxaca (Av. Víctor Bravo Ahuja 125)
-- -----------------------------------------------------------------------------
INSERT INTO core (nombre, ip_management, descripcion) VALUES
  ('Core Principal', '192.168.1.1', 'Core del Tecnológico')
ON DUPLICATE KEY UPDATE nombre = nombre;

SET @core_id = (SELECT id FROM core LIMIT 1);
INSERT INTO switches (core_id, nombre, ip_management, ubicacion, lat, lng) VALUES
  (@core_id, 'Switch Edificio A', '192.168.1.10', 'Edificio A', 17.0698, -96.7256),
  (@core_id, 'Switch Edificio B', '192.168.1.11', 'Edificio B', 17.0690, -96.7250)
ON DUPLICATE KEY UPDATE nombre = nombre, lat = VALUES(lat), lng = VALUES(lng);

SET @sw1 = (SELECT id FROM switches WHERE nombre = 'Switch Edificio A' LIMIT 1);
SET @sw2 = (SELECT id FROM switches WHERE nombre = 'Switch Edificio B' LIMIT 1);
INSERT INTO edificios (nombre, ubicacion, lat, lng, switch_id) VALUES
  ('Edificio A', 'Edificio A', 17.0698, -96.7256, @sw1),
  ('Edificio B', 'Edificio B', 17.0690, -96.7250, @sw2)
ON DUPLICATE KEY UPDATE nombre = nombre;

SET @ed1 = (SELECT id FROM edificios WHERE nombre = 'Edificio A' LIMIT 1);
SET @ed2 = (SELECT id FROM edificios WHERE nombre = 'Edificio B' LIMIT 1);
INSERT INTO telefonos (switch_id, edificio_id, extension, ip, vlan_id, ubicacion) VALUES
  (@sw1, @ed1, '1001', '192.168.100.10', 23, 'Oficina 101'),
  (@sw1, @ed1, '1002', '192.168.100.11', 23, 'Oficina 102'),
  (@sw2, @ed2, '2001', '192.168.100.20', 23, 'Oficina 201'),
  (@sw2, @ed2, '2002', '192.168.100.21', 23, 'Oficina 202')
ON DUPLICATE KEY UPDATE extension = extension;

-- -----------------------------------------------------------------------------
-- Migraciones (ejecutar si aplica)
-- -----------------------------------------------------------------------------
-- Si tienes problemas con los roles:
--   ALTER TABLE usuarios ADD COLUMN rol VARCHAR(20) DEFAULT 'admin';
--   UPDATE usuarios SET rol = 'admin' WHERE usuario = 'admin' OR rol IS NULL;
--
-- Si ya tenías una BD sin edificios:
--   ALTER TABLE telefonos ADD COLUMN edificio_id INT NULL;
--   ALTER TABLE telefonos ADD CONSTRAINT fk_telefonos_edificio FOREIGN KEY (edificio_id) REFERENCES edificios(id) ON DELETE SET NULL;

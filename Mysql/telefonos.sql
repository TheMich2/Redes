-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-02-2026 a las 18:03:45
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `redes_tecnologico`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `telefonos`
--

CREATE TABLE `telefonos` (
  `id` int(11) NOT NULL,
  `switch_id` int(11) NOT NULL,
  `extension` varchar(20) NOT NULL,
  `ip` varchar(45) NOT NULL,
  `mac` varchar(17) DEFAULT NULL,
  `vlan_id` int(11) DEFAULT 23,
  `ubicacion` varchar(255) DEFAULT NULL,
  `modelo` varchar(100) DEFAULT NULL,
  `lat` decimal(10,7) DEFAULT NULL,
  `lng` decimal(10,7) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `ultimo_ping_ok` tinyint(1) DEFAULT NULL,
  `ultimo_ping_at` timestamp NULL DEFAULT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `edificio_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `telefonos`
--

INSERT INTO `telefonos` (`id`, `switch_id`, `extension`, `ip`, `mac`, `vlan_id`, `ubicacion`, `modelo`, `lat`, `lng`, `activo`, `ultimo_ping_ok`, `ultimo_ping_at`, `creado_en`, `actualizado_en`, `edificio_id`) VALUES
(30, 61, '1001', '192.168.23.101', NULL, 23, 'Directora', 'Fanvil X6U', NULL, NULL, 1, 1, '2026-02-19 16:55:07', '2026-02-16 07:32:08', '2026-02-19 16:55:07', 15),
(32, 61, '1002', '192.168.23.102', NULL, 23, 'Sec Directora', 'Fanvil 3XSP', NULL, NULL, 1, 0, '2026-02-19 16:55:09', '2026-02-16 08:32:00', '2026-02-19 16:55:09', 15),
(33, 61, '1003', '192.168.23.103', NULL, 23, 'Sub dirección Academica', 'Fanvil V64', NULL, NULL, 1, 0, '2026-02-19 16:55:11', '2026-02-16 14:38:08', '2026-02-19 16:55:11', 15),
(34, 61, '1004', '192.168.23.104', NULL, 23, 'Sec Sub Dirrecion Academica', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:11', '2026-02-16 14:38:44', '2026-02-19 16:55:11', 15),
(35, 61, '1005', '192.168.23.105', NULL, 23, 'Sub Dirreción planeacion y vinculación', 'Fanvil V64', NULL, NULL, 1, 0, '2026-02-19 16:55:13', '2026-02-16 14:39:24', '2026-02-19 16:55:13', 15),
(36, 61, '1006', '192.168.23.106', NULL, 23, 'Sec Sub Dirreción Planeacion y vinculacion', 'Fanvil 3XSP', NULL, NULL, 1, 0, '2026-02-19 16:55:15', '2026-02-16 14:39:59', '2026-02-19 16:55:15', 15),
(37, 61, '1007', '192.168.23.107', NULL, 23, 'Subdirreción administrativa', 'Fanvil V64', NULL, NULL, 1, 1, '2026-02-19 16:55:15', '2026-02-16 14:40:35', '2026-02-19 16:55:15', 15),
(38, 61, '1008', '192.168.23.108', NULL, 23, 'Sec sub administrativa', 'Fanvil 3XSP', NULL, NULL, 1, 0, '2026-02-19 16:55:17', '2026-02-16 14:41:15', '2026-02-19 16:55:17', 15),
(39, 97, '1009', '192.168.23.109', NULL, 23, 'Jefatura de Sistemas', 'Fanvil V64', NULL, NULL, 1, 1, '2026-02-19 16:55:17', '2026-02-16 14:42:24', '2026-02-19 16:55:17', 18),
(40, 97, '1010', '192.168.23.110', NULL, 23, 'Secretaria centro computo', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:17', '2026-02-16 14:44:32', '2026-02-19 16:55:17', 18),
(41, 97, '1050', '192.168.23.150', NULL, 23, 'Coordinacion de servicios de internet', 'Grandstream GXP1610', NULL, NULL, 1, 0, '2026-02-19 16:55:19', '2026-02-16 15:18:34', '2026-02-19 16:55:19', 18),
(42, 97, '1012', '192.168.23.112', NULL, 23, 'Materiales', 'Fanvil 3XSP', NULL, NULL, 1, 0, '2026-02-19 16:55:21', '2026-02-16 15:19:03', '2026-02-19 16:55:21', 18),
(43, 78, '1013', '192.168.23.113', NULL, 23, 'Jefatura de sistemas', 'Fanvil V64', NULL, NULL, 1, 0, '2026-02-19 16:55:23', '2026-02-16 15:22:07', '2026-02-19 16:55:23', 20),
(44, 78, '1014', '192.168.23.114', NULL, 23, 'Secretaria de sistemas', 'Fanvil 3XSP', NULL, NULL, 1, 0, '2026-02-19 16:55:25', '2026-02-16 15:22:33', '2026-02-19 16:55:25', 20),
(45, 59, '1015', '192.168.23.115', NULL, 23, 'Jefatura ciencias basicas', 'Fanvil X6U', NULL, NULL, 1, 1, '2026-02-19 16:55:25', '2026-02-16 15:23:09', '2026-02-19 16:55:25', 21),
(46, 59, '1016', '192.168.23.116', NULL, 23, 'Secretaria ciencias basicas', 'Fanvil X6U', NULL, NULL, 1, 1, '2026-02-19 16:55:25', '2026-02-16 15:23:30', '2026-02-19 16:55:25', 21),
(47, 79, '1017', '192.168.23.117', NULL, 23, 'Servicios escolares', 'Fanvil X6U', NULL, NULL, 1, 1, '2026-02-19 16:55:25', '2026-02-16 15:23:59', '2026-02-19 16:55:25', 26),
(48, 79, '1018', '192.168.23.118', NULL, 23, 'Secretaria servicios escolares', 'Fanvil X6U', NULL, NULL, 1, 1, '2026-02-19 16:55:25', '2026-02-16 15:24:28', '2026-02-19 16:55:25', 26),
(49, 77, '1019', '192.168.23.119', NULL, 23, 'Centro de informacion', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:25', '2026-02-16 15:24:52', '2026-02-19 16:55:25', 17),
(50, 77, '1020', '192.168.23.120', NULL, 23, 'Secretaria centro de informacion', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:25', '2026-02-16 15:25:54', '2026-02-19 16:55:25', 17),
(51, 79, '1021', '192.168.23.121', NULL, 23, 'Division de estudios profesionales', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:25', '2026-02-16 15:26:37', '2026-02-19 16:55:25', 23),
(52, 79, '1022', '192.168.23.122', NULL, 23, 'Secretaria division estudios profesionales', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:25', '2026-02-16 15:27:11', '2026-02-19 16:55:25', 23),
(53, 82, '1023', '192.168.23.123', NULL, 23, 'Jefatura industrial', 'Fanvil 3XSP', NULL, NULL, 1, 0, '2026-02-19 16:55:27', '2026-02-16 15:27:44', '2026-02-19 16:55:27', 19),
(54, 82, '1024', '192.168.23.124', NULL, 23, 'Secretaria jefatura industrial', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:27', '2026-02-16 15:30:10', '2026-02-19 16:55:27', 19),
(55, 82, '1025', '192.168.23.125', NULL, 23, 'Jefatura quimica', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:27', '2026-02-16 15:30:39', '2026-02-19 16:55:27', 19),
(56, 82, '1026', '192.168.23.126', NULL, 23, 'Secretaria jefatura quimica', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:27', '2026-02-16 15:31:08', '2026-02-19 16:55:27', 19),
(57, 86, '1027', '192.168.23.127', NULL, 23, 'Ciencias economicas administrativas', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:27', '2026-02-16 15:32:03', '2026-02-19 16:55:27', 24),
(58, 86, '1028', '192.168.23.128', NULL, 23, 'Secretaria CEA', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:27', '2026-02-16 15:32:43', '2026-02-19 16:55:27', 24),
(59, 62, '1029', '192.168.23.129', NULL, 23, 'Recursos humanos', 'Fanvil 3XSP', NULL, NULL, 1, 1, '2026-02-19 16:55:27', '2026-02-16 15:33:05', '2026-02-19 16:55:27', 22),
(60, 62, '1030', '192.168.23.130', NULL, 23, 'Secretaria recursos humanos', 'Favil 3SXP', NULL, NULL, 1, 0, '2026-02-19 16:55:29', '2026-02-16 15:33:30', '2026-02-19 16:55:29', 22),
(62, 83, '1040', '192.168.23.140', NULL, 23, 'Directora', 'Fanvil X6U', NULL, NULL, 1, 0, '2026-02-19 16:55:31', '2026-02-17 20:49:11', '2026-02-19 16:55:31', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `telefonos`
--
ALTER TABLE `telefonos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_extension` (`extension`),
  ADD KEY `switch_id` (`switch_id`),
  ADD KEY `fk_telefonos_edificio` (`edificio_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `telefonos`
--
ALTER TABLE `telefonos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `telefonos`
--
ALTER TABLE `telefonos`
  ADD CONSTRAINT `fk_telefonos_edificio` FOREIGN KEY (`edificio_id`) REFERENCES `edificios` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `telefonos_ibfk_1` FOREIGN KEY (`switch_id`) REFERENCES `switches` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

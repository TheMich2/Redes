-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-02-2026 a las 18:03:53
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
-- Estructura de tabla para la tabla `switches`
--

CREATE TABLE `switches` (
  `id` int(11) NOT NULL,
  `core_id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `ip_management` varchar(45) DEFAULT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `lat` decimal(10,7) DEFAULT NULL,
  `lng` decimal(10,7) DEFAULT NULL,
  `ultimo_ping_ok` tinyint(1) DEFAULT NULL,
  `ultimo_ping_at` timestamp NULL DEFAULT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `switches`
--

INSERT INTO `switches` (`id`, `core_id`, `nombre`, `ip_management`, `ubicacion`, `lat`, `lng`, `ultimo_ping_ok`, `ultimo_ping_at`, `creado_en`) VALUES
(1, 1, 'Switch Edificio A', '192.168.1.10', 'Edificio A', 17.0698000, -96.7256000, 1, '2026-02-16 04:58:09', '2026-02-14 03:02:06'),
(2, 1, 'Switch Edificio B', '192.168.1.11', 'Edificio B', 17.0690000, -96.7250000, 1, '2026-02-15 05:12:04', '2026-02-14 03:02:06'),
(51, 1, 'Switch Cómputo', '10.168.0.130', 'Cómputo', NULL, NULL, 0, '2026-02-15 05:12:06', '2026-02-15 05:05:35'),
(52, 1, 'Switch Lap Omar', '10.168.0.131', 'Lap Omar', NULL, NULL, 0, '2026-02-15 05:12:08', '2026-02-15 05:05:35'),
(53, 1, 'Switch Civil L', '10.168.0.132', 'Civil Edificio L', NULL, NULL, 0, '2026-02-16 04:58:49', '2026-02-15 05:05:35'),
(54, 1, 'Switch Electrónica', '10.168.0.133', 'Cubículos Electrónica', NULL, NULL, 0, '2026-02-15 05:12:04', '2026-02-15 05:05:35'),
(55, 1, 'Switch Ind. D53E', '10.168.0.134', 'Laboratorio Industrial', NULL, NULL, 0, '2026-02-15 05:12:06', '2026-02-15 05:05:35'),
(56, 1, 'Switch Wi-Fi Test', '10.168.0.135', 'pruebas wi-fi', NULL, NULL, 0, '2026-02-15 05:12:08', '2026-02-15 05:05:35'),
(57, 1, 'Switch Extreme Sys', '10.168.0.136', 'Extreme Sistemas', NULL, NULL, 0, '2026-02-15 05:12:10', '2026-02-15 05:05:35'),
(58, 1, 'Switch Escolar PSZ', '10.168.0.137', 'Servicios Escolares', NULL, NULL, 0, '2026-02-15 05:12:04', '2026-02-15 05:05:35'),
(59, 1, 'Switch Cs. Básicas', '10.168.0.138', 'Ciencias Básicas', NULL, NULL, 1, '2026-02-19 16:55:33', '2026-02-15 05:05:35'),
(60, 1, 'Switch Posgrado', '10.168.0.139', 'Posgrado', NULL, NULL, 0, '2026-02-16 04:58:25', '2026-02-15 05:05:35'),
(61, 1, 'Switch Dirección', '10.168.0.140', 'Dirección', NULL, NULL, 0, '2026-02-19 16:55:33', '2026-02-15 05:05:35'),
(62, 1, 'Switch RRHH', '10.168.0.141', 'Recursos Humanos', NULL, NULL, 0, '2026-02-19 16:55:35', '2026-02-15 05:05:35'),
(63, 1, 'Switch Depto Elec', '10.168.0.142', 'Electrónica - Depto.', NULL, NULL, 0, '2026-02-15 05:12:00', '2026-02-15 05:05:35'),
(64, 1, 'Switch Residentes', '10.168.0.143', 'OFICINA RESIDENTES', NULL, NULL, 0, '2026-02-15 05:12:02', '2026-02-15 05:05:35'),
(65, 1, 'Switch CEA Main', '10.168.0.144', 'CEA', NULL, NULL, 0, '2026-02-15 05:12:04', '2026-02-15 05:05:35'),
(66, 1, 'Switch Civil L (2)', '10.168.0.145', 'Civil Edificio L', NULL, NULL, 0, '2026-02-15 05:12:06', '2026-02-15 05:05:35'),
(67, 1, 'Switch Conacyt', '10.168.0.147', 'Cátedras Conacyt', NULL, NULL, 0, '2026-02-15 05:12:08', '2026-02-15 05:05:35'),
(68, 1, 'Switch Posgrado B', '10.168.0.148', 'Posgrado', NULL, NULL, 0, '2026-02-15 05:12:10', '2026-02-15 05:05:35'),
(69, 1, 'Switch Maestría', '10.168.0.149', 'Maestría en construccion', NULL, NULL, 0, '2026-02-15 05:11:59', '2026-02-15 05:05:35'),
(70, 1, 'Switch Eléctrica', '10.168.0.150', 'Eléctrica - Depto.', NULL, NULL, 0, '2026-02-15 05:12:01', '2026-02-15 05:05:35'),
(71, 1, 'Switch Simulación', '10.168.0.151', 'Simulación', NULL, NULL, 1, '2026-02-17 20:50:23', '2026-02-15 05:05:35'),
(72, 1, 'Switch Sim. Mecánica', '10.168.0.152', 'Simulación Mecánica', NULL, NULL, 0, '2026-02-16 04:58:11', '2026-02-15 05:05:35'),
(73, 1, 'Switch Mecánica', '10.168.0.153', 'Mecánica', NULL, NULL, 0, '2026-02-15 05:12:07', '2026-02-15 05:05:35'),
(74, 1, 'Switch Lab Elec 1', '10.168.0.154', 'Lab. Eléctrica 1', NULL, NULL, 0, '2026-02-15 05:12:09', '2026-02-15 05:05:35'),
(75, 1, 'Switch Des. Acad', '10.168.0.155', 'Desarrollo Académico', NULL, NULL, 1, '2026-02-17 15:28:31', '2026-02-15 05:05:35'),
(76, 1, 'Switch Depto Elec 2', '10.168.0.157', 'Electrónica - Depto.', NULL, NULL, 0, '2026-02-16 04:58:13', '2026-02-15 05:05:35'),
(77, 1, 'Switch Centro Info', '10.168.0.158', 'Centro de Información', NULL, NULL, 1, '2026-02-19 16:55:33', '2026-02-15 05:05:35'),
(78, 1, 'Switch Sistemas', '10.168.0.159', 'Sistemas - Depto', NULL, NULL, 1, '2026-02-19 16:55:33', '2026-02-15 05:05:35'),
(79, 1, 'Switch Escolares 2', '10.168.0.162', 'Servicios Escolares', NULL, NULL, 1, '2026-02-19 16:55:33', '2026-02-15 05:05:35'),
(80, 1, 'Switch Dirección 2', '10.168.0.163', 'Dirección', NULL, NULL, 0, '2026-02-17 15:28:11', '2026-02-15 05:05:35'),
(81, 1, 'Switch Centro Info 2', '10.168.0.164', 'Centro de Información', NULL, NULL, 0, '2026-02-15 05:12:06', '2026-02-15 05:05:35'),
(82, 1, 'Switch Bioquímica', '10.168.0.165', 'Bioquímica', NULL, NULL, 1, '2026-02-19 16:55:33', '2026-02-15 05:05:35'),
(83, 1, 'Switch Posgrado 0', '10.168.0.170', 'Posgrado 0', NULL, NULL, 1, '2026-02-19 16:55:35', '2026-02-15 05:05:35'),
(84, 1, 'Switch Posgrado 1', '10.168.0.171', 'Posgrado 1', NULL, NULL, 0, '2026-02-15 05:11:56', '2026-02-15 05:05:35'),
(85, 1, 'Switch Posgrado 2', '10.168.0.172', 'Posgrado 2', NULL, NULL, 0, '2026-02-15 05:11:58', '2026-02-15 05:05:35'),
(86, 1, 'Switch CEA 2', '10.168.0.173', 'CEA', NULL, NULL, 1, '2026-02-19 16:55:33', '2026-02-15 05:05:35'),
(87, 1, 'Switch Posgrado 3', '10.168.0.174', 'Posgrado 3', NULL, NULL, 0, '2026-02-15 05:12:02', '2026-02-15 05:05:35'),
(88, 1, 'Switch Lab Elec 2', '10.168.0.175', 'Lab. Eléctrica 2', NULL, NULL, 0, '2026-02-15 05:12:04', '2026-02-15 05:05:35'),
(89, 1, 'Switch Química 1', '10.168.0.181', 'Química 1', NULL, NULL, 0, '2026-02-15 05:12:06', '2026-02-15 05:05:35'),
(90, 1, 'Switch Química 2', '10.168.0.182', 'Química 2', NULL, NULL, 0, '2026-02-15 05:12:08', '2026-02-15 05:05:35'),
(91, 1, 'Switch Química 3', '10.168.0.183', 'Química 3', NULL, NULL, 0, '2026-02-15 05:12:10', '2026-02-15 05:05:35'),
(92, 1, 'Switch Química 4', '10.168.0.184', 'Química 4', NULL, NULL, 0, '2026-02-15 05:11:57', '2026-02-15 05:05:35'),
(93, 1, 'Switch Audiovisual', '10.168.0.185', 'Audiovisual Ing', NULL, NULL, 0, '2026-02-15 05:11:59', '2026-02-15 05:05:35'),
(94, 1, 'Switch Química 5', '10.168.0.186', 'Química 5', NULL, NULL, 0, '2026-02-15 05:12:01', '2026-02-15 05:05:35'),
(95, 1, 'Switch Química 6', '10.168.0.187', 'Química 6', NULL, NULL, 0, '2026-02-15 05:12:03', '2026-02-15 05:05:35'),
(96, 1, 'Switch Industrial', '10.168.0.188', 'Industrial', NULL, NULL, 0, '2026-02-15 05:12:05', '2026-02-15 05:05:35'),
(97, 1, 'Switch Cómputo Final', '10.168.0.189', 'COMPUTO', NULL, NULL, 1, '2026-02-19 16:55:33', '2026-02-15 05:05:35');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `switches`
--
ALTER TABLE `switches`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_switches_core` (`core_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `switches`
--
ALTER TABLE `switches`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=98;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `switches`
--
ALTER TABLE `switches`
  ADD CONSTRAINT `switches_ibfk_1` FOREIGN KEY (`core_id`) REFERENCES `core` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

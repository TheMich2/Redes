-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-02-2026 a las 18:03:57
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
-- Estructura de tabla para la tabla `edificios`
--

CREATE TABLE `edificios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `lat` decimal(10,7) DEFAULT NULL,
  `lng` decimal(10,7) DEFAULT NULL,
  `switch_id` int(11) DEFAULT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `edificios`
--

INSERT INTO `edificios` (`id`, `nombre`, `ubicacion`, `lat`, `lng`, `switch_id`, `creado_en`) VALUES
(15, 'Dirrecion', 'Dirrecion planta alta', 17.0774100, -96.7451150, 61, '2026-02-16 05:03:38'),
(17, 'Centro de informacion', 'Biblioteca', 17.0775950, -96.7442050, 77, '2026-02-16 05:47:37'),
(18, 'Centro de computo', 'Planta alta', 17.0790730, -96.7443340, 97, '2026-02-16 05:48:32'),
(19, 'Bioquimica', 'Bioquimica planta alta', 17.0793940, -96.7438460, 82, '2026-02-16 06:14:49'),
(20, 'Edificio de sistemas', 'Cubiculos', 17.0760560, -96.7447420, 78, '2026-02-16 06:15:44'),
(21, 'Ciencias basicas', 'Cubiculos', 17.0769050, -96.7445430, 59, '2026-02-16 06:17:56'),
(22, 'Recursos humanos', 'Dirrecion planta alta', 17.0774820, -96.7451870, 62, '2026-02-16 06:21:00'),
(23, 'Division estudios', 'Division de estudios', 17.0776590, -96.7449910, 79, '2026-02-16 06:21:37'),
(24, 'Ciencias economicas administrativo', 'Ciencias economicas administrativo', 17.0766950, -96.7445650, 86, '2026-02-16 06:23:17'),
(26, 'Servicios escolares', 'Servicios escolares', 17.0776840, -96.7451230, 79, '2026-02-17 15:16:49');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `edificios`
--
ALTER TABLE `edificios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_edificio_nombre` (`nombre`),
  ADD KEY `switch_id` (`switch_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `edificios`
--
ALTER TABLE `edificios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `edificios`
--
ALTER TABLE `edificios`
  ADD CONSTRAINT `edificios_ibfk_1` FOREIGN KEY (`switch_id`) REFERENCES `switches` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

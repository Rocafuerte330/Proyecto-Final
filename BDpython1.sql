-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 15-07-2025 a las 21:59:12
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `BDpython1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `DICOM_NIFTI`
--

CREATE TABLE `DICOM_NIFTI` (
  `Primario` int(50) NOT NULL,
  `Ruta_Dicom` varchar(500) DEFAULT NULL,
  `Nombre_Carpeta` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Otros_archivos`
--

CREATE TABLE `Otros_archivos` (
  `id_archivo` int(11) NOT NULL,
  `tipo_archivo` enum('csv','mat','jpg','png') DEFAULT NULL,
  `nombre_archivo` varchar(255) NOT NULL,
  `fecha_trabajo` date NOT NULL DEFAULT current_timestamp(),
  `ruta_archivo` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Usuarios`
--

CREATE TABLE `Usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre_usuario` varchar(50) NOT NULL,
  `contrasena` varchar(50) NOT NULL,
  `tipo_usuario` enum('Experto en Imágenes','Experto en Señales') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Usuarios`
--

INSERT INTO `Usuarios` (`id_usuario`, `nombre_usuario`, `contrasena`, `tipo_usuario`) VALUES
(1, 'Jose.R', 'loleljuego_01', 'Experto en Imágenes'),
(2, 'Dani.A', 'loleljuego_02', 'Experto en Señales');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `DICOM_NIFTI`
--
ALTER TABLE `DICOM_NIFTI`
  ADD PRIMARY KEY (`Primario`);

--
-- Indices de la tabla `Otros_archivos`
--
ALTER TABLE `Otros_archivos`
  ADD PRIMARY KEY (`id_archivo`);

--
-- Indices de la tabla `Usuarios`
--
ALTER TABLE `Usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `DICOM_NIFTI`
--
ALTER TABLE `DICOM_NIFTI`
  MODIFY `Primario` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `Otros_archivos`
--
ALTER TABLE `Otros_archivos`
  MODIFY `id_archivo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT de la tabla `Usuarios`
--
ALTER TABLE `Usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

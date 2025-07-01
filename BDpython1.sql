-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 01-07-2025 a las 02:10:36
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
  `Patient_ID` varchar(50) NOT NULL,
  `Patient_Name` varchar(255) DEFAULT NULL,
  `Patient_Birth_Date` date DEFAULT NULL,
  `Patient_Sex` enum('M','F','O') DEFAULT NULL,
  `Ruta_Dicom` varchar(500) DEFAULT NULL,
  `Ruta_Nifti` varchar(500) DEFAULT NULL,
  `Pixel_Array` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`Pixel_Array`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `DICOM_NIFTI`
--

INSERT INTO `DICOM_NIFTI` (`Patient_ID`, `Patient_Name`, `Patient_Birth_Date`, `Patient_Sex`, `Ruta_Dicom`, `Ruta_Nifti`, `Pixel_Array`) VALUES
('C3N-00247', 'C3N-00247', NULL, 'F', NULL, NULL, '{\r\n  \"array\": [\r\n    [356, 244, 201, 190, 224, 76],\r\n    [309, 387, 370, 122, 17, 6],\r\n    [334, 476, 486, 29, 46, 47],\r\n    [98, 188, 186, 156, 86, 125],\r\n    [66, 138, 139, 221, 74, 81],\r\n    [168, 173, 100, 188, 135, 147]\r\n  ],\r\n  \"shape\": [512, 512],\r\n  \"dtype\": \"uint16\"\r\n}');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Otros_archivos`
--

CREATE TABLE `Otros_archivos` (
  `id_archivo` int(11) NOT NULL,
  `tipo_archivo` enum('csv','mat','jpg','png') NOT NULL,
  `nombre_archivo` varchar(255) NOT NULL,
  `fecha_trabajo` date NOT NULL,
  `ruta_archivo` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Otros_archivos`
--

INSERT INTO `Otros_archivos` (`id_archivo`, `tipo_archivo`, `nombre_archivo`, `fecha_trabajo`, `ruta_archivo`) VALUES
(1, 'csv', 'archivo1.csv', '2025-06-30', 'otros_archivos/archivo1.csv');

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
  ADD PRIMARY KEY (`Patient_ID`);

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
-- AUTO_INCREMENT de la tabla `Otros_archivos`
--
ALTER TABLE `Otros_archivos`
  MODIFY `id_archivo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `Usuarios`
--
ALTER TABLE `Usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

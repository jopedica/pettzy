-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: pettzy
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `about_blocks`
--

DROP TABLE IF EXISTS `about_blocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `about_blocks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(120) NOT NULL,
  `body` text,
  `image` varchar(200) DEFAULT '',
  `icon` varchar(100) DEFAULT '',
  `section` varchar(40) DEFAULT 'default',
  `display_order` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_about_section_order` (`section`,`display_order`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `about_blocks`
--

LOCK TABLES `about_blocks` WRITE;
/*!40000 ALTER TABLE `about_blocks` DISABLE KEYS */;
INSERT INTO `about_blocks` VALUES (1,'Nossa história','A Petzzy nasceu para facilitar a vida de tutores, conectando serviços de qualidade com agendamento simples e transparente.','','fa-paw','story',10,'2025-09-25 03:48:43','2025-09-25 03:48:43'),(2,'Missão','Cuidar do bem-estar dos pets oferecendo uma experiência prática, confiável e acessível para tutores e prestadores.','','fa-heart','mission',20,'2025-09-25 03:48:43','2025-09-25 03:48:43'),(3,'Visão','teste123','','fa-star','vision',30,'2025-09-25 03:48:43','2025-09-25 05:55:23'),(4,'Valores','Amor aos animais, confiança, transparência, acessibilidade e melhoria contínua.','','fa-handshake','values',40,'2025-09-25 03:48:43','2025-09-25 03:48:43');
/*!40000 ALTER TABLE `about_blocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT '0.00',
  `icon` varchar(200) DEFAULT '',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_services_active_name` (`is_active`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'Banho & Tosa','Higienização completa com produtos hipoalergênicos e tosa higiênica.',80.00,'banho.png',1,'2025-09-25 03:48:43','2025-09-25 04:04:11'),(2,'Vacinação','Aplicação de vacinas com controle de carteira e lembretes automáticos.',120.00,'vacinacao.jpg',1,'2025-09-25 03:48:43','2025-09-25 04:14:20'),(3,'Consulta Veterinária','Atendimento clínico geral com avaliação completa e orientações.',150.00,'consulta.png',1,'2025-09-25 03:48:43','2025-09-25 04:14:20'),(4,'Dog Walk','Passeio com seu cachorro',40.00,'passeio.png',1,'2025-09-25 04:33:26','2025-09-25 04:33:28');
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `email` varchar(120) NOT NULL,
  `cpf` char(11) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_email` (`email`),
  UNIQUE KEY `uq_users_cpf` (`cpf`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'João Pedro Dias Carvalho','jopedica1330@gmail.com','05651341161','61999711460','scrypt:32768:8:1$5AjXuVLn1ztUm01P$3f999d85f99feb334836e8998c878e1ed917c17a1606f4906b475cacca047fd1718812831e947588996b79fd89a5b091872ee92f44c87e755f404d26dec9a1aa','2025-09-25 04:57:24','2025-09-25 04:57:24'),(2,'manel','manelpinga@gmail.com','27973280197','12121212122','scrypt:32768:8:1$tTXZQnoTcIG4GZWS$cc409923b6a4b6021dc0bd9076f6438269ebaa3ac8708cc4ac9fc6f7e2664c60f2bac6cd3376dac4902330f9cca11b41c4a9358c5c8337cf680c5fa2f971c461','2025-09-25 05:51:22','2025-09-25 05:51:22');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-25  2:56:27

-- MySQL dump 10.13  Distrib 5.5.20, for Linux (x86_64)
--
-- Host: localhost    Database: rws_dnrd
-- ------------------------------------------------------
-- Server version	5.5.20-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `roid` varchar(30) COLLATE utf8_bin NOT NULL,
  `email` varchar(80) COLLATE utf8_bin NOT NULL,
  `voice` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `voice_x` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `fax` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `fax_x` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `authInfo` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `clID` smallint(5) unsigned NOT NULL,
  `crID` smallint(5) unsigned DEFAULT NULL,
  `upID` int(10) unsigned DEFAULT NULL,
  `crDate` datetime NOT NULL,
  `upDate` datetime DEFAULT NULL,
  `trDate` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `alias` (`roid`),
  KEY `clID` (`clID`),
  KEY `crID` (`crID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contact_disclose`
--

DROP TABLE IF EXISTS `contact_disclose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_disclose` (
  `contact_id` int(10) unsigned NOT NULL,
  `field` varchar(30) COLLATE utf8_bin NOT NULL,
  `type` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `flag` tinyint(3) unsigned NOT NULL DEFAULT '1',
  UNIQUE KEY `contact_id_2` (`contact_id`,`field`,`type`),
  KEY `contact_id` (`contact_id`),
  CONSTRAINT `contact_disclose_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `contact` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contact_postalinfo`
--

DROP TABLE IF EXISTS `contact_postalinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_postalinfo` (
  `contact_id` int(10) unsigned NOT NULL,
  `name` varchar(100) COLLATE utf8_bin NOT NULL,
  `org` varchar(100) COLLATE utf8_bin NOT NULL,
  `addr1` varchar(100) COLLATE utf8_bin NOT NULL,
  `addr2` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `addr3` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `city` varchar(60) COLLATE utf8_bin NOT NULL,
  `sp` varchar(60) COLLATE utf8_bin NOT NULL,
  `pc` varchar(20) COLLATE utf8_bin NOT NULL,
  `cc` varchar(2) COLLATE utf8_bin NOT NULL,
  `type` tinyint(4) NOT NULL,
  UNIQUE KEY `contact_type_uq` (`contact_id`,`type`),
  KEY `contact_id` (`contact_id`),
  CONSTRAINT `contact_postalinfo_ibfk_3` FOREIGN KEY (`contact_id`) REFERENCES `contact` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contact_status`
--

DROP TABLE IF EXISTS `contact_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_status` (
  `contact_id` int(10) unsigned NOT NULL,
  `status_id` tinyint(3) unsigned NOT NULL,
  UNIQUE KEY `contact_id` (`contact_id`,`status_id`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `contact_status_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `contact` (`id`),
  CONSTRAINT `contact_status_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Table structure for table `domain`
--

DROP TABLE IF EXISTS `domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `roid` varchar(30) COLLATE utf8_bin NOT NULL,
  `name` varchar(100) COLLATE utf8_bin NOT NULL,
  `registrant_contact_id` int(10) unsigned NOT NULL,
  `authInfo` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `clID` smallint(6) NOT NULL,
  `crID` smallint(6) DEFAULT NULL,
  `upID` smallint(6) DEFAULT NULL,
  `crDate` datetime DEFAULT NULL,
  `upDate` datetime DEFAULT NULL,
  `exDate` datetime NOT NULL,
  `trDate` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `registrant_contact_id` (`registrant_contact_id`),
  CONSTRAINT `domain_ibfk_1` FOREIGN KEY (`registrant_contact_id`) REFERENCES `contact` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Table structure for table `domain_contact`
--

DROP TABLE IF EXISTS `domain_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_contact` (
  `domain_id` int(10) unsigned NOT NULL,
  `domain_contact_type_id` tinyint(3) unsigned NOT NULL,
  `contact_id` int(10) unsigned NOT NULL,
  UNIQUE KEY `domain_type_contact_uq` (`domain_id`,`domain_contact_type_id`,`contact_id`),
  KEY `domain_contact_type_id` (`domain_contact_type_id`),
  KEY `contact_id` (`contact_id`),
  CONSTRAINT `domain_contact_ibfk_1` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`),
  CONSTRAINT `domain_contact_ibfk_2` FOREIGN KEY (`domain_contact_type_id`) REFERENCES `domain_contact_type` (`id`),
  CONSTRAINT `domain_contact_ibfk_3` FOREIGN KEY (`contact_id`) REFERENCES `contact` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Table structure for table `domain_contact_type`
--

DROP TABLE IF EXISTS `domain_contact_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_contact_type` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `domain_host`
--

DROP TABLE IF EXISTS `domain_host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_host` (
  `domain_id` int(10) unsigned NOT NULL,
  `host_id` int(10) unsigned NOT NULL,
  UNIQUE KEY `domain_host_uq` (`domain_id`,`host_id`),
  KEY `host_id` (`host_id`),
  CONSTRAINT `domain_host_ibfk_1` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`),
  CONSTRAINT `domain_host_ibfk_2` FOREIGN KEY (`host_id`) REFERENCES `host` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `domain_ns`
--

DROP TABLE IF EXISTS `domain_ns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_ns` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `domain_id` int(10) unsigned NOT NULL,
  `hostname` varchar(80) COLLATE utf8_bin DEFAULT NULL,
  `host_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `domain_id_2` (`domain_id`,`hostname`,`host_id`),
  KEY `domain_id` (`domain_id`),
  KEY `host_id` (`host_id`),
  CONSTRAINT `domain_ns_ibfk_1` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`),
  CONSTRAINT `domain_ns_ibfk_2` FOREIGN KEY (`host_id`) REFERENCES `host` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `domain_ns_ip`
--

DROP TABLE IF EXISTS `domain_ns_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_ns_ip` (
  `domain_ns_id` int(10) unsigned NOT NULL,
  `ip` varchar(48) COLLATE utf8_bin NOT NULL,
  `type` tinyint(4) NOT NULL DEFAULT '4',
  KEY `domain_ns_id` (`domain_ns_id`),
  CONSTRAINT `domain_ns_ip_ibfk_1` FOREIGN KEY (`domain_ns_id`) REFERENCES `domain_ns` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='help table for hostAttr IPs';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `domain_status`
--

DROP TABLE IF EXISTS `domain_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_status` (
  `domain_id` int(10) unsigned NOT NULL,
  `status_id` tinyint(3) unsigned NOT NULL,
  UNIQUE KEY `domain_id` (`domain_id`,`status_id`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `domain_status_ibfk_1` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`),
  CONSTRAINT `domain_status_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `host`
--

DROP TABLE IF EXISTS `host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_bin NOT NULL,
  `clID` smallint(5) unsigned NOT NULL,
  `crID` smallint(5) unsigned NOT NULL,
  `upID` smallint(5) unsigned DEFAULT NULL,
  `crDate` datetime NOT NULL,
  `upDate` datetime DEFAULT NULL,
  `trDate` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `clID` (`clID`),
  KEY `crID` (`crID`),
  KEY `upID` (`upID`),
  CONSTRAINT `host_ibfk_1` FOREIGN KEY (`clID`) REFERENCES `registrar` (`id`),
  CONSTRAINT `host_ibfk_2` FOREIGN KEY (`crID`) REFERENCES `registrar` (`id`),
  CONSTRAINT `host_ibfk_3` FOREIGN KEY (`upID`) REFERENCES `registrar` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `host_ip`
--

DROP TABLE IF EXISTS `host_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_ip` (
  `host_id` int(10) unsigned NOT NULL,
  `ip` varchar(48) COLLATE utf8_bin NOT NULL,
  `type` tinyint(4) NOT NULL DEFAULT '4',
  KEY `host_id` (`host_id`),
  CONSTRAINT `host_ip_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `host` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `host_status`
--

DROP TABLE IF EXISTS `host_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_status` (
  `host_id` int(10) unsigned NOT NULL,
  `status_id` tinyint(3) unsigned NOT NULL,
  UNIQUE KEY `host_id` (`host_id`,`status_id`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `host_status_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `host` (`id`),
  CONSTRAINT `host_status_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Table structure for table `registrar`
--

DROP TABLE IF EXISTS `registrar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registrar` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `roid` varchar(10) COLLATE utf8_bin NOT NULL,
  `name` varchar(60) COLLATE utf8_bin NOT NULL,
  `href` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `alias` (`roid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES (1,'clientDeleteProhibited'),(2,'serverDeleteProhibited'),(3,'clientUpdateProhibited'),(4,'serverUpdateProhibited'),(5,'linked'),(6,'ok'),(7,'pendingCreate'),(8,'pendingDelete'),(9,'pendingTransfer'),(10,'pendingUpdate'),(11,'clientHold'),(12,'serverHold'),(13,'clientRenewProhibited'),(14,'serverRenewProhibited'),(15,'clientTransferProhibited'),(16,'serverTransferProhibited'),(17,'inactive'),(18,'pendingTransfer'),(19,'pendingRenew'),(20,'pendingRestore'),(21,'redemptionPeriod');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-06-11 19:06:10

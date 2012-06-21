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
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (1,'CR12376439','domain-admin@icann.org','+1.4242171313',NULL,'+1.4242171313',NULL,NULL,1,1,NULL,'1998-09-14 04:00:00','2012-01-10 21:32:13',NULL),(2,'C2576748-LRMS','dns-admin@GOOGLE.COM','+1.6503300100',NULL,'+1.6506181499',NULL,NULL,2,2,2,'2002-10-01 18:53:30','2012-05-17 17:14:39',NULL),(3,'C1439798-LRMS','hostmaster@alldomains.com','+1.9256859600',NULL,'+1.9256859620',NULL,NULL,2,2,2,'2001-11-07 23:41:24','2012-05-17 17:18:16',NULL);
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `contact_disclose`
--

LOCK TABLES `contact_disclose` WRITE;
/*!40000 ALTER TABLE `contact_disclose` DISABLE KEYS */;
INSERT INTO `contact_disclose` VALUES (1,'email',0,0),(1,'name',2,1);
/*!40000 ALTER TABLE `contact_disclose` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `contact_postalinfo`
--

LOCK TABLES `contact_postalinfo` WRITE;
/*!40000 ALTER TABLE `contact_postalinfo` DISABLE KEYS */;
INSERT INTO `contact_postalinfo` VALUES (1,'Domain Administrator','ICANN','4676 Admiralty Way #330',NULL,NULL,'Marina del Rey','CA','90292','US',1),(1,'Domain Administrator','ICÄNN','4676 Admiralty Way #330',NULL,NULL,'Marina del Rey','CA','90292','US',2),(2,'DNS Admin','Google Inc.','2400 E. Bayshore Pkwy',NULL,NULL,'Mountain View','CA','94043','US',1),(3,'Center Network','Alldomains.com','1800 Sutter St.','Suite 100','<a href=\"test\">Testescape</a>','Concord','CA','94520','US',1);
/*!40000 ALTER TABLE `contact_postalinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `contact_status`
--

LOCK TABLES `contact_status` WRITE;
/*!40000 ALTER TABLE `contact_status` DISABLE KEYS */;
INSERT INTO `contact_status` VALUES (1,3),(1,15);
/*!40000 ALTER TABLE `contact_status` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `domain`
--

LOCK TABLES `domain` WRITE;
/*!40000 ALTER TABLE `domain` DISABLE KEYS */;
INSERT INTO `domain` VALUES (1,'D2347548-LROR','icann.org',1,NULL,1,1,NULL,'1998-09-14 04:00:00','2012-01-10 21:32:13','2017-12-07 17:04:26',NULL),(2,'D5785415-LRMS','xn--ggle-5qaa.info',2,NULL,2,2,NULL,'2004-03-17 01:33:06','2012-05-17 17:14:39','2013-03-17 01:33:06',NULL);
/*!40000 ALTER TABLE `domain` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `domain_contact`
--

LOCK TABLES `domain_contact` WRITE;
/*!40000 ALTER TABLE `domain_contact` DISABLE KEYS */;
INSERT INTO `domain_contact` VALUES (1,2,1),(2,2,2),(1,3,1),(2,3,3),(2,4,2);
/*!40000 ALTER TABLE `domain_contact` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `domain_contact_type`
--

LOCK TABLES `domain_contact_type` WRITE;
/*!40000 ALTER TABLE `domain_contact_type` DISABLE KEYS */;
INSERT INTO `domain_contact_type` VALUES (2,'admin'),(4,'billing'),(3,'tech');
/*!40000 ALTER TABLE `domain_contact_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `domain_host`
--

LOCK TABLES `domain_host` WRITE;
/*!40000 ALTER TABLE `domain_host` DISABLE KEYS */;
INSERT INTO `domain_host` VALUES (1,1);
/*!40000 ALTER TABLE `domain_host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `domain_ns`
--

LOCK TABLES `domain_ns` WRITE;
/*!40000 ALTER TABLE `domain_ns` DISABLE KEYS */;
INSERT INTO `domain_ns` VALUES (1,1,NULL,1),(2,1,'A.IANA-SERVERS.NET',NULL),(3,1,'B.IANA-SERVERS.NET',NULL),(4,1,'C.IANA-SERVERS.NET',NULL),(5,1,'D.IANA-SERVERS.NET',NULL),(6,2,'ns1.google.com',NULL),(7,2,'ns2.google.com',NULL),(8,2,'ns3.google.com',NULL),(9,2,'ns4.google.com',NULL);
/*!40000 ALTER TABLE `domain_ns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `domain_ns_ip`
--

LOCK TABLES `domain_ns_ip` WRITE;
/*!40000 ALTER TABLE `domain_ns_ip` DISABLE KEYS */;
INSERT INTO `domain_ns_ip` VALUES (2,'199.43.132.53',4),(2,'2001:500:8c::53',6),(3,'199.43.133.53',4),(3,'2001:500:8d::53',6);
/*!40000 ALTER TABLE `domain_ns_ip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `domain_status`
--

LOCK TABLES `domain_status` WRITE;
/*!40000 ALTER TABLE `domain_status` DISABLE KEYS */;
INSERT INTO `domain_status` VALUES (1,1),(1,2),(1,3),(1,4),(1,13),(1,14),(1,15),(1,16);
/*!40000 ALTER TABLE `domain_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `host`
--

LOCK TABLES `host` WRITE;
/*!40000 ALTER TABLE `host` DISABLE KEYS */;
INSERT INTO `host` VALUES (1,'ns.icann.org',1,1,NULL,'1998-09-14 04:00:00',NULL,NULL);
/*!40000 ALTER TABLE `host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `host_ip`
--

LOCK TABLES `host_ip` WRITE;
/*!40000 ALTER TABLE `host_ip` DISABLE KEYS */;
INSERT INTO `host_ip` VALUES (1,'199.4.138.53',4),(1,'2001:500:89::53',6);
/*!40000 ALTER TABLE `host_ip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `host_status`
--

LOCK TABLES `host_status` WRITE;
/*!40000 ALTER TABLE `host_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_status` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `registrar`
--

LOCK TABLES `registrar` WRITE;
/*!40000 ALTER TABLE `registrar` DISABLE KEYS */;
INSERT INTO `registrar` VALUES (1,'R91-LROR','GoDaddy.com, LLC','http://www.godaddy.com/'),(2,'R151-LRMS','Markmonitor Inc.','http://www.markmonitor.com/');
/*!40000 ALTER TABLE `registrar` ENABLE KEYS */;
UNLOCK TABLES;

-- Dump completed on 2012-06-11 19:06:10

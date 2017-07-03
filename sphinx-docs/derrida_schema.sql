-- MySQL dump 10.13  Distrib 5.7.17, for osx10.12 (x86_64)
--
-- Host: localhost    Database: test_derrida
-- ------------------------------------------------------
-- Server version	5.7.17

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Data Editors');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,13),(2,1,14),(3,1,15),(4,1,25),(5,1,26),(6,1,27),(7,1,28),(8,1,29),(9,1,30),(10,1,31),(11,1,32),(12,1,33),(13,1,34),(14,1,35),(15,1,36),(16,1,37),(17,1,38),(18,1,39),(19,1,40),(20,1,41),(21,1,42),(22,1,43),(23,1,44),(24,1,45),(25,1,46),(26,1,47),(27,1,48),(28,1,49),(29,1,50),(30,1,51),(31,1,52),(32,1,53),(33,1,54),(34,1,55),(35,1,56),(36,1,57),(37,1,58),(38,1,59),(39,1,60),(40,1,61),(41,1,62),(42,1,63),(43,1,64),(44,1,65),(45,1,66),(46,1,67),(47,1,68),(48,1,69),(49,1,70),(50,1,71),(51,1,72),(52,1,73),(53,1,74),(54,1,75),(55,1,76),(56,1,77),(57,1,78),(58,1,79),(59,1,80),(60,1,81),(61,1,82),(62,1,83),(63,1,84),(64,1,85),(65,1,86),(66,1,87),(67,1,88),(68,1,89),(69,1,90),(70,1,91),(71,1,92),(72,1,93);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add group',4,'add_group'),(11,'Can change group',4,'change_group'),(12,'Can delete group',4,'delete_group'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add proxy granting ticket',7,'add_proxygrantingticket'),(20,'Can change proxy granting ticket',7,'change_proxygrantingticket'),(21,'Can delete proxy granting ticket',7,'delete_proxygrantingticket'),(22,'Can add session ticket',8,'add_sessionticket'),(23,'Can change session ticket',8,'change_sessionticket'),(24,'Can delete session ticket',8,'delete_sessionticket'),(25,'Can add owning institution',9,'add_owninginstitution'),(26,'Can change owning institution',9,'change_owninginstitution'),(27,'Can delete owning institution',9,'delete_owninginstitution'),(28,'Can add Catalogue',10,'add_instancecatalogue'),(29,'Can change Catalogue',10,'change_instancecatalogue'),(30,'Can delete Catalogue',10,'delete_instancecatalogue'),(31,'Can add Person/Book Interaction',11,'add_personbook'),(32,'Can change Person/Book Interaction',11,'change_personbook'),(33,'Can delete Person/Book Interaction',11,'delete_personbook'),(34,'Can add creator type',12,'add_creatortype'),(35,'Can change creator type',12,'change_creatortype'),(36,'Can delete creator type',12,'delete_creatortype'),(37,'Can add derrida work',13,'add_derridawork'),(38,'Can change derrida work',13,'change_derridawork'),(39,'Can delete derrida work',13,'delete_derridawork'),(40,'Can add reference type',14,'add_referencetype'),(41,'Can change reference type',14,'change_referencetype'),(42,'Can delete reference type',14,'delete_referencetype'),(43,'Can add person book relationship type',15,'add_personbookrelationshiptype'),(44,'Can change person book relationship type',15,'change_personbookrelationshiptype'),(45,'Can delete person book relationship type',15,'delete_personbookrelationshiptype'),(46,'Can add Derrida library work instance',16,'add_instance'),(47,'Can change Derrida library work instance',16,'change_instance'),(48,'Can delete Derrida library work instance',16,'delete_instance'),(49,'Can add journal',17,'add_journal'),(50,'Can change journal',17,'change_journal'),(51,'Can delete journal',17,'delete_journal'),(52,'Can add Language',18,'add_instancelanguage'),(53,'Can change Language',18,'change_instancelanguage'),(54,'Can delete Language',18,'delete_instancelanguage'),(55,'Can add language',19,'add_language'),(56,'Can change language',19,'change_language'),(57,'Can delete language',19,'delete_language'),(58,'Can add publisher',20,'add_publisher'),(59,'Can change publisher',20,'change_publisher'),(60,'Can delete publisher',20,'delete_publisher'),(61,'Can add Subject',21,'add_worksubject'),(62,'Can change Subject',21,'change_worksubject'),(63,'Can delete Subject',21,'delete_worksubject'),(64,'Can add subject',22,'add_subject'),(65,'Can change subject',22,'change_subject'),(66,'Can delete subject',22,'delete_subject'),(67,'Can add Language',23,'add_worklanguage'),(68,'Can change Language',23,'change_worklanguage'),(69,'Can delete Language',23,'delete_worklanguage'),(70,'Can add Derrida library work',24,'add_work'),(71,'Can change Derrida library work',24,'change_work'),(72,'Can delete Derrida library work',24,'delete_work'),(73,'Can add reference',25,'add_reference'),(74,'Can change reference',25,'change_reference'),(75,'Can delete reference',25,'delete_reference'),(76,'Can add instance creator',26,'add_instancecreator'),(77,'Can change instance creator',26,'change_instancecreator'),(78,'Can delete instance creator',26,'delete_instancecreator'),(79,'Can add place',27,'add_place'),(80,'Can change place',27,'change_place'),(81,'Can delete place',27,'delete_place'),(82,'Can add relationship',28,'add_relationship'),(83,'Can change relationship',28,'change_relationship'),(84,'Can delete relationship',28,'delete_relationship'),(85,'Can add person',29,'add_person'),(86,'Can change person',29,'change_person'),(87,'Can delete person',29,'delete_person'),(88,'Can add residence',30,'add_residence'),(89,'Can change residence',30,'change_residence'),(90,'Can delete residence',30,'delete_residence'),(91,'Can add relationship type',31,'add_relationshiptype'),(92,'Can change relationship type',31,'change_relationshiptype'),(93,'Can delete relationship type',31,'delete_relationshiptype'),(94,'Can add source type',32,'add_sourcetype'),(95,'Can change source type',32,'change_sourcetype'),(96,'Can delete source type',32,'delete_sourcetype'),(97,'Can add bibliography',33,'add_bibliography'),(98,'Can change bibliography',33,'change_bibliography'),(99,'Can delete bibliography',33,'delete_bibliography'),(100,'Can add footnote',34,'add_footnote'),(101,'Can change footnote',34,'change_footnote'),(102,'Can delete footnote',34,'delete_footnote');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_creatortype`
--

DROP TABLE IF EXISTS `books_creatortype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_creatortype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  `uri` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_creatortype`
--

LOCK TABLES `books_creatortype` WRITE;
/*!40000 ALTER TABLE `books_creatortype` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_creatortype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_derridawork`
--

DROP TABLE IF EXISTS `books_derridawork`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_derridawork` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `short_title` varchar(255) NOT NULL,
  `full_citation` longtext NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_derridawork`
--

LOCK TABLES `books_derridawork` WRITE;
/*!40000 ALTER TABLE `books_derridawork` DISABLE KEYS */;
INSERT INTO `books_derridawork` VALUES (1,'','De la grammatologie','Placeholder citation',0);
/*!40000 ALTER TABLE `books_derridawork` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_instance`
--

DROP TABLE IF EXISTS `books_instance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_instance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `alternate_title` varchar(255) NOT NULL,
  `zotero_id` varchar(255) NOT NULL,
  `is_extant` tinyint(1) NOT NULL,
  `is_annotated` tinyint(1) NOT NULL,
  `is_translation` tinyint(1) NOT NULL,
  `dimensions` varchar(255) NOT NULL,
  `copyright_year` int(10) unsigned DEFAULT NULL,
  `print_date` date DEFAULT NULL,
  `print_date_day_known` tinyint(1) NOT NULL,
  `print_date_month_known` tinyint(1) NOT NULL,
  `print_date_year_known` tinyint(1) NOT NULL,
  `uri` varchar(200) NOT NULL,
  `has_dedication` tinyint(1) NOT NULL,
  `has_insertions` tinyint(1) NOT NULL,
  `start_page` varchar(20) DEFAULT NULL,
  `end_page` varchar(20) DEFAULT NULL,
  `collected_in_id` int(11) DEFAULT NULL,
  `journal_id` int(11) DEFAULT NULL,
  `publisher_id` int(11) DEFAULT NULL,
  `work_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_instance_collected_in_id_dbb43376_fk_books_instance_id` (`collected_in_id`),
  KEY `books_instance_journal_id_dfbd8d81_fk_books_journal_id` (`journal_id`),
  KEY `books_instance_publisher_id_749c6e79_fk_books_publisher_id` (`publisher_id`),
  KEY `books_instance_work_id_c6e78f6b_fk_books_work_id` (`work_id`),
  CONSTRAINT `books_instance_collected_in_id_dbb43376_fk_books_instance_id` FOREIGN KEY (`collected_in_id`) REFERENCES `books_instance` (`id`),
  CONSTRAINT `books_instance_journal_id_dfbd8d81_fk_books_journal_id` FOREIGN KEY (`journal_id`) REFERENCES `books_journal` (`id`),
  CONSTRAINT `books_instance_publisher_id_749c6e79_fk_books_publisher_id` FOREIGN KEY (`publisher_id`) REFERENCES `books_publisher` (`id`),
  CONSTRAINT `books_instance_work_id_c6e78f6b_fk_books_work_id` FOREIGN KEY (`work_id`) REFERENCES `books_work` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_instance`
--

LOCK TABLES `books_instance` WRITE;
/*!40000 ALTER TABLE `books_instance` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_instance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_instance_cited_in`
--

DROP TABLE IF EXISTS `books_instance_cited_in`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_instance_cited_in` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` int(11) NOT NULL,
  `derridawork_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_instance_cited_in_instance_id_derridawork_id_c2cce7cc_uniq` (`instance_id`,`derridawork_id`),
  KEY `books_instance_cited_derridawork_id_18c0d15c_fk_books_der` (`derridawork_id`),
  CONSTRAINT `books_instance_cited_derridawork_id_18c0d15c_fk_books_der` FOREIGN KEY (`derridawork_id`) REFERENCES `books_derridawork` (`id`),
  CONSTRAINT `books_instance_cited_instance_id_b5928328_fk_books_ins` FOREIGN KEY (`instance_id`) REFERENCES `books_instance` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_instance_cited_in`
--

LOCK TABLES `books_instance_cited_in` WRITE;
/*!40000 ALTER TABLE `books_instance_cited_in` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_instance_cited_in` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_instance_pub_place`
--

DROP TABLE IF EXISTS `books_instance_pub_place`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_instance_pub_place` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` int(11) NOT NULL,
  `place_id` int(11) NOT NULL,
  `sort_value` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_instance_pub_place_instance_id_place_id_0e02bb60_uniq` (`instance_id`,`place_id`),
  KEY `books_instance_pub_place_place_id_a08c9401_fk_places_place_id` (`place_id`),
  CONSTRAINT `books_instance_pub_p_instance_id_429a90a7_fk_books_ins` FOREIGN KEY (`instance_id`) REFERENCES `books_instance` (`id`),
  CONSTRAINT `books_instance_pub_place_place_id_a08c9401_fk_places_place_id` FOREIGN KEY (`place_id`) REFERENCES `places_place` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_instance_pub_place`
--

LOCK TABLES `books_instance_pub_place` WRITE;
/*!40000 ALTER TABLE `books_instance_pub_place` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_instance_pub_place` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_instancecatalogue`
--

DROP TABLE IF EXISTS `books_instancecatalogue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_instancecatalogue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `start_year` smallint(6) DEFAULT NULL,
  `end_year` smallint(6) DEFAULT NULL,
  `is_current` tinyint(1) NOT NULL,
  `call_number` varchar(255) DEFAULT NULL,
  `instance_id` int(11) NOT NULL,
  `institution_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_instancecatalo_instance_id_fd1a4076_fk_books_ins` (`instance_id`),
  KEY `books_instancecatalo_institution_id_2c619c8c_fk_books_own` (`institution_id`),
  CONSTRAINT `books_instancecatalo_instance_id_fd1a4076_fk_books_ins` FOREIGN KEY (`instance_id`) REFERENCES `books_instance` (`id`),
  CONSTRAINT `books_instancecatalo_institution_id_2c619c8c_fk_books_own` FOREIGN KEY (`institution_id`) REFERENCES `books_owninginstitution` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_instancecatalogue`
--

LOCK TABLES `books_instancecatalogue` WRITE;
/*!40000 ALTER TABLE `books_instancecatalogue` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_instancecatalogue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_instancecreator`
--

DROP TABLE IF EXISTS `books_instancecreator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_instancecreator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `creator_type_id` int(11) NOT NULL,
  `instance_id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_instancecreato_creator_type_id_11d8e320_fk_books_cre` (`creator_type_id`),
  KEY `books_instancecreator_instance_id_1e622c93_fk_books_instance_id` (`instance_id`),
  KEY `books_instancecreator_person_id_ce281917_fk_people_person_id` (`person_id`),
  CONSTRAINT `books_instancecreato_creator_type_id_11d8e320_fk_books_cre` FOREIGN KEY (`creator_type_id`) REFERENCES `books_creatortype` (`id`),
  CONSTRAINT `books_instancecreator_instance_id_1e622c93_fk_books_instance_id` FOREIGN KEY (`instance_id`) REFERENCES `books_instance` (`id`),
  CONSTRAINT `books_instancecreator_person_id_ce281917_fk_people_person_id` FOREIGN KEY (`person_id`) REFERENCES `people_person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_instancecreator`
--

LOCK TABLES `books_instancecreator` WRITE;
/*!40000 ALTER TABLE `books_instancecreator` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_instancecreator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_instancelanguage`
--

DROP TABLE IF EXISTS `books_instancelanguage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_instancelanguage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `instance_id` int(11) NOT NULL,
  `language_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_instancelanguage_instance_id_language_id_2ab05277_uniq` (`instance_id`,`language_id`),
  KEY `books_instancelanguage_language_id_efe94860_fk_books_language_id` (`language_id`),
  CONSTRAINT `books_instancelanguage_instance_id_2fb214dc_fk_books_instance_id` FOREIGN KEY (`instance_id`) REFERENCES `books_instance` (`id`),
  CONSTRAINT `books_instancelanguage_language_id_efe94860_fk_books_language_id` FOREIGN KEY (`language_id`) REFERENCES `books_language` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_instancelanguage`
--

LOCK TABLES `books_instancelanguage` WRITE;
/*!40000 ALTER TABLE `books_instancelanguage` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_instancelanguage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_journal`
--

DROP TABLE IF EXISTS `books_journal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_journal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_journal`
--

LOCK TABLES `books_journal` WRITE;
/*!40000 ALTER TABLE `books_journal` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_journal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_language`
--

DROP TABLE IF EXISTS `books_language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  `uri` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_language`
--

LOCK TABLES `books_language` WRITE;
/*!40000 ALTER TABLE `books_language` DISABLE KEYS */;
INSERT INTO `books_language` VALUES (1,'French','',''),(2,'German','',''),(3,'English','','');
/*!40000 ALTER TABLE `books_language` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_owninginstitution`
--

DROP TABLE IF EXISTS `books_owninginstitution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_owninginstitution` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  `short_name` varchar(255) NOT NULL,
  `contact_info` longtext NOT NULL,
  `place_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `books_owninginstitution_place_id_0b36e487_fk_places_place_id` (`place_id`),
  CONSTRAINT `books_owninginstitution_place_id_0b36e487_fk_places_place_id` FOREIGN KEY (`place_id`) REFERENCES `places_place` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_owninginstitution`
--

LOCK TABLES `books_owninginstitution` WRITE;
/*!40000 ALTER TABLE `books_owninginstitution` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_owninginstitution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_personbook`
--

DROP TABLE IF EXISTS `books_personbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_personbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `start_year` smallint(6) DEFAULT NULL,
  `end_year` smallint(6) DEFAULT NULL,
  `book_id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  `relationship_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_personbook_book_id_56dcda5e_fk_books_instance_id` (`book_id`),
  KEY `books_personbook_person_id_e1b12de0_fk_people_person_id` (`person_id`),
  KEY `books_personbook_relationship_type_id_3b2e151a_fk_books_per` (`relationship_type_id`),
  CONSTRAINT `books_personbook_book_id_56dcda5e_fk_books_instance_id` FOREIGN KEY (`book_id`) REFERENCES `books_instance` (`id`),
  CONSTRAINT `books_personbook_person_id_e1b12de0_fk_people_person_id` FOREIGN KEY (`person_id`) REFERENCES `people_person` (`id`),
  CONSTRAINT `books_personbook_relationship_type_id_3b2e151a_fk_books_per` FOREIGN KEY (`relationship_type_id`) REFERENCES `books_personbookrelationshiptype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_personbook`
--

LOCK TABLES `books_personbook` WRITE;
/*!40000 ALTER TABLE `books_personbook` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_personbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_personbookrelationshiptype`
--

DROP TABLE IF EXISTS `books_personbookrelationshiptype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_personbookrelationshiptype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  `uri` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_personbookrelationshiptype`
--

LOCK TABLES `books_personbookrelationshiptype` WRITE;
/*!40000 ALTER TABLE `books_personbookrelationshiptype` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_personbookrelationshiptype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_publisher`
--

DROP TABLE IF EXISTS `books_publisher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_publisher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_publisher`
--

LOCK TABLES `books_publisher` WRITE;
/*!40000 ALTER TABLE `books_publisher` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_publisher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_reference`
--

DROP TABLE IF EXISTS `books_reference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_reference` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `derridawork_page` varchar(10) NOT NULL,
  `derridawork_pageloc` varchar(2) NOT NULL,
  `book_page` varchar(255) NOT NULL,
  `anchor_text` longtext NOT NULL,
  `derridawork_id` int(11) NOT NULL,
  `instance_id` int(11) DEFAULT NULL,
  `reference_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_reference_derridawork_id_da11617d_fk_books_derridawork_id` (`derridawork_id`),
  KEY `books_reference_instance_id_f1aa0cb8_fk_books_instance_id` (`instance_id`),
  KEY `books_reference_reference_type_id_639c5015_fk_books_ref` (`reference_type_id`),
  CONSTRAINT `books_reference_derridawork_id_da11617d_fk_books_derridawork_id` FOREIGN KEY (`derridawork_id`) REFERENCES `books_derridawork` (`id`),
  CONSTRAINT `books_reference_instance_id_f1aa0cb8_fk_books_instance_id` FOREIGN KEY (`instance_id`) REFERENCES `books_instance` (`id`),
  CONSTRAINT `books_reference_reference_type_id_639c5015_fk_books_ref` FOREIGN KEY (`reference_type_id`) REFERENCES `books_referencetype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_reference`
--

LOCK TABLES `books_reference` WRITE;
/*!40000 ALTER TABLE `books_reference` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_reference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_referencetype`
--

DROP TABLE IF EXISTS `books_referencetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_referencetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_referencetype`
--

LOCK TABLES `books_referencetype` WRITE;
/*!40000 ALTER TABLE `books_referencetype` DISABLE KEYS */;
INSERT INTO `books_referencetype` VALUES (1,'Citation',''),(2,'Quotation',''),(3,'Epigraph',''),(4,'Footnote',''),(5,'Unset','');
/*!40000 ALTER TABLE `books_referencetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_subject`
--

DROP TABLE IF EXISTS `books_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_subject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  `uri` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_subject`
--

LOCK TABLES `books_subject` WRITE;
/*!40000 ALTER TABLE `books_subject` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_work`
--

DROP TABLE IF EXISTS `books_work`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_work` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `primary_title` longtext NOT NULL,
  `short_title` varchar(255) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `uri` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_work`
--

LOCK TABLES `books_work` WRITE;
/*!40000 ALTER TABLE `books_work` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_work` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_work_authors`
--

DROP TABLE IF EXISTS `books_work_authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_work_authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `work_id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_work_authors_work_id_person_id_95cac2d6_uniq` (`work_id`,`person_id`),
  KEY `books_work_authors_person_id_683a89ae_fk_people_person_id` (`person_id`),
  CONSTRAINT `books_work_authors_person_id_683a89ae_fk_people_person_id` FOREIGN KEY (`person_id`) REFERENCES `people_person` (`id`),
  CONSTRAINT `books_work_authors_work_id_be7409fe_fk_books_work_id` FOREIGN KEY (`work_id`) REFERENCES `books_work` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_work_authors`
--

LOCK TABLES `books_work_authors` WRITE;
/*!40000 ALTER TABLE `books_work_authors` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_work_authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_worklanguage`
--

DROP TABLE IF EXISTS `books_worklanguage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_worklanguage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `language_id` int(11) NOT NULL,
  `work_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_worklanguage_work_id_language_id_0de17110_uniq` (`work_id`,`language_id`),
  KEY `books_worklanguage_language_id_57098f39_fk_books_language_id` (`language_id`),
  CONSTRAINT `books_worklanguage_language_id_57098f39_fk_books_language_id` FOREIGN KEY (`language_id`) REFERENCES `books_language` (`id`),
  CONSTRAINT `books_worklanguage_work_id_e603df07_fk_books_work_id` FOREIGN KEY (`work_id`) REFERENCES `books_work` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_worklanguage`
--

LOCK TABLES `books_worklanguage` WRITE;
/*!40000 ALTER TABLE `books_worklanguage` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_worklanguage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_worksubject`
--

DROP TABLE IF EXISTS `books_worksubject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_worksubject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `work_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_worksubject_subject_id_work_id_6d18957d_uniq` (`subject_id`,`work_id`),
  KEY `books_worksubject_work_id_75203c14_fk_books_work_id` (`work_id`),
  CONSTRAINT `books_worksubject_subject_id_a3613253_fk_books_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `books_subject` (`id`),
  CONSTRAINT `books_worksubject_work_id_75203c14_fk_books_work_id` FOREIGN KEY (`work_id`) REFERENCES `books_work` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_worksubject`
--

LOCK TABLES `books_worksubject` WRITE;
/*!40000 ALTER TABLE `books_worksubject` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_worksubject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_cas_ng_proxygrantingticket`
--

DROP TABLE IF EXISTS `django_cas_ng_proxygrantingticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_cas_ng_proxygrantingticket` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_key` varchar(255) DEFAULT NULL,
  `pgtiou` varchar(255) DEFAULT NULL,
  `pgt` varchar(255) DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_cas_ng_proxygrant_session_key_user_id_4cd2ea19_uniq` (`session_key`,`user_id`),
  KEY `django_cas_ng_proxyg_user_id_f833edd2_fk_auth_user` (`user_id`),
  CONSTRAINT `django_cas_ng_proxyg_user_id_f833edd2_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_cas_ng_proxygrantingticket`
--

LOCK TABLES `django_cas_ng_proxygrantingticket` WRITE;
/*!40000 ALTER TABLE `django_cas_ng_proxygrantingticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_cas_ng_proxygrantingticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_cas_ng_sessionticket`
--

DROP TABLE IF EXISTS `django_cas_ng_sessionticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_cas_ng_sessionticket` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_key` varchar(255) NOT NULL,
  `ticket` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_cas_ng_sessionticket`
--

LOCK TABLES `django_cas_ng_sessionticket` WRITE;
/*!40000 ALTER TABLE `django_cas_ng_sessionticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_cas_ng_sessionticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(4,'auth','group'),(2,'auth','permission'),(3,'auth','user'),(12,'books','creatortype'),(13,'books','derridawork'),(16,'books','instance'),(10,'books','instancecatalogue'),(26,'books','instancecreator'),(18,'books','instancelanguage'),(17,'books','journal'),(19,'books','language'),(9,'books','owninginstitution'),(11,'books','personbook'),(15,'books','personbookrelationshiptype'),(20,'books','publisher'),(25,'books','reference'),(14,'books','referencetype'),(22,'books','subject'),(24,'books','work'),(23,'books','worklanguage'),(21,'books','worksubject'),(5,'contenttypes','contenttype'),(7,'django_cas_ng','proxygrantingticket'),(8,'django_cas_ng','sessionticket'),(33,'footnotes','bibliography'),(34,'footnotes','footnote'),(32,'footnotes','sourcetype'),(29,'people','person'),(28,'people','relationship'),(31,'people','relationshiptype'),(30,'people','residence'),(27,'places','place'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-07-03 18:41:22.866356'),(2,'auth','0001_initial','2017-07-03 18:41:23.075720'),(3,'admin','0001_initial','2017-07-03 18:41:23.124646'),(4,'admin','0002_logentry_remove_auto_add','2017-07-03 18:41:23.145978'),(5,'contenttypes','0002_remove_content_type_name','2017-07-03 18:41:23.194179'),(6,'auth','0002_alter_permission_name_max_length','2017-07-03 18:41:23.215670'),(7,'auth','0003_alter_user_email_max_length','2017-07-03 18:41:23.240547'),(8,'auth','0004_alter_user_username_opts','2017-07-03 18:41:23.251602'),(9,'auth','0005_alter_user_last_login_null','2017-07-03 18:41:23.278154'),(10,'auth','0006_require_contenttypes_0002','2017-07-03 18:41:23.279683'),(11,'auth','0007_alter_validators_add_error_messages','2017-07-03 18:41:23.290267'),(12,'auth','0008_alter_user_username_max_length','2017-07-03 18:41:23.315596'),(13,'places','0001_initial','2017-07-03 18:41:23.331258'),(14,'people','0001_initial','2017-07-03 18:41:23.492161'),(15,'people','0002_allow_neg_years_bc','2017-07-03 18:41:23.638861'),(16,'books','0001_initial','2017-07-03 18:41:25.079878'),(17,'books','0002_add_citationality_models','2017-07-03 18:41:25.081578'),(18,'books','0003_citationality_postmeeting_revisions','2017-07-03 18:41:25.083396'),(19,'books','0004_make_uri_optional_creator_type','2017-07-03 18:41:25.085058'),(20,'books','0005_optional_uri_fields_language_subject','2017-07-03 18:41:25.086834'),(21,'books','0006_initial_languages','2017-07-03 18:41:25.088442'),(22,'books','0007_fix_pluralizatition_citationality','2017-07-03 18:41:25.089979'),(23,'books','0008_add_str_referencetype_derridawork','2017-07-03 18:41:25.091476'),(24,'books','0009_ref_type_use_common','2017-07-03 18:41:25.092989'),(25,'books','0010_initial_reftypes','2017-07-03 18:41:25.094461'),(26,'books','0011_add_foreign_key_ref_reftype','2017-07-03 18:41:25.095888'),(27,'books','0012_template_derrida_work','2017-07-03 18:41:25.097276'),(28,'books','0013_add_journal_type_item_type_dates','2017-07-03 18:41:25.098910'),(29,'books','0014_add_flags_pub_date','2017-07-03 18:41:25.100583'),(30,'books','0015_add_uri_book','2017-07-03 18:41:25.102207'),(31,'books','0016_allow_neg_years_bc','2017-07-03 18:41:25.103754'),(32,'books','0017_additional_derrida_flags','2017-07-03 18:41:25.105395'),(33,'books','0018_add_page_range','2017-07-03 18:41:25.107000'),(34,'books','0019_rename_journal_id_journal','2017-07-03 18:41:25.108579'),(35,'books','0020_add_initial_item_types','2017-07-03 18:41:25.110216'),(36,'books','0021_add_initial_item_types','2017-07-03 18:41:25.111997'),(37,'books','0022_help_text_pub_date','2017-07-03 18:41:25.113525'),(38,'books','0023_raise_char_limit_book_page','2017-07-03 18:41:25.115049'),(39,'books','0024_expand_larger_title_space_improve_admin_clarity','2017-07-03 18:41:25.116691'),(40,'books','0025_help_text_catatalogue','2017-07-03 18:41:25.118650'),(41,'books','0026_book_many_to_many_self','2017-07-03 18:41:25.120463'),(42,'books','0027_remove_symmetrical_flag_associated_books','2017-07-03 18:41:25.123064'),(43,'books','0028_add_derrida_workbook','2017-07-03 18:41:25.124806'),(44,'books','0029_add_anchor_text_reference','2017-07-03 18:41:25.126377'),(45,'books','0030_split_book_into_work_instance','2017-07-03 18:41:25.127936'),(46,'books','0031_migrate_books_to_works_instances','2017-07-03 18:41:25.129557'),(47,'books','0032_cited_in_optional_subject_default_not_primary','2017-07-03 18:41:25.131166'),(48,'books','0033_remove_book_models','2017-07-03 18:41:25.133029'),(49,'common','0001_data_editor_group_init','2017-07-03 18:41:25.184324'),(50,'django_cas_ng','0001_initial','2017-07-03 18:41:25.259909'),(51,'footnotes','0001_initial','2017-07-03 18:41:25.376133'),(52,'sessions','0001_initial','2017-07-03 18:41:25.398561'),(53,'books','0001_squashed_0033_remove_book_models','2017-07-03 18:41:25.402560');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `footnotes_bibliography`
--

DROP TABLE IF EXISTS `footnotes_bibliography`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `footnotes_bibliography` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `bibliographic_note` longtext NOT NULL,
  `source_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `footnotes_bibliograp_source_type_id_9f345508_fk_footnotes` (`source_type_id`),
  CONSTRAINT `footnotes_bibliograp_source_type_id_9f345508_fk_footnotes` FOREIGN KEY (`source_type_id`) REFERENCES `footnotes_sourcetype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `footnotes_bibliography`
--

LOCK TABLES `footnotes_bibliography` WRITE;
/*!40000 ALTER TABLE `footnotes_bibliography` DISABLE KEYS */;
/*!40000 ALTER TABLE `footnotes_bibliography` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `footnotes_footnote`
--

DROP TABLE IF EXISTS `footnotes_footnote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `footnotes_footnote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `location` longtext NOT NULL,
  `snippet_text` longtext NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  `is_agree` tinyint(1) NOT NULL,
  `bibliography_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `footnotes_footnote_bibliography_id_d331761a_fk_footnotes` (`bibliography_id`),
  KEY `footnotes_footnote_content_type_id_2044e4b6_fk_django_co` (`content_type_id`),
  CONSTRAINT `footnotes_footnote_bibliography_id_d331761a_fk_footnotes` FOREIGN KEY (`bibliography_id`) REFERENCES `footnotes_bibliography` (`id`),
  CONSTRAINT `footnotes_footnote_content_type_id_2044e4b6_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `footnotes_footnote`
--

LOCK TABLES `footnotes_footnote` WRITE;
/*!40000 ALTER TABLE `footnotes_footnote` DISABLE KEYS */;
/*!40000 ALTER TABLE `footnotes_footnote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `footnotes_sourcetype`
--

DROP TABLE IF EXISTS `footnotes_sourcetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `footnotes_sourcetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `footnotes_sourcetype`
--

LOCK TABLES `footnotes_sourcetype` WRITE;
/*!40000 ALTER TABLE `footnotes_sourcetype` DISABLE KEYS */;
/*!40000 ALTER TABLE `footnotes_sourcetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_person`
--

DROP TABLE IF EXISTS `people_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `start_year` smallint(6) DEFAULT NULL,
  `end_year` smallint(6) DEFAULT NULL,
  `authorized_name` varchar(255) NOT NULL,
  `viaf_id` varchar(200) DEFAULT NULL,
  `sort_name` varchar(255) NOT NULL,
  `family_group` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_person`
--

LOCK TABLES `people_person` WRITE;
/*!40000 ALTER TABLE `people_person` DISABLE KEYS */;
/*!40000 ALTER TABLE `people_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_relationship`
--

DROP TABLE IF EXISTS `people_relationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_relationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `start_year` smallint(6) DEFAULT NULL,
  `end_year` smallint(6) DEFAULT NULL,
  `from_person_id` int(11) NOT NULL,
  `relationship_type_id` int(11) NOT NULL,
  `to_person_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `people_relationship_from_person_id_5f14b94e_fk_people_person_id` (`from_person_id`),
  KEY `people_relationship_relationship_type_id_67bbe297_fk_people_re` (`relationship_type_id`),
  KEY `people_relationship_to_person_id_c459ac2d_fk_people_person_id` (`to_person_id`),
  CONSTRAINT `people_relationship_from_person_id_5f14b94e_fk_people_person_id` FOREIGN KEY (`from_person_id`) REFERENCES `people_person` (`id`),
  CONSTRAINT `people_relationship_relationship_type_id_67bbe297_fk_people_re` FOREIGN KEY (`relationship_type_id`) REFERENCES `people_relationshiptype` (`id`),
  CONSTRAINT `people_relationship_to_person_id_c459ac2d_fk_people_person_id` FOREIGN KEY (`to_person_id`) REFERENCES `people_person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_relationship`
--

LOCK TABLES `people_relationship` WRITE;
/*!40000 ALTER TABLE `people_relationship` DISABLE KEYS */;
/*!40000 ALTER TABLE `people_relationship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_relationshiptype`
--

DROP TABLE IF EXISTS `people_relationshiptype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_relationshiptype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  `is_symmetric` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_relationshiptype`
--

LOCK TABLES `people_relationshiptype` WRITE;
/*!40000 ALTER TABLE `people_relationshiptype` DISABLE KEYS */;
/*!40000 ALTER TABLE `people_relationshiptype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_residence`
--

DROP TABLE IF EXISTS `people_residence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_residence` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `start_year` smallint(6) DEFAULT NULL,
  `end_year` smallint(6) DEFAULT NULL,
  `person_id` int(11) NOT NULL,
  `place_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `people_residence_person_id_8f8d598c_fk_people_person_id` (`person_id`),
  KEY `people_residence_place_id_c5caf1b7_fk_places_place_id` (`place_id`),
  CONSTRAINT `people_residence_person_id_8f8d598c_fk_people_person_id` FOREIGN KEY (`person_id`) REFERENCES `people_person` (`id`),
  CONSTRAINT `people_residence_place_id_c5caf1b7_fk_places_place_id` FOREIGN KEY (`place_id`) REFERENCES `places_place` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_residence`
--

LOCK TABLES `people_residence` WRITE;
/*!40000 ALTER TABLE `people_residence` DISABLE KEYS */;
/*!40000 ALTER TABLE `people_residence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `places_place`
--

DROP TABLE IF EXISTS `places_place`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `places_place` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  `geonames_id` varchar(200) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `places_place`
--

LOCK TABLES `places_place` WRITE;
/*!40000 ALTER TABLE `places_place` DISABLE KEYS */;
/*!40000 ALTER TABLE `places_place` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-03 14:41:32

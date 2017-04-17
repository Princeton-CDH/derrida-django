-- MySQL dump 10.13  Distrib 5.7.13, for osx10.11 (x86_64)
--
-- Host: localhost    Database: testderrida
-- ------------------------------------------------------
-- Server version	5.7.13

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
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
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
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add session ticket',7,'add_sessionticket'),(20,'Can change session ticket',7,'change_sessionticket'),(21,'Can delete session ticket',7,'delete_sessionticket'),(22,'Can add proxy granting ticket',8,'add_proxygrantingticket'),(23,'Can change proxy granting ticket',8,'change_proxygrantingticket'),(24,'Can delete proxy granting ticket',8,'delete_proxygrantingticket'),(25,'Can add Associated Book',9,'add_associatedbook'),(26,'Can change Associated Book',9,'change_associatedbook'),(27,'Can delete Associated Book',9,'delete_associatedbook'),(28,'Can add derrida work',10,'add_derridawork'),(29,'Can change derrida work',10,'change_derridawork'),(30,'Can delete derrida work',10,'delete_derridawork'),(31,'Can add item type',11,'add_itemtype'),(32,'Can change item type',11,'change_itemtype'),(33,'Can delete item type',11,'delete_itemtype'),(34,'Can add language',12,'add_language'),(35,'Can change language',12,'change_language'),(36,'Can delete language',12,'delete_language'),(37,'Can add catalogue',13,'add_catalogue'),(38,'Can change catalogue',13,'change_catalogue'),(39,'Can delete catalogue',13,'delete_catalogue'),(40,'Can add journal',14,'add_journal'),(41,'Can change journal',14,'change_journal'),(42,'Can delete journal',14,'delete_journal'),(43,'Can add Person/Book Interaction',15,'add_personbook'),(44,'Can change Person/Book Interaction',15,'change_personbook'),(45,'Can delete Person/Book Interaction',15,'delete_personbook'),(46,'Can add reference',16,'add_reference'),(47,'Can change reference',16,'change_reference'),(48,'Can delete reference',16,'delete_reference'),(49,'Can add subject',17,'add_subject'),(50,'Can change subject',17,'change_subject'),(51,'Can delete subject',17,'delete_subject'),(52,'Can add owning institution',18,'add_owninginstitution'),(53,'Can change owning institution',18,'change_owninginstitution'),(54,'Can delete owning institution',18,'delete_owninginstitution'),(55,'Can add reference type',19,'add_referencetype'),(56,'Can change reference type',19,'change_referencetype'),(57,'Can delete reference type',19,'delete_referencetype'),(58,'Can add book language',20,'add_booklanguage'),(59,'Can change book language',20,'change_booklanguage'),(60,'Can delete book language',20,'delete_booklanguage'),(61,'Can add Derrida library work',21,'add_book'),(62,'Can change Derrida library work',21,'change_book'),(63,'Can delete Derrida library work',21,'delete_book'),(64,'Can add creator',22,'add_creator'),(65,'Can change creator',22,'change_creator'),(66,'Can delete creator',22,'delete_creator'),(67,'Can add publisher',23,'add_publisher'),(68,'Can change publisher',23,'change_publisher'),(69,'Can delete publisher',23,'delete_publisher'),(70,'Can add person book relationship type',24,'add_personbookrelationshiptype'),(71,'Can change person book relationship type',24,'change_personbookrelationshiptype'),(72,'Can delete person book relationship type',24,'delete_personbookrelationshiptype'),(73,'Can add creator type',25,'add_creatortype'),(74,'Can change creator type',25,'change_creatortype'),(75,'Can delete creator type',25,'delete_creatortype'),(76,'Can add book subject',26,'add_booksubject'),(77,'Can change book subject',26,'change_booksubject'),(78,'Can delete book subject',26,'delete_booksubject'),(79,'Can add place',27,'add_place'),(80,'Can change place',27,'change_place'),(81,'Can delete place',27,'delete_place'),(82,'Can add relationship',28,'add_relationship'),(83,'Can change relationship',28,'change_relationship'),(84,'Can delete relationship',28,'delete_relationship'),(85,'Can add relationship type',29,'add_relationshiptype'),(86,'Can change relationship type',29,'change_relationshiptype'),(87,'Can delete relationship type',29,'delete_relationshiptype'),(88,'Can add residence',30,'add_residence'),(89,'Can change residence',30,'change_residence'),(90,'Can delete residence',30,'delete_residence'),(91,'Can add person',31,'add_person'),(92,'Can change person',31,'change_person'),(93,'Can delete person',31,'delete_person'),(94,'Can add source type',32,'add_sourcetype'),(95,'Can change source type',32,'change_sourcetype'),(96,'Can delete source type',32,'delete_sourcetype'),(97,'Can add bibliography',33,'add_bibliography'),(98,'Can change bibliography',33,'change_bibliography'),(99,'Can delete bibliography',33,'delete_bibliography'),(100,'Can add footnote',34,'add_footnote'),(101,'Can change footnote',34,'change_footnote'),(102,'Can delete footnote',34,'delete_footnote'),(103,'Can add Edition - Derrida work relation',35,'add_derridaworkbook'),(104,'Can change Edition - Derrida work relation',35,'change_derridaworkbook'),(105,'Can delete Edition - Derrida work relation',35,'delete_derridaworkbook');
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
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
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
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
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
-- Table structure for table `books_associatedbook`
--

DROP TABLE IF EXISTS `books_associatedbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_associatedbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_book_id` int(11) NOT NULL,
  `to_book_id` int(11) NOT NULL,
  `is_collection` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_associatedbook_from_book_id_831ebcb8_fk_books_book_id` (`from_book_id`),
  KEY `books_associatedbook_to_book_id_821aa5a7_fk_books_book_id` (`to_book_id`),
  CONSTRAINT `books_associatedbook_from_book_id_831ebcb8_fk_books_book_id` FOREIGN KEY (`from_book_id`) REFERENCES `books_book` (`id`),
  CONSTRAINT `books_associatedbook_to_book_id_821aa5a7_fk_books_book_id` FOREIGN KEY (`to_book_id`) REFERENCES `books_book` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_associatedbook`
--

LOCK TABLES `books_associatedbook` WRITE;
/*!40000 ALTER TABLE `books_associatedbook` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_associatedbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_book`
--

DROP TABLE IF EXISTS `books_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `primary_title` longtext NOT NULL,
  `short_title` varchar(255) NOT NULL,
  `zotero_id` varchar(255) NOT NULL,
  `original_pub_info` longtext,
  `is_extant` tinyint(1) NOT NULL,
  `is_annotated` tinyint(1) NOT NULL,
  `is_digitized` tinyint(1) NOT NULL,
  `dimensions` varchar(255) NOT NULL,
  `pub_place_id` int(11),
  `publisher_id` int(11),
  `copyright_year` int(10) unsigned,
  `larger_work_title` longtext,
  `pub_date` date,
  `work_year` int(11),
  `item_type_id` int(11) NOT NULL,
  `journal_id` int(11) DEFAULT NULL,
  `pub_day_missing` tinyint(1) NOT NULL,
  `pub_month_missing` tinyint(1) NOT NULL,
  `uri` varchar(200),
  `has_dedication` tinyint(1) NOT NULL,
  `has_insertions` tinyint(1) NOT NULL,
  `is_translation` tinyint(1) NOT NULL,
  `page_range` varchar(20),
  PRIMARY KEY (`id`),
  KEY `books_book_pub_place_id_43f2b06f_fk_places_place_id` (`pub_place_id`),
  KEY `books_book_publisher_id_189e6c56_fk_books_publisher_id` (`publisher_id`),
  KEY `books_book_item_type_id_17551829_fk_books_itemtype_id` (`item_type_id`),
  KEY `books_book_journal_id_cc75fc8e_fk_books_journal_id` (`journal_id`),
  CONSTRAINT `books_book_item_type_id_17551829_fk_books_itemtype_id` FOREIGN KEY (`item_type_id`) REFERENCES `books_itemtype` (`id`),
  CONSTRAINT `books_book_journal_id_cc75fc8e_fk_books_journal_id` FOREIGN KEY (`journal_id`) REFERENCES `books_journal` (`id`),
  CONSTRAINT `books_book_pub_place_id_43f2b06f_fk_places_place_id` FOREIGN KEY (`pub_place_id`) REFERENCES `places_place` (`id`),
  CONSTRAINT `books_book_publisher_id_189e6c56_fk_books_publisher_id` FOREIGN KEY (`publisher_id`) REFERENCES `books_publisher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_book`
--

LOCK TABLES `books_book` WRITE;
/*!40000 ALTER TABLE `books_book` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_booklanguage`
--

DROP TABLE IF EXISTS `books_booklanguage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_booklanguage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `book_id` int(11) NOT NULL,
  `language_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_booklanguage_book_id_b9d73941_uniq` (`book_id`,`language_id`),
  KEY `books_booklanguage_language_id_38b30a68_fk_books_language_id` (`language_id`),
  CONSTRAINT `books_booklanguage_book_id_7d306792_fk_books_book_id` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`),
  CONSTRAINT `books_booklanguage_language_id_38b30a68_fk_books_language_id` FOREIGN KEY (`language_id`) REFERENCES `books_language` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_booklanguage`
--

LOCK TABLES `books_booklanguage` WRITE;
/*!40000 ALTER TABLE `books_booklanguage` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_booklanguage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_booksubject`
--

DROP TABLE IF EXISTS `books_booksubject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_booksubject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `book_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_booksubject_subject_id_37fc26f2_uniq` (`subject_id`,`book_id`),
  KEY `books_booksubject_book_id_f294fe86_fk_books_book_id` (`book_id`),
  CONSTRAINT `books_booksubject_book_id_f294fe86_fk_books_book_id` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`),
  CONSTRAINT `books_booksubject_subject_id_f2170134_fk_books_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `books_subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_booksubject`
--

LOCK TABLES `books_booksubject` WRITE;
/*!40000 ALTER TABLE `books_booksubject` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_booksubject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_catalogue`
--

DROP TABLE IF EXISTS `books_catalogue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_catalogue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `start_year` smallint(6) DEFAULT NULL,
  `end_year` smallint(6) DEFAULT NULL,
  `is_current` tinyint(1) NOT NULL,
  `call_number` varchar(255) DEFAULT NULL,
  `book_id` int(11) NOT NULL,
  `institution_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_catalogue_book_id_49cd11fc_fk_books_book_id` (`book_id`),
  KEY `books_cata_institution_id_cad715a2_fk_books_owninginstitution_id` (`institution_id`),
  CONSTRAINT `books_cata_institution_id_cad715a2_fk_books_owninginstitution_id` FOREIGN KEY (`institution_id`) REFERENCES `books_owninginstitution` (`id`),
  CONSTRAINT `books_catalogue_book_id_49cd11fc_fk_books_book_id` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_catalogue`
--

LOCK TABLES `books_catalogue` WRITE;
/*!40000 ALTER TABLE `books_catalogue` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_catalogue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_creator`
--

DROP TABLE IF EXISTS `books_creator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_creator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `book_id` int(11) NOT NULL,
  `creator_type_id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_creator_book_id_99e473d8_fk_books_book_id` (`book_id`),
  KEY `books_creator_creator_type_id_6a9eb7db_fk_books_creatortype_id` (`creator_type_id`),
  KEY `books_creator_person_id_16dbca83_fk_people_person_id` (`person_id`),
  CONSTRAINT `books_creator_book_id_99e473d8_fk_books_book_id` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`),
  CONSTRAINT `books_creator_creator_type_id_6a9eb7db_fk_books_creatortype_id` FOREIGN KEY (`creator_type_id`) REFERENCES `books_creatortype` (`id`),
  CONSTRAINT `books_creator_person_id_16dbca83_fk_people_person_id` FOREIGN KEY (`person_id`) REFERENCES `people_person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_creator`
--

LOCK TABLES `books_creator` WRITE;
/*!40000 ALTER TABLE `books_creator` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_creator` ENABLE KEYS */;
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
-- Table structure for table `books_derridaworkbook`
--

DROP TABLE IF EXISTS `books_derridaworkbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_derridaworkbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `book_id` int(11) NOT NULL,
  `derridawork_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_derridaworkbook_book_id_89e83591_fk_books_book_id` (`book_id`),
  KEY `books_derridawor_derridawork_id_0d6e2f9a_fk_books_derridawork_id` (`derridawork_id`),
  CONSTRAINT `books_derridawor_derridawork_id_0d6e2f9a_fk_books_derridawork_id` FOREIGN KEY (`derridawork_id`) REFERENCES `books_derridawork` (`id`),
  CONSTRAINT `books_derridaworkbook_book_id_89e83591_fk_books_book_id` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_derridaworkbook`
--

LOCK TABLES `books_derridaworkbook` WRITE;
/*!40000 ALTER TABLE `books_derridaworkbook` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_derridaworkbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_itemtype`
--

DROP TABLE IF EXISTS `books_itemtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_itemtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_itemtype`
--

LOCK TABLES `books_itemtype` WRITE;
/*!40000 ALTER TABLE `books_itemtype` DISABLE KEYS */;
INSERT INTO `books_itemtype` VALUES (1,'Book',''),(2,'Book Section',''),(3,'Journal Article','');
/*!40000 ALTER TABLE `books_itemtype` ENABLE KEYS */;
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
  KEY `books_personbook_book_id_56dcda5e_fk_books_book_id` (`book_id`),
  KEY `books_personbook_person_id_e1b12de0_fk_people_person_id` (`person_id`),
  KEY `D6ee85a90b18e96c7219aeb01a5b9d1e` (`relationship_type_id`),
  CONSTRAINT `D6ee85a90b18e96c7219aeb01a5b9d1e` FOREIGN KEY (`relationship_type_id`) REFERENCES `books_personbookrelationshiptype` (`id`),
  CONSTRAINT `books_personbook_book_id_56dcda5e_fk_books_book_id` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`),
  CONSTRAINT `books_personbook_person_id_e1b12de0_fk_people_person_id` FOREIGN KEY (`person_id`) REFERENCES `people_person` (`id`)
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
  `book_id` int(11) NOT NULL,
  `derridawork_id` int(11) NOT NULL,
  `book_page` varchar(255) DEFAULT NULL,
  `reference_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_references_book_id_7515783b_fk_books_book_id` (`book_id`),
  KEY `books_references_derridawork_id_10c31e1c_fk_books_derridawork_id` (`derridawork_id`),
  KEY `books_refer_reference_type_id_639c5015_fk_books_referencetype_id` (`reference_type_id`),
  CONSTRAINT `books_refer_reference_type_id_639c5015_fk_books_referencetype_id` FOREIGN KEY (`reference_type_id`) REFERENCES `books_referencetype` (`id`),
  CONSTRAINT `books_references_book_id_7515783b_fk_books_book_id` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`),
  CONSTRAINT `books_references_derridawork_id_10c31e1c_fk_books_derridawork_id` FOREIGN KEY (`derridawork_id`) REFERENCES `books_derridawork` (`id`)
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
  `notes` longtext NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_referencetype`
--

LOCK TABLES `books_referencetype` WRITE;
/*!40000 ALTER TABLE `books_referencetype` DISABLE KEYS */;
INSERT INTO `books_referencetype` VALUES (1,'','Citation'),(2,'','Quotation'),(3,'','Epigraph'),(4,'','Footnote'),(5,'','Unset');
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
  `uri` varchar(200),
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
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
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
  UNIQUE KEY `django_cas_ng_proxygrantingticket_session_key_4cd2ea19_uniq` (`session_key`,`user_id`),
  KEY `django_cas_ng_proxygrantingtick_user_id_f833edd2_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_cas_ng_proxygrantingtick_user_id_f833edd2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
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
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(9,'books','associatedbook'),(21,'books','book'),(20,'books','booklanguage'),(26,'books','booksubject'),(13,'books','catalogue'),(22,'books','creator'),(25,'books','creatortype'),(10,'books','derridawork'),(35,'books','derridaworkbook'),(11,'books','itemtype'),(14,'books','journal'),(12,'books','language'),(18,'books','owninginstitution'),(15,'books','personbook'),(24,'books','personbookrelationshiptype'),(23,'books','publisher'),(16,'books','reference'),(19,'books','referencetype'),(17,'books','subject'),(5,'contenttypes','contenttype'),(8,'django_cas_ng','proxygrantingticket'),(7,'django_cas_ng','sessionticket'),(33,'footnotes','bibliography'),(34,'footnotes','footnote'),(32,'footnotes','sourcetype'),(31,'people','person'),(28,'people','relationship'),(29,'people','relationshiptype'),(30,'people','residence'),(27,'places','place'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-04-17 17:57:52.138438'),(2,'auth','0001_initial','2017-04-17 17:57:52.460123'),(3,'admin','0001_initial','2017-04-17 17:57:52.534730'),(4,'admin','0002_logentry_remove_auto_add','2017-04-17 17:57:52.574235'),(5,'contenttypes','0002_remove_content_type_name','2017-04-17 17:57:52.647163'),(6,'auth','0002_alter_permission_name_max_length','2017-04-17 17:57:52.676148'),(7,'auth','0003_alter_user_email_max_length','2017-04-17 17:57:52.709768'),(8,'auth','0004_alter_user_username_opts','2017-04-17 17:57:52.720215'),(9,'auth','0005_alter_user_last_login_null','2017-04-17 17:57:52.745348'),(10,'auth','0006_require_contenttypes_0002','2017-04-17 17:57:52.748628'),(11,'auth','0007_alter_validators_add_error_messages','2017-04-17 17:57:52.763654'),(12,'auth','0008_alter_user_username_max_length','2017-04-17 17:57:52.797408'),(13,'places','0001_initial','2017-04-17 17:57:52.816738'),(14,'people','0001_initial','2017-04-17 17:57:53.083746'),(15,'books','0001_initial','2017-04-17 17:57:54.163332'),(16,'books','0002_add_citationality_models','2017-04-17 17:57:54.284608'),(17,'books','0003_citationality_postmeeting_revisions','2017-04-17 17:57:54.342749'),(18,'books','0004_make_uri_optional_creator_type','2017-04-17 17:57:54.430073'),(19,'books','0005_optional_uri_fields_language_subject','2017-04-17 17:57:54.527601'),(20,'books','0006_initial_languages','2017-04-17 17:57:54.550098'),(21,'books','0007_fix_pluralizatition_citationality','2017-04-17 17:57:54.602089'),(22,'books','0008_add_str_referencetype_derridawork','2017-04-17 17:57:54.642880'),(23,'books','0009_ref_type_use_common','2017-04-17 17:57:54.669967'),(24,'books','0010_initial_reftypes','2017-04-17 17:57:54.682400'),(25,'books','0011_add_foreign_key_ref_reftype','2017-04-17 17:57:54.798747'),(26,'books','0012_template_derrida_work','2017-04-17 17:57:54.807876'),(27,'books','0013_add_journal_type_item_type_dates','2017-04-17 17:57:55.299842'),(28,'books','0014_add_flags_pub_date','2017-04-17 17:57:55.413115'),(29,'books','0015_add_uri_book','2017-04-17 17:57:55.470786'),(30,'books','0016_allow_neg_years_bc','2017-04-17 17:57:55.694857'),(31,'books','0017_additional_derrida_flags','2017-04-17 17:57:55.915108'),(32,'books','0018_add_page_range','2017-04-17 17:57:55.973569'),(33,'books','0019_rename_journal_id_journal','2017-04-17 17:57:56.052440'),(34,'books','0020_add_initial_item_types','2017-04-17 17:57:56.063463'),(35,'books','0021_add_initial_item_types','2017-04-17 17:57:56.065588'),(36,'books','0022_help_text_pub_date','2017-04-17 17:57:56.088396'),(37,'books','0023_raise_char_limit_book_page','2017-04-17 17:57:56.146451'),(38,'books','0024_expand_larger_title_space_improve_admin_clarity','2017-04-17 17:57:56.252078'),(39,'books','0025_help_text_catatalogue','2017-04-17 17:57:56.293426'),(40,'books','0026_book_many_to_many_self','2017-04-17 17:57:56.418983'),(41,'books','0027_remove_symmetrical_flag_associated_books','2017-04-17 17:57:56.462175'),(42,'common','0001_data_editor_group_init','2017-04-17 17:57:56.486804'),(43,'django_cas_ng','0001_initial','2017-04-17 17:57:56.582510'),(44,'footnotes','0001_initial','2017-04-17 17:57:56.763656'),(45,'people','0002_allow_neg_years_bc','2017-04-17 17:57:57.027950'),(46,'sessions','0001_initial','2017-04-17 17:57:57.064638'),(47,'books','0028_add_derrida_workbook','2017-04-17 17:58:37.587117');
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
  KEY `django_session_de54fa62` (`expire_date`)
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
  KEY `footnotes_bib_source_type_id_9f345508_fk_footnotes_sourcetype_id` (`source_type_id`),
  CONSTRAINT `footnotes_bib_source_type_id_9f345508_fk_footnotes_sourcetype_id` FOREIGN KEY (`source_type_id`) REFERENCES `footnotes_sourcetype` (`id`)
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
  KEY `footnotes__bibliography_id_d331761a_fk_footnotes_bibliography_id` (`bibliography_id`),
  KEY `footnotes_foo_content_type_id_2044e4b6_fk_django_content_type_id` (`content_type_id`),
  CONSTRAINT `footnotes__bibliography_id_d331761a_fk_footnotes_bibliography_id` FOREIGN KEY (`bibliography_id`) REFERENCES `footnotes_bibliography` (`id`),
  CONSTRAINT `footnotes_foo_content_type_id_2044e4b6_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
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
  KEY `peop_relationship_type_id_67bbe297_fk_people_relationshiptype_id` (`relationship_type_id`),
  KEY `people_relationship_to_person_id_c459ac2d_fk_people_person_id` (`to_person_id`),
  CONSTRAINT `peop_relationship_type_id_67bbe297_fk_people_relationshiptype_id` FOREIGN KEY (`relationship_type_id`) REFERENCES `people_relationshiptype` (`id`),
  CONSTRAINT `people_relationship_from_person_id_5f14b94e_fk_people_person_id` FOREIGN KEY (`from_person_id`) REFERENCES `people_person` (`id`),
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

-- Dump completed on 2017-04-17 13:59:57

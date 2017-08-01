-- MySQL dump 10.13  Distrib 5.7.17, for osx10.12 (x86_64)
--
-- Host: localhost    Database: testderrida
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
-- Table structure for table `annotator_store_annotation`
--

DROP TABLE IF EXISTS `annotator_store_annotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `annotator_store_annotation` (
  `id` char(32) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `text` longtext NOT NULL,
  `quote` longtext NOT NULL,
  `uri` varchar(200) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `annotator_store_annotation_user_id_0eb79fc4_fk_auth_user_id` (`user_id`),
  CONSTRAINT `annotator_store_annotation_user_id_0eb79fc4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `annotator_store_annotation`
--

LOCK TABLES `annotator_store_annotation` WRITE;
/*!40000 ALTER TABLE `annotator_store_annotation` DISABLE KEYS */;
/*!40000 ALTER TABLE `annotator_store_annotation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `annotator_store_annotationgroup`
--

DROP TABLE IF EXISTS `annotator_store_annotationgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `annotator_store_annotationgroup` (
  `group_ptr_id` int(11) NOT NULL,
  `notes` longtext NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`group_ptr_id`),
  CONSTRAINT `annotator_store_anno_group_ptr_id_b4c67cb8_fk_auth_grou` FOREIGN KEY (`group_ptr_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `annotator_store_annotationgroup`
--

LOCK TABLES `annotator_store_annotationgroup` WRITE;
/*!40000 ALTER TABLE `annotator_store_annotationgroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `annotator_store_annotationgroup` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (88,1,4),(89,1,5),(90,1,6),(91,1,7),(1,1,21),(2,1,22),(3,1,23),(4,1,24),(5,1,25),(6,1,26),(7,1,27),(8,1,28),(9,1,29),(10,1,30),(11,1,31),(12,1,32),(13,1,33),(14,1,34),(15,1,35),(16,1,36),(17,1,37),(18,1,38),(19,1,39),(20,1,40),(21,1,41),(22,1,42),(23,1,43),(24,1,44),(25,1,45),(26,1,46),(27,1,47),(28,1,48),(29,1,49),(30,1,50),(31,1,51),(32,1,52),(33,1,53),(34,1,54),(35,1,55),(36,1,56),(37,1,57),(38,1,58),(39,1,59),(40,1,60),(41,1,61),(42,1,62),(43,1,63),(44,1,64),(45,1,65),(46,1,66),(47,1,67),(48,1,68),(49,1,69),(50,1,70),(51,1,71),(52,1,72),(53,1,73),(54,1,74),(55,1,75),(56,1,76),(57,1,77),(82,1,81),(83,1,85),(73,1,86),(74,1,87),(75,1,88),(79,1,89),(80,1,90),(81,1,91),(76,1,92),(77,1,93),(78,1,94),(84,1,98),(85,1,99),(86,1,100),(87,1,101),(58,1,102),(59,1,103),(60,1,104),(61,1,105),(62,1,106),(63,1,107),(64,1,108),(65,1,109),(66,1,110),(67,1,111),(68,1,112),(69,1,113),(70,1,114),(71,1,115),(72,1,116);
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
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add annotation',2,'add_annotation'),(5,'Can change annotation',2,'change_annotation'),(6,'Can delete annotation',2,'delete_annotation'),(7,'View annotation',2,'view_annotation'),(8,'Manage annotation',2,'admin_annotation'),(9,'Can add annotation group',3,'add_annotationgroup'),(10,'Can change annotation group',3,'change_annotationgroup'),(11,'Can delete annotation group',3,'delete_annotationgroup'),(12,'Can add permission',4,'add_permission'),(13,'Can change permission',4,'change_permission'),(14,'Can delete permission',4,'delete_permission'),(15,'Can add user',5,'add_user'),(16,'Can change user',5,'change_user'),(17,'Can delete user',5,'delete_user'),(18,'Can add group',6,'add_group'),(19,'Can change group',6,'change_group'),(20,'Can delete group',6,'delete_group'),(21,'Can add creator type',7,'add_creatortype'),(22,'Can change creator type',7,'change_creatortype'),(23,'Can delete creator type',7,'delete_creatortype'),(24,'Can add instance creator',8,'add_instancecreator'),(25,'Can change instance creator',8,'change_instancecreator'),(26,'Can delete instance creator',8,'delete_instancecreator'),(27,'Can add reference type',9,'add_referencetype'),(28,'Can change reference type',9,'change_referencetype'),(29,'Can delete reference type',9,'delete_referencetype'),(30,'Can add Language',10,'add_instancelanguage'),(31,'Can change Language',10,'change_instancelanguage'),(32,'Can delete Language',10,'delete_instancelanguage'),(33,'Can add Person/Book Interaction',11,'add_personbook'),(34,'Can change Person/Book Interaction',11,'change_personbook'),(35,'Can delete Person/Book Interaction',11,'delete_personbook'),(36,'Can add Catalogue',12,'add_instancecatalogue'),(37,'Can change Catalogue',12,'change_instancecatalogue'),(38,'Can delete Catalogue',12,'delete_instancecatalogue'),(39,'Can add reference',13,'add_reference'),(40,'Can change reference',13,'change_reference'),(41,'Can delete reference',13,'delete_reference'),(42,'Can add journal',14,'add_journal'),(43,'Can change journal',14,'change_journal'),(44,'Can delete journal',14,'delete_journal'),(45,'Can add Language',15,'add_worklanguage'),(46,'Can change Language',15,'change_worklanguage'),(47,'Can delete Language',15,'delete_worklanguage'),(48,'Can add owning institution',16,'add_owninginstitution'),(49,'Can change owning institution',16,'change_owninginstitution'),(50,'Can delete owning institution',16,'delete_owninginstitution'),(51,'Can add publisher',17,'add_publisher'),(52,'Can change publisher',17,'change_publisher'),(53,'Can delete publisher',17,'delete_publisher'),(54,'Can add subject',18,'add_subject'),(55,'Can change subject',18,'change_subject'),(56,'Can delete subject',18,'delete_subject'),(57,'Can add person book relationship type',19,'add_personbookrelationshiptype'),(58,'Can change person book relationship type',19,'change_personbookrelationshiptype'),(59,'Can delete person book relationship type',19,'delete_personbookrelationshiptype'),(60,'Can add derrida work',20,'add_derridawork'),(61,'Can change derrida work',20,'change_derridawork'),(62,'Can delete derrida work',20,'delete_derridawork'),(63,'Can add Derrida library work instance',21,'add_instance'),(64,'Can change Derrida library work instance',21,'change_instance'),(65,'Can delete Derrida library work instance',21,'delete_instance'),(66,'Can add Derrida library work',22,'add_work'),(67,'Can change Derrida library work',22,'change_work'),(68,'Can delete Derrida library work',22,'delete_work'),(69,'Can add Subject',23,'add_worksubject'),(70,'Can change Subject',23,'change_worksubject'),(71,'Can delete Subject',23,'delete_worksubject'),(72,'Can add language',24,'add_language'),(73,'Can change language',24,'change_language'),(74,'Can delete language',24,'delete_language'),(75,'Can add content type',25,'add_contenttype'),(76,'Can change content type',25,'change_contenttype'),(77,'Can delete content type',25,'delete_contenttype'),(78,'Can add IIIF Canvas',26,'add_canvas'),(79,'Can change IIIF Canvas',26,'change_canvas'),(80,'Can delete IIIF Canvas',26,'delete_canvas'),(81,'Can view IIIF Canvas',26,'view_manifest'),(82,'Can add IIIF Manifest',27,'add_manifest'),(83,'Can change IIIF Manifest',27,'change_manifest'),(84,'Can delete IIIF Manifest',27,'delete_manifest'),(85,'Can view IIIF Manifest',27,'view_canvas'),(86,'Can add bibliography',28,'add_bibliography'),(87,'Can change bibliography',28,'change_bibliography'),(88,'Can delete bibliography',28,'delete_bibliography'),(89,'Can add source type',29,'add_sourcetype'),(90,'Can change source type',29,'change_sourcetype'),(91,'Can delete source type',29,'delete_sourcetype'),(92,'Can add footnote',30,'add_footnote'),(93,'Can change footnote',30,'change_footnote'),(94,'Can delete footnote',30,'delete_footnote'),(95,'Can add tag',31,'add_tag'),(96,'Can change tag',31,'change_tag'),(97,'Can delete tag',31,'delete_tag'),(98,'Can add intervention',32,'add_intervention'),(99,'Can change intervention',32,'change_intervention'),(100,'Can delete intervention',32,'delete_intervention'),(101,'View intervention',32,'view_intervention'),(102,'Can add residence',33,'add_residence'),(103,'Can change residence',33,'change_residence'),(104,'Can delete residence',33,'delete_residence'),(105,'Can add relationship type',34,'add_relationshiptype'),(106,'Can change relationship type',34,'change_relationshiptype'),(107,'Can delete relationship type',34,'delete_relationshiptype'),(108,'Can add relationship',35,'add_relationship'),(109,'Can change relationship',35,'change_relationship'),(110,'Can delete relationship',35,'delete_relationship'),(111,'Can add person',36,'add_person'),(112,'Can change person',36,'change_person'),(113,'Can delete person',36,'delete_person'),(114,'Can add place',37,'add_place'),(115,'Can change place',37,'change_place'),(116,'Can delete place',37,'delete_place'),(117,'Can add session',38,'add_session'),(118,'Can change session',38,'change_session'),(119,'Can delete session',38,'delete_session'),(120,'Can add site',39,'add_site'),(121,'Can change site',39,'change_site'),(122,'Can delete site',39,'delete_site'),(123,'Can add session ticket',40,'add_sessionticket'),(124,'Can change session ticket',40,'change_sessionticket'),(125,'Can delete session ticket',40,'delete_sessionticket'),(126,'Can add proxy granting ticket',41,'add_proxygrantingticket'),(127,'Can change proxy granting ticket',41,'change_proxygrantingticket'),(128,'Can delete proxy granting ticket',41,'delete_proxygrantingticket');
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
  `digital_edition_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `digital_edition_id` (`digital_edition_id`),
  KEY `books_instance_collected_in_id_dbb43376_fk_books_instance_id` (`collected_in_id`),
  KEY `books_instance_journal_id_dfbd8d81_fk_books_journal_id` (`journal_id`),
  KEY `books_instance_publisher_id_749c6e79_fk_books_publisher_id` (`publisher_id`),
  KEY `books_instance_work_id_c6e78f6b_fk_books_work_id` (`work_id`),
  CONSTRAINT `books_instance_collected_in_id_dbb43376_fk_books_instance_id` FOREIGN KEY (`collected_in_id`) REFERENCES `books_instance` (`id`),
  CONSTRAINT `books_instance_digital_edition_id_aecd5704_fk_djiffy_manifest_id` FOREIGN KEY (`digital_edition_id`) REFERENCES `djiffy_manifest` (`id`),
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
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'annotator_store','annotation'),(3,'annotator_store','annotationgroup'),(6,'auth','group'),(4,'auth','permission'),(5,'auth','user'),(7,'books','creatortype'),(20,'books','derridawork'),(21,'books','instance'),(12,'books','instancecatalogue'),(8,'books','instancecreator'),(10,'books','instancelanguage'),(14,'books','journal'),(24,'books','language'),(16,'books','owninginstitution'),(11,'books','personbook'),(19,'books','personbookrelationshiptype'),(17,'books','publisher'),(13,'books','reference'),(9,'books','referencetype'),(18,'books','subject'),(22,'books','work'),(15,'books','worklanguage'),(23,'books','worksubject'),(25,'contenttypes','contenttype'),(41,'django_cas_ng','proxygrantingticket'),(40,'django_cas_ng','sessionticket'),(26,'djiffy','canvas'),(27,'djiffy','manifest'),(28,'footnotes','bibliography'),(30,'footnotes','footnote'),(29,'footnotes','sourcetype'),(32,'interventions','intervention'),(31,'interventions','tag'),(36,'people','person'),(35,'people','relationship'),(34,'people','relationshiptype'),(33,'people','residence'),(37,'places','place'),(38,'sessions','session'),(39,'sites','site');
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
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-08-01 18:18:25.649327'),(2,'auth','0001_initial','2017-08-01 18:18:25.997238'),(3,'admin','0001_initial','2017-08-01 18:18:26.063357'),(4,'admin','0002_logentry_remove_auto_add','2017-08-01 18:18:26.099865'),(5,'contenttypes','0002_remove_content_type_name','2017-08-01 18:18:26.172792'),(6,'auth','0002_alter_permission_name_max_length','2017-08-01 18:18:26.194811'),(7,'auth','0003_alter_user_email_max_length','2017-08-01 18:18:26.226546'),(8,'auth','0004_alter_user_username_opts','2017-08-01 18:18:26.240635'),(9,'auth','0005_alter_user_last_login_null','2017-08-01 18:18:26.268551'),(10,'auth','0006_require_contenttypes_0002','2017-08-01 18:18:26.270765'),(11,'annotator_store','0001_initial','2017-08-01 18:18:26.403009'),(12,'annotator_store','0002_annotation_quote_text_optional','2017-08-01 18:18:26.422020'),(13,'auth','0007_alter_validators_add_error_messages','2017-08-01 18:18:26.432561'),(14,'auth','0008_alter_user_username_max_length','2017-08-01 18:18:26.461287'),(15,'djiffy','0001_initial','2017-08-01 18:18:26.594838'),(16,'places','0001_initial','2017-08-01 18:18:26.615968'),(17,'people','0001_initial','2017-08-01 18:18:26.842160'),(18,'people','0002_allow_neg_years_bc','2017-08-01 18:18:26.993890'),(19,'books','0001_squashed_0033_remove_book_models','2017-08-01 18:18:28.841543'),(20,'books','0002_connect_book_references_canvases_manifests','2017-08-01 18:18:28.912179'),(21,'djiffy','0002_view_permissions','2017-08-01 18:18:28.937848'),(22,'interventions','0001_initial','2017-08-01 18:18:29.355642'),(23,'footnotes','0001_initial','2017-08-01 18:18:29.571434'),(24,'common','0001_data_editor_group','2017-08-01 18:18:29.833189'),(25,'common','0002_data_editors_footnotes_iiif_interventions','2017-08-01 18:18:29.979968'),(26,'django_cas_ng','0001_initial','2017-08-01 18:18:30.100782'),(27,'sessions','0001_initial','2017-08-01 18:18:30.142596'),(28,'sites','0001_initial','2017-08-01 18:18:30.167652'),(29,'sites','0002_alter_domain_unique','2017-08-01 18:18:30.194797');
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
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djiffy_canvas`
--

DROP TABLE IF EXISTS `djiffy_canvas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djiffy_canvas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` longtext NOT NULL,
  `short_id` varchar(255) NOT NULL,
  `uri` varchar(200) NOT NULL,
  `iiif_image_id` varchar(200) NOT NULL,
  `thumbnail` tinyint(1) NOT NULL,
  `order` int(10) unsigned NOT NULL,
  `manifest_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `djiffy_canvas_short_id_manifest_id_904833bf_uniq` (`short_id`,`manifest_id`),
  KEY `djiffy_canvas_manifest_id_3d28dbb6_fk_djiffy_manifest_id` (`manifest_id`),
  CONSTRAINT `djiffy_canvas_manifest_id_3d28dbb6_fk_djiffy_manifest_id` FOREIGN KEY (`manifest_id`) REFERENCES `djiffy_manifest` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djiffy_canvas`
--

LOCK TABLES `djiffy_canvas` WRITE;
/*!40000 ALTER TABLE `djiffy_canvas` DISABLE KEYS */;
/*!40000 ALTER TABLE `djiffy_canvas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djiffy_manifest`
--

DROP TABLE IF EXISTS `djiffy_manifest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djiffy_manifest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` longtext NOT NULL,
  `short_id` varchar(255) NOT NULL,
  `uri` varchar(200) NOT NULL,
  `metadata` longtext NOT NULL,
  `created` date NOT NULL,
  `last_modified` date NOT NULL,
  `extra_data` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `short_id` (`short_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djiffy_manifest`
--

LOCK TABLES `djiffy_manifest` WRITE;
/*!40000 ALTER TABLE `djiffy_manifest` DISABLE KEYS */;
/*!40000 ALTER TABLE `djiffy_manifest` ENABLE KEYS */;
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
-- Table structure for table `interventions_intervention`
--

DROP TABLE IF EXISTS `interventions_intervention`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interventions_intervention` (
  `id` char(32) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `text` longtext NOT NULL,
  `quote` longtext NOT NULL,
  `uri` varchar(200) NOT NULL,
  `extra_data` longtext NOT NULL,
  `intervention_type` varchar(2) NOT NULL,
  `text_translation` longtext NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  `canvas_id` int(11) DEFAULT NULL,
  `quote_language_id` int(11) DEFAULT NULL,
  `text_language_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `interventions_interv_author_id_66406b29_fk_people_pe` (`author_id`),
  KEY `interventions_interv_canvas_id_4bb99c18_fk_djiffy_ca` (`canvas_id`),
  KEY `interventions_interv_quote_language_id_f8eb4116_fk_books_lan` (`quote_language_id`),
  KEY `interventions_interv_text_language_id_9ac4e3a9_fk_books_lan` (`text_language_id`),
  KEY `interventions_intervention_user_id_ce2f9cca_fk_auth_user_id` (`user_id`),
  CONSTRAINT `interventions_interv_author_id_66406b29_fk_people_pe` FOREIGN KEY (`author_id`) REFERENCES `people_person` (`id`),
  CONSTRAINT `interventions_interv_canvas_id_4bb99c18_fk_djiffy_ca` FOREIGN KEY (`canvas_id`) REFERENCES `djiffy_canvas` (`id`),
  CONSTRAINT `interventions_interv_quote_language_id_f8eb4116_fk_books_lan` FOREIGN KEY (`quote_language_id`) REFERENCES `books_language` (`id`),
  CONSTRAINT `interventions_interv_text_language_id_9ac4e3a9_fk_books_lan` FOREIGN KEY (`text_language_id`) REFERENCES `books_language` (`id`),
  CONSTRAINT `interventions_intervention_user_id_ce2f9cca_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interventions_intervention`
--

LOCK TABLES `interventions_intervention` WRITE;
/*!40000 ALTER TABLE `interventions_intervention` DISABLE KEYS */;
/*!40000 ALTER TABLE `interventions_intervention` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interventions_intervention_tags`
--

DROP TABLE IF EXISTS `interventions_intervention_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interventions_intervention_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `intervention_id` char(32) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `interventions_interventi_intervention_id_tag_id_6938eead_uniq` (`intervention_id`,`tag_id`),
  KEY `interventions_interv_tag_id_107f3917_fk_intervent` (`tag_id`),
  CONSTRAINT `interventions_interv_intervention_id_092efd64_fk_intervent` FOREIGN KEY (`intervention_id`) REFERENCES `interventions_intervention` (`id`),
  CONSTRAINT `interventions_interv_tag_id_107f3917_fk_intervent` FOREIGN KEY (`tag_id`) REFERENCES `interventions_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interventions_intervention_tags`
--

LOCK TABLES `interventions_intervention_tags` WRITE;
/*!40000 ALTER TABLE `interventions_intervention_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `interventions_intervention_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interventions_tag`
--

DROP TABLE IF EXISTS `interventions_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interventions_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  `applies_to` varchar(2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interventions_tag`
--

LOCK TABLES `interventions_tag` WRITE;
/*!40000 ALTER TABLE `interventions_tag` DISABLE KEYS */;
INSERT INTO `interventions_tag` VALUES (1,'underlining','','A'),(2,'circling','','A'),(3,'arrow','','A'),(4,'bracket(s)','','A'),(5,'line','','A'),(6,'correction','','A'),(7,'marginal mark','','A'),(8,'punctuation mark','','A'),(9,'flyleaf note','','A'),(10,'text illegible','','AI'),(11,'transcription uncertain','','AI'),(12,'blue ink','','A'),(13,'black ink','','A');
/*!40000 ALTER TABLE `interventions_tag` ENABLE KEYS */;
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

-- Dump completed on 2017-08-01 14:18:51

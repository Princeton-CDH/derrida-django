-- MySQL dump 10.13  Distrib 5.7.21, for osx10.13 (x86_64)
--
-- Host: localhost    Database: testderrida
-- ------------------------------------------------------
-- Server version	5.7.21

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
  KEY `annotator_store_annotation_user_id_0eb79fc4_fk` (`user_id`),
  CONSTRAINT `annotator_store_annotation_user_id_0eb79fc4_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
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
INSERT INTO `auth_group_permissions` VALUES (88,1,4),(89,1,5),(90,1,6),(91,1,7),(1,1,21),(2,1,22),(3,1,23),(4,1,24),(5,1,25),(6,1,26),(7,1,27),(8,1,28),(9,1,29),(10,1,30),(11,1,31),(12,1,32),(13,1,33),(14,1,34),(15,1,35),(16,1,36),(17,1,37),(18,1,38),(19,1,39),(20,1,40),(21,1,41),(22,1,42),(23,1,43),(24,1,44),(25,1,45),(26,1,46),(27,1,47),(28,1,48),(29,1,49),(30,1,50),(31,1,51),(32,1,52),(33,1,53),(34,1,54),(35,1,55),(36,1,56),(37,1,57),(38,1,58),(39,1,59),(40,1,60),(41,1,61),(42,1,62),(43,1,63),(44,1,64),(45,1,65),(46,1,66),(47,1,67),(48,1,68),(49,1,69),(50,1,70),(51,1,71),(52,1,72),(53,1,73),(54,1,74),(55,1,78),(56,1,79),(57,1,80),(82,1,84),(83,1,88),(73,1,89),(74,1,90),(75,1,91),(76,1,92),(77,1,93),(78,1,94),(79,1,95),(80,1,96),(81,1,97),(84,1,98),(85,1,99),(86,1,100),(87,1,101),(58,1,105),(59,1,106),(60,1,107),(61,1,108),(62,1,109),(63,1,110),(64,1,111),(65,1,112),(66,1,113),(67,1,114),(68,1,115),(69,1,116),(70,1,117),(71,1,118),(72,1,119);
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
) ENGINE=InnoDB AUTO_INCREMENT=172 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add annotation',2,'add_annotation'),(5,'Can change annotation',2,'change_annotation'),(6,'Can delete annotation',2,'delete_annotation'),(7,'View annotation',2,'view_annotation'),(8,'Manage annotation',2,'admin_annotation'),(9,'Can add annotation group',3,'add_annotationgroup'),(10,'Can change annotation group',3,'change_annotationgroup'),(11,'Can delete annotation group',3,'delete_annotationgroup'),(12,'Can add permission',4,'add_permission'),(13,'Can change permission',4,'change_permission'),(14,'Can delete permission',4,'delete_permission'),(15,'Can add group',5,'add_group'),(16,'Can change group',5,'change_group'),(17,'Can delete group',5,'delete_group'),(18,'Can add user',6,'add_user'),(19,'Can change user',6,'change_user'),(20,'Can delete user',6,'delete_user'),(21,'Can add creator type',7,'add_creatortype'),(22,'Can change creator type',7,'change_creatortype'),(23,'Can delete creator type',7,'delete_creatortype'),(24,'Can add derrida work',8,'add_derridawork'),(25,'Can change derrida work',8,'change_derridawork'),(26,'Can delete derrida work',8,'delete_derridawork'),(27,'Can add Derrida library work instance',9,'add_instance'),(28,'Can change Derrida library work instance',9,'change_instance'),(29,'Can delete Derrida library work instance',9,'delete_instance'),(30,'Can add Catalogue',10,'add_instancecatalogue'),(31,'Can change Catalogue',10,'change_instancecatalogue'),(32,'Can delete Catalogue',10,'delete_instancecatalogue'),(33,'Can add instance creator',11,'add_instancecreator'),(34,'Can change instance creator',11,'change_instancecreator'),(35,'Can delete instance creator',11,'delete_instancecreator'),(36,'Can add Language',12,'add_instancelanguage'),(37,'Can change Language',12,'change_instancelanguage'),(38,'Can delete Language',12,'delete_instancelanguage'),(39,'Can add journal',13,'add_journal'),(40,'Can change journal',13,'change_journal'),(41,'Can delete journal',13,'delete_journal'),(42,'Can add language',14,'add_language'),(43,'Can change language',14,'change_language'),(44,'Can delete language',14,'delete_language'),(45,'Can add owning institution',15,'add_owninginstitution'),(46,'Can change owning institution',15,'change_owninginstitution'),(47,'Can delete owning institution',15,'delete_owninginstitution'),(48,'Can add Person/Book Interaction',16,'add_personbook'),(49,'Can change Person/Book Interaction',16,'change_personbook'),(50,'Can delete Person/Book Interaction',16,'delete_personbook'),(51,'Can add person book relationship type',17,'add_personbookrelationshiptype'),(52,'Can change person book relationship type',17,'change_personbookrelationshiptype'),(53,'Can delete person book relationship type',17,'delete_personbookrelationshiptype'),(54,'Can add publisher',18,'add_publisher'),(55,'Can change publisher',18,'change_publisher'),(56,'Can delete publisher',18,'delete_publisher'),(57,'Can add reference',19,'add_reference'),(58,'Can change reference',19,'change_reference'),(59,'Can delete reference',19,'delete_reference'),(60,'Can add reference type',20,'add_referencetype'),(61,'Can change reference type',20,'change_referencetype'),(62,'Can delete reference type',20,'delete_referencetype'),(63,'Can add subject',21,'add_subject'),(64,'Can change subject',21,'change_subject'),(65,'Can delete subject',21,'delete_subject'),(66,'Can add Derrida library work',22,'add_work'),(67,'Can change Derrida library work',22,'change_work'),(68,'Can delete Derrida library work',22,'delete_work'),(69,'Can add Language',23,'add_worklanguage'),(70,'Can change Language',23,'change_worklanguage'),(71,'Can delete Language',23,'delete_worklanguage'),(72,'Can add Subject',24,'add_worksubject'),(73,'Can change Subject',24,'change_worksubject'),(74,'Can delete Subject',24,'delete_worksubject'),(75,'Can add derrida work section',25,'add_derridaworksection'),(76,'Can change derrida work section',25,'change_derridaworksection'),(77,'Can delete derrida work section',25,'delete_derridaworksection'),(78,'Can add content type',26,'add_contenttype'),(79,'Can change content type',26,'change_contenttype'),(80,'Can delete content type',26,'delete_contenttype'),(81,'Can add IIIF Canvas',27,'add_canvas'),(82,'Can change IIIF Canvas',27,'change_canvas'),(83,'Can delete IIIF Canvas',27,'delete_canvas'),(84,'Can view IIIF Canvas',27,'view_manifest'),(85,'Can add IIIF Manifest',28,'add_manifest'),(86,'Can change IIIF Manifest',28,'change_manifest'),(87,'Can delete IIIF Manifest',28,'delete_manifest'),(88,'Can view IIIF Manifest',28,'view_canvas'),(89,'Can add bibliography',29,'add_bibliography'),(90,'Can change bibliography',29,'change_bibliography'),(91,'Can delete bibliography',29,'delete_bibliography'),(92,'Can add footnote',30,'add_footnote'),(93,'Can change footnote',30,'change_footnote'),(94,'Can delete footnote',30,'delete_footnote'),(95,'Can add source type',31,'add_sourcetype'),(96,'Can change source type',31,'change_sourcetype'),(97,'Can delete source type',31,'delete_sourcetype'),(98,'Can add intervention',32,'add_intervention'),(99,'Can change intervention',32,'change_intervention'),(100,'Can delete intervention',32,'delete_intervention'),(101,'View intervention',32,'view_intervention'),(102,'Can add tag',33,'add_tag'),(103,'Can change tag',33,'change_tag'),(104,'Can delete tag',33,'delete_tag'),(105,'Can add person',34,'add_person'),(106,'Can change person',34,'change_person'),(107,'Can delete person',34,'delete_person'),(108,'Can add relationship',35,'add_relationship'),(109,'Can change relationship',35,'change_relationship'),(110,'Can delete relationship',35,'delete_relationship'),(111,'Can add relationship type',36,'add_relationshiptype'),(112,'Can change relationship type',36,'change_relationshiptype'),(113,'Can delete relationship type',36,'delete_relationshiptype'),(114,'Can add residence',37,'add_residence'),(115,'Can change residence',37,'change_residence'),(116,'Can delete residence',37,'delete_residence'),(117,'Can add place',38,'add_place'),(118,'Can change place',38,'change_place'),(119,'Can delete place',38,'delete_place'),(120,'Can add redirect',39,'add_redirect'),(121,'Can change redirect',39,'change_redirect'),(122,'Can delete redirect',39,'delete_redirect'),(123,'Can add session',40,'add_session'),(124,'Can change session',40,'change_session'),(125,'Can delete session',40,'delete_session'),(126,'Can add site',41,'add_site'),(127,'Can change site',41,'change_site'),(128,'Can delete site',41,'delete_site'),(129,'Can add proxy granting ticket',42,'add_proxygrantingticket'),(130,'Can change proxy granting ticket',42,'change_proxygrantingticket'),(131,'Can delete proxy granting ticket',42,'delete_proxygrantingticket'),(132,'Can add session ticket',43,'add_sessionticket'),(133,'Can change session ticket',43,'change_sessionticket'),(134,'Can delete session ticket',43,'delete_sessionticket'),(135,'Can add Setting',44,'add_setting'),(136,'Can change Setting',44,'change_setting'),(137,'Can delete Setting',44,'delete_setting'),(138,'Can add Site permission',45,'add_sitepermission'),(139,'Can change Site permission',45,'change_sitepermission'),(140,'Can delete Site permission',45,'delete_sitepermission'),(141,'Can add assigned keyword',46,'add_assignedkeyword'),(142,'Can change assigned keyword',46,'change_assignedkeyword'),(143,'Can delete assigned keyword',46,'delete_assignedkeyword'),(144,'Can add Keyword',47,'add_keyword'),(145,'Can change Keyword',47,'change_keyword'),(146,'Can delete Keyword',47,'delete_keyword'),(147,'Can add Rating',48,'add_rating'),(148,'Can change Rating',48,'change_rating'),(149,'Can delete Rating',48,'delete_rating'),(150,'Can add Comment',49,'add_threadedcomment'),(151,'Can change Comment',49,'change_threadedcomment'),(152,'Can delete Comment',49,'delete_threadedcomment'),(153,'Can add Page',50,'add_page'),(154,'Can change Page',50,'change_page'),(155,'Can delete Page',50,'delete_page'),(156,'Can add Link',51,'add_link'),(157,'Can change Link',51,'change_link'),(158,'Can delete Link',51,'delete_link'),(159,'Can add Rich text page',52,'add_richtextpage'),(160,'Can change Rich text page',52,'change_richtextpage'),(161,'Can delete Rich text page',52,'delete_richtextpage'),(162,'Can add outwork',53,'add_outwork'),(163,'Can change outwork',53,'change_outwork'),(164,'Can delete outwork',53,'delete_outwork'),(165,'Can add comment',54,'add_comment'),(166,'Can change comment',54,'change_comment'),(167,'Can delete comment',54,'delete_comment'),(168,'Can moderate comments',54,'can_moderate'),(169,'Can add comment flag',55,'add_commentflag'),(170,'Can change comment flag',55,'change_commentflag'),(171,'Can delete comment flag',55,'delete_commentflag');
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
  `slug` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_derridawork_slug_38ee457a` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_derridawork`
--

LOCK TABLES `books_derridawork` WRITE;
/*!40000 ALTER TABLE `books_derridawork` DISABLE KEYS */;
INSERT INTO `books_derridawork` VALUES (1,'','De la grammatologie','Placeholder citation',0,'de-la-grammatologie');
/*!40000 ALTER TABLE `books_derridawork` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_derridaworksection`
--

DROP TABLE IF EXISTS `books_derridaworksection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_derridaworksection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `order` int(10) unsigned NOT NULL,
  `start_page` int(11) DEFAULT NULL,
  `end_page` int(11) DEFAULT NULL,
  `derridawork_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_derridaworksec_derridawork_id_ca048cbf_fk_books_der` (`derridawork_id`),
  CONSTRAINT `books_derridaworksec_derridawork_id_ca048cbf_fk_books_der` FOREIGN KEY (`derridawork_id`) REFERENCES `books_derridawork` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_derridaworksection`
--

LOCK TABLES `books_derridaworksection` WRITE;
/*!40000 ALTER TABLE `books_derridaworksection` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_derridaworksection` ENABLE KEYS */;
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
  `slug` varchar(255) NOT NULL,
  `copy` varchar(1) NOT NULL,
  `suppress_all_images` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_instance_slug_6fed72c5_uniq` (`slug`),
  UNIQUE KEY `digital_edition_id` (`digital_edition_id`),
  UNIQUE KEY `books_instance_work_id_copyright_year_copy_2a8b17cf_uniq` (`work_id`,`copyright_year`,`copy`),
  KEY `books_instance_collected_in_id_dbb43376_fk_books_instance_id` (`collected_in_id`),
  KEY `books_instance_journal_id_dfbd8d81_fk_books_journal_id` (`journal_id`),
  KEY `books_instance_publisher_id_749c6e79_fk_books_publisher_id` (`publisher_id`),
  KEY `books_instance_slug_6fed72c5` (`slug`),
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
-- Table structure for table `books_instance_suppressed_images`
--

DROP TABLE IF EXISTS `books_instance_suppressed_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_instance_suppressed_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` int(11) NOT NULL,
  `canvas_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_instance_suppresse_instance_id_canvas_id_0a13da4d_uniq` (`instance_id`,`canvas_id`),
  KEY `books_instance_suppr_canvas_id_bc01c8c5_fk_djiffy_ca` (`canvas_id`),
  CONSTRAINT `books_instance_suppr_canvas_id_bc01c8c5_fk_djiffy_ca` FOREIGN KEY (`canvas_id`) REFERENCES `djiffy_canvas` (`id`),
  CONSTRAINT `books_instance_suppr_instance_id_3f2135fb_fk_books_ins` FOREIGN KEY (`instance_id`) REFERENCES `books_instance` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_instance_suppressed_images`
--

LOCK TABLES `books_instance_suppressed_images` WRITE;
/*!40000 ALTER TABLE `books_instance_suppressed_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_instance_suppressed_images` ENABLE KEYS */;
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
  `derridawork_page` int(11) NOT NULL,
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
-- Table structure for table `books_reference_canvases`
--

DROP TABLE IF EXISTS `books_reference_canvases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_reference_canvases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reference_id` int(11) NOT NULL,
  `canvas_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_reference_canvases_reference_id_canvas_id_a107fac3_uniq` (`reference_id`,`canvas_id`),
  KEY `books_reference_canvases_canvas_id_ecdfdbbb_fk_djiffy_canvas_id` (`canvas_id`),
  CONSTRAINT `books_reference_canv_reference_id_53dc1f53_fk_books_ref` FOREIGN KEY (`reference_id`) REFERENCES `books_reference` (`id`),
  CONSTRAINT `books_reference_canvases_canvas_id_ecdfdbbb_fk_djiffy_canvas_id` FOREIGN KEY (`canvas_id`) REFERENCES `djiffy_canvas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_reference_canvases`
--

LOCK TABLES `books_reference_canvases` WRITE;
/*!40000 ALTER TABLE `books_reference_canvases` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_reference_canvases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_reference_interventions`
--

DROP TABLE IF EXISTS `books_reference_interventions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_reference_interventions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reference_id` int(11) NOT NULL,
  `intervention_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_reference_interven_reference_id_interventio_d12b645a_uniq` (`reference_id`,`intervention_id`),
  KEY `books_reference_inte_intervention_id_f54ec74b_fk_intervent` (`intervention_id`),
  CONSTRAINT `books_reference_inte_intervention_id_f54ec74b_fk_intervent` FOREIGN KEY (`intervention_id`) REFERENCES `interventions_intervention` (`id`),
  CONSTRAINT `books_reference_inte_reference_id_710b482f_fk_books_ref` FOREIGN KEY (`reference_id`) REFERENCES `books_reference` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_reference_interventions`
--

LOCK TABLES `books_reference_interventions` WRITE;
/*!40000 ALTER TABLE `books_reference_interventions` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_reference_interventions` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_referencetype`
--

LOCK TABLES `books_referencetype` WRITE;
/*!40000 ALTER TABLE `books_referencetype` DISABLE KEYS */;
INSERT INTO `books_referencetype` VALUES (1,'Citation',''),(2,'Quotation',''),(3,'Epigraph',''),(4,'Footnote','');
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
-- Table structure for table `conf_setting`
--

DROP TABLE IF EXISTS `conf_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conf_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `value` varchar(2000) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `conf_setting_site_id_b235f7ed_fk_django_site_id` (`site_id`),
  CONSTRAINT `conf_setting_site_id_b235f7ed_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conf_setting`
--

LOCK TABLES `conf_setting` WRITE;
/*!40000 ALTER TABLE `conf_setting` DISABLE KEYS */;
/*!40000 ALTER TABLE `conf_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_sitepermission`
--

DROP TABLE IF EXISTS `core_sitepermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_sitepermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `core_sitepermission_user_id_0a3cbb11_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_sitepermission`
--

LOCK TABLES `core_sitepermission` WRITE;
/*!40000 ALTER TABLE `core_sitepermission` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_sitepermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_sitepermission_sites`
--

DROP TABLE IF EXISTS `core_sitepermission_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_sitepermission_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sitepermission_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_sitepermission_site_sitepermission_id_site_i_e3e7353a_uniq` (`sitepermission_id`,`site_id`),
  KEY `core_sitepermission_sites_site_id_38038b76_fk_django_site_id` (`site_id`),
  CONSTRAINT `core_sitepermission__sitepermission_id_d33bc79e_fk_core_site` FOREIGN KEY (`sitepermission_id`) REFERENCES `core_sitepermission` (`id`),
  CONSTRAINT `core_sitepermission_sites_site_id_38038b76_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_sitepermission_sites`
--

LOCK TABLES `core_sitepermission_sites` WRITE;
/*!40000 ALTER TABLE `core_sitepermission_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_sitepermission_sites` ENABLE KEYS */;
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
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
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
-- Table structure for table `django_comment_flags`
--

DROP TABLE IF EXISTS `django_comment_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_comment_flags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flag` varchar(30) NOT NULL,
  `flag_date` datetime(6) NOT NULL,
  `comment_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_comment_flags_user_id_comment_id_flag_537f77a7_uniq` (`user_id`,`comment_id`,`flag`),
  KEY `django_comment_flags_comment_id_d8054933_fk_django_comments_id` (`comment_id`),
  KEY `django_comment_flags_flag_8b141fcb` (`flag`),
  CONSTRAINT `django_comment_flags_comment_id_d8054933_fk_django_comments_id` FOREIGN KEY (`comment_id`) REFERENCES `django_comments` (`id`),
  CONSTRAINT `django_comment_flags_user_id_f3f81f0a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_comment_flags`
--

LOCK TABLES `django_comment_flags` WRITE;
/*!40000 ALTER TABLE `django_comment_flags` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_comment_flags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_comments`
--

DROP TABLE IF EXISTS `django_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_pk` longtext NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_email` varchar(254) NOT NULL,
  `user_url` varchar(200) NOT NULL,
  `comment` longtext NOT NULL,
  `submit_date` datetime(6) NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `is_public` tinyint(1) NOT NULL,
  `is_removed` tinyint(1) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `django_comments_content_type_id_c4afe962_fk_django_co` (`content_type_id`),
  KEY `django_comments_site_id_9dcf666e_fk_django_site_id` (`site_id`),
  KEY `django_comments_user_id_a0a440a1_fk_auth_user_id` (`user_id`),
  KEY `django_comments_submit_date_514ed2d9` (`submit_date`),
  CONSTRAINT `django_comments_content_type_id_c4afe962_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_comments_site_id_9dcf666e_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`),
  CONSTRAINT `django_comments_user_id_a0a440a1_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_comments`
--

LOCK TABLES `django_comments` WRITE;
/*!40000 ALTER TABLE `django_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_comments` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'annotator_store','annotation'),(3,'annotator_store','annotationgroup'),(5,'auth','group'),(4,'auth','permission'),(6,'auth','user'),(7,'books','creatortype'),(8,'books','derridawork'),(25,'books','derridaworksection'),(9,'books','instance'),(10,'books','instancecatalogue'),(11,'books','instancecreator'),(12,'books','instancelanguage'),(13,'books','journal'),(14,'books','language'),(15,'books','owninginstitution'),(16,'books','personbook'),(17,'books','personbookrelationshiptype'),(18,'books','publisher'),(19,'books','reference'),(20,'books','referencetype'),(21,'books','subject'),(22,'books','work'),(23,'books','worklanguage'),(24,'books','worksubject'),(44,'conf','setting'),(26,'contenttypes','contenttype'),(45,'core','sitepermission'),(42,'django_cas_ng','proxygrantingticket'),(43,'django_cas_ng','sessionticket'),(54,'django_comments','comment'),(55,'django_comments','commentflag'),(27,'djiffy','canvas'),(28,'djiffy','manifest'),(29,'footnotes','bibliography'),(30,'footnotes','footnote'),(31,'footnotes','sourcetype'),(46,'generic','assignedkeyword'),(47,'generic','keyword'),(48,'generic','rating'),(49,'generic','threadedcomment'),(32,'interventions','intervention'),(33,'interventions','tag'),(53,'outwork','outwork'),(51,'pages','link'),(50,'pages','page'),(52,'pages','richtextpage'),(34,'people','person'),(35,'people','relationship'),(36,'people','relationshiptype'),(37,'people','residence'),(38,'places','place'),(39,'redirects','redirect'),(40,'sessions','session'),(41,'sites','site');
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
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-04-10 19:38:57.673858'),(2,'auth','0001_initial','2018-04-10 19:38:58.068802'),(3,'admin','0001_initial','2018-04-10 19:38:58.159476'),(4,'admin','0002_logentry_remove_auto_add','2018-04-10 19:38:58.205048'),(5,'contenttypes','0002_remove_content_type_name','2018-04-10 19:38:58.287675'),(6,'auth','0002_alter_permission_name_max_length','2018-04-10 19:38:58.314712'),(7,'auth','0003_alter_user_email_max_length','2018-04-10 19:38:58.348638'),(8,'auth','0004_alter_user_username_opts','2018-04-10 19:38:58.359461'),(9,'auth','0005_alter_user_last_login_null','2018-04-10 19:38:58.392688'),(10,'auth','0006_require_contenttypes_0002','2018-04-10 19:38:58.396778'),(11,'annotator_store','0001_initial','2018-04-10 19:38:58.550452'),(12,'annotator_store','0002_annotation_quote_text_optional','2018-04-10 19:38:58.571857'),(13,'auth','0007_alter_validators_add_error_messages','2018-04-10 19:38:58.608799'),(14,'auth','0008_alter_user_username_max_length','2018-04-10 19:38:58.727766'),(15,'djiffy','0001_initial','2018-04-10 19:38:58.865182'),(16,'djiffy','0002_view_permissions','2018-04-10 19:38:58.875477'),(17,'places','0001_initial','2018-04-10 19:38:58.898940'),(18,'people','0001_initial','2018-04-10 19:38:59.176179'),(19,'people','0002_allow_neg_years_bc','2018-04-10 19:38:59.347832'),(20,'books','0001_squashed_0033_remove_book_models','2018-04-10 19:39:01.409399'),(21,'books','0002_connect_book_references_canvases_manifests','2018-04-10 19:39:01.484797'),(22,'interventions','0001_initial','2018-04-10 19:39:01.938429'),(23,'books','0003_add_foreignkey_reference_canvas_intervention','2018-04-10 19:39:02.227616'),(24,'books','0004_derridawork_section_slug','2018-04-10 19:39:02.623352'),(25,'books','0005_add_slugs_copy','2018-04-10 19:39:02.890531'),(26,'books','0006_suppress_images_fields','2018-04-10 19:39:03.062469'),(27,'books','0007_fix_collectedwork_references','2018-04-10 19:39:03.120055'),(28,'books','0008_instance_work_year_copy_unique_together','2018-04-10 19:39:03.222016'),(29,'books','0009_migrate_plum_to_figgy','2018-04-10 19:39:03.345126'),(30,'books','0010_work_author_optional','2018-04-10 19:39:03.455481'),(31,'footnotes','0001_initial','2018-04-10 19:39:03.714711'),(32,'common','0001_data_editor_group','2018-04-10 19:39:04.012560'),(33,'common','0002_data_editors_footnotes_iiif_interventions','2018-04-10 19:39:04.184143'),(34,'sites','0001_initial','2018-04-10 19:39:04.206795'),(35,'conf','0001_initial','2018-04-10 19:39:04.255486'),(36,'core','0001_initial','2018-04-10 19:39:04.401348'),(37,'core','0002_auto_20150414_2140','2018-04-10 19:39:04.483888'),(38,'django_cas_ng','0001_initial','2018-04-10 19:39:04.621068'),(39,'django_comments','0001_initial','2018-04-10 19:39:04.916147'),(40,'django_comments','0002_update_user_email_field_length','2018-04-10 19:39:04.962357'),(41,'django_comments','0003_add_submit_date_index','2018-04-10 19:39:05.005728'),(42,'generic','0001_initial','2018-04-10 19:39:05.528311'),(43,'generic','0002_auto_20141227_0224','2018-04-10 19:39:05.543150'),(44,'generic','0003_auto_20170411_0504','2018-04-10 19:39:05.597228'),(45,'sites','0002_alter_domain_unique','2018-04-10 19:39:05.624061'),(46,'pages','0001_initial','2018-04-10 19:39:05.903271'),(47,'pages','0002_auto_20141227_0224','2018-04-10 19:39:05.929809'),(48,'pages','0003_auto_20150527_1555','2018-04-10 19:39:05.964164'),(49,'pages','0004_auto_20170411_0504','2018-04-10 19:39:06.029406'),(50,'outwork','0001_initial','2018-04-10 19:39:06.151877'),(51,'outwork','0002_initial_pages','2018-04-10 19:39:06.233356'),(52,'redirects','0001_initial','2018-04-10 19:39:06.351594'),(53,'sessions','0001_initial','2018-04-10 19:39:06.393228');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_redirect`
--

DROP TABLE IF EXISTS `django_redirect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_redirect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site_id` int(11) NOT NULL,
  `old_path` varchar(200) NOT NULL,
  `new_path` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_redirect_site_id_old_path_ac5dd16b_uniq` (`site_id`,`old_path`),
  KEY `django_redirect_old_path_c6cc94d3` (`old_path`),
  CONSTRAINT `django_redirect_site_id_c3e37341_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_redirect`
--

LOCK TABLES `django_redirect` WRITE;
/*!40000 ALTER TABLE `django_redirect` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_redirect` ENABLE KEYS */;
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
INSERT INTO `django_site` VALUES (1,'','');
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
-- Table structure for table `generic_assignedkeyword`
--

DROP TABLE IF EXISTS `generic_assignedkeyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `generic_assignedkeyword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `_order` int(11) DEFAULT NULL,
  `object_pk` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `keyword_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `generic_assignedkeyw_content_type_id_3dd89a7f_fk_django_co` (`content_type_id`),
  KEY `generic_assignedkeyw_keyword_id_44c17f9d_fk_generic_k` (`keyword_id`),
  CONSTRAINT `generic_assignedkeyw_content_type_id_3dd89a7f_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `generic_assignedkeyw_keyword_id_44c17f9d_fk_generic_k` FOREIGN KEY (`keyword_id`) REFERENCES `generic_keyword` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `generic_assignedkeyword`
--

LOCK TABLES `generic_assignedkeyword` WRITE;
/*!40000 ALTER TABLE `generic_assignedkeyword` DISABLE KEYS */;
/*!40000 ALTER TABLE `generic_assignedkeyword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `generic_keyword`
--

DROP TABLE IF EXISTS `generic_keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `generic_keyword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(500) NOT NULL,
  `slug` varchar(2000) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `generic_keyword_site_id_c5be0acc_fk_django_site_id` (`site_id`),
  CONSTRAINT `generic_keyword_site_id_c5be0acc_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `generic_keyword`
--

LOCK TABLES `generic_keyword` WRITE;
/*!40000 ALTER TABLE `generic_keyword` DISABLE KEYS */;
/*!40000 ALTER TABLE `generic_keyword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `generic_rating`
--

DROP TABLE IF EXISTS `generic_rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `generic_rating` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` int(11) NOT NULL,
  `rating_date` datetime(6) DEFAULT NULL,
  `object_pk` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `generic_rating_content_type_id_eaf475fa_fk_django_co` (`content_type_id`),
  KEY `generic_rating_user_id_60020469_fk_auth_user_id` (`user_id`),
  CONSTRAINT `generic_rating_content_type_id_eaf475fa_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `generic_rating_user_id_60020469_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `generic_rating`
--

LOCK TABLES `generic_rating` WRITE;
/*!40000 ALTER TABLE `generic_rating` DISABLE KEYS */;
/*!40000 ALTER TABLE `generic_rating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `generic_threadedcomment`
--

DROP TABLE IF EXISTS `generic_threadedcomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `generic_threadedcomment` (
  `comment_ptr_id` int(11) NOT NULL,
  `rating_count` int(11) NOT NULL,
  `rating_sum` int(11) NOT NULL,
  `rating_average` double NOT NULL,
  `by_author` tinyint(1) NOT NULL,
  `replied_to_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`comment_ptr_id`),
  KEY `generic_threadedcomm_replied_to_id_d0a08d73_fk_generic_t` (`replied_to_id`),
  CONSTRAINT `generic_threadedcomm_comment_ptr_id_e208ed60_fk_django_co` FOREIGN KEY (`comment_ptr_id`) REFERENCES `django_comments` (`id`),
  CONSTRAINT `generic_threadedcomm_replied_to_id_d0a08d73_fk_generic_t` FOREIGN KEY (`replied_to_id`) REFERENCES `generic_threadedcomment` (`comment_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `generic_threadedcomment`
--

LOCK TABLES `generic_threadedcomment` WRITE;
/*!40000 ALTER TABLE `generic_threadedcomment` DISABLE KEYS */;
/*!40000 ALTER TABLE `generic_threadedcomment` ENABLE KEYS */;
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
-- Table structure for table `outwork_outwork`
--

DROP TABLE IF EXISTS `outwork_outwork`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `outwork_outwork` (
  `page_ptr_id` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `orig_pubdate` date DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`page_ptr_id`),
  KEY `outwork_outwork_author_id_318acad2_fk_people_person_id` (`author_id`),
  CONSTRAINT `outwork_outwork_author_id_318acad2_fk_people_person_id` FOREIGN KEY (`author_id`) REFERENCES `people_person` (`id`),
  CONSTRAINT `outwork_outwork_page_ptr_id_5a69a107_fk_pages_page_id` FOREIGN KEY (`page_ptr_id`) REFERENCES `pages_page` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outwork_outwork`
--

LOCK TABLES `outwork_outwork` WRITE;
/*!40000 ALTER TABLE `outwork_outwork` DISABLE KEYS */;
/*!40000 ALTER TABLE `outwork_outwork` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pages_link`
--

DROP TABLE IF EXISTS `pages_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pages_link` (
  `page_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`page_ptr_id`),
  CONSTRAINT `pages_link_page_ptr_id_37d469f7_fk_pages_page_id` FOREIGN KEY (`page_ptr_id`) REFERENCES `pages_page` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pages_link`
--

LOCK TABLES `pages_link` WRITE;
/*!40000 ALTER TABLE `pages_link` DISABLE KEYS */;
/*!40000 ALTER TABLE `pages_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pages_page`
--

DROP TABLE IF EXISTS `pages_page`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pages_page` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords_string` varchar(500) NOT NULL,
  `title` varchar(500) NOT NULL,
  `slug` varchar(2000) NOT NULL,
  `_meta_title` varchar(500) DEFAULT NULL,
  `description` longtext NOT NULL,
  `gen_description` tinyint(1) NOT NULL,
  `created` datetime(6) DEFAULT NULL,
  `updated` datetime(6) DEFAULT NULL,
  `status` int(11) NOT NULL,
  `publish_date` datetime(6) DEFAULT NULL,
  `expiry_date` datetime(6) DEFAULT NULL,
  `short_url` varchar(200) DEFAULT NULL,
  `in_sitemap` tinyint(1) NOT NULL,
  `_order` int(11) DEFAULT NULL,
  `in_menus` varchar(100) DEFAULT NULL,
  `titles` varchar(1000) DEFAULT NULL,
  `content_model` varchar(50) DEFAULT NULL,
  `login_required` tinyint(1) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pages_page_parent_id_133fa4d3_fk_pages_page_id` (`parent_id`),
  KEY `pages_page_site_id_47a43e5b_fk_django_site_id` (`site_id`),
  KEY `pages_page_publish_date_eb7c8d46` (`publish_date`),
  CONSTRAINT `pages_page_parent_id_133fa4d3_fk_pages_page_id` FOREIGN KEY (`parent_id`) REFERENCES `pages_page` (`id`),
  CONSTRAINT `pages_page_site_id_47a43e5b_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pages_page`
--

LOCK TABLES `pages_page` WRITE;
/*!40000 ALTER TABLE `pages_page` DISABLE KEYS */;
INSERT INTO `pages_page` VALUES (1,'','Derrida\'s Margins','/','','An online research tool for Derrida’s annotations that provides a behind-the-scenes look at his reading practices and the philosophy of deconstruction',0,'2018-04-10 19:39:06.217450','2018-04-10 19:39:06.217450',2,'2018-04-10 19:39:06.217450',NULL,NULL,1,1,'3','Derrida\'s Margins','richtextpage',0,NULL,1),(2,'','Outwork','outwork','','',1,'2018-04-10 19:39:06.217450','2018-04-10 19:39:06.217450',2,'2018-04-10 19:39:06.217450',NULL,NULL,1,2,'3','Outwork','richtextpage',0,NULL,1),(3,'','How to Cite','cite','','',1,'2018-04-10 19:39:06.217450','2018-04-10 19:39:06.217450',2,'2018-04-10 19:39:06.217450',NULL,NULL,1,3,'3','How to Cite','richtextpage',0,NULL,1),(4,'','Contact','contact','','',1,'2018-04-10 19:39:06.217450','2018-04-10 19:39:06.217450',2,'2018-04-10 19:39:06.217450',NULL,NULL,1,4,'3','Contact','richtextpage',0,NULL,1),(5,'','Derrida\'s Library','library','','Browse Derrida’s personal copies of the books referenced in his published works.',0,'2018-04-10 19:39:06.217450','2018-04-10 19:39:06.217450',2,'2018-04-10 19:39:06.217450',NULL,NULL,1,5,'1,3','Derrida\'s Library','richtextpage',0,NULL,1),(6,'','Reference List','references','','Explore the quotations and references in Derrida’s works.',0,'2018-04-10 19:39:06.217450','2018-04-10 19:39:06.217450',2,'2018-04-10 19:39:06.217450',NULL,NULL,1,6,'1,3','Reference List','richtextpage',0,NULL,1),(7,'','Interventions','interventions','','Explore the traces of Derrida’s reading.',0,'2018-04-10 19:39:06.217450','2018-04-10 19:39:06.217450',2,'2018-04-10 19:39:06.217450',NULL,NULL,1,7,'1,3','Interventions','richtextpage',0,NULL,1),(8,'','Visualization','references/histogram/de-la-grammatologie','References by Section ‖ Visualization','Explore all quotations and references in Derrida’s works.',0,'2018-04-10 19:39:06.217450','2018-04-10 19:39:06.217450',2,'2018-04-10 19:39:06.217450',NULL,NULL,1,8,'1,3','Visualization','richtextpage',0,NULL,1),(9,'','Visualization by Author','references/histogram','References by Author ‖ Visualization','Explore all quotations and references in Derrida’s works.',0,'2018-04-10 19:39:06.217450','2018-04-10 19:39:06.217450',2,'2018-04-10 19:39:06.217450',NULL,NULL,1,9,'','Visualization by Author','richtextpage',0,NULL,1);
/*!40000 ALTER TABLE `pages_page` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pages_richtextpage`
--

DROP TABLE IF EXISTS `pages_richtextpage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pages_richtextpage` (
  `page_ptr_id` int(11) NOT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`page_ptr_id`),
  CONSTRAINT `pages_richtextpage_page_ptr_id_8ca99b83_fk_pages_page_id` FOREIGN KEY (`page_ptr_id`) REFERENCES `pages_page` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pages_richtextpage`
--

LOCK TABLES `pages_richtextpage` WRITE;
/*!40000 ALTER TABLE `pages_richtextpage` DISABLE KEYS */;
INSERT INTO `pages_richtextpage` VALUES (1,'\n<section>\n    <q>And yet did we not know that... only in the book, coming back to it unceasingly, drawing all our resources from it, could we indefinitely designate the writing beyond the book?</q>\n    <p class=\"quote-cite\">Jacques Derrida, <i>Writing and Difference</i></p>\n    <p>“Derrida’s Margins” unpacks the library contained within each of Derrida’s published works, starting with the landmark 1967 text <i>De la grammatologie</i>. Additional texts will be added as the project continues.</p>\n    <p>This scholarly tool enables researchers to approach the development of deconstruction in an unprecedented way by exploring the relationship between Derrida’s thought and his reading practices.  Users may browse or search: Derrida’s personal copies of books that are referenced in <i>De la grammatologie</i>; the nearly one thousand <strong>references</strong> (quotations, citations, footnotes, or epigraphs) found in the pages of <i>De la grammatologie</i>; and the <strong>interventions</strong> Derrida made in his books (annotations, marginalia, bookmarks, tipped-in pages, notes, etc.) that correspond to each reference. The website also provides data <strong>visualizations</strong> of Derrida’s references.\n    <p>The Library of Jacques Derrida is housed in Princeton University Library’s Rare Books and Special Collections.</p>\n</section>\n<section class=\"credits\">\n    <ul class=\"credits__group\">\n    <li class=\"credits__role\">Project Director</li>\n    <li class=\"credits__name\">Katie Chenoweth</li>\n    </ul>\n    <ul class=\"credits__group\">\n    <li class=\"credits__role\">Project Manager</li>\n    <li class=\"credits__name\">Alex Raiffe</li>\n    </ul>\n    <ul class=\"credits__group\">\n    <li class=\"credits__role\">Technical Lead</li>\n    <li class=\"credits__name\">Rebecca Sutton Koeser</li>\n    </ul>\n    <ul class=\"credits__group\">\n    <li class=\"credits__role\">Project Designer</li>\n    <li class=\"credits__name\">Rebecca Munson</li>\n    </ul>\n    <ul class=\"credits__group\">\n    <li class=\"credits__role\">User Experience Designer</li>\n    <li class=\"credits__name\">Xinyi Li</li>\n    </ul>\n    <ul class=\"credits__group\">\n    <li class=\"credits__role\">Web Developers</li>\n    <li class=\"credits__name\">Benjamin Hicks</li>\n    <li class=\"credits__name\">Kevin Glover</li>\n    <li class=\"credits__name\">Nick Budak</li>\n    </ul>\n    <ul class=\"credits__group\">\n    <li class=\"credits__role\">Database Designer</li>\n    <li class=\"credits__name\">Jean Bauer</li>\n    </ul>\n    <ul class=\"credits__group\">\n    <li class=\"credits__role\">Graduate Research Assistants</li>\n    <li class=\"credits__name\">Ren&eacute;e Altergott</li>\n    <li class=\"credits__name\">Chad C&oacute;rdova</li>\n    <li class=\"credits__name\">Austin Hancock</li>\n    <li class=\"credits__name\">Chlo&eacute; Vettier</li>\n    </ul>\n    <ul class=\"credits__group\">\n    <li class=\"credits__role\">Undergraduate Research Assistants</li>\n    <li class=\"credits__name\">Jin Chow</li>\n    <li class=\"credits__name\">Elise Freeman</li>\n    </ul>\n    <ul class=\"credits__group\">\n    <li class=\"credits__role\">Advisors</li>\n    <li class=\"credits__name\">Avital Ronell</li>\n    <li class=\"credits__name\">Eduardo Cadava</li>\n    <li class=\"credits__name\">Geoffrey Bennington</li>\n    </ul>\n</section>\n'),(2,'[placeholder]'),(3,'[placeholder]'),(4,'[placeholder]'),(5,'[placeholder]'),(6,'[placeholder]'),(7,'[placeholder]'),(8,'[placeholder]'),(9,'[placeholder]');
/*!40000 ALTER TABLE `pages_richtextpage` ENABLE KEYS */;
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

-- Dump completed on 2018-04-10 15:39:31

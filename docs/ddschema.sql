-- MySQL dump 10.13  Distrib 5.1.73, for debian-linux-gnu (x86_64)
--
-- Host: example.com    Database: dracidoupe_cz
-- ------------------------------------------------------
-- Server version	5.7.26

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
-- Table structure for table `aktivni_uzivatele`
--

DROP TABLE IF EXISTS `aktivni_uzivatele`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aktivni_uzivatele` (
  `relid` varchar(32) NOT NULL DEFAULT '',
  `id_uzivatele` int(11) NOT NULL DEFAULT '0',
  `lastused` int(11) unsigned NOT NULL DEFAULT '0',
  `agend` varchar(100) NOT NULL DEFAULT '',
  `IP` varchar(15) NOT NULL DEFAULT '',
  `nck` varchar(50) NOT NULL DEFAULT '',
  `timelimit` int(11) NOT NULL DEFAULT '900',
  `relid_cookie` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`relid`),
  KEY `timelimit` (`timelimit`),
  KEY `relid_cookie` (`relid_cookie`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `aktuality`
--

DROP TABLE IF EXISTS `aktuality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aktuality` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `datum` datetime NOT NULL DEFAULT '2001-07-07 12:00:00',
  `autor` tinytext NOT NULL,
  `autmail` tinytext NOT NULL,
  `text` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=638 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `alchpredmety`
--

DROP TABLE IF EXISTS `alchpredmety`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alchpredmety` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno` longtext NOT NULL,
  `mag` int(11) DEFAULT '0',
  `suroviny` smallint(11) DEFAULT NULL,
  `zaklad` varchar(150) DEFAULT NULL,
  `nalezeni` varchar(150) DEFAULT NULL,
  `trvani` varchar(30) DEFAULT NULL,
  `vyroba` varchar(30) DEFAULT NULL,
  `nebezpecnost` varchar(30) DEFAULT NULL,
  `sila` varchar(30) DEFAULT NULL,
  `bcz` varchar(30) DEFAULT NULL,
  `denmag` mediumint(11) DEFAULT NULL,
  `dosah_ucinku` varchar(20) DEFAULT NULL,
  `uroven_vyrobce` varchar(10) NOT NULL DEFAULT '',
  `sfera` varchar(20) NOT NULL,
  `popis` text NOT NULL,
  `pochvez` varchar(5) NOT NULL,
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `zdroj` longtext,
  `zdrojmail` longtext,
  `datum` datetime NOT NULL DEFAULT '2001-08-08 21:13:48',
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `skupina` varchar(30) NOT NULL DEFAULT '',
  `tisknuto` int(11) NOT NULL,
  `pocet_hlasujicich` int(11) DEFAULT NULL,
  `hodnota_hlasovani` int(11) DEFAULT '0',
  `precteno` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=681 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ankety`
--

DROP TABLE IF EXISTS `ankety`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ankety` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `otazka` tinytext,
  `odp1` varchar(250) NOT NULL DEFAULT '',
  `p1` int(11) NOT NULL DEFAULT '0',
  `odp2` varchar(250) NOT NULL DEFAULT '',
  `p2` int(11) NOT NULL DEFAULT '0',
  `odp3` varchar(250) NOT NULL DEFAULT '',
  `p3` int(11) NOT NULL DEFAULT '0',
  `odp4` varchar(250) NOT NULL DEFAULT '',
  `p4` int(11) NOT NULL DEFAULT '0',
  `odp5` varchar(250) NOT NULL DEFAULT '',
  `p5` int(11) NOT NULL DEFAULT '0',
  `odp6` varchar(250) NOT NULL DEFAULT '',
  `p6` int(11) NOT NULL DEFAULT '0',
  `odp7` varchar(250) NOT NULL DEFAULT '',
  `p7` int(11) NOT NULL DEFAULT '0',
  `odp8` varchar(250) NOT NULL DEFAULT '',
  `p8` int(11) NOT NULL DEFAULT '0',
  `odp9` varchar(250) NOT NULL DEFAULT '',
  `p9` int(11) NOT NULL DEFAULT '0',
  `odp10` varchar(250) NOT NULL DEFAULT '',
  `p10` int(11) NOT NULL DEFAULT '0',
  `spusteno` int(11) NOT NULL DEFAULT '0',
  `konec` int(11) NOT NULL DEFAULT '0',
  `id_stolu` int(11) NOT NULL DEFAULT '0',
  `jmenovite` char(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1280 DEFAULT CHARSET=latin2 PACK_KEYS=0;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ankety_hlasy`
--

DROP TABLE IF EXISTS `ankety_hlasy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ankety_hlasy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `anketa_id` int(11) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL DEFAULT '0',
  `answer_id` int(11) NOT NULL DEFAULT '0',
  `user_comment` varchar(1023) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `anketa_id` (`anketa_id`,`user_id`),
  KEY `answer_id` (`answer_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14364 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=646 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=20000 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `banned_ip`
--

DROP TABLE IF EXISTS `banned_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `banned_ip` (
  `ip` varchar(16) NOT NULL DEFAULT '',
  `popis` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`ip`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2 COMMENT='Obsahuje ip adresy, ze kterych nejde pristupovat jako anonym';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bestiar`
--

DROP TABLE IF EXISTS `bestiar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bestiar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jmeno` tinytext NOT NULL,
  `zvt` tinytext NOT NULL,
  `uc` tinytext NOT NULL,
  `oc` tinytext NOT NULL,
  `odl` char(3) NOT NULL DEFAULT '',
  `inteligence` varchar(50) DEFAULT NULL,
  `vel` varchar(20) NOT NULL DEFAULT '',
  `zran` tinytext,
  `poh` tinytext,
  `pres` tinytext,
  `pokl` tinytext,
  `zkus` varchar(50) NOT NULL DEFAULT '0',
  `popis` longtext NOT NULL,
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `datum` datetime NOT NULL DEFAULT '2001-08-08 21:45:59',
  `pochvez` varchar(5) NOT NULL,
  `zdroj` tinytext,
  `zdrojmail` longtext,
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `skupina` tinytext NOT NULL,
  `bojovnost` varchar(50) DEFAULT NULL,
  `SM` varchar(50) NOT NULL DEFAULT '0',
  `tisknuto` int(11) NOT NULL,
  `pocet_hlasujicich` int(11) DEFAULT NULL,
  `hodnota_hlasovani` int(11) DEFAULT '0',
  `precteno` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1718 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat1_zaloha`
--

DROP TABLE IF EXISTS `chat1_zaloha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat1_zaloha` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pro` int(10) NOT NULL DEFAULT '0',
  `od` int(10) NOT NULL DEFAULT '0',
  `cas` int(15) NOT NULL DEFAULT '0',
  `zprava` text NOT NULL,
  `nick` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `CAS` (`cas`)
) ENGINE=MyISAM AUTO_INCREMENT=2059124 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat1_zaloha2`
--

DROP TABLE IF EXISTS `chat1_zaloha2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat1_zaloha2` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pro` int(10) NOT NULL DEFAULT '0',
  `od` int(10) NOT NULL DEFAULT '0',
  `cas` int(15) NOT NULL DEFAULT '0',
  `zprava` text NOT NULL,
  `nick` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `CAS` (`cas`)
) ENGINE=MyISAM AUTO_INCREMENT=2141188 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_1`
--

DROP TABLE IF EXISTS `chat_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_1` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pro` int(10) NOT NULL DEFAULT '0',
  `od` int(10) NOT NULL DEFAULT '0',
  `cas` int(15) NOT NULL DEFAULT '0',
  `zprava` text NOT NULL,
  `nick` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `CAS` (`cas`)
) ENGINE=MyISAM AUTO_INCREMENT=676781 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_2`
--

DROP TABLE IF EXISTS `chat_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_2` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pro` int(10) NOT NULL DEFAULT '0',
  `od` int(10) NOT NULL DEFAULT '0',
  `cas` int(15) NOT NULL DEFAULT '0',
  `zprava` text NOT NULL,
  `nick` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=255989 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_2106`
--

DROP TABLE IF EXISTS `chat_2106`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_2106` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pro` int(10) NOT NULL DEFAULT '0',
  `od` int(10) NOT NULL DEFAULT '0',
  `cas` int(15) NOT NULL,
  `zprava` text NOT NULL,
  `nick` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_2107`
--

DROP TABLE IF EXISTS `chat_2107`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_2107` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pro` int(10) NOT NULL DEFAULT '0',
  `od` int(10) NOT NULL DEFAULT '0',
  `cas` int(15) NOT NULL,
  `zprava` text NOT NULL,
  `nick` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_3`
--

DROP TABLE IF EXISTS `chat_3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_3` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pro` int(10) NOT NULL DEFAULT '0',
  `od` int(10) NOT NULL DEFAULT '0',
  `cas` int(15) NOT NULL DEFAULT '0',
  `zprava` text NOT NULL,
  `nick` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=816922 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_4`
--

DROP TABLE IF EXISTS `chat_4`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_4` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `pro` int(10) NOT NULL DEFAULT '0',
  `od` int(10) NOT NULL DEFAULT '0',
  `cas` int(15) NOT NULL DEFAULT '0',
  `zprava` text NOT NULL,
  `nick` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=700610 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_aktivni`
--

DROP TABLE IF EXISTS `chat_aktivni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_aktivni` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `nick` tinytext,
  `cas` int(15) DEFAULT NULL,
  `mistnost` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `cas` (`cas`)
) ENGINE=MyISAM AUTO_INCREMENT=172860 DEFAULT CHARSET=latin2 PACK_KEYS=0;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_mistnosti`
--

DROP TABLE IF EXISTS `chat_mistnosti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_mistnosti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nazev` varchar(40) NOT NULL DEFAULT '',
  `popis` varchar(255) NOT NULL DEFAULT '',
  `stala` tinyint(1) NOT NULL DEFAULT '0',
  `spravce` int(11) NOT NULL DEFAULT '0',
  `septani` tinyint(1) NOT NULL DEFAULT '1',
  `zamknuto` tinyint(1) NOT NULL DEFAULT '0',
  `sprava` tinyint(1) NOT NULL DEFAULT '1',
  `bez_hostu` int(11) NOT NULL DEFAULT '0',
  `duch` smallint(8) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `duch` (`duch`)
) ENGINE=MyISAM AUTO_INCREMENT=2108 DEFAULT CHARSET=latin2 PACK_KEYS=0;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_pristupy`
--

DROP TABLE IF EXISTS `chat_pristupy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_pristupy` (
  `mistnost_id` int(10) unsigned NOT NULL DEFAULT '0',
  `nick` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`mistnost_id`,`nick`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_properties`
--

DROP TABLE IF EXISTS `chat_properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_properties` (
  `id_uz` int(8) unsigned NOT NULL DEFAULT '0',
  `param` varchar(25) NOT NULL DEFAULT '',
  `value` varchar(25) NOT NULL DEFAULT '',
  KEY `id` (`id_uz`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ddcz_author`
--

DROP TABLE IF EXISTS `ddcz_author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ddcz_author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author_type` varchar(1) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `website_email` varchar(255) DEFAULT NULL,
  `anonymous_user_nick` varchar(255) DEFAULT NULL,
  `user_nick` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3846 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ddcz_creativepage`
--

DROP TABLE IF EXISTS `ddcz_creativepage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ddcz_creativepage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `slug` varchar(30) NOT NULL,
  `model_class` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ddcz_creativepage_slug_9fd2dc5f` (`slug`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ddcz_creativepageconcept`
--

DROP TABLE IF EXISTS `ddcz_creativepageconcept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ddcz_creativepageconcept` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `page_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `page_id` (`page_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ddcz_creativepagesection`
--

DROP TABLE IF EXISTS `ddcz_creativepagesection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ddcz_creativepagesection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `slug` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ddcz_creativepagesection_slug_1e226240` (`slug`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diskuze`
--

DROP TABLE IF EXISTS `diskuze`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `diskuze` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cizi` int(11) NOT NULL DEFAULT '0',
  `nickname` varchar(25) NOT NULL DEFAULT '',
  `email` varchar(40) NOT NULL DEFAULT '',
  `text` mediumtext NOT NULL,
  `datum` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `cizi_tbl` varchar(20) NOT NULL DEFAULT '',
  `reputace` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `RUBRIKA` (`cizi_tbl`),
  KEY `CIZI` (`id_cizi`)
) ENGINE=MyISAM AUTO_INCREMENT=129656 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diskuze_maillist`
--

DROP TABLE IF EXISTS `diskuze_maillist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `diskuze_maillist` (
  `id_uz` int(11) NOT NULL DEFAULT '0',
  `id_cizi` int(11) NOT NULL DEFAULT '0',
  `email` varchar(40) NOT NULL DEFAULT '',
  `cizi_tbl` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_uz`,`id_cizi`,`cizi_tbl`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=MyISAM AUTO_INCREMENT=199 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=71 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dobrodruzstvi`
--

DROP TABLE IF EXISTS `dobrodruzstvi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dobrodruzstvi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno` tinytext NOT NULL,
  `anotace` tinytext NOT NULL,
  `cesta` tinytext,
  `klicsl` tinytext NOT NULL,
  `pochvez` varchar(5) NOT NULL,
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `datum` datetime NOT NULL DEFAULT '2001-07-04 12:00:00',
  `zdroj` tinytext,
  `zdrojmail` tinytext,
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `pocet_hlasujicich` int(11) DEFAULT NULL,
  `hodnota_hlasovani` int(11) DEFAULT NULL,
  `precteno` int(11) NOT NULL DEFAULT '0',
  `tisknuto` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dovednosti`
--

DROP TABLE IF EXISTS `dovednosti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dovednosti` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno` tinytext NOT NULL,
  `vlastnost` tinytext NOT NULL,
  `obtiznost` tinytext NOT NULL,
  `overovani` tinytext NOT NULL,
  `totuspech` text NOT NULL,
  `uspech` text NOT NULL,
  `neuspech` text NOT NULL,
  `fatneuspech` text NOT NULL,
  `popis` text NOT NULL,
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `zdroj` longtext,
  `zdrojmail` longtext,
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `datum` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `tisknuto` int(11) NOT NULL,
  `pochvez` varchar(5) NOT NULL,
  `pocet_hlasujicich` int(11) DEFAULT '0',
  `hodnota_hlasovani` int(11) DEFAULT '0',
  `hlasoval` text,
  `precteno` int(4) NOT NULL DEFAULT '0',
  `skupina` varchar(30) NOT NULL DEFAULT '',
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=406 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `downloady`
--

DROP TABLE IF EXISTS `downloady`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `downloady` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno` tinytext NOT NULL,
  `cesta` tinytext,
  `pochvez` varchar(5) NOT NULL,
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `datum` datetime NOT NULL DEFAULT '2001-07-04 12:00:00',
  `zdroj` tinytext,
  `zdrojmail` tinytext,
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `format` tinytext NOT NULL,
  `popis` text NOT NULL,
  `velikost` mediumint(9) NOT NULL DEFAULT '0',
  `skupina` tinytext NOT NULL,
  `pocet_hlasujicich` int(11) DEFAULT NULL,
  `hodnota_hlasovani` int(11) DEFAULT '0',
  `precteno` int(11) NOT NULL,
  `tisknuto` int(11) NOT NULL,
  `item` varchar(100) DEFAULT NULL,
  `download_counter` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=99 DEFAULT CHARSET=latin2 PACK_KEYS=0;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_acls`
--

DROP TABLE IF EXISTS `drd_reklama_acls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_acls` (
  `bannerid` mediumint(9) NOT NULL DEFAULT '0',
  `acl_con` set('and','or') NOT NULL DEFAULT '',
  `acl_type` enum('clientip','useragent','weekday','domain','source','time','language') NOT NULL DEFAULT 'clientip',
  `acl_data` varchar(255) NOT NULL DEFAULT '',
  `acl_ad` set('allow','deny') NOT NULL DEFAULT '',
  `acl_order` int(10) unsigned NOT NULL DEFAULT '0',
  UNIQUE KEY `bannerid_2` (`bannerid`,`acl_order`),
  KEY `bannerid` (`bannerid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_adclicks`
--

DROP TABLE IF EXISTS `drd_reklama_adclicks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_adclicks` (
  `bannerid` mediumint(9) NOT NULL DEFAULT '0',
  `zoneid` mediumint(9) NOT NULL DEFAULT '0',
  `t_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `host` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(50) NOT NULL DEFAULT '',
  KEY `bannerid_date` (`bannerid`,`t_stamp`),
  KEY `date` (`t_stamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_adstats`
--

DROP TABLE IF EXISTS `drd_reklama_adstats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_adstats` (
  `views` int(11) NOT NULL DEFAULT '0',
  `clicks` int(11) NOT NULL DEFAULT '0',
  `day` date NOT NULL DEFAULT '0000-00-00',
  `hour` tinyint(4) NOT NULL DEFAULT '0',
  `bannerid` smallint(6) NOT NULL DEFAULT '0',
  `zoneid` smallint(6) NOT NULL DEFAULT '0',
  `source` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`day`,`hour`,`bannerid`,`zoneid`,`source`),
  KEY `bannerid_day` (`bannerid`,`day`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_adviews`
--

DROP TABLE IF EXISTS `drd_reklama_adviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_adviews` (
  `bannerid` mediumint(9) NOT NULL DEFAULT '0',
  `zoneid` mediumint(9) NOT NULL DEFAULT '0',
  `t_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `host` varchar(255) NOT NULL DEFAULT '',
  `source` varchar(50) NOT NULL DEFAULT '',
  KEY `bannerid_date` (`bannerid`,`t_stamp`),
  KEY `date` (`t_stamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_affiliates`
--

DROP TABLE IF EXISTS `drd_reklama_affiliates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_affiliates` (
  `affiliateid` mediumint(9) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `contact` varchar(255) DEFAULT NULL,
  `email` varchar(64) NOT NULL DEFAULT '',
  `website` varchar(255) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `permissions` mediumint(9) DEFAULT NULL,
  `language` varchar(64) DEFAULT NULL,
  `publiczones` enum('t','f') NOT NULL DEFAULT 'f',
  PRIMARY KEY (`affiliateid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_banners`
--

DROP TABLE IF EXISTS `drd_reklama_banners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_banners` (
  `bannerid` mediumint(9) NOT NULL AUTO_INCREMENT,
  `clientid` mediumint(9) NOT NULL DEFAULT '0',
  `active` enum('t','f') NOT NULL DEFAULT 't',
  `priority` int(11) NOT NULL DEFAULT '0',
  `contenttype` enum('gif','jpeg','png','html','swf','dcr','rpm','mov') NOT NULL DEFAULT 'gif',
  `pluginversion` mediumint(9) NOT NULL DEFAULT '0',
  `storagetype` enum('sql','web','url','html','network') NOT NULL DEFAULT 'sql',
  `filename` varchar(255) NOT NULL DEFAULT '',
  `imageurl` varchar(255) NOT NULL DEFAULT '',
  `htmltemplate` blob NOT NULL,
  `htmlcache` blob NOT NULL,
  `width` smallint(6) NOT NULL DEFAULT '0',
  `height` smallint(6) NOT NULL DEFAULT '0',
  `weight` tinyint(4) NOT NULL DEFAULT '1',
  `seq` tinyint(4) NOT NULL DEFAULT '0',
  `target` varchar(16) NOT NULL DEFAULT '',
  `url` varchar(255) NOT NULL DEFAULT '',
  `alt` varchar(255) NOT NULL DEFAULT '',
  `status` varchar(255) NOT NULL DEFAULT '',
  `keyword` varchar(255) NOT NULL DEFAULT '',
  `bannertext` varchar(255) NOT NULL DEFAULT '',
  `description` varchar(255) NOT NULL DEFAULT '',
  `autohtml` enum('t','f') NOT NULL DEFAULT 't',
  `block` int(11) NOT NULL DEFAULT '0',
  `capping` int(11) NOT NULL DEFAULT '0',
  `compiledlimitation` blob NOT NULL,
  PRIMARY KEY (`bannerid`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_clients`
--

DROP TABLE IF EXISTS `drd_reklama_clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_clients` (
  `clientid` mediumint(9) NOT NULL AUTO_INCREMENT,
  `clientname` varchar(255) NOT NULL DEFAULT '',
  `contact` varchar(255) DEFAULT NULL,
  `email` varchar(64) NOT NULL DEFAULT '',
  `views` mediumint(9) DEFAULT NULL,
  `clicks` mediumint(9) DEFAULT NULL,
  `clientusername` varchar(64) NOT NULL DEFAULT '',
  `clientpassword` varchar(64) NOT NULL DEFAULT '',
  `expire` date DEFAULT '0000-00-00',
  `activate` date DEFAULT '0000-00-00',
  `permissions` mediumint(9) DEFAULT NULL,
  `language` varchar(64) DEFAULT NULL,
  `active` enum('t','f') NOT NULL DEFAULT 't',
  `weight` tinyint(4) NOT NULL DEFAULT '1',
  `target` int(11) NOT NULL DEFAULT '0',
  `parent` mediumint(9) NOT NULL DEFAULT '0',
  `report` enum('t','f') NOT NULL DEFAULT 't',
  `reportinterval` mediumint(9) NOT NULL DEFAULT '7',
  `reportlastdate` date NOT NULL DEFAULT '0000-00-00',
  `reportdeactivate` enum('t','f') NOT NULL DEFAULT 't',
  PRIMARY KEY (`clientid`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_config`
--

DROP TABLE IF EXISTS `drd_reklama_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_config` (
  `configid` tinyint(2) NOT NULL DEFAULT '0',
  `config_version` decimal(7,3) NOT NULL DEFAULT '0.000',
  `table_border_color` varchar(7) DEFAULT '#000099',
  `table_back_color` varchar(7) DEFAULT '#CCCCCC',
  `table_back_color_alternative` varchar(7) DEFAULT '#F7F7F7',
  `main_back_color` varchar(7) DEFAULT '#FFFFFF',
  `my_header` varchar(255) DEFAULT NULL,
  `my_footer` varchar(255) DEFAULT NULL,
  `language` varchar(32) DEFAULT 'english',
  `name` varchar(32) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT 'mysite.com',
  `override_gd_imageformat` varchar(4) DEFAULT NULL,
  `begin_of_week` tinyint(2) DEFAULT '1',
  `percentage_decimals` tinyint(2) DEFAULT '2',
  `type_sql_allow` enum('t','f') DEFAULT 't',
  `type_url_allow` enum('t','f') DEFAULT 't',
  `type_web_allow` enum('t','f') DEFAULT 'f',
  `type_html_allow` enum('t','f') DEFAULT 't',
  `type_web_mode` tinyint(2) DEFAULT '0',
  `type_web_dir` varchar(255) DEFAULT NULL,
  `type_web_ftp` varchar(255) DEFAULT NULL,
  `type_web_url` varchar(255) DEFAULT NULL,
  `admin` varchar(64) DEFAULT 'phpadsuser',
  `admin_pw` varchar(64) DEFAULT 'phpadspass',
  `admin_fullname` varchar(255) DEFAULT 'Your Name',
  `admin_email` varchar(64) DEFAULT 'your@email.com',
  `admin_email_headers` varchar(64) DEFAULT NULL,
  `admin_novice` enum('t','f') DEFAULT 't',
  `default_banner_weight` tinyint(4) DEFAULT '1',
  `default_campaign_weight` tinyint(4) DEFAULT '1',
  `client_welcome` enum('t','f') DEFAULT 't',
  `client_welcome_msg` text,
  `content_gzip_compression` enum('t','f') DEFAULT 'f',
  `userlog_email` enum('t','f') DEFAULT 't',
  `userlog_priority` enum('t','f') DEFAULT 't',
  `gui_show_campaign_info` enum('t','f') DEFAULT 't',
  `gui_show_campaign_preview` enum('t','f') DEFAULT 'f',
  `gui_show_banner_info` enum('t','f') DEFAULT 't',
  `gui_show_banner_preview` enum('t','f') DEFAULT 't',
  `gui_show_banner_html` enum('t','f') DEFAULT 'f',
  `gui_hide_inactive` enum('t','f') DEFAULT 'f',
  `qmail_patch` enum('t','f') DEFAULT 'f',
  `updates_frequency` tinyint(2) DEFAULT '7',
  `updates_timestamp` int(11) DEFAULT '0',
  `updates_last_seen` decimal(7,3) DEFAULT '0.000',
  `allow_invocation_plain` enum('t','f') DEFAULT 't',
  `allow_invocation_js` enum('t','f') DEFAULT 't',
  `allow_invocation_frame` enum('t','f') DEFAULT 't',
  `allow_invocation_xmlrpc` enum('t','f') DEFAULT 't',
  `allow_invocation_local` enum('t','f') DEFAULT 't',
  `allow_invocation_interstitial` enum('t','f') DEFAULT 't',
  `allow_invocation_popup` enum('t','f') DEFAULT 't',
  PRIMARY KEY (`configid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_images`
--

DROP TABLE IF EXISTS `drd_reklama_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_images` (
  `filename` varchar(128) NOT NULL DEFAULT '',
  `contents` mediumblob NOT NULL,
  PRIMARY KEY (`filename`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_session`
--

DROP TABLE IF EXISTS `drd_reklama_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_session` (
  `sessionid` varchar(32) NOT NULL DEFAULT '',
  `sessiondata` blob NOT NULL,
  `lastused` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sessionid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_userlog`
--

DROP TABLE IF EXISTS `drd_reklama_userlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_userlog` (
  `userlogid` mediumint(9) NOT NULL AUTO_INCREMENT,
  `timestamp` int(11) NOT NULL DEFAULT '0',
  `usertype` tinyint(4) NOT NULL DEFAULT '0',
  `userid` mediumint(9) NOT NULL DEFAULT '0',
  `action` mediumint(9) NOT NULL DEFAULT '0',
  `object` mediumint(9) DEFAULT NULL,
  `details` blob,
  PRIMARY KEY (`userlogid`)
) ENGINE=MyISAM AUTO_INCREMENT=39 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drd_reklama_zones`
--

DROP TABLE IF EXISTS `drd_reklama_zones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drd_reklama_zones` (
  `zoneid` mediumint(9) NOT NULL AUTO_INCREMENT,
  `affiliateid` mediumint(9) DEFAULT NULL,
  `zonename` varchar(245) NOT NULL DEFAULT '',
  `description` varchar(255) NOT NULL DEFAULT '',
  `delivery` smallint(6) NOT NULL DEFAULT '0',
  `zonetype` smallint(6) NOT NULL DEFAULT '0',
  `what` blob NOT NULL,
  `width` smallint(6) NOT NULL DEFAULT '0',
  `height` smallint(6) NOT NULL DEFAULT '0',
  `cachecontents` mediumblob,
  `cachetimestamp` int(11) NOT NULL DEFAULT '0',
  `chain` blob NOT NULL,
  `append` blob NOT NULL,
  PRIMARY KEY (`zoneid`),
  KEY `zonenameid` (`zonename`,`zoneid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `duchovo`
--

DROP TABLE IF EXISTS `duchovo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `duchovo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datum` int(12) NOT NULL DEFAULT '1',
  `param` varchar(15) NOT NULL DEFAULT 'nic',
  `value` tinytext,
  PRIMARY KEY (`id`),
  KEY `datum` (`datum`,`param`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `duchovo1`
--

DROP TABLE IF EXISTS `duchovo1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `duchovo1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datum` int(12) NOT NULL DEFAULT '1',
  `param` varchar(15) NOT NULL DEFAULT 'nic',
  `value` tinytext,
  PRIMARY KEY (`id`),
  KEY `datum` (`datum`,`param`)
) ENGINE=MyISAM AUTO_INCREMENT=885 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forum`
--

DROP TABLE IF EXISTS `forum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forum` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `nickname` varchar(64) NOT NULL DEFAULT '',
  `email` tinytext,
  `datum` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `text` text NOT NULL,
  `reg` varchar(50) NOT NULL DEFAULT '0',
  `reputace` tinyint(4) NOT NULL DEFAULT '0',
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_user_id_d33ebc1a` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=40132 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forum_bck_2006_7_19`
--

DROP TABLE IF EXISTS `forum_bck_2006_7_19`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forum_bck_2006_7_19` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `nickname` tinytext NOT NULL,
  `email` tinytext,
  `datum` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `text` text NOT NULL,
  `reg` varchar(50) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=24051 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forums`
--

DROP TABLE IF EXISTS `forums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forums` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(50) NOT NULL DEFAULT '',
  `active` smallint(6) NOT NULL DEFAULT '0',
  `description` char(255) NOT NULL DEFAULT '',
  `config_suffix` char(50) NOT NULL DEFAULT '',
  `folder` char(1) NOT NULL DEFAULT '0',
  `parent` int(11) NOT NULL DEFAULT '0',
  `display` int(10) unsigned NOT NULL DEFAULT '0',
  `table_name` char(50) NOT NULL DEFAULT '',
  `moderation` char(1) NOT NULL DEFAULT 'n',
  `email_list` char(50) NOT NULL DEFAULT '',
  `email_return` char(50) NOT NULL DEFAULT '',
  `email_tag` char(50) NOT NULL DEFAULT '',
  `check_dup` smallint(5) unsigned NOT NULL DEFAULT '0',
  `multi_level` smallint(5) unsigned NOT NULL DEFAULT '0',
  `collapse` smallint(5) unsigned NOT NULL DEFAULT '0',
  `flat` smallint(5) unsigned NOT NULL DEFAULT '0',
  `lang` char(50) NOT NULL DEFAULT '',
  `html` char(40) NOT NULL DEFAULT 'N',
  `table_width` char(4) NOT NULL DEFAULT '',
  `table_header_color` char(7) NOT NULL DEFAULT '',
  `table_header_font_color` char(7) NOT NULL DEFAULT '',
  `table_body_color_1` char(7) NOT NULL DEFAULT '',
  `table_body_color_2` char(7) NOT NULL DEFAULT '',
  `table_body_font_color_1` char(7) NOT NULL DEFAULT '',
  `table_body_font_color_2` char(7) NOT NULL DEFAULT '',
  `nav_color` char(7) NOT NULL DEFAULT '',
  `nav_font_color` char(7) NOT NULL DEFAULT '',
  `allow_uploads` char(1) NOT NULL DEFAULT 'N',
  `upload_types` char(100) NOT NULL DEFAULT '',
  `upload_size` int(10) unsigned NOT NULL DEFAULT '0',
  `max_uploads` int(10) unsigned NOT NULL DEFAULT '0',
  `security` int(10) unsigned NOT NULL DEFAULT '0',
  `showip` smallint(5) unsigned NOT NULL DEFAULT '1',
  `emailnotification` smallint(5) unsigned NOT NULL DEFAULT '0',
  `body_color` char(7) NOT NULL DEFAULT '',
  `body_link_color` char(7) NOT NULL DEFAULT '',
  `body_alink_color` char(7) NOT NULL DEFAULT '',
  `body_vlink_color` char(7) NOT NULL DEFAULT '',
  `required_level` smallint(6) NOT NULL DEFAULT '0',
  `permissions` smallint(6) NOT NULL DEFAULT '0',
  `allow_edit` smallint(6) NOT NULL DEFAULT '1',
  `allow_langsel` smallint(6) NOT NULL DEFAULT '0',
  `displayflag` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `active` (`active`),
  KEY `parent` (`parent`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forums_auth`
--

DROP TABLE IF EXISTS `forums_auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forums_auth` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `username` varchar(50) NOT NULL DEFAULT '',
  `password` varchar(50) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `webpage` varchar(200) NOT NULL DEFAULT '',
  `image` varchar(200) NOT NULL DEFAULT '',
  `icq` varchar(50) NOT NULL DEFAULT '',
  `aol` varchar(50) NOT NULL DEFAULT '',
  `yahoo` varchar(50) NOT NULL DEFAULT '',
  `msn` varchar(50) NOT NULL DEFAULT '',
  `jabber` varchar(50) NOT NULL DEFAULT '',
  `signature` varchar(255) NOT NULL DEFAULT '',
  `max_group_permission_level` int(10) unsigned NOT NULL DEFAULT '0',
  `permission_level` int(10) unsigned NOT NULL DEFAULT '0',
  `hide_email` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `lang` varchar(50) NOT NULL DEFAULT '',
  `password_tmp` varchar(50) NOT NULL DEFAULT '',
  `combined_token` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `username` (`username`),
  KEY `password` (`password`),
  KEY `userpass` (`username`,`password`)
) ENGINE=MyISAM AUTO_INCREMENT=934 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forums_forum2group`
--

DROP TABLE IF EXISTS `forums_forum2group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forums_forum2group` (
  `forum_id` int(10) unsigned NOT NULL DEFAULT '0',
  `group_id` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`group_id`,`forum_id`),
  KEY `forum_id` (`forum_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forums_groups`
--

DROP TABLE IF EXISTS `forums_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forums_groups` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `permission_level` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forums_moderators`
--

DROP TABLE IF EXISTS `forums_moderators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forums_moderators` (
  `user_id` int(10) unsigned NOT NULL DEFAULT '0',
  `forum_id` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`,`forum_id`),
  KEY `forum_id` (`forum_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fotogalerie`
--

DROP TABLE IF EXISTS `fotogalerie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fotogalerie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jmeno` tinytext NOT NULL,
  `cesta` tinytext NOT NULL,
  `pochvez` varchar(5) NOT NULL,
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `datum` datetime NOT NULL DEFAULT '2001-07-04 12:00:00',
  `zdroj` tinytext,
  `zdrojmail` longtext,
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `cestathumb` tinytext NOT NULL,
  `hodnota_hlasovani` int(11) DEFAULT NULL,
  `pocet_hlasujicich` int(11) DEFAULT NULL,
  `precteno` int(11) NOT NULL,
  `tisknuto` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=42 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `galerie`
--

DROP TABLE IF EXISTS `galerie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `galerie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jmeno` tinytext NOT NULL,
  `cesta` tinytext NOT NULL,
  `pochvez` varchar(5) NOT NULL,
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `datum` datetime NOT NULL DEFAULT '2001-07-04 12:00:00',
  `zdroj` tinytext,
  `zdrojmail` longtext,
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `cestathumb` tinytext NOT NULL,
  `hodnota_hlasovani` int(11) DEFAULT NULL,
  `pocet_hlasujicich` int(11) DEFAULT NULL,
  `precteno` int(11) NOT NULL,
  `tisknuto` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=972 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `grouplimits`
--

DROP TABLE IF EXISTS `grouplimits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grouplimits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_uz` int(11) NOT NULL DEFAULT '0',
  `max_soukr` smallint(6) DEFAULT '-1',
  `max_verej` smallint(6) DEFAULT '-1',
  PRIMARY KEY (`id`),
  KEY `id_uz` (`id_uz`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin2 COMMENT='Pokud ma nektery uzivatel dostat vyjimku pro zalozeni mailgr';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `groupmembers`
--

DROP TABLE IF EXISTS `groupmembers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groupmembers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_skupiny` int(11) NOT NULL DEFAULT '0',
  `id_uz` int(11) NOT NULL DEFAULT '0',
  `clenstvi` mediumint(9) DEFAULT '0',
  `caszmeny` datetime DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `id_skupiny` (`id_skupiny`,`id_uz`)
) ENGINE=MyISAM AUTO_INCREMENT=1040 DEFAULT CHARSET=latin2 COMMENT='10spr/7akt/6pas/5pozv.zad/4pozv/3zad/2pozv.zrus/1zakaz';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hlasovani_prispevky`
--

DROP TABLE IF EXISTS `hlasovani_prispevky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hlasovani_prispevky` (
  `id_uz` int(11) NOT NULL DEFAULT '0',
  `id_cizi` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(20) NOT NULL DEFAULT '',
  `pochvez` tinyint(4) NOT NULL DEFAULT '0',
  `time` int(11) NOT NULL DEFAULT '0',
  `opraveno` enum('0','1') NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_uz`,`id_cizi`,`rubrika`),
  UNIQUE KEY `hlasovani_prispevky_id_uz_id_cizi_rubrika_37c0d5f7_uniq` (`id_uz`,`id_cizi`,`rubrika`),
  KEY `opraveno` (`opraveno`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hranicarkouzla`
--

DROP TABLE IF EXISTS `hranicarkouzla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hranicarkouzla` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno` tinytext NOT NULL,
  `mag` smallint(4) NOT NULL DEFAULT '0',
  `magpop` tinytext NOT NULL,
  `dosah` smallint(4) DEFAULT NULL,
  `dosahpop` tinytext,
  `rozsah` smallint(4) DEFAULT NULL,
  `rozsahpop` tinytext,
  `vyvolani` smallint(4) DEFAULT NULL,
  `vyvolanipop` tinytext,
  `druh` tinytext,
  `skupina` tinytext NOT NULL,
  `cetnost` tinytext,
  `pomucky` tinytext,
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `zdroj` tinytext,
  `zdrojmail` tinytext,
  `schvaleno` char(1) NOT NULL DEFAULT '',
  `datum` datetime NOT NULL DEFAULT '2001-09-09 12:48:26',
  `pochvez` varchar(5) NOT NULL,
  `popis` text NOT NULL,
  `tisknuto` mediumint(3) NOT NULL DEFAULT '0',
  `pocet_hlasujicich` int(11) DEFAULT NULL,
  `hodnota_hlasovani` int(11) DEFAULT '0',
  `precteno` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=241 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inzerce`
--

DROP TABLE IF EXISTS `inzerce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inzerce` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sekce` varchar(20) NOT NULL DEFAULT '',
  `jmeno` varchar(30) DEFAULT NULL,
  `mail` varchar(30) DEFAULT NULL,
  `telefon` varchar(15) DEFAULT NULL,
  `mobil` varchar(15) DEFAULT NULL,
  `okres` varchar(20) DEFAULT NULL,
  `text` text NOT NULL,
  `datum` varchar(12) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1261 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ips2log`
--

DROP TABLE IF EXISTS `ips2log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ips2log` (
  `ip` varchar(15) NOT NULL DEFAULT '',
  PRIMARY KEY (`ip`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kouzla`
--

DROP TABLE IF EXISTS `kouzla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kouzla` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno` tinytext NOT NULL,
  `kouzsl` tinytext NOT NULL,
  `mag` smallint(6) NOT NULL DEFAULT '0',
  `magpop` tinytext NOT NULL,
  `past` tinytext,
  `dosah` tinyint(4) DEFAULT NULL,
  `dosahpop` tinytext,
  `rozsah` tinyint(4) NOT NULL DEFAULT '0',
  `rozsahpop` tinytext,
  `vyvolani` tinyint(4) NOT NULL DEFAULT '0',
  `vyvolanipop` tinytext NOT NULL,
  `trvani` tinyint(4) NOT NULL DEFAULT '0',
  `trvanipop` tinytext,
  `popis` text NOT NULL,
  `skupina` tinytext NOT NULL,
  `pochvez` varchar(5) NOT NULL,
  `datum` datetime NOT NULL DEFAULT '2001-08-08 13:28:01',
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `zdroj` tinytext,
  `zdrojmail` tinytext,
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `tisknuto` int(11) NOT NULL,
  `pocet_hlasujicich` int(11) DEFAULT NULL,
  `hodnota_hlasovani` int(11) DEFAULT '0',
  `precteno` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=933 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `level_parametry_2`
--

DROP TABLE IF EXISTS `level_parametry_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `level_parametry_2` (
  `parametr` varchar(40) NOT NULL,
  `hodnota` varchar(30) NOT NULL,
  PRIMARY KEY (`parametr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `limity`
--

DROP TABLE IF EXISTS `limity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `limity` (
  `oprava_hlasovani_po` int(10) unsigned NOT NULL DEFAULT '10800',
  `platnost` enum('a','n') NOT NULL DEFAULT 'n',
  `oprava_hlasovani_pred` int(11) NOT NULL DEFAULT '172800',
  `platnost_limitu_pred` enum('a','n') NOT NULL DEFAULT 'n',
  PRIMARY KEY (`oprava_hlasovani_po`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `linky`
--

DROP TABLE IF EXISTS `linky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `linky` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nazev` tinytext NOT NULL,
  `adresa` tinytext NOT NULL,
  `popis` text NOT NULL,
  `pochvez` char(1) NOT NULL DEFAULT '',
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `datum` datetime NOT NULL DEFAULT '2001-10-08 15:45:31',
  `pocet_hlasujicich` int(11) DEFAULT NULL,
  `hodnota_hlasovani` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=148 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `logged_aliens`
--

DROP TABLE IF EXISTS `logged_aliens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logged_aliens` (
  `nick` varchar(40) NOT NULL DEFAULT '',
  `ip` varchar(15) NOT NULL DEFAULT '',
  `psw` varchar(40) NOT NULL DEFAULT '',
  `time` int(11) NOT NULL DEFAULT '0',
  KEY `ip` (`ip`),
  KEY `nick` (`nick`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mailgroups`
--

DROP TABLE IF EXISTS `mailgroups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailgroups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `verejna` set('0','1') NOT NULL DEFAULT '0',
  `nazev_skupiny` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nazev_skupiny` (`nazev_skupiny`),
  KEY `verejna` (`verejna`)
) ENGINE=MyISAM AUTO_INCREMENT=108 DEFAULT CHARSET=latin2 COMMENT='Seznam vsech skupin';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `maillist_ceka`
--

DROP TABLE IF EXISTS `maillist_ceka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maillist_ceka` (
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `data` text NOT NULL,
  `dataplain` text NOT NULL,
  `datum` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  KEY `RUBRIKA` (`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mentat_newbie`
--

DROP TABLE IF EXISTS `mentat_newbie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mentat_newbie` (
  `newbie_id` int(11) NOT NULL DEFAULT '0',
  `mentat_id` int(11) NOT NULL DEFAULT '0',
  `newbie_rate` tinyint(4) NOT NULL DEFAULT '0',
  `mentat_rate` tinyint(4) NOT NULL DEFAULT '0',
  `locked` enum('-1','0','1') NOT NULL DEFAULT '0',
  `penalty` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`newbie_id`,`mentat_id`),
  KEY `penalty` (`penalty`),
  KEY `mentat_id` (`mentat_id`),
  KEY `newbie_rate` (`newbie_rate`),
  KEY `mentat_rate` (`mentat_rate`),
  KEY `locked` (`locked`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mentats_avail`
--

DROP TABLE IF EXISTS `mentats_avail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mentats_avail` (
  `user_id` int(11) NOT NULL DEFAULT '0',
  `intro_m` text NOT NULL,
  `intro_z` text NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_dilna`
--

DROP TABLE IF EXISTS `ms_dilna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_dilna` (
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `datestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  `parent` int(10) unsigned NOT NULL DEFAULT '0',
  `author` varchar(37) NOT NULL DEFAULT '',
  `subject` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `host` varchar(255) NOT NULL DEFAULT '',
  `email_reply` char(1) NOT NULL DEFAULT 'N',
  `approved` char(1) NOT NULL DEFAULT 'N',
  `msgid` varchar(100) NOT NULL DEFAULT '',
  `modifystamp` int(10) unsigned NOT NULL DEFAULT '0',
  `userid` int(10) unsigned NOT NULL DEFAULT '0',
  `closed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  KEY `datestamp` (`datestamp`),
  KEY `subject` (`subject`),
  KEY `thread` (`thread`),
  KEY `parent` (`parent`),
  KEY `approved` (`approved`),
  KEY `msgid` (`msgid`),
  KEY `modifystamp` (`modifystamp`),
  KEY `userid` (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_dilna_attachments`
--

DROP TABLE IF EXISTS `ms_dilna_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_dilna_attachments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `message_id` int(10) unsigned NOT NULL DEFAULT '0',
  `filename` char(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`message_id`),
  KEY `lookup` (`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_dilna_bodies`
--

DROP TABLE IF EXISTS `ms_dilna_bodies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_dilna_bodies` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `body` text NOT NULL,
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `thread` (`thread`)
) ENGINE=MyISAM AUTO_INCREMENT=34752 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_dracidoupecz`
--

DROP TABLE IF EXISTS `ms_dracidoupecz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_dracidoupecz` (
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `datestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  `parent` int(10) unsigned NOT NULL DEFAULT '0',
  `author` varchar(37) NOT NULL DEFAULT '',
  `subject` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `host` varchar(255) NOT NULL DEFAULT '',
  `email_reply` char(1) NOT NULL DEFAULT 'N',
  `approved` char(1) NOT NULL DEFAULT 'N',
  `msgid` varchar(100) NOT NULL DEFAULT '',
  `modifystamp` int(10) unsigned NOT NULL DEFAULT '0',
  `userid` int(10) unsigned NOT NULL DEFAULT '0',
  `closed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  KEY `userid` (`userid`),
  KEY `datestamp` (`datestamp`),
  KEY `subject` (`subject`),
  KEY `thread` (`thread`),
  KEY `parent` (`parent`),
  KEY `approved` (`approved`),
  KEY `msgid` (`msgid`),
  KEY `modifystamp` (`modifystamp`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_dracidoupecz_bodies`
--

DROP TABLE IF EXISTS `ms_dracidoupecz_bodies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_dracidoupecz_bodies` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `body` text NOT NULL,
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `thread` (`thread`)
) ENGINE=MyISAM AUTO_INCREMENT=2085 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_galerie_dilna`
--

DROP TABLE IF EXISTS `ms_galerie_dilna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_galerie_dilna` (
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `datestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  `parent` int(10) unsigned NOT NULL DEFAULT '0',
  `author` varchar(37) NOT NULL DEFAULT '',
  `subject` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `host` varchar(255) NOT NULL DEFAULT '',
  `email_reply` char(1) NOT NULL DEFAULT 'N',
  `approved` char(1) NOT NULL DEFAULT 'N',
  `msgid` varchar(100) NOT NULL DEFAULT '',
  `modifystamp` int(10) unsigned NOT NULL DEFAULT '0',
  `userid` int(10) unsigned NOT NULL DEFAULT '0',
  `closed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  KEY `datestamp` (`datestamp`),
  KEY `subject` (`subject`),
  KEY `thread` (`thread`),
  KEY `parent` (`parent`),
  KEY `approved` (`approved`),
  KEY `msgid` (`msgid`),
  KEY `modifystamp` (`modifystamp`),
  KEY `userid` (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_galerie_dilna_attachments`
--

DROP TABLE IF EXISTS `ms_galerie_dilna_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_galerie_dilna_attachments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `message_id` int(10) unsigned NOT NULL DEFAULT '0',
  `filename` char(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`message_id`),
  KEY `lookup` (`message_id`)
) ENGINE=MyISAM AUTO_INCREMENT=266 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_galerie_dilna_bodies`
--

DROP TABLE IF EXISTS `ms_galerie_dilna_bodies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_galerie_dilna_bodies` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `body` text NOT NULL,
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `thread` (`thread`)
) ENGINE=MyISAM AUTO_INCREMENT=657 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_htmldilna`
--

DROP TABLE IF EXISTS `ms_htmldilna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_htmldilna` (
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `datestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  `parent` int(10) unsigned NOT NULL DEFAULT '0',
  `author` varchar(37) NOT NULL DEFAULT '',
  `subject` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `host` varchar(255) NOT NULL DEFAULT '',
  `email_reply` char(1) NOT NULL DEFAULT 'N',
  `approved` char(1) NOT NULL DEFAULT 'N',
  `msgid` varchar(100) NOT NULL DEFAULT '',
  `modifystamp` int(10) unsigned NOT NULL DEFAULT '0',
  `userid` int(10) unsigned NOT NULL DEFAULT '0',
  `closed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  KEY `datestamp` (`datestamp`),
  KEY `subject` (`subject`),
  KEY `thread` (`thread`),
  KEY `parent` (`parent`),
  KEY `approved` (`approved`),
  KEY `msgid` (`msgid`),
  KEY `modifystamp` (`modifystamp`),
  KEY `userid` (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_htmldilna_attachments`
--

DROP TABLE IF EXISTS `ms_htmldilna_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_htmldilna_attachments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `message_id` int(10) unsigned NOT NULL DEFAULT '0',
  `filename` char(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`message_id`),
  KEY `lookup` (`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_htmldilna_bodies`
--

DROP TABLE IF EXISTS `ms_htmldilna_bodies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_htmldilna_bodies` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `body` text NOT NULL,
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `thread` (`thread`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_ostatni`
--

DROP TABLE IF EXISTS `ms_ostatni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_ostatni` (
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `datestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  `parent` int(10) unsigned NOT NULL DEFAULT '0',
  `author` varchar(37) NOT NULL DEFAULT '',
  `subject` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `host` varchar(255) NOT NULL DEFAULT '',
  `email_reply` char(1) NOT NULL DEFAULT 'N',
  `approved` char(1) NOT NULL DEFAULT 'N',
  `msgid` varchar(100) NOT NULL DEFAULT '',
  `modifystamp` int(10) unsigned NOT NULL DEFAULT '0',
  `userid` int(10) unsigned NOT NULL DEFAULT '0',
  `closed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  KEY `datestamp` (`datestamp`),
  KEY `subject` (`subject`),
  KEY `thread` (`thread`),
  KEY `parent` (`parent`),
  KEY `approved` (`approved`),
  KEY `msgid` (`msgid`),
  KEY `modifystamp` (`modifystamp`),
  KEY `userid` (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_ostatni_attachments`
--

DROP TABLE IF EXISTS `ms_ostatni_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_ostatni_attachments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `message_id` int(10) unsigned NOT NULL DEFAULT '0',
  `filename` char(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`message_id`),
  KEY `lookup` (`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_ostatni_bodies`
--

DROP TABLE IF EXISTS `ms_ostatni_bodies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_ostatni_bodies` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `body` text NOT NULL,
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `thread` (`thread`)
) ENGINE=MyISAM AUTO_INCREMENT=3583 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_pj`
--

DROP TABLE IF EXISTS `ms_pj`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_pj` (
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `datestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  `parent` int(10) unsigned NOT NULL DEFAULT '0',
  `author` varchar(37) NOT NULL DEFAULT '',
  `subject` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `host` varchar(255) NOT NULL DEFAULT '',
  `email_reply` char(1) NOT NULL DEFAULT 'N',
  `approved` char(1) NOT NULL DEFAULT 'N',
  `msgid` varchar(100) NOT NULL DEFAULT '',
  `modifystamp` int(10) unsigned NOT NULL DEFAULT '0',
  `userid` int(10) unsigned NOT NULL DEFAULT '0',
  `closed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  KEY `datestamp` (`datestamp`),
  KEY `subject` (`subject`),
  KEY `thread` (`thread`),
  KEY `parent` (`parent`),
  KEY `approved` (`approved`),
  KEY `msgid` (`msgid`),
  KEY `modifystamp` (`modifystamp`),
  KEY `userid` (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_pj_attachments`
--

DROP TABLE IF EXISTS `ms_pj_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_pj_attachments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `message_id` int(10) unsigned NOT NULL DEFAULT '0',
  `filename` char(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`message_id`),
  KEY `lookup` (`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_pj_bodies`
--

DROP TABLE IF EXISTS `ms_pj_bodies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_pj_bodies` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `body` text NOT NULL,
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `thread` (`thread`)
) ENGINE=MyISAM AUTO_INCREMENT=4192 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_pravidla`
--

DROP TABLE IF EXISTS `ms_pravidla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_pravidla` (
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `datestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  `parent` int(10) unsigned NOT NULL DEFAULT '0',
  `author` varchar(37) NOT NULL DEFAULT '',
  `subject` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `host` varchar(255) NOT NULL DEFAULT '',
  `email_reply` char(1) NOT NULL DEFAULT 'N',
  `approved` char(1) NOT NULL DEFAULT 'N',
  `msgid` varchar(100) NOT NULL DEFAULT '',
  `modifystamp` int(10) unsigned NOT NULL DEFAULT '0',
  `userid` int(10) unsigned NOT NULL DEFAULT '0',
  `closed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  KEY `datestamp` (`datestamp`),
  KEY `subject` (`subject`),
  KEY `thread` (`thread`),
  KEY `parent` (`parent`),
  KEY `approved` (`approved`),
  KEY `msgid` (`msgid`),
  KEY `modifystamp` (`modifystamp`),
  KEY `userid` (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_pravidla_attachments`
--

DROP TABLE IF EXISTS `ms_pravidla_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_pravidla_attachments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `message_id` int(10) unsigned NOT NULL DEFAULT '0',
  `filename` char(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`message_id`),
  KEY `lookup` (`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_pravidla_bodies`
--

DROP TABLE IF EXISTS `ms_pravidla_bodies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_pravidla_bodies` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `body` text NOT NULL,
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `thread` (`thread`)
) ENGINE=MyISAM AUTO_INCREMENT=2646 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_ring`
--

DROP TABLE IF EXISTS `ms_ring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_ring` (
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `datestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  `parent` int(10) unsigned NOT NULL DEFAULT '0',
  `author` varchar(37) NOT NULL DEFAULT '',
  `subject` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `host` varchar(255) NOT NULL DEFAULT '',
  `email_reply` char(1) NOT NULL DEFAULT 'N',
  `approved` char(1) NOT NULL DEFAULT 'N',
  `msgid` varchar(100) NOT NULL DEFAULT '',
  `modifystamp` int(10) unsigned NOT NULL DEFAULT '0',
  `userid` int(10) unsigned NOT NULL DEFAULT '0',
  `closed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  KEY `datestamp` (`datestamp`),
  KEY `subject` (`subject`),
  KEY `thread` (`thread`),
  KEY `parent` (`parent`),
  KEY `approved` (`approved`),
  KEY `msgid` (`msgid`),
  KEY `modifystamp` (`modifystamp`),
  KEY `userid` (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_ring_attachments`
--

DROP TABLE IF EXISTS `ms_ring_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_ring_attachments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `message_id` int(10) unsigned NOT NULL DEFAULT '0',
  `filename` char(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`message_id`),
  KEY `lookup` (`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_ring_bodies`
--

DROP TABLE IF EXISTS `ms_ring_bodies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_ring_bodies` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `body` text NOT NULL,
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `thread` (`thread`)
) ENGINE=MyISAM AUTO_INCREMENT=1182 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_roleplaying`
--

DROP TABLE IF EXISTS `ms_roleplaying`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_roleplaying` (
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `datestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  `parent` int(10) unsigned NOT NULL DEFAULT '0',
  `author` varchar(37) NOT NULL DEFAULT '',
  `subject` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `host` varchar(255) NOT NULL DEFAULT '',
  `email_reply` char(1) NOT NULL DEFAULT 'N',
  `approved` char(1) NOT NULL DEFAULT 'N',
  `msgid` varchar(100) NOT NULL DEFAULT '',
  `modifystamp` int(10) unsigned NOT NULL DEFAULT '0',
  `userid` int(10) unsigned NOT NULL DEFAULT '0',
  `closed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  KEY `datestamp` (`datestamp`),
  KEY `subject` (`subject`),
  KEY `thread` (`thread`),
  KEY `parent` (`parent`),
  KEY `approved` (`approved`),
  KEY `msgid` (`msgid`),
  KEY `modifystamp` (`modifystamp`),
  KEY `userid` (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_roleplaying_attachments`
--

DROP TABLE IF EXISTS `ms_roleplaying_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_roleplaying_attachments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `message_id` int(10) unsigned NOT NULL DEFAULT '0',
  `filename` char(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`,`message_id`),
  KEY `lookup` (`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_roleplaying_bodies`
--

DROP TABLE IF EXISTS `ms_roleplaying_bodies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_roleplaying_bodies` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `body` text NOT NULL,
  `thread` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `thread` (`thread`)
) ENGINE=MyISAM AUTO_INCREMENT=1943 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `navstevnost`
--

DROP TABLE IF EXISTS `navstevnost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `navstevnost` (
  `ip` varchar(16) NOT NULL DEFAULT '',
  `naposled` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ip`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pokus`
--

DROP TABLE IF EXISTS `pokus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pokus` (
  `a` int(11) NOT NULL AUTO_INCREMENT,
  `b` int(11) NOT NULL DEFAULT '5',
  `c` int(11) NOT NULL DEFAULT '10',
  PRIMARY KEY (`a`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pomocnici`
--

DROP TABLE IF EXISTS `pomocnici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pomocnici` (
  `id_zaznamu` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_pomocnika` int(10) unsigned NOT NULL DEFAULT '0',
  `nick_pomocnika` varchar(25) NOT NULL DEFAULT '',
  `nazev_dila` varchar(50) DEFAULT NULL,
  UNIQUE KEY `id_zaznamu` (`id_zaznamu`),
  KEY `id_pomocnika` (`id_pomocnika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `posta`
--

DROP TABLE IF EXISTS `posta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `posta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `odesilatel` varchar(25) NOT NULL DEFAULT '',
  `prijemce` varchar(25) NOT NULL DEFAULT '',
  `viditelnost` char(1) NOT NULL DEFAULT '3',
  `text` text NOT NULL,
  `datum` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `datum` (`datum`,`odesilatel`,`prijemce`,`viditelnost`)
) ENGINE=MyISAM AUTO_INCREMENT=359691 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pravomoci`
--

DROP TABLE IF EXISTS `pravomoci`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pravomoci` (
  `id_user` int(11) NOT NULL DEFAULT '0',
  `funkce` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT '',
  `stupen` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_user`,`funkce`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Zapsanim uzivatele sem mu poskytnu urcite pravomoci';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `predmety`
--

DROP TABLE IF EXISTS `predmety`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `predmety` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno` text NOT NULL,
  `UC` tinytext,
  `KZ` char(3) DEFAULT NULL,
  `delka` char(3) DEFAULT NULL,
  `cena` int(20) NOT NULL DEFAULT '0',
  `popis` text NOT NULL,
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `datum` datetime NOT NULL DEFAULT '2001-08-08 15:45:34',
  `pochvez` varchar(5) NOT NULL,
  `malydostrel` tinyint(4) DEFAULT '0',
  `strednidostrel` tinyint(4) DEFAULT '0',
  `velkydostrel` tinyint(4) DEFAULT '0',
  `sfera` tinyint(4) DEFAULT '0',
  `vaha` int(11) NOT NULL DEFAULT '0',
  `zdroj` tinytext,
  `zdrojmail` tinytext,
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `skupina` tinytext NOT NULL,
  `tisknuto` int(11) NOT NULL,
  `pocet_hlasujicich` int(11) DEFAULT NULL,
  `hodnota_hlasovani` int(11) DEFAULT '0',
  `precteno` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1904 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prispevky_dlouhe`
--

DROP TABLE IF EXISTS `prispevky_dlouhe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prispevky_dlouhe` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno` tinytext NOT NULL,
  `text` longtext NOT NULL,
  `autor` varchar(50) DEFAULT NULL,
  `autmail` varchar(50) DEFAULT NULL,
  `datum` datetime NOT NULL DEFAULT '2001-08-08 22:35:48',
  `schvaleno` char(1) NOT NULL DEFAULT 'n',
  `zdroj` tinytext,
  `zdrojmail` longtext,
  `pocet_hlasujicich` int(11) DEFAULT '0',
  `hodnota_hlasovani` int(11) DEFAULT '0',
  `pochvez` varchar(5) NOT NULL DEFAULT '0',
  `precteno` int(11) NOT NULL DEFAULT '0',
  `tisknuto` mediumint(9) NOT NULL DEFAULT '0',
  `skupina` varchar(30) DEFAULT NULL,
  `anotace` tinytext,
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `RUBRIKA` (`rubrika`),
  KEY `SCHVALENO` (`schvaleno`),
  KEY `SKUPINA` (`skupina`)
) ENGINE=MyISAM AUTO_INCREMENT=4647 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `psi_smecka`
--

DROP TABLE IF EXISTS `psi_smecka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `psi_smecka` (
  `id_uz` int(11) NOT NULL DEFAULT '0',
  `cizi_tbl` varchar(20) NOT NULL DEFAULT '',
  `id_dilo` int(11) NOT NULL DEFAULT '0',
  `navstiveno` int(11) NOT NULL DEFAULT '0',
  `neprectenych` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_uz`,`cizi_tbl`,`id_dilo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_book`
--

DROP TABLE IF EXISTS `putyka_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_book` (
  `id_stolu` mediumint(9) NOT NULL DEFAULT '0',
  `id_uz` mediumint(9) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_stolu`,`id_uz`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_linky`
--

DROP TABLE IF EXISTS `putyka_linky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_linky` (
  `id_stolu` int(11) NOT NULL DEFAULT '0',
  `id_linku` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_stolu`,`id_linku`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2 COMMENT='Linky mezi stoly v Putyce';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_nastenky`
--

DROP TABLE IF EXISTS `putyka_nastenky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_nastenky` (
  `id_stolu` int(11) NOT NULL DEFAULT '0',
  `nazev_stolu` varchar(128) NOT NULL DEFAULT '',
  `text_nastenky` mediumtext NOT NULL,
  `posledni_zmena` datetime DEFAULT '0000-00-00 00:00:00',
  `zmenil` varchar(25) NOT NULL DEFAULT '',
  UNIQUE KEY `id_stolu` (`id_stolu`),
  KEY `nazev_stolu` (`nazev_stolu`,`posledni_zmena`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2 COMMENT='Obsahuje nastenky stolu v Putyce. Edituje Admin, cte kdokoli';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_navstevnost`
--

DROP TABLE IF EXISTS `putyka_navstevnost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_navstevnost` (
  `cas` datetime NOT NULL,
  `misto` varchar(31) NOT NULL,
  `pocet` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`cas`,`misto`),
  KEY `misto_cas` (`misto`,`cas`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_neoblibene`
--

DROP TABLE IF EXISTS `putyka_neoblibene`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_neoblibene` (
  `id_uz` int(11) NOT NULL DEFAULT '0',
  `id_stolu` int(11) NOT NULL DEFAULT '0',
  KEY `id_uz` (`id_uz`,`id_stolu`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_prispevky`
--

DROP TABLE IF EXISTS `putyka_prispevky`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_prispevky` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `id_stolu` int(11) NOT NULL DEFAULT '0',
  `text` text NOT NULL,
  `autor` varchar(30) NOT NULL DEFAULT '',
  `reputace` tinyint(4) NOT NULL DEFAULT '0',
  `datum` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `STUL` (`id_stolu`),
  KEY `AUTOR` (`autor`),
  KEY `DATUM` (`datum`)
) ENGINE=MyISAM AUTO_INCREMENT=536185 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_pristup`
--

DROP TABLE IF EXISTS `putyka_pristup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_pristup` (
  `id_stolu` int(11) NOT NULL DEFAULT '0',
  `typ_pristupu` varchar(5) NOT NULL DEFAULT '',
  `nick_usera` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_stolu`,`typ_pristupu`,`nick_usera`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_sekce`
--

DROP TABLE IF EXISTS `putyka_sekce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_sekce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kod` int(11) NOT NULL DEFAULT '0',
  `poradi` int(11) NOT NULL DEFAULT '0',
  `nazev` varchar(50) NOT NULL DEFAULT '',
  `popis` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `kod` (`kod`,`poradi`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_slucovani`
--

DROP TABLE IF EXISTS `putyka_slucovani`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_slucovani` (
  `id_ja` int(11) NOT NULL DEFAULT '0',
  `id_on` int(11) NOT NULL DEFAULT '0',
  `zustavam` smallint(6) NOT NULL DEFAULT '0',
  `oznaceni` varchar(60) NOT NULL DEFAULT '',
  KEY `id_ja` (`id_ja`,`id_on`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2 COMMENT='Ktery stul s kterym sloucit';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_stoly`
--

DROP TABLE IF EXISTS `putyka_stoly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_stoly` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno` varchar(255) CHARACTER SET latin2 NOT NULL,
  `popis` varchar(255) CHARACTER SET latin2 NOT NULL DEFAULT '',
  `vlastnik` varchar(30) CHARACTER SET latin2 NOT NULL DEFAULT '',
  `povol_hodnoceni` char(1) CHARACTER SET latin2 NOT NULL DEFAULT '0',
  `min_level` char(1) CHARACTER SET latin2 NOT NULL DEFAULT '0',
  `zalozen` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `verejny` char(1) CHARACTER SET latin2 NOT NULL DEFAULT '1',
  `celkem` int(11) DEFAULT NULL,
  `sekce` int(11) NOT NULL DEFAULT '3',
  PRIMARY KEY (`id`),
  UNIQUE KEY `JMENO` (`jmeno`),
  KEY `VLASTNIK` (`vlastnik`),
  KEY `VEREJNY` (`verejny`),
  KEY `celkem` (`celkem`)
) ENGINE=MyISAM AUTO_INCREMENT=2550 DEFAULT CHARSET=latin2 COLLATE=latin2_czech_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `putyka_uzivatele`
--

DROP TABLE IF EXISTS `putyka_uzivatele`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `putyka_uzivatele` (
  `id_stolu` int(11) NOT NULL DEFAULT '0',
  `id_uzivatele` int(11) NOT NULL DEFAULT '0',
  `oblibenost` int(11) NOT NULL DEFAULT '0' COMMENT '0-nic, 1-book, -1-ignore',
  `navstiveno` datetime DEFAULT NULL,
  `neprectenych` int(11) DEFAULT NULL,
  `sprava` int(11) NOT NULL DEFAULT '0' COMMENT '0-nic, 1-pomocnik',
  `pristup` int(11) NOT NULL DEFAULT '0' COMMENT '0-OK, 1-pristup povolen, 2-zapis povolen, -1-zapis zakazan, -2-pristup zakazan',
  PRIMARY KEY (`id_stolu`,`id_uzivatele`),
  KEY `navstiveno` (`navstiveno`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reklama_bannery_zasobnik`
--

DROP TABLE IF EXISTS `reklama_bannery_zasobnik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reklama_bannery_zasobnik` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vlastnik` int(11) NOT NULL DEFAULT '0',
  `cesta` varchar(60) DEFAULT NULL,
  `cislo` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reklama_kampane_bannery`
--

DROP TABLE IF EXISTS `reklama_kampane_bannery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reklama_kampane_bannery` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vlastnik` int(11) NOT NULL DEFAULT '0',
  `cesta` varchar(60) NOT NULL DEFAULT '',
  `odkaz` varchar(60) NOT NULL DEFAULT '',
  `imp_zadane` int(11) NOT NULL DEFAULT '0',
  `imp_zobrazene` int(11) NOT NULL DEFAULT '0',
  `poc_kliku` int(11) NOT NULL DEFAULT '0',
  `zacatek` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reklama_kampane_text`
--

DROP TABLE IF EXISTS `reklama_kampane_text`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reklama_kampane_text` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vlastnik` int(11) NOT NULL DEFAULT '0',
  `text` varchar(255) NOT NULL DEFAULT '',
  `odkaz` varchar(60) NOT NULL DEFAULT '',
  `bezici` char(1) NOT NULL DEFAULT '0',
  `imp_zadane` int(11) NOT NULL DEFAULT '0',
  `imp_zobrazene` int(11) NOT NULL DEFAULT '0',
  `poc_kliku` int(11) NOT NULL DEFAULT '0',
  `zacatek` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reklama_mail`
--

DROP TABLE IF EXISTS `reklama_mail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reklama_mail` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `text` text NOT NULL,
  `k_roz` int(10) unsigned NOT NULL DEFAULT '0',
  `rozeslano` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reklama_ukoncene`
--

DROP TABLE IF EXISTS `reklama_ukoncene`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reklama_ukoncene` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vlastnik` int(11) NOT NULL DEFAULT '0',
  `imp_zobrazene` int(11) NOT NULL DEFAULT '0',
  `poc_kliku` int(11) NOT NULL DEFAULT '0',
  `zacatek` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `konec` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `typ` char(1) NOT NULL DEFAULT 'b',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reklama_users`
--

DROP TABLE IF EXISTS `reklama_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reklama_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `loginname` varchar(30) NOT NULL DEFAULT '',
  `heslo` varchar(35) NOT NULL DEFAULT '',
  `email` varchar(30) NOT NULL DEFAULT '',
  `imprese_ban` int(11) NOT NULL DEFAULT '0',
  `imprese_txt` int(11) NOT NULL DEFAULT '0',
  `info` tinytext,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reputace_log`
--

DROP TABLE IF EXISTS `reputace_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reputace_log` (
  `id_zaznamu` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `dal` varchar(30) NOT NULL DEFAULT '',
  `prijal` varchar(30) NOT NULL DEFAULT '',
  `akce` char(3) NOT NULL DEFAULT '',
  `v_diskusi` enum('a','n','z','s','f') DEFAULT NULL,
  `id_prispevku` int(10) unsigned DEFAULT NULL,
  `date` int(12) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_zaznamu`)
) ENGINE=MyISAM AUTO_INCREMENT=28393 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reputace_special`
--

DROP TABLE IF EXISTS `reputace_special`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reputace_special` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prijal_nick` varchar(25) NOT NULL DEFAULT '',
  `duvod_udeleni` varchar(200) NOT NULL DEFAULT '',
  `hodnota` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rubriky_pristup`
--

DROP TABLE IF EXISTS `rubriky_pristup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rubriky_pristup` (
  `id_usr` int(11) unsigned NOT NULL DEFAULT '0',
  `id_cizi` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `datum` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id_usr`,`id_cizi`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `runy`
--

DROP TABLE IF EXISTS `runy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `runy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_darce` int(11) NOT NULL DEFAULT '0',
  `nick_darce` varchar(30) NOT NULL DEFAULT '',
  `id_prijemce` int(11) DEFAULT NULL,
  `nick_prijemce` varchar(30) NOT NULL DEFAULT '',
  `typ` varchar(15) NOT NULL DEFAULT '',
  `grafika` smallint(6) NOT NULL DEFAULT '0',
  `venovani` mediumtext NOT NULL,
  `datum` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `id_darce` (`id_darce`),
  KEY `id_prijemce` (`id_prijemce`),
  KEY `typ` (`typ`),
  KEY `grafika` (`grafika`)
) ENGINE=MyISAM AUTO_INCREMENT=323 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seznamka`
--

DROP TABLE IF EXISTS `seznamka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seznamka` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno` varchar(40) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `telefon` varchar(20) DEFAULT NULL,
  `mobil` varchar(20) DEFAULT NULL,
  `vek` tinyint(2) DEFAULT '0',
  `okres` varchar(40) DEFAULT NULL,
  `doba` varchar(20) DEFAULT NULL,
  `datum` datetime DEFAULT '0000-00-00 00:00:00',
  `text` text,
  `sekce` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2171 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `skiny`
--

DROP TABLE IF EXISTS `skiny`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `skiny` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `nazev` varchar(10) NOT NULL DEFAULT '',
  `jmeno` varchar(50) NOT NULL DEFAULT '',
  `autor` varchar(20) NOT NULL DEFAULT '',
  `autmail` varchar(40) NOT NULL DEFAULT '',
  `popis` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `slovnicek`
--

DROP TABLE IF EXISTS `slovnicek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `slovnicek` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `jazyk` int(11) NOT NULL DEFAULT '0',
  `kat` set('prid','pod','pris','slov','xxxx','bon1','spoj') NOT NULL DEFAULT 'xxxx',
  `cis` set('s','p','u','x') NOT NULL DEFAULT 'x',
  `rod` set('s','z','m','u','x') NOT NULL DEFAULT 'x',
  `spc1` smallint(6) NOT NULL DEFAULT '0',
  `spc2` smallint(6) NOT NULL DEFAULT '0',
  `text` varchar(40) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `cis` (`cis`),
  KEY `rod` (`rod`),
  KEY `kat` (`kat`),
  KEY `jazyk` (`jazyk`)
) ENGINE=MyISAM AUTO_INCREMENT=3087 DEFAULT CHARSET=latin2 COMMENT='Barvinkuv slovnicek';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sort_prim`
--

DROP TABLE IF EXISTS `sort_prim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sort_prim` (
  `autor` varchar(30) NOT NULL DEFAULT '',
  `prumer` char(3) NOT NULL DEFAULT '',
  `pocet_prispevku` mediumint(9) NOT NULL DEFAULT '0',
  `pocet_v_diskuzi` mediumint(9) NOT NULL DEFAULT '0',
  `reputace` mediumint(9) NOT NULL DEFAULT '0',
  `level` char(1) NOT NULL DEFAULT '',
  `level_new` char(1) NOT NULL DEFAULT '',
  PRIMARY KEY (`autor`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spravci`
--

DROP TABLE IF EXISTS `spravci`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spravci` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `loginname` varchar(200) NOT NULL DEFAULT '',
  `pass` varchar(32) NOT NULL DEFAULT '',
  `rubaktuality` char(1) NOT NULL DEFAULT '0',
  `hrbitov` char(1) NOT NULL DEFAULT '0',
  `rubdobrodruzstvi` char(1) NOT NULL DEFAULT '0',
  `rubclanky` char(1) NOT NULL DEFAULT '0',
  `rublinky` char(1) NOT NULL DEFAULT '0',
  `rubbestiar` char(1) NOT NULL DEFAULT '0',
  `rubvalecnik` char(1) NOT NULL DEFAULT '0',
  `rubhranicar` char(1) NOT NULL DEFAULT '0',
  `rubalchymista` char(1) NOT NULL DEFAULT '0',
  `rubkouzelnik` char(1) NOT NULL DEFAULT '0',
  `rubzlodej` char(1) NOT NULL DEFAULT '0',
  `rubnovapovolani` char(1) NOT NULL DEFAULT '0',
  `mail` varchar(255) NOT NULL DEFAULT '',
  `rubpredmety` char(1) NOT NULL DEFAULT '0',
  `rubdownloady` char(1) NOT NULL DEFAULT '0',
  `rubgalerie` char(1) NOT NULL DEFAULT '0',
  `rubdovednosti` char(1) NOT NULL DEFAULT '0',
  `rubnoverasy` char(1) NOT NULL DEFAULT '0',
  `uzivatele` char(1) NOT NULL DEFAULT '0',
  `rubexpanze` char(1) NOT NULL DEFAULT '0',
  `alchpred` char(1) NOT NULL DEFAULT '0',
  `hrankouzla` char(1) NOT NULL DEFAULT '0',
  `kkouzla` char(1) NOT NULL DEFAULT '0',
  `rubputyka` char(1) NOT NULL DEFAULT '0',
  `rubprogram` char(1) NOT NULL DEFAULT '0',
  `rubMS` char(1) NOT NULL DEFAULT '0',
  `rubfotogalerie` char(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=95 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistiky_autori`
--

DROP TABLE IF EXISTS `statistiky_autori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistiky_autori` (
  `autor` varchar(25) CHARACTER SET latin2 NOT NULL,
  `rubrika` varchar(25) CHARACTER SET latin2 NOT NULL,
  `pocet` int(11) NOT NULL,
  PRIMARY KEY (`autor`,`rubrika`),
  KEY `pocet` (`pocet`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistiky_dila`
--

DROP TABLE IF EXISTS `statistiky_dila`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistiky_dila` (
  `autor` varchar(32) NOT NULL,
  `rubrika` varchar(32) NOT NULL,
  `skupina` varchar(32) NOT NULL,
  `hodnoceni` float NOT NULL,
  `datum` datetime NOT NULL,
  KEY `autor_2` (`autor`),
  KEY `rubrika` (`rubrika`),
  KEY `skupina` (`skupina`),
  KEY `hodnoceni` (`hodnoceni`),
  KEY `datum` (`datum`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temptable`
--

DROP TABLE IF EXISTS `temptable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `temptable` (
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `id_cizi` int(10) unsigned NOT NULL DEFAULT '0',
  `rubrika` varchar(20) DEFAULT NULL,
  `pochvez` tinyint(4) unsigned NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_ratings`
--

DROP TABLE IF EXISTS `user_ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_ratings` (
  `record_id` int(11) NOT NULL AUTO_INCREMENT,
  `rating_time` int(11) NOT NULL DEFAULT '0',
  `byFK` int(11) NOT NULL DEFAULT '0',
  `forFK` int(11) NOT NULL DEFAULT '0',
  `visible` smallint(6) NOT NULL DEFAULT '0',
  `rating_text` text NOT NULL,
  PRIMARY KEY (`record_id`),
  UNIQUE KEY `ForAndBy` (`byFK`,`forFK`)
) ENGINE=MyISAM AUTO_INCREMENT=232 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_stats`
--

DROP TABLE IF EXISTS `user_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_stats` (
  `user_id` int(11) NOT NULL DEFAULT '0',
  `loghistory` varchar(200) NOT NULL DEFAULT 'x',
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users2log`
--

DROP TABLE IF EXISTS `users2log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users2log` (
  `nick` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`nick`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uzivatele`
--

DROP TABLE IF EXISTS `uzivatele`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uzivatele` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `jmeno_uzivatele` varchar(20) NOT NULL DEFAULT '',
  `nick_uzivatele` varchar(25) NOT NULL DEFAULT '',
  `prijmeni_uzivatele` varchar(20) NOT NULL DEFAULT '',
  `psw_uzivatele` varchar(40) NOT NULL DEFAULT '',
  `email_uzivatele` varchar(50) NOT NULL DEFAULT '',
  `pohlavi_uzivatele` varchar(4) DEFAULT NULL,
  `vek_uzivatele` int(11) NOT NULL DEFAULT '0',
  `kraj_uzivatele` varchar(20) NOT NULL DEFAULT 'Praha',
  `chat_barva` varchar(6) NOT NULL DEFAULT 'cccccc',
  `chat_pismo` tinyint(1) NOT NULL DEFAULT '12',
  `chat_reload` tinyint(3) NOT NULL DEFAULT '20',
  `chat_zprav` tinyint(3) NOT NULL DEFAULT '20',
  `chat_filtr` varchar(255) DEFAULT NULL,
  `chat_filtr_zobrazit` tinyint(1) NOT NULL DEFAULT '0',
  `pospristup` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `level` char(1) NOT NULL DEFAULT '0',
  `icq_uzivatele` int(15) NOT NULL DEFAULT '0',
  `vypsat_udaje` varchar(15) NOT NULL DEFAULT '0,0,0,0,0,0,0',
  `ikonka_uzivatele` varchar(25) DEFAULT NULL,
  `popis_uzivatele` varchar(255) DEFAULT NULL,
  `nova_posta` tinyint(3) NOT NULL DEFAULT '0',
  `skin` varchar(10) NOT NULL DEFAULT 'dark',
  `reputace` mediumint(9) NOT NULL DEFAULT '0',
  `reputace_rozdel` tinyint(4) unsigned NOT NULL DEFAULT '0',
  `status` char(1) NOT NULL DEFAULT '4',
  `reg_schval_datum` datetime DEFAULT NULL,
  `indexhodnotitele` decimal(4,2) NOT NULL DEFAULT '-5.50',
  `reload` char(1) NOT NULL DEFAULT '0',
  `max_level` tinyint(4) DEFAULT NULL,
  `api_key` varchar(40) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `NICK` (`nick_uzivatele`),
  UNIQUE KEY `API_KEY` (`api_key`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `LEVEL` (`level`)
) ENGINE=MyISAM AUTO_INCREMENT=17439 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uzivatele_cekajici`
--

DROP TABLE IF EXISTS `uzivatele_cekajici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uzivatele_cekajici` (
  `id_zaznamu` int(11) NOT NULL AUTO_INCREMENT,
  `nick_uzivatele` varchar(30) NOT NULL DEFAULT '',
  `email` varchar(40) NOT NULL DEFAULT '',
  `jmeno` varchar(40) NOT NULL DEFAULT '',
  `prijmeni` varchar(40) NOT NULL DEFAULT '',
  `pohlavi` varchar(4) NOT NULL DEFAULT '',
  `datum` int(11) NOT NULL DEFAULT '0',
  `patron` int(11) NOT NULL DEFAULT '0',
  `primluvy` int(11) NOT NULL DEFAULT '0',
  `osloveni` varchar(50) DEFAULT NULL,
  `popis_text` text NOT NULL,
  PRIMARY KEY (`id_zaznamu`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `JMENOAPRIJMENI` (`jmeno`,`prijmeni`),
  UNIQUE KEY `nick_uzivatele` (`nick_uzivatele`)
) ENGINE=MyISAM AUTO_INCREMENT=10649 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uzivatele_filtry`
--

DROP TABLE IF EXISTS `uzivatele_filtry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uzivatele_filtry` (
  `id_uz` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(20) NOT NULL DEFAULT '',
  `filtr` varchar(15) NOT NULL DEFAULT '',
  `hodnota` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_uz`,`rubrika`,`filtr`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uzivatele_maillist`
--

DROP TABLE IF EXISTS `uzivatele_maillist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uzivatele_maillist` (
  `id_uz` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(20) CHARACTER SET ascii COLLATE ascii_bin NOT NULL DEFAULT '',
  `email_uz` varchar(40) NOT NULL DEFAULT '',
  `MIME` char(1) NOT NULL DEFAULT 'p',
  PRIMARY KEY (`id_uz`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uzivatele_zamitnuti`
--

DROP TABLE IF EXISTS `uzivatele_zamitnuti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uzivatele_zamitnuti` (
  `nick_uzivatele` varchar(30) NOT NULL DEFAULT '',
  `email` varchar(50) NOT NULL DEFAULT '',
  `jmeno` varchar(40) NOT NULL DEFAULT '',
  `prijmeni` varchar(40) NOT NULL DEFAULT '',
  `pohlavi` varchar(4) NOT NULL DEFAULT '',
  `datum` int(11) NOT NULL DEFAULT '0',
  KEY `nick_uzivatele` (`nick_uzivatele`,`email`,`prijmeni`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `v_diskuse`
--

DROP TABLE IF EXISTS `v_diskuse`;
/*!50001 DROP VIEW IF EXISTS `v_diskuse`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_diskuse` (
 `count` tinyint NOT NULL,
  `nick` tinyint NOT NULL,
  `rubrika` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_rubriky`
--

DROP TABLE IF EXISTS `v_rubriky`;
/*!50001 DROP VIEW IF EXISTS `v_rubriky`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_rubriky` (
 `jmeno` tinyint NOT NULL,
  `anotace` tinyint NOT NULL,
  `tabulka` tinyint NOT NULL,
  `text` tinyint NOT NULL,
  `autor` tinyint NOT NULL,
  `rubrika` tinyint NOT NULL,
  `skupina` tinyint NOT NULL,
  `pochvez` tinyint NOT NULL,
  `datum` tinyint NOT NULL,
  `uri` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `zld_hlasovani`
--

DROP TABLE IF EXISTS `zld_hlasovani`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_hlasovani` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  `rocnik` varchar(6) NOT NULL,
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`,`rocnik`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`,`rocnik`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_main`
--

DROP TABLE IF EXISTS `zld_main`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_main` (
  `rocnik` char(6) NOT NULL DEFAULT '',
  `status` char(1) NOT NULL DEFAULT '',
  UNIQUE KEY `ROCNIK` (`rocnik`),
  KEY `STATUS` (`status`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace`
--

DROP TABLE IF EXISTS `zld_nominace`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `rocnik` varchar(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=132 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2001_2`
--

DROP TABLE IF EXISTS `zld_nominace_2001_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2001_2` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2001_2_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2001_2_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2001_2_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2002_1`
--

DROP TABLE IF EXISTS `zld_nominace_2002_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2002_1` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=87 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2002_1_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2002_1_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2002_1_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2002_2`
--

DROP TABLE IF EXISTS `zld_nominace_2002_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2002_2` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=181 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2002_2_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2002_2_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2002_2_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2003_1`
--

DROP TABLE IF EXISTS `zld_nominace_2003_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2003_1` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=199 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2003_1_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2003_1_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2003_1_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2003_2`
--

DROP TABLE IF EXISTS `zld_nominace_2003_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2003_2` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=97 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2003_2_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2003_2_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2003_2_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2004_1`
--

DROP TABLE IF EXISTS `zld_nominace_2004_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2004_1` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=104 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2004_1_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2004_1_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2004_1_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2004_2`
--

DROP TABLE IF EXISTS `zld_nominace_2004_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2004_2` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=39 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2004_2_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2004_2_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2004_2_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2005_1`
--

DROP TABLE IF EXISTS `zld_nominace_2005_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2005_1` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=94 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2005_1_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2005_1_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2005_1_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2005_2`
--

DROP TABLE IF EXISTS `zld_nominace_2005_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2005_2` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=53 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2005_2_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2005_2_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2005_2_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2006_1`
--

DROP TABLE IF EXISTS `zld_nominace_2006_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2006_1` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=61 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2006_1_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2006_1_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2006_1_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2006_2`
--

DROP TABLE IF EXISTS `zld_nominace_2006_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2006_2` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=43 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2006_2_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2006_2_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2006_2_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2007_1`
--

DROP TABLE IF EXISTS `zld_nominace_2007_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2007_1` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=65 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2007_1_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2007_1_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2007_1_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2007_2`
--

DROP TABLE IF EXISTS `zld_nominace_2007_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2007_2` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=49 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2007_2_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2007_2_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2007_2_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2008_1`
--

DROP TABLE IF EXISTS `zld_nominace_2008_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2008_1` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=49 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2008_1_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2008_1_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2008_1_hlasoval` (
  `id_usr` int(11) NOT NULL DEFAULT '0',
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` char(3) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2008_2`
--

DROP TABLE IF EXISTS `zld_nominace_2008_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2008_2` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL,
  `jmeno` varchar(255) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2008_2_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2008_2_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2008_2_hlasoval` (
  `id_usr` int(11) NOT NULL,
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` varchar(3) NOT NULL,
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2009_1`
--

DROP TABLE IF EXISTS `zld_nominace_2009_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2009_1` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL,
  `jmeno` varchar(255) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=48 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2009_1_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2009_1_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2009_1_hlasoval` (
  `id_usr` int(11) NOT NULL,
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` varchar(3) NOT NULL,
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2009_2`
--

DROP TABLE IF EXISTS `zld_nominace_2009_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2009_2` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cizi_id` int(11) NOT NULL,
  `jmeno` varchar(255) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_nominace_2009_2_hlasoval`
--

DROP TABLE IF EXISTS `zld_nominace_2009_2_hlasoval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_nominace_2009_2_hlasoval` (
  `id_usr` int(11) NOT NULL,
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` varchar(3) NOT NULL,
  PRIMARY KEY (`id_usr`,`pocet_bodu`,`rubrika`),
  UNIQUE KEY `JENJEDNOU` (`id_usr`,`id_prispevku`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2001_2`
--

DROP TABLE IF EXISTS `zld_pocitam_2001_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2001_2` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(3) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2002_1`
--

DROP TABLE IF EXISTS `zld_pocitam_2002_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2002_1` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(3) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2002_2`
--

DROP TABLE IF EXISTS `zld_pocitam_2002_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2002_2` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(3) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2003_1`
--

DROP TABLE IF EXISTS `zld_pocitam_2003_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2003_1` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(3) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2003_2`
--

DROP TABLE IF EXISTS `zld_pocitam_2003_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2003_2` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(3) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2004_1`
--

DROP TABLE IF EXISTS `zld_pocitam_2004_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2004_1` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(3) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2004_2`
--

DROP TABLE IF EXISTS `zld_pocitam_2004_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2004_2` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(3) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2005_1`
--

DROP TABLE IF EXISTS `zld_pocitam_2005_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2005_1` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(3) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2005_2`
--

DROP TABLE IF EXISTS `zld_pocitam_2005_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2005_2` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(3) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2006_1`
--

DROP TABLE IF EXISTS `zld_pocitam_2006_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2006_1` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(10) NOT NULL DEFAULT '0',
  `misto1` int(10) NOT NULL DEFAULT '0',
  `misto2` int(10) NOT NULL DEFAULT '0',
  `misto3` int(10) NOT NULL DEFAULT '0',
  `cernyd` int(10) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2006_2`
--

DROP TABLE IF EXISTS `zld_pocitam_2006_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2006_2` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(10) NOT NULL DEFAULT '0',
  `misto1` int(10) NOT NULL DEFAULT '0',
  `misto2` int(10) NOT NULL DEFAULT '0',
  `misto3` int(10) NOT NULL DEFAULT '0',
  `cernyd` int(10) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2007_1`
--

DROP TABLE IF EXISTS `zld_pocitam_2007_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2007_1` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(10) NOT NULL DEFAULT '0',
  `misto1` int(10) NOT NULL DEFAULT '0',
  `misto2` int(10) NOT NULL DEFAULT '0',
  `misto3` int(10) NOT NULL DEFAULT '0',
  `cernyd` int(10) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2007_2`
--

DROP TABLE IF EXISTS `zld_pocitam_2007_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2007_2` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(10) NOT NULL DEFAULT '0',
  `misto1` int(10) NOT NULL DEFAULT '0',
  `misto2` int(10) NOT NULL DEFAULT '0',
  `misto3` int(10) NOT NULL DEFAULT '0',
  `cernyd` int(10) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2008_1`
--

DROP TABLE IF EXISTS `zld_pocitam_2008_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2008_1` (
  `id_prispevku` int(11) NOT NULL DEFAULT '0',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `pocet_bodu` int(10) NOT NULL DEFAULT '0',
  `misto1` int(10) NOT NULL DEFAULT '0',
  `misto2` int(10) NOT NULL DEFAULT '0',
  `misto3` int(10) NOT NULL DEFAULT '0',
  `cernyd` int(10) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2008_2`
--

DROP TABLE IF EXISTS `zld_pocitam_2008_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2008_2` (
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` int(10) NOT NULL,
  `misto1` int(10) NOT NULL,
  `misto2` int(10) NOT NULL,
  `misto3` int(10) NOT NULL,
  `cernyd` int(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2009_1`
--

DROP TABLE IF EXISTS `zld_pocitam_2009_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2009_1` (
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` int(10) NOT NULL,
  `misto1` int(10) NOT NULL,
  `misto2` int(10) NOT NULL,
  `misto3` int(10) NOT NULL,
  `cernyd` int(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2009_2`
--

DROP TABLE IF EXISTS `zld_pocitam_2009_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2009_2` (
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` int(10) NOT NULL,
  `misto1` int(10) NOT NULL,
  `misto2` int(10) NOT NULL,
  `misto3` int(10) NOT NULL,
  `cernyd` int(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2010`
--

DROP TABLE IF EXISTS `zld_pocitam_2010`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2010` (
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` int(10) NOT NULL,
  `misto1` int(10) NOT NULL,
  `misto2` int(10) NOT NULL,
  `misto3` int(10) NOT NULL,
  `cernyd` int(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2011`
--

DROP TABLE IF EXISTS `zld_pocitam_2011`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2011` (
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` int(10) NOT NULL,
  `misto1` int(10) NOT NULL,
  `misto2` int(10) NOT NULL,
  `misto3` int(10) NOT NULL,
  `cernyd` int(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2012`
--

DROP TABLE IF EXISTS `zld_pocitam_2012`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2012` (
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` int(10) NOT NULL,
  `misto1` int(10) NOT NULL,
  `misto2` int(10) NOT NULL,
  `misto3` int(10) NOT NULL,
  `cernyd` int(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2013`
--

DROP TABLE IF EXISTS `zld_pocitam_2013`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2013` (
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` int(10) NOT NULL,
  `misto1` int(10) NOT NULL,
  `misto2` int(10) NOT NULL,
  `misto3` int(10) NOT NULL,
  `cernyd` int(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_pocitam_2014`
--

DROP TABLE IF EXISTS `zld_pocitam_2014`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_pocitam_2014` (
  `id_prispevku` int(11) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `pocet_bodu` int(10) NOT NULL,
  `misto1` int(10) NOT NULL,
  `misto2` int(10) NOT NULL,
  `misto3` int(10) NOT NULL,
  `cernyd` int(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove`
--

DROP TABLE IF EXISTS `zld_vitezove`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  `rocnik` varchar(6) NOT NULL,
  PRIMARY KEY (`cizi_id`,`rubrika`,`rocnik`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2001_2`
--

DROP TABLE IF EXISTS `zld_vitezove_2001_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2001_2` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2002_1`
--

DROP TABLE IF EXISTS `zld_vitezove_2002_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2002_1` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2002_2`
--

DROP TABLE IF EXISTS `zld_vitezove_2002_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2002_2` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2003_1`
--

DROP TABLE IF EXISTS `zld_vitezove_2003_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2003_1` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2003_2`
--

DROP TABLE IF EXISTS `zld_vitezove_2003_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2003_2` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2004_1`
--

DROP TABLE IF EXISTS `zld_vitezove_2004_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2004_1` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2004_2`
--

DROP TABLE IF EXISTS `zld_vitezove_2004_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2004_2` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2005_1`
--

DROP TABLE IF EXISTS `zld_vitezove_2005_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2005_1` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2005_2`
--

DROP TABLE IF EXISTS `zld_vitezove_2005_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2005_2` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2006_1`
--

DROP TABLE IF EXISTS `zld_vitezove_2006_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2006_1` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2006_2`
--

DROP TABLE IF EXISTS `zld_vitezove_2006_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2006_2` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2007_1`
--

DROP TABLE IF EXISTS `zld_vitezove_2007_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2007_1` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2007_2`
--

DROP TABLE IF EXISTS `zld_vitezove_2007_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2007_2` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2008_1`
--

DROP TABLE IF EXISTS `zld_vitezove_2008_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2008_1` (
  `cizi_id` int(11) NOT NULL DEFAULT '0',
  `jmeno` varchar(255) NOT NULL DEFAULT '',
  `rubrika` varchar(30) NOT NULL DEFAULT '',
  `autor` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2008_2`
--

DROP TABLE IF EXISTS `zld_vitezove_2008_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2008_2` (
  `cizi_id` int(11) NOT NULL,
  `jmeno` varchar(255) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `autor` varchar(30) NOT NULL,
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2009_1`
--

DROP TABLE IF EXISTS `zld_vitezove_2009_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2009_1` (
  `cizi_id` int(11) NOT NULL,
  `jmeno` varchar(255) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `autor` varchar(30) NOT NULL,
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `zld_vitezove_2009_2`
--

DROP TABLE IF EXISTS `zld_vitezove_2009_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zld_vitezove_2009_2` (
  `cizi_id` int(11) NOT NULL,
  `jmeno` varchar(255) NOT NULL,
  `rubrika` varchar(30) NOT NULL,
  `autor` varchar(30) NOT NULL,
  PRIMARY KEY (`cizi_id`,`rubrika`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `v_diskuse`
--

/*!50001 DROP TABLE IF EXISTS `v_diskuse`*/;
/*!50001 DROP VIEW IF EXISTS `v_diskuse`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `v_diskuse` AS select count(0) AS `count`,`putyka_prispevky`.`autor` AS `nick`,_utf8'putyka' AS `rubrika` from `putyka_prispevky` group by `putyka_prispevky`.`autor` union all select count(0) AS `count`,`diskuze`.`nickname` AS `nick`,_utf8'diskuze' AS `rubrika` from `diskuze` group by `diskuze`.`nickname` union all select count(0) AS `count`,`forum`.`nickname` AS `nick`,_utf8'forum' AS `rubrika` from `forum` group by `forum`.`nickname` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_rubriky`
--

/*!50001 DROP TABLE IF EXISTS `v_rubriky`*/;
/*!50001 DROP VIEW IF EXISTS `v_rubriky`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `v_rubriky` AS select `alchpredmety`.`jmeno` AS `jmeno`,NULL AS `anotace`,concat_ws(_utf8'',_utf8'magenergie: ',cast(`alchpredmety`.`mag` as char(11) charset utf8),_utf8' magu<br />suroviny: ',cast(`alchpredmety`.`suroviny` as char(11) charset utf8),_utf8' zl<br />zaklad: ',convert(`alchpredmety`.`zaklad` using utf8),_utf8'<br />nalezeni: ',convert(`alchpredmety`.`nalezeni` using utf8),_utf8'<br />trvani: ',convert(`alchpredmety`.`trvani` using utf8),_utf8'<br />nebezpecnost: ',convert(`alchpredmety`.`nebezpecnost` using utf8),_utf8'<br />sila: ',convert(`alchpredmety`.`sila` using utf8),_utf8'<br />barva/chut/zapach: ',convert(`alchpredmety`.`bcz` using utf8),_utf8'<br />denni magenergie: ',cast(`alchpredmety`.`denmag` as char(11) charset utf8),_utf8' magu<br />dosah: ',convert(`alchpredmety`.`dosah_ucinku` using utf8),_utf8'<br />uroven vyrobce: ',convert(`alchpredmety`.`uroven_vyrobce` using utf8),_utf8'<br />') AS `tabulka`,`alchpredmety`.`popis` AS `text`,`alchpredmety`.`autor` AS `autor`,_utf8'alchpredmety' AS `rubrika`,`alchpredmety`.`skupina` AS `skupina`,`alchpredmety`.`pochvez` AS `pochvez`,`alchpredmety`.`datum` AS `datum`,NULL AS `uri` from `alchpredmety` union all select `bestiar`.`jmeno` AS `jmeno`,NULL AS `anotace`,concat_ws(_latin2'',_latin2'zivotaschopnost: ',`bestiar`.`zvt`,_latin2'<br />UC: ',`bestiar`.`uc`,_latin2'<br />OC: ',`bestiar`.`oc`,_latin2'<br />odolnost: ',`bestiar`.`odl`,_latin2'<br />inteligence: ',`bestiar`.`inteligence`,_latin2'<br />velikost: ',`bestiar`.`vel`,_latin2'<br />zranitelnost: ',`bestiar`.`zran`,_latin2'<br />pohyblivost: ',`bestiar`.`poh`,_latin2'<br />presvedceni: ',`bestiar`.`pres`,_latin2'<br />bojovnost: ',`bestiar`.`bojovnost`,_latin2'<br />sila mysli: ',`bestiar`.`SM`,_latin2'<br />poklady',`bestiar`.`pokl`,_latin2'<br />zkusenost:',`bestiar`.`zkus`) AS `tabulka`,`bestiar`.`popis` AS `text`,`bestiar`.`autor` AS `autor`,_utf8'bestiar' AS `rubrika`,`bestiar`.`skupina` AS `skupina`,`bestiar`.`pochvez` AS `pochvez`,`bestiar`.`datum` AS `datum`,NULL AS `uri` from `bestiar` union all select `dovednosti`.`jmeno` AS `jmeno`,NULL AS `anotace`,concat_ws(_latin2'',_latin2'vlastnost: ',`dovednosti`.`vlastnost`,_latin2'<br />obtiznost: ',`dovednosti`.`obtiznost`,_latin2'<br />overovani: ',`dovednosti`.`overovani`,_latin2'<br />totalni uspech: ',`dovednosti`.`totuspech`,_latin2'<br />uspech: ',`dovednosti`.`uspech`,_latin2'<br />neuspech: ',`dovednosti`.`neuspech`,_latin2'<br />fatalni neuspech: ',`dovednosti`.`fatneuspech`) AS `tabulka`,`dovednosti`.`popis` AS `text`,`dovednosti`.`autor` AS `autor`,_utf8'dovednosti' AS `rubrika`,`dovednosti`.`skupina` AS `skupina`,`dovednosti`.`pochvez` AS `pochvez`,`dovednosti`.`datum` AS `datum`,NULL AS `uri` from `dovednosti` union all select `hranicarkouzla`.`jmeno` AS `jmeno`,NULL AS `anotace`,concat_ws(_utf8'',_utf8'magenergie: ',cast(`hranicarkouzla`.`mag` as char(11) charset utf8),_utf8' ',convert(`hranicarkouzla`.`magpop` using utf8),_utf8'<br />dosah: ',cast(`hranicarkouzla`.`dosah` as char(11) charset utf8),_utf8' ',convert(`hranicarkouzla`.`dosahpop` using utf8),_utf8'<br />rozsah: ',cast(`hranicarkouzla`.`rozsah` as char(11) charset utf8),_utf8' ',convert(`hranicarkouzla`.`rozsahpop` using utf8),_utf8'<br />vyvolani: ',cast(`hranicarkouzla`.`vyvolani` as char(11) charset utf8),_utf8' ',convert(`hranicarkouzla`.`vyvolanipop` using utf8),_utf8'<br />druh: ',convert(`hranicarkouzla`.`druh` using utf8),_utf8'<br />skupina: ',convert(`hranicarkouzla`.`skupina` using utf8),_utf8'<br />cetnost: ',convert(`hranicarkouzla`.`cetnost` using utf8),_utf8'<br />pomucky: ',convert(`hranicarkouzla`.`pomucky` using utf8)) AS `tabulka`,`hranicarkouzla`.`popis` AS `text`,`hranicarkouzla`.`autor` AS `autor`,_utf8'hranicarkouzla' AS `rubrika`,`hranicarkouzla`.`skupina` AS `skupina`,`hranicarkouzla`.`pochvez` AS `pochvez`,`hranicarkouzla`.`datum` AS `datum`,NULL AS `uri` from `hranicarkouzla` union all select `kouzla`.`jmeno` AS `jmeno`,NULL AS `anotace`,concat_ws(_utf8'',_utf8'kouzelna slova: ',convert(`kouzla`.`kouzsl` using utf8),_utf8'magenergie: ',cast(`kouzla`.`mag` as char(11) charset utf8),_utf8' ',convert(`kouzla`.`magpop` using utf8),_utf8'<br />past: ',convert(`kouzla`.`past` using utf8),_utf8'<br />dosah: ',cast(`kouzla`.`dosah` as char(11) charset utf8),_utf8' ',convert(`kouzla`.`dosahpop` using utf8),_utf8'<br />rozsah: ',cast(`kouzla`.`rozsah` as char(11) charset utf8),_utf8' ',convert(`kouzla`.`rozsahpop` using utf8),_utf8'<br />vyvolani: ',cast(`kouzla`.`vyvolani` as char(11) charset utf8),_utf8' ',convert(`kouzla`.`vyvolanipop` using utf8),_utf8'<br />trvani: ',cast(`kouzla`.`trvani` as char(11) charset utf8),_utf8' ',convert(`kouzla`.`trvanipop` using utf8)) AS `tabulka`,`kouzla`.`popis` AS `text`,`kouzla`.`autor` AS `autor`,_utf8'kouzla' AS `rubrika`,`kouzla`.`skupina` AS `skupina`,`kouzla`.`pochvez` AS `pochvez`,`kouzla`.`datum` AS `datum`,NULL AS `uri` from `kouzla` union all select `predmety`.`jmeno` AS `jmeno`,NULL AS `anotace`,concat_ws(_utf8'',_utf8'UC: ',convert(`predmety`.`UC` using utf8),_utf8'<br />KZ/obrana zbrane: ',convert(`predmety`.`KZ` using utf8),_utf8'<br />delka',convert(`predmety`.`delka` using utf8),_utf8'<br />cena: ',cast(`predmety`.`cena` as char(11) charset utf8),_utf8'<br />maly dostrel: ',cast(`predmety`.`malydostrel` as char(11) charset utf8),_utf8'<br />stredni dostrel: ',cast(`predmety`.`strednidostrel` as char(11) charset utf8),_utf8'<br />velky dostrel: ',cast(`predmety`.`velkydostrel` as char(11) charset utf8),_utf8'<br />sfera:',cast(`predmety`.`sfera` as char(11) charset utf8),_utf8'<br />vaha:',cast(`predmety`.`vaha` as char(11) charset utf8)) AS `tabulka`,`predmety`.`popis` AS `text`,`predmety`.`autor` AS `autor`,_utf8'predmety' AS `rubrika`,`predmety`.`skupina` AS `skupina`,`predmety`.`pochvez` AS `pochvez`,`predmety`.`datum` AS `datum`,NULL AS `uri` from `predmety` union all select `prispevky_dlouhe`.`jmeno` AS `jmeno`,`prispevky_dlouhe`.`anotace` AS `anotace`,NULL AS `tabulka`,`prispevky_dlouhe`.`text` AS `text`,`prispevky_dlouhe`.`autor` AS `autor`,`prispevky_dlouhe`.`rubrika` AS `rubrika`,`prispevky_dlouhe`.`skupina` AS `skupina`,`prispevky_dlouhe`.`pochvez` AS `pochvez`,`prispevky_dlouhe`.`datum` AS `datum`,NULL AS `uri` from `prispevky_dlouhe` union all select `downloady`.`jmeno` AS `jmeno`,NULL AS `anotace`,NULL AS `tabulka`,`downloady`.`popis` AS `text`,`downloady`.`autor` AS `autor`,_utf8'downloady' AS `rubrika`,`downloady`.`skupina` AS `skupina`,`downloady`.`pochvez` AS `pochvez`,`downloady`.`datum` AS `datum`,concat(_latin2'/',_latin2'soub',`downloady`.`cesta`) AS `uri` from `downloady` union all select `galerie`.`jmeno` AS `jmeno`,NULL AS `anotace`,NULL AS `tabulka`,NULL AS `text`,`galerie`.`autor` AS `autor`,_utf8'galerie' AS `rubrika`,NULL AS `skupina`,`galerie`.`pochvez` AS `pochvez`,`galerie`.`datum` AS `datum`,concat(_latin2'/',_latin2'galerie',`galerie`.`cesta`) AS `uri` from `galerie` union all select `dobrodruzstvi`.`jmeno` AS `jmeno`,`dobrodruzstvi`.`anotace` AS `anotace`,NULL AS `tabulka`,NULL AS `text`,`dobrodruzstvi`.`autor` AS `autor`,_utf8'dobrodruzstvi' AS `rubrika`,NULL AS `skupina`,`dobrodruzstvi`.`pochvez` AS `pochvez`,`dobrodruzstvi`.`datum` AS `datum`,concat(_utf8'/',_utf8'dobrodruzstvi',cast(`dobrodruzstvi`.`id` as char(11) charset utf8),convert(`dobrodruzstvi`.`cesta` using utf8)) AS `uri` from `dobrodruzstvi` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-02 17:42:19

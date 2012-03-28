-- MySQL dump 10.13  Distrib 5.1.49, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: feiying_new
-- ------------------------------------------------------
-- Server version	5.1.49-3

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
-- Table structure for table `fy_business_status`
--

DROP TABLE IF EXISTS `fy_business_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_business_status` (
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_device_info`
--

DROP TABLE IF EXISTS `fy_device_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_device_info` (
  `username` bigint(20) NOT NULL,
  `brand` varchar(20) DEFAULT NULL,
  `model` varchar(20) DEFAULT NULL,
  `release_ver` varchar(20) DEFAULT NULL,
  `sdk` varchar(20) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_fav`
--

DROP TABLE IF EXISTS `fy_fav`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_fav` (
  `username` bigint(20) unsigned NOT NULL,
  `source_id` varchar(32) NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`source_id`,`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_feedback`
--

DROP TABLE IF EXISTS `fy_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(50) DEFAULT NULL,
  `comment` varchar(500) DEFAULT NULL,
  `type` varchar(20) DEFAULT 'problem',
  PRIMARY KEY (`id`),
  KEY `type` (`type`),
  CONSTRAINT `fy_feedback_fk` FOREIGN KEY (`type`) REFERENCES `fy_feedback_type` (`type`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_feedback_type`
--

DROP TABLE IF EXISTS `fy_feedback_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_feedback_type` (
  `type` varchar(20) NOT NULL,
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_keywords`
--

DROP TABLE IF EXISTS `fy_keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(50) NOT NULL,
  `count` int(11) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_mobile_version`
--

DROP TABLE IF EXISTS `fy_mobile_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_mobile_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL,
  `app_name` varchar(50) DEFAULT NULL,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `version` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_movie`
--

DROP TABLE IF EXISTS `fy_movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_movie` (
  `source_id` varchar(32) NOT NULL,
  `time` varchar(8) DEFAULT NULL,
  `size` varchar(8) DEFAULT NULL,
  `video_url` varchar(256) NOT NULL,
  `director` varchar(32) DEFAULT NULL COMMENT '导演',
  `actor` varchar(64) DEFAULT NULL COMMENT '演员',
  `release_date` varchar(16) DEFAULT NULL COMMENT '上映日期',
  `origin` varchar(8) DEFAULT NULL COMMENT '产地',
  `description` varchar(512) DEFAULT NULL COMMENT '电影描述',
  PRIMARY KEY (`source_id`),
  CONSTRAINT `fy_movie_fk` FOREIGN KEY (`source_id`) REFERENCES `fy_video` (`source_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_share`
--

DROP TABLE IF EXISTS `fy_share`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_share` (
  `share_id` int(11) NOT NULL,
  `send` bigint(20) unsigned NOT NULL,
  `send_state` varchar(20) NOT NULL,
  `source_id` varchar(32) NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`share_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_share_recv`
--

DROP TABLE IF EXISTS `fy_share_recv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_share_recv` (
  `share_id` int(11) NOT NULL,
  `receive` bigint(20) unsigned NOT NULL,
  `receive_state` varchar(20) NOT NULL,
  PRIMARY KEY (`share_id`,`receive`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_short_video`
--

DROP TABLE IF EXISTS `fy_short_video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_short_video` (
  `source_id` varchar(32) NOT NULL,
  `time` varchar(8) NOT NULL,
  `size` varchar(8) NOT NULL,
  `video_url` varchar(256) NOT NULL,
  PRIMARY KEY (`source_id`),
  CONSTRAINT `fy_short_video_fk` FOREIGN KEY (`source_id`) REFERENCES `fy_video` (`source_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_tv_episode`
--

DROP TABLE IF EXISTS `fy_tv_episode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_tv_episode` (
  `source_id` varchar(32) NOT NULL,
  `time` varchar(8) DEFAULT NULL,
  `size` varchar(8) DEFAULT NULL,
  `status` tinyint(4) unsigned zerofill NOT NULL DEFAULT '0000',
  `episode_index` smallint(6) unsigned zerofill NOT NULL DEFAULT '000000',
  `image_url` varchar(256) NOT NULL,
  `video_url` varchar(256) NOT NULL,
  PRIMARY KEY (`source_id`,`episode_index`),
  CONSTRAINT `fy_tv_episode_fk` FOREIGN KEY (`source_id`) REFERENCES `fy_video` (`source_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_tv_series`
--

DROP TABLE IF EXISTS `fy_tv_series`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_tv_series` (
  `source_id` varchar(32) NOT NULL,
  `director` varchar(32) DEFAULT NULL,
  `actor` varchar(64) DEFAULT NULL,
  `release_date` varchar(16) DEFAULT NULL,
  `origin` varchar(8) DEFAULT NULL,
  `description` varchar(512) DEFAULT NULL,
  `episode_count` smallint(6) unsigned zerofill NOT NULL DEFAULT '000000',
  `episode_all` tinyint(4) unsigned zerofill NOT NULL DEFAULT '0001',
  PRIMARY KEY (`source_id`),
  CONSTRAINT `fy_tv_series_fk` FOREIGN KEY (`source_id`) REFERENCES `fy_video` (`source_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_user`
--

DROP TABLE IF EXISTS `fy_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_user` (
  `username` bigint(20) unsigned NOT NULL,
  `userpass` char(32) NOT NULL,
  `userkey` char(32) NOT NULL,
  `business_status` varchar(20) DEFAULT 'unopened',
  PRIMARY KEY (`username`),
  KEY `business_status` (`business_status`),
  CONSTRAINT `fy_user_fk` FOREIGN KEY (`business_status`) REFERENCES `fy_business_status` (`status`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fy_video`
--

DROP TABLE IF EXISTS `fy_video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fy_video` (
  `source_id` varchar(32) NOT NULL,
  `title` varchar(128) NOT NULL,
  `image_url` varchar(256) NOT NULL,
  `channel` tinyint(4) unsigned NOT NULL,
  `status` tinyint(4) unsigned zerofill NOT NULL DEFAULT '0000' COMMENT '0,刚抓取下来；1,已经进入下载队列；2,正在下载；100,下载完成；101,该电视剧的更新已经进入下载队列；102,该电视剧的更新正在下载中；',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `play_count` int(11) unsigned zerofill NOT NULL DEFAULT '00000000000',
  `fav_count` int(11) unsigned zerofill NOT NULL DEFAULT '00000000000',
  `share_count` int(11) unsigned zerofill NOT NULL DEFAULT '00000000000',
  PRIMARY KEY (`source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=154;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-03-28 10:12:06

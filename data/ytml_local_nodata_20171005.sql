-- MySQL dump 10.15  Distrib 10.0.25-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ytml
-- ------------------------------------------------------
-- Server version	10.0.25-MariaDB-0ubuntu0.15.10.1

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
-- Table structure for table `classrooms`
--

DROP TABLE IF EXISTS `classrooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classrooms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(36) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `uid` varchar(36) NOT NULL DEFAULT '',
  `title` varchar(255) NOT NULL,
  `memo` varchar(255) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `task_ids` varchar(255) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `title_UNIQUE` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ejdic`
--

DROP TABLE IF EXISTS `ejdic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ejdic` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `en` text,
  `ja` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46726 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `games`
--

DROP TABLE IF EXISTS `games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `games` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mode` varchar(9) NOT NULL,
  `task_id` varchar(36) NOT NULL DEFAULT '',
  `tid` varchar(36) DEFAULT NULL,
  `q_num` int(11) NOT NULL,
  `done` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `video_id` varchar(255) DEFAULT NULL,
  `fullmarks` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `completed` varchar(3000) DEFAULT NULL,
  `fail_list` varchar(255) DEFAULT NULL,
  `fine_list` varchar(255) DEFAULT NULL,
  `success_list` varchar(255) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26831 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jacet`
--

DROP TABLE IF EXISTS `jacet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jacet` (
  `rank` int(11) unsigned NOT NULL,
  `en` varchar(45) DEFAULT NULL,
  `tag` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`rank`),
  UNIQUE KEY `rank_UNIQUE` (`rank`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `postags`
--

DROP TABLE IF EXISTS `postags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `postags` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tag` varchar(4) DEFAULT NULL,
  `description` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scripts`
--

DROP TABLE IF EXISTS `scripts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scripts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tid` varchar(36) DEFAULT NULL,
  `vid` varchar(36) DEFAULT NULL,
  `video_id` varchar(255) DEFAULT NULL,
  `q_num` int(11) DEFAULT '0',
  `timestamp` text,
  `script_main` text,
  `script_local` text,
  `user_level` int(11) DEFAULT NULL,
  `user_level2` int(11) DEFAULT NULL,
  `question` text,
  `question2` text,
  `probability` text,
  `probability2` text,
  `blank_rate` int(11) DEFAULT NULL,
  `blank_rate2` text,
  `token` text,
  `stopword` text,
  `tagged` text,
  `tag_id` text,
  `lemma` text,
  `jacet` text,
  `comment` text,
  `advice` text,
  `done` int(11) DEFAULT '0',
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=92307 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scripts_ex`
--

DROP TABLE IF EXISTS `scripts_ex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scripts_ex` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tid` varchar(36) DEFAULT NULL,
  `vid` varchar(36) DEFAULT NULL,
  `video_id` varchar(255) DEFAULT NULL,
  `q_num` int(11) DEFAULT '0',
  `timestamp` text,
  `script_main` text,
  `script_local` text,
  `user_level` int(11) DEFAULT NULL,
  `user_level2` int(11) DEFAULT NULL,
  `question` text,
  `question2` text,
  `probability` text,
  `probability2` text,
  `blank_rate` int(11) DEFAULT NULL,
  `blank_rate2` text,
  `token` text,
  `stopword` text,
  `tagged` text,
  `tag_id` text,
  `lemma` text,
  `jacet` text,
  `comment` text,
  `advice` text,
  `done` int(11) DEFAULT '0',
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=805 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(36) DEFAULT NULL,
  `status` int(11) DEFAULT '1',
  `uid` varchar(36) DEFAULT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `vid` varchar(11) DEFAULT NULL,
  `video_id` varchar(255) DEFAULT NULL,
  `video_key` varchar(255) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `origin` varchar(36) DEFAULT NULL,
  `follow` int(11) DEFAULT NULL,
  `follow_id` varchar(36) DEFAULT NULL,
  `vol` int(11) DEFAULT NULL,
  `start_q` int(11) DEFAULT NULL,
  `end_q` int(11) DEFAULT NULL,
  `total_q` int(11) DEFAULT NULL,
  `memo` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `title_local` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `host` varchar(45) DEFAULT NULL,
  `mode` varchar(45) DEFAULT NULL,
  `lang` varchar(45) DEFAULT NULL,
  `local_lang` varchar(45) DEFAULT NULL,
  `chunk` tinyint(4) DEFAULT NULL,
  `level` varchar(45) DEFAULT NULL,
  `score` int(11) DEFAULT '0',
  `progress` int(11) DEFAULT '0',
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `owner_name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `download_url` varchar(255) DEFAULT NULL,
  `v_relate` int(11) DEFAULT NULL,
  `v_enjoy` int(11) DEFAULT NULL,
  `v_play` int(11) DEFAULT NULL,
  `v_understand` int(11) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2407 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tasks_ex`
--

DROP TABLE IF EXISTS `tasks_ex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tasks_ex` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(36) DEFAULT NULL,
  `status` int(11) DEFAULT '1',
  `uid` varchar(36) DEFAULT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `vid` varchar(11) DEFAULT NULL,
  `video_id` varchar(255) DEFAULT NULL,
  `video_key` varchar(255) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `origin` varchar(36) DEFAULT NULL,
  `follow` int(11) DEFAULT NULL,
  `follow_id` varchar(36) DEFAULT NULL,
  `vol` int(11) DEFAULT NULL,
  `start_q` int(11) DEFAULT NULL,
  `end_q` int(11) DEFAULT NULL,
  `total_q` int(11) DEFAULT NULL,
  `memo` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `title_local` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `host` varchar(45) DEFAULT NULL,
  `mode` varchar(45) DEFAULT NULL,
  `lang` varchar(45) DEFAULT NULL,
  `local_lang` varchar(45) DEFAULT NULL,
  `chunk` tinyint(4) DEFAULT NULL,
  `level` varchar(45) DEFAULT NULL,
  `score` int(11) DEFAULT '0',
  `progress` int(11) DEFAULT '0',
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `owner_name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `download_url` varchar(255) DEFAULT NULL,
  `v_relate` int(11) DEFAULT NULL,
  `v_enjoy` int(11) DEFAULT NULL,
  `v_play` int(11) DEFAULT NULL,
  `v_understand` int(11) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tasksets`
--

DROP TABLE IF EXISTS `tasksets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tasksets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classroom_id` varchar(36) DEFAULT NULL,
  `tid` varchar(36) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `uid` varchar(36) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=190 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `uuid` varchar(36) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `local_lang` varchar(9) DEFAULT 'ja',
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL,
  `school` varchar(45) DEFAULT NULL,
  `grade` varchar(45) DEFAULT NULL,
  `affiliation` varchar(45) DEFAULT NULL,
  `student_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `videos`
--

DROP TABLE IF EXISTS `videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `video_id` varchar(17) DEFAULT NULL,
  `video_key` varchar(255) DEFAULT NULL,
  `host` varchar(7) DEFAULT '',
  `lang` varchar(3) DEFAULT NULL,
  `video_lang` varchar(3) DEFAULT NULL,
  `lang_list` text,
  `url` text,
  `title` text,
  `plot` text,
  `plot_id` varchar(11) DEFAULT NULL,
  `subtitle` text,
  `description` text,
  `memo` text,
  `img` text,
  `video_date` text,
  `channel` varchar(255) DEFAULT NULL,
  `channel_id` varchar(11) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `author_id` varchar(11) DEFAULT NULL,
  `video_link` text,
  `duration` int(11) DEFAULT NULL,
  `adjustment` float DEFAULT NULL,
  `keywords` text,
  `tags` text,
  `rating` text,
  `viewed` int(11) DEFAULT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `size` text,
  `difficulty1` text,
  `difficulty2` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=400 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `videos_ex`
--

DROP TABLE IF EXISTS `videos_ex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `videos_ex` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `video_id` varchar(17) DEFAULT NULL,
  `video_key` varchar(255) DEFAULT NULL,
  `host` varchar(7) DEFAULT '',
  `lang` varchar(3) DEFAULT NULL,
  `video_lang` varchar(3) DEFAULT NULL,
  `lang_list` text,
  `url` text,
  `title` text,
  `plot` text,
  `plot_id` varchar(11) DEFAULT NULL,
  `subtitle` text,
  `description` text,
  `memo` text,
  `img` text,
  `video_date` text,
  `channel` varchar(255) DEFAULT NULL,
  `channel_id` varchar(11) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `author_id` varchar(11) DEFAULT NULL,
  `video_link` text,
  `duration` int(11) DEFAULT NULL,
  `adjustment` float DEFAULT NULL,
  `keywords` text,
  `tags` text,
  `rating` text,
  `viewed` int(11) DEFAULT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `size` text,
  `difficulty1` text,
  `difficulty2` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `words`
--

DROP TABLE IF EXISTS `words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `words` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lemma` varchar(255) DEFAULT NULL,
  `word` varchar(255) NOT NULL,
  `user_id` varchar(36) NOT NULL DEFAULT '',
  `uid` varchar(36) NOT NULL,
  `tid` varchar(36) DEFAULT NULL,
  `q_num` int(11) DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `jacet` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `t_success` int(11) DEFAULT NULL,
  `t_miss` int(11) DEFAULT NULL,
  `t_dict` int(11) DEFAULT NULL,
  `t_save` int(11) DEFAULT NULL,
  `t_repeat` int(11) DEFAULT NULL,
  `t_cheat` int(11) DEFAULT NULL,
  `t_skip` int(11) DEFAULT NULL,
  `t_complete` int(11) DEFAULT NULL,
  `mark` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98789 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-01 22:06:01

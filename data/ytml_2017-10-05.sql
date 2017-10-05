# ************************************************************
# Sequel Pro SQL dump
# バージョン 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# ホスト: 127.0.0.1 (MySQL 5.5.5-10.0.25-MariaDB-0ubuntu0.15.10.1)
# データベース: ytml
# 作成時刻: 2017-10-05 01:14:19 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# テーブルのダンプ ejdic
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ejdic`;

CREATE TABLE `ejdic` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `en` text,
  `ja` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# テーブルのダンプ jacet
# ------------------------------------------------------------

DROP TABLE IF EXISTS `jacet`;

CREATE TABLE `jacet` (
  `rank` int(11) unsigned NOT NULL,
  `en` varchar(45) DEFAULT NULL,
  `tag` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`rank`),
  UNIQUE KEY `rank_UNIQUE` (`rank`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# テーブルのダンプ postags
# ------------------------------------------------------------

DROP TABLE IF EXISTS `postags`;

CREATE TABLE `postags` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tag` varchar(4) DEFAULT NULL,
  `description` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

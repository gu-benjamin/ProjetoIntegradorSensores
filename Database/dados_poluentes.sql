CREATE TABLE `dados_poluentes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` datetime NOT NULL,
  `pm25` float NOT NULL,
  `pm10` float NOT NULL,
  `o3` float NOT NULL,
  `no2` float NOT NULL,
  `so2` float NOT NULL,
  `co` float NOT NULL,
  `latitude` FLOAT NOT NULL,
  `latitude` FLOAT NOT NULL,
  PRIMARY KEY (`id`)
)
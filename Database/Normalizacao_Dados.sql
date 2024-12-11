ALTER TABLE registro_abc
ADD COLUMN `latitude` DOUBLE DEFAULT -23.615022924191905,
ADD COLUMN `longitude` DOUBLE DEFAULT -46.57074877922242,
ADD COLUMN `regiao` VARCHAR(50) DEFAULT 'ABC';

ALTER TABLE registro_centro
ADD COLUMN `latitude` DOUBLE DEFAULT -23.549882894676934,
ADD COLUMN `longitude` DOUBLE DEFAULT -46.633180975797764,
ADD COLUMN `regiao` VARCHAR(50) DEFAULT 'Centro';

ALTER TABLE registro_guaianazes
ADD COLUMN `latitude` DOUBLE DEFAULT -23.573801814158454,
ADD COLUMN `longitude` DOUBLE DEFAULT -46.40862070437357,
ADD COLUMN `regiao` VARCHAR(50) DEFAULT 'Zona Leste';

CREATE TABLE `tb_registro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `temperatura` decimal(10,2) DEFAULT NULL,
  `pressao` decimal(10,2) DEFAULT NULL,
  `altitude` decimal(10,2) DEFAULT NULL,
  `umidade` decimal(10,2) DEFAULT NULL,
  `co2` decimal(10,2) DEFAULT NULL,
  `tempo_registro` datetime DEFAULT NULL,
  `regiao` varchar(100) DEFAULT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  PRIMARY KEY (`id`)
);

INSERT INTO tb_registro (temperatura, pressao, altitude, umidade, co2, tempo_registro, regiao, latitude, longitude)
SELECT temperatura, pressao, altitude, umidade, co2, tempo_registro, 'ABC', latitude, longitude
FROM registro_abc;

INSERT INTO tb_registro (temperatura, pressao, altitude, umidade, co2, tempo_registro, regiao, latitude, longitude)
SELECT temperatura, pressao, altitude, umidade, co2, tempo_registro, 'Centro', latitude, longitude
FROM registro_centro;

INSERT INTO tb_registro (temperatura, pressao, altitude, umidade, co2, tempo_registro, regiao, latitude, longitude)
SELECT temperatura, pressao, altitude, umidade, co2, tempo_registro, 'Zona Leste', latitude, longitude
FROM registro_guaianazes;
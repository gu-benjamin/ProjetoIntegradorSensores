ALTER TABLE tb_registro
ADD `latitude` FLOAT NOT NULL,
ADD `longitude` FLOAT NOT NULL;

-- Atualiza Latitude e Longitude para regiao = "Sao Paulo"
UPDATE tb_registro
SET latitude = -23.573801814158454,
    longitude = -46.40862070437357
WHERE regiao = 'Sao Paulo';

-- Atualiza Latitude e Longitude para regiao = "ABC"
UPDATE tb_registro
SET latitude = -23.615022924191905,
    longitude = -46.57074877922242
WHERE regiao = 'ABC';

-- Atualiza Latitude e Longitude para regiao = "Centro"
UPDATE tb_registro
SET latitude = -23.549882894676934,
    longitude = -46.633180975797764
WHERE regiao = 'Centro';

SET SQL_SAFE_UPDATES = 0;
create database petshop
use petshop

create table donos(
	id int primary key,
	nome_dono varchar(30),
	telefone varchar(15)
);

CREATE TABLE petshop(
    id INT PRIMARY KEY,
    tipo_pet VARCHAR(30),
    nome_pet VARCHAR(30),
    idade INT,
	id_dono int,
	foreign key (id_dono) references donos(id)
);

CREATE TRIGGER ajusta_id
ON petshop
AFTER DELETE
AS
BEGIN
    DECLARE @novo_id INT = 1;

    CREATE TABLE #PetsTemp (id INT, tipo_pet VARCHAR(30), nome_pet VARCHAR(30), idade INT, id_dono INT);

    INSERT INTO #PetsTemp (id, tipo_pet, nome_pet, idade, id_dono)
    SELECT @novo_id, tipo_pet, nome_pet, idade, id_dono
    FROM petshop
    ORDER BY id;

    SET @novo_id = @novo_id + 1;

    DELETE FROM petshop;

    INSERT INTO petshop (id, tipo_pet, nome_pet, idade, id_dono)
    SELECT id, tipo_pet, nome_pet, idade, id_dono
    FROM #PetsTemp;

    DROP TABLE #PetsTemp;
END;
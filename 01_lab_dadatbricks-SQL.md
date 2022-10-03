## Conceito

O Azure Databricks é uma plataforma de análise de dados otimizada para a plataforma de Serviços de Nuvem do Microsoft Azure. O Azure Databricks oferece três ambientes para o desenvolvimento de aplicativos com uso intensivo de dados: Databricks SQL, Engenharia de Ciência de Dados do Databricks e Databricks Machine Learning. </br>

O Databricks SQL fornece uma plataforma fácil de usar para analistas que desejam executar consultas SQL em data lake, criar vários tipos de visualização para explorar os resultados da consulta de diferentes perspectivas, além de criar e compartilhar painéis. </br>

<img src="https://raw.githubusercontent.com/Databricks-BR/labs/main/images/databricks_sql.png" width="700px">

## Objetivos do Exercício



## Exercício 01 - Criação do database

``` sql
-- The following creates a database the Databricks Academy learner can use
CREATE DATABASE IF NOT EXISTS raielo_dbacademy;
-- The following grants SELECT, CREATE, MODIFY, READ_METADATA, and CREATE_NAMED_FUNCTION privileges to the learner for this database
-- **You MUST change the username to the learner’s username**

GRANT ALL PRIVILEGES ON DATABASE dbacademy TO `learner’s_username`;
USE dbacademy;

--The following ensures the table uses the latest data set
DROP TABLE IF EXISTS intro_to_databricks_sql_gym_logs;

-- The following creates a table for use in the current course
-- Data for the table comes from a read-only object store

CREATE TABLE intro_to_databricks_sql_gym_logs
USING JSON
LOCATION ‘wasbs://courseware@dbacademy.blob.core.windows.net/introduction-to-databricks-sql/v01/gym-logs’;

```

## Exercício 02 - SQL de visualização simples

``` sql
SELECT
 *
FROM
 dbacademy.intro_to_databricks_sql_gym_logs;
``` 

 ## Exercício 03 - Verificando as Academias mais Populares
 
``` sql
SELECT
 gym,
 count(gym)
FROM
 dbacademy.intro_to_databricks_sql_gym_logs
GROUP BY
 gym
ORDER BY
 gym;
``` 
## Exercício 04 - Avaliando a faixa (range) de Datas 

``` sql
-- Tab: Which Dates
SELECT
 from_unixtime(min(first_timestamp), “d MMMM y”) First_Date,
 from_unixtime(max(last_timestamp), “d MMMM y”) Last_Date
FROM
 dbacademy.intro_to_databricks_sql_gym_logs;
``` 

## Exercício 05 - Calculando a média de tempo na academia

``` sql
-- Tab: Avg Time Spent
SELECT
 from_unixtime(first_timestamp, “dd”) as day,
 avg((last_timestamp - first_timestamp) / 60) as avg_time
FROM
 dbacademy.intro_to_databricks_sql_gym_logs
group by
 day
ORDER BY
 from_unixtime(first_timestamp, “dd”); (edited) 
```  

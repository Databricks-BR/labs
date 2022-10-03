## Conceito

O Azure Databricks é uma plataforma de análise de dados otimizada para a plataforma de Serviços de Nuvem do Microsoft Azure. O Azure Databricks oferece três ambientes para o desenvolvimento de aplicativos com uso intensivo de dados: Databricks SQL, Engenharia de Ciência de Dados do Databricks e Databricks Machine Learning. </br>

O Databricks SQL fornece uma plataforma fácil de usar para analistas que desejam executar consultas SQL em data lake, criar vários tipos de visualização para explorar os resultados da consulta de diferentes perspectivas, além de criar e compartilhar painéis. </br>

<img src="https://raw.githubusercontent.com/Databricks-BR/labs/main/images/databricks_sql.png" width="700px">

## Objetivos do Exercício

O objetivo desse laboratório é conhecer as funcionalidades de consulta (_Query_) da plataforma Azure Databricks, utilizando a linguagem SQL (e as interfaces visuais), explorando os potenciais Analíticos, e ao final, construindo um painel gerencial (_Dashboard_). </br>
</br>
O caso de uso do exercício utiliza uma base de dados de uma Academia de Ginática, onde vamos simular uma análise exploratória interativa para avaliar o perfil dos frequentadores, os tempos de utilização e as filiais mais frequentadas.

## Exercício 01 - Criação do database

``` sql

CREATE DATABASE IF NOT EXISTS <seu_nome>_dbacademy;


GRANT ALL PRIVILEGES ON DATABASE dbacademy TO `learner’s_username`;

USE <seu_nome>_dbacademy;


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
 <seu_nome>_dbacademy.intro_to_databricks_sql_gym_logs
GROUP BY
 gym
ORDER BY
 gym;
``` 
## Exercício 04 - Avaliando a faixa (range) de Datas 

``` sql

SELECT
 from_unixtime(min(first_timestamp), “d MMMM y”) First_Date,
 from_unixtime(max(last_timestamp), “d MMMM y”) Last_Date
FROM
 <seu_nome>_dbacademy.intro_to_databricks_sql_gym_logs;
``` 

## Exercício 05 - Calculando a média de tempo na academia

``` sql

SELECT
 from_unixtime(first_timestamp, “dd”) as day,
 avg((last_timestamp - first_timestamp) / 60) as avg_time
FROM
 <seu_nome>_dbacademy.intro_to_databricks_sql_gym_logs
group by
 day
ORDER BY
 from_unixtime(first_timestamp, “dd”); (edited) 
```  

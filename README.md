# Realtime.quiz02
## Design
![image](https://user-images.githubusercontent.com/22583786/234262295-7466da5a-97db-4b58-b5cb-0f22539e82c7.png)


## Docker File 
#### 1. unzip docker_quiz02.zip
#### 2. $ cd docker_quiz02
#### 3. $ docker-compose up

## Installation and running
### Install psycopg2 (postgresql client)
```shell
conda install -c anaconda psycopg2
```
### PostgreSQL
Create database on postgresql.
```sql
CREATE DATABASE quiz02_raw;
```
### Create Table
$ python create_table.py $file_input $table_name

```shell
python create_table.py food_coded.csv quiz02_raw
```

### Kafka 

#### Create Kafka topic

```shell
docker exec -it kafka.quiz02 /bin/bash
```
```shell
kafka-topics --bootstrap-server kafka.quiz02:9092 --topic quiz02_raw
```
```shell
kafka-topics --bootstrap-server kafka.quiz02:9092 --topic quiz02_persist
```
### KSQL

#### ksqldb-cli
Run bash to ksqldb-cli.
```shell
docker exec -it ksqldb-cli.quiz02 /bin/bash
```
Run ksql-cli
```shell
ksql http://ksqldb-server.quiz02:8088
```

set offset to begin (Option)
```sql
SET 'auto.offset.reset' = 'earliest';
```

#### Create Stream
Raw Zone: create_ksqldb_quiz02_raw_table.sql
```sql
CREATE STREAM quiz02_raw (
index int,
GPA varchar,
Gender int,
breakfast int,
calories_chicken int,
calories_day double,
calories_scone double,
coffee int,
comfort_food varchar,
comfort_food_reasons varchar,
comfort_food_reasons_coded double,
cook double,
comfort_food_reasons_coded_1 int,
cuisine double,
diet_current varchar,
diet_current_coded int,
drink double,
eating_changes varchar,
eating_changes_coded int,
eating_changes_coded1 int,
eating_out int,
employment double,
ethnic_food int,
exercise double,
father_education double,
father_profession varchar,
fav_cuisine varchar,
fav_cuisine_coded int,
fav_food double,
food_childhood varchar,
fries int,
fruit_day int,
grade_level int,
greek_food int,
healthy_feeling int,
healthy_meal varchar,
ideal_diet varchar,
ideal_diet_coded int,
income double,
indian_food int,
italian_food int,
life_rewarding double,
marital_status double,
meals_dinner_friend varchar,
mother_education double,
mother_profession varchar,
nutritional_check int,
on_off_campus double,
parents_cook int,
pay_meal_out int,
persian_food double,
self_perception_weight double,
soup double,
sports double,
thai_food int,
tortilla_calories double,
turkey_calories int,
type_sports varchar,
veggies_day int,
vitamins int,
waffle_calories int,
weight varchar )  WITH (KAFKA_TOPIC='quiz02_raw',VALUE_FORMAT='AVRO');

```

####
Persist Zone: create_ksqldb_quiz02_persist_table.sql
```sql
CREATE STREAM quiz02_persist
with (
    KAFKA_TOPIC = 'quiz02_persist',
    VALUE_FORMAT = 'AVRO',
    PARTITIONS = 2
) as SELECT index,breakfast,coffee,calories_day,drink,eating_changes_coded,exercise,fries,soup,nutritional_check,employment,fav_food,income,sports,
veggies_day,indian_food,Italian_food,persian_food,thai_food,vitamins,self_perception_weight,weight
FROM quiz02_raw 
where calories_day >= 1.0
EMIT CHANGES;
```
#### Verify Stream
![image](https://user-images.githubusercontent.com/22583786/234232662-a1a9e051-1085-47fa-aeed-d2f7e0b24a5c.png)

#### Create Connector
ksql> RUN SCRIPT '/etc/sql/all.sql';

Create source.
```sql
CREATE SOURCE CONNECTOR `postgres-source` WITH(
    "connector.class"='io.confluent.connect.jdbc.JdbcSourceConnector',
    "connection.url"='jdbc:postgresql://postgres:5432/root?user=root&password=secret',
    "mode"='incrementing',
    "incrementing.column.name"='id',
    "topic.prefix"='',
    "table.whitelist"='quiz02_raw',
    "key"='id');
```

Create sink.
```sql
CREATE SINK CONNECTOR `elasticsearch-sink` WITH(
    "connector.class"='io.confluent.connect.elasticsearch.ElasticsearchSinkConnector',
    "connection.url"='http://elasticsearch:9200',
    "connection.username"='',
    "connection.password"='',
    "batch.size"='1',
    "write.method"='insert',
    "topics"='quiz02_persist',
    "type.name"='changes',
    "key"='title_id');

```



#### Verify quiz02_raw
```sql
SELECT index,breakfast,coffee,calories_day,drink,eating_changes_coded,exercise,fries,soup,nutritional_check,employment,fav_food,income,sports,
veggies_day,indian_food,Italian_food,persian_food,thai_food,vitamins,self_perception_weight,weight
FROM quiz02_raw
EMIT CHANGES;
```

### Insert Data
$ python insert_data.py  $file_input $table_name

```shell
python insert_data.py food_coded.csv quiz02_raw
```

Result

![image](https://user-images.githubusercontent.com/22583786/235335788-fdac6dfc-bce6-4e0e-8849-9c02c0f4af20.png)



### ksql Cleansing (quiz02_raw -> quiz02_persist)
```sql
CREATE STREAM quiz02_persist
with (
    KAFKA_TOPIC = 'quiz02_persist',
    VALUE_FORMAT = 'AVRO',
    PARTITIONS = 2
) as SELECT index,breakfast,coffee,calories_day,drink,eating_changes_coded,exercise,fries,soup,nutritional_check,employment,fav_food,income,sports,
veggies_day,indian_food,Italian_food,persian_food,thai_food,vitamins,self_perception_weight,weight
FROM quiz02_raw 
where calories_day >= 1.0
EMIT CHANGES;
```

### KSQLDB Analyze
Analyze Zone:
```sql
CREATE STREAM quiz02_analze
with (
    KAFKA_TOPIC = 'quiz02_persist',
    VALUE_FORMAT = 'AVRO',
    PARTITIONS = 2
) as SELECT index,breakfast,coffee,calories_day,drink,eating_changes_coded,exercise,fries,soup,nutritional_check,employment,fav_food,income,sports,
veggies_day,indian_food,Italian_food,persian_food,thai_food,vitamins,self_perception_weight,weight
FROM quiz02_persist 
where calories_day >= 1.0
EMIT CHANGES;
```

## Sink NoSQL

## Visualize

## Note

Show connector information
```sql
DESCRIBE connector `postgres_test02`;
```
![image](https://user-images.githubusercontent.com/22583786/235336731-9b15db7b-00c0-438a-9bdf-106a9eebf5a7.png)

Show stream information
```sql
DESCRIBE quiz02_raw;
```
![image](https://user-images.githubusercontent.com/22583786/235336810-400fd581-7f07-4a17-8270-1b527e11f09c.png)


Delete connector
```sql
drop connector `postgres_test01`;
```

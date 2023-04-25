# Realtime.quiz02
## Design
![image](https://user-images.githubusercontent.com/22583786/234248928-9f85ed83-529f-4227-9f2c-74a2b7255782.png)


## Docker File 
#### 1. unzip docker_quiz02.zip
#### 2. $ cd docker_quiz02
#### 3. $ docker-compose up

## Application
### Install psycopg2 (postgresql client)
$ conda install -c anaconda psycopg2

### Create Table
$ python create_table.py $file_input $table_name



### KSQL

#### ksqldb-cli
$ docker exec -it ksqldb-cli.quiz02 /bin/bash

$ ksql http://ksqldb-server.quiz02:8088

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
...
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
```sql
CREATE SOURCE CONNECTOR `postgres-source` WITH(
    "connector.class"='io.confluent.connect.jdbc.JdbcSourceConnector',
    "connection.url"='jdbc:postgresql://postgres:5432/root?user=root&password=secret',
    "mode"='incrementing',
    "incrementing.column.name"='id',
    "topic.prefix"='',
    "table.whitelist"='titles',
    "key"='id');


CREATE SINK CONNECTOR `elasticsearch-sink` WITH(
    "connector.class"='io.confluent.connect.elasticsearch.ElasticsearchSinkConnector',
    "connection.url"='http://elasticsearch:9200',
    "connection.username"='',
    "connection.password"='',
    "batch.size"='1',
    "write.method"='insert',
    "topics"='titles',
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

![image](https://user-images.githubusercontent.com/22583786/234234015-1e851d7f-7697-4657-a6b4-d8cb5b12069a.png)


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

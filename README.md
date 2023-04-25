# Realtime.quiz02
## Design
![image](https://user-images.githubusercontent.com/22583786/233766388-f2bffc1f-9a72-48c8-be50-e5d10e239836.png)


## Docker File 
#### 1. unzip docker_quiz02.zip
#### 2. $ cd docker_quiz02
#### 3. $ docker-compose up

## Application
### Install psycopg2 (postgresql client)
$ conda install -c anaconda psycopg2

### Create Table
$ python create_table.py $file_input $table_name

### Insert Data
$ python insert_data.py  $file_input $table_name

### ksql Create Table
file: create_ksqldb_quiz02_table.sql

### ksql Cleansing


### ksql Analyze

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 10:43:23 2023

@author: LEGION
"""

import psycopg2
import json
import pandas as pd
import sys


def getColumnDtypes(dataTypes):
    dataList = []
    for x in dataTypes:
        if(x == 'int64'):
            dataList.append('int')
        elif (x == 'float64'):
            dataList.append('float')
        elif (x == 'bool'):
            dataList.append('boolean')
        else:
            dataList.append('varchar')
    return dataList



source_file=sys.argv[1]
table_name=sys.argv[2]

conn = psycopg2.connect(
    dbname="quiz02_dev",  # Replace with your database name
    user="root",  # Replace with your username
    password="secret",  # Replace with your password
    host="localhost",  # Replace with your host address
    port="5432"  # Replace with your port number
)

cur = conn.cursor()

df = pd.read_csv(source_file).reset_index(drop=False)

columnDataType = getColumnDtypes(df.dtypes)
columnName = list(df.columns.values)
columnName = [x.replace('.', '_') for x in columnName]

numofrow = df.shape[0]

for i in range(0,numofrow):
    aa = df.loc[df['index']== i,:]
    columnData = aa.values.tolist()
    #print(columnData)
    sql = f'INSERT INTO {table_name} ('
    for k in range(len(columnDataType)):
        #sql = sql + '\n' + columnName[k] +  ','
        sql = sql + columnName[k] +  ','
    
    sql = sql[:-1] + ' ) values ('
    
    for j in range(0,len(columnData[0])):
        if columnDataType[j] == "varchar":
            #sql = sql + '\n' +"\'"  + str(columnData[0][j])  +"\'" + ','
            #sql = sql + '\n' +"\""  + str(columnData[0][j])  +"\"" + ','
            #sql = sql + '\n' +"%s" + ','
            sql = sql +"%s" + ','
        else:
            #sql = sql + '\n' +"\'"  + str(columnData[0][j]) +"\'" + ','
            #sql = sql + '\n' +"\'"  + str(columnData[0][j])  +"\'" + ','
            #sql = sql + '\n' +"%s" + ','
            sql = sql +"%s" + ','
        #print(f"# {j} {len(columnData)}")
        #print(columnData[0][j])
    
    sql = sql[:-1] + ');'
    #print(sql)
    #cur.execute(sql)
    cur.execute(sql,columnData[0])
    
    conn.commit()

print(df.shape[0])

cur.close()
        
    
    
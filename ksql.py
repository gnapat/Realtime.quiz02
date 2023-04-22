# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 11:39:53 2023

@author: LEGION
"""

#from ksql import KSQLAPI
import ksql
#logging.basicConfig(level=logging.DEBUG)

client = ksql('http://ksqldb-server.quiz02:8088')

query = client.query('SELECT * FROM titles EMIT CHANGES;')
import pandas as pd
import pyodbc
from pathlib import Path 
import os


def db_conn(driver,server,db,user=None,password=None,local=True):
    if local:
        conn=pyodbc.connect('driver={%s};server=%s;database=%s;Trusted_Connection=yes;' % ( driver, server, db) )
    else:
        conn = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % ( driver, server, db, user, password ) )
    return conn


def sql_query(query,conn):
    sql_query = pd.read_sql_query(str(query),conn)
    return sql_query
    
    
#Test 
 



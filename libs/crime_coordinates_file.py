#Import app useful modules
import os
from pathlib import Path
import sys

path = Path(os.getcwd())
sys.path.append(os.path.join(path.parent,'libs'))

import database_handler as dbh

#Connect databse
driver='ODBC Driver 17 for SQL Server'
server='DESKTOP-T2HC97J' # Server name
db='chicago_crime'    
conn=dbh.db_conn(driver,server,db)
query='SELECT DISTINCT latitude,longitude FROM chicago_crime.dbo.location'
crime_coordinates=dbh.sql_query(query,conn)
#print(crime_coordinates)
#print(type(crime_coordinates))

#save crime coordinates to file
path = Path(os.getcwd()) 
csv_path=os.path.join(path.parent,'data','crime_coordinates.csv')
crime_coordinates.to_csv(csv_path,header=['Latitude','Longitude'])
print('Crime coordinates csv file created at ',csv_path,'with shape ',str(crime_coordinates.shape))
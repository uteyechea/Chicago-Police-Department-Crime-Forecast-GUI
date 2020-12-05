#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import random
#Import app useful modules
import os
from pathlib import Path
import sys

path = Path(os.getcwd())
sys.path.append(os.path.join(path.parent,'libs'))

import database_handler as dbh

import hermosillo_beats as hb


# In[2]:

def get_primary_type_color(primary_type):
    
    color={}
    
    color['THEFT']='red'
    color['BATTERY']='purple'
    color['CRIMINAL DAMAGE']='blue'
    color['NARCOTICS']='yellow'
    color['ASSAULT']='orange'
    color['OTHER OFFENSE']='green'
    color['BURGLARY']='pink'
    color['MOTOR VEHICLE THEFT']='brown'
    color['DECEPTIVE PRACTICE']='black'
    color['ROBBERY']='orangered'
    color['CRIMINAL TRESPASS']='khaki'
    
    primary_type_color=color[str(primary_type)]
    
    return primary_type_color
    
    
#Connect databse
"""
driver= #odbc name
server= # Server name
db= # Database name
"""
def fake_forecast(number_of_predictions=20,driver='ODBC Driver 17 for SQL Server',server='DESKTOP-T2HC97J',db='chicago_crime'):
    conn=dbh.db_conn(driver,server,db)
    # Count number of police beats.
    query='SELECT COUNT(DISTINCT beat) FROM chicago_crime.dbo.location_detail'
    beat_tally=dbh.sql_query(query,conn)
    beat_tally=beat_tally.iloc[0,0] # Returns int total number of police beats.
    # Count the number of primary_type crimes in the city over all criminal history.
    query='SELECT COUNT(primary_type) FROM chicago_crime.dbo.crime'
    primary_type_tally=dbh.sql_query(query,conn)
    primary_type_tally=primary_type_tally.iloc[0,0] # Returns int total number of crimes.
    # Count number of crimes per primary_type
    query='SELECT primary_type,COUNT(primary_type) FROM chicago_crime.dbo.crime GROUP BY primary_type ORDER BY COUNT(primary_type) DESC' 
    primary_type=(dbh.sql_query(query,conn)) # Returns (35,2) shape DataFrame.
    # Get city's beat code lookup_table
    query='SELECT DISTINCT beat FROM chicago_crime.dbo.location_detail ORDER BY beat ASC'
    beat_lookup=dbh.sql_query(query,conn)
    # Get number of primary_type crime per beat
    query='SELECT beat,primary_type, count(primary_type) AS primary_type_tally FROM chicago_crime.dbo.crime AS c,chicago_crime.dbo.location_detail as ld,chicago_crime.dbo.location as l WHERE c.location_id = l.id AND l.location_detail_id = ld.id GROUP BY beat,primary_type'
    beat_primary_type_tally=dbh.sql_query(query,conn)
    for i in range(len(beat_primary_type_tally)):
        beat=beat_primary_type_tally.loc[i,'beat']
        beat_match=(beat_lookup['beat']==beat)
        match=beat_match.index[beat_match==True][0]
        beat_primary_type_tally.loc[i,'beat']=match # Returns (n,3) DataFrame with columns [beat,primary_type,primary_type_tally]
        
    # Compute crime ocurrence probability based on Chicago's primary_types
    probability=primary_type.iloc[:,1].astype(float) /primary_type_tally
    crime_tally=np.around(probability*number_of_predictions,0)
    if np.sum(crime_tally) != number_of_predictions:
        crime_tally[0]+=number_of_predictions-np.sum(crime_tally)
        
    #Get some primary_type crime properties (historical)
    #query=''
    
    #Create dash_leaflet polygon verticis
    #Record vertex of square on top of city of interest (Hermosillo, Sonora, Mexico)
    beat_grid_vertex={'top':[[29.1540,-111.0070],[29.1540,-110.9400]],
                  'bottom':[[29.0080,-111.0070],[29.0080,-110.9400]]
                  }
    #Map coordinates per beat
    beat_polygon=hb.beat_polygon_vertex(beat_tally=beat_tally,beat_grid_vertex=beat_grid_vertex)
    
    #Generate temporary data holder DataFrame
    data={}
    data['primary_type']=primary_type.iloc[:,0].astype(str)
    data['probability']=primary_type.iloc[:,1].astype(float) /primary_type_tally
    data['primary_type_tally']=crime_tally.astype(int)
    data=pd.DataFrame(data)
    
    #Generate fake forecast
    forecast={}
    forecast['polygon_vertices']=[]
    forecast['color']=[]
    primary_types=[]
    forecast['beat']=random.sample(range(1,beat_tally), number_of_predictions)
    for i in range(len(data)):
        primary_types+=[data.loc[i,'primary_type']]*data.loc[i,'primary_type_tally']
    forecast['primary_type']=primary_types
    forecast['probability']=np.random.rand(number_of_predictions)
    forecast['primary_type_per_tally']=np.random.randint(1,1000,(number_of_predictions,))
    for beat in forecast['beat']:
        forecast['polygon_vertices'].append(beat_polygon[beat])
    
    for type in primary_types:
        forecast['color'].append(get_primary_type_color(type))
    
    forecast=pd.DataFrame(forecast)
    
    return forecast
    


# In[3]:


"""
#Usage Example
forecast=fake_forecast()
#save fake forecast to file
path = Path(os.getcwd()) 
csv_path=os.path.join(path.parent,'data','fake_forecast.csv')
forecast.to_csv(csv_path,header=['polygon_vertices','Beat','Primary_Type','Probability','Primary_Type_per_Beat_tally'])


print('Fake forecast csv file created at %s with shape %s'%(csv_path,str(forecast.shape)))


list(forecast['polygon_vertices'])[:]
"""


#from jupyter_dash import JupyterDash # To run server inline while in a Jupyter notebook
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_leaflet as dl
import numpy as np
import pandas as pd
import math
import dash # Use for standalone window server

import os
from pathlib import Path
import sys

path = Path(os.getcwd())
sys.path.append(os.path.join(path.parent,'libs'))

import fake_forecast as fk 


forecast=fk.fake_forecast(number_of_predictions=20) # Switch to read_csv when loading real forecast.



# Generate map polygons per crime per beat
overlays={}
for primary_type in forecast['primary_type'].unique():

    columns=forecast.loc[forecast['primary_type']==primary_type]
   
    polygons=dl.Polygon(positions=list(columns['polygon_vertices'])[:],color=str(columns['color'].unique()[0]),stroke=False,fillOpacity=0.5)
    
    overlays[str(primary_type)]=dl.Overlay(dl.LayerGroup(polygons),name=primary_type,checked=True)


#App colors
colors={
    'background':'#white',
    'text':'black'
}

# Where to center map on first time app run 
hermosillo_coordinates = (29.0730,-110.9559)
    

# Some tile urls.
#keys = ["Dark", "Light",'terrain']

#url=url_template.format(key)
#url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'

# Some tile urls.
#keys = ["watercolor", "toner", "terrain"]
#url_template = "http://{{s}}.tile.stamen.com/{}/{{z}}/{{x}}/{{y}}.png"
#url=url_template.format(key)

keys=['Dark','Light']
url_template=['https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png','https://a.tile.openstreetmap.org/{z}/{x}/{y}.png']

#Pending
test_coordinates=[29.0730,-110.9559]
def get_beat_from_coordinates(coordinates=test_coordinates,forecast=forecast):
    vertex_average_coordinates=[]
    #polygons= list(map(float, forecast['polygon_vertices'])) #[float(i) for i in lst]
    polygons=forecast['polygon_vertices']
    for i,vertices in enumerate(polygons):
        #print(i,vertices,np.average(vertices))
        vertex_average_coordinate=np.average(vertices)
        vertex_average_coordinates.append(vertex_average_coordinate)
    x=list( np.sqrt((vertex_average_coordinates-np.average(coordinates))**2) )
    #print(x)
    #print(x.index(min(x)))
    #print(distances)
    #avg=np.average(distances,axis=1)
    #print(min(avg).index())
    #print(min(distance))
    beat_index=x.index(min(x)) #more like forecast_index
    return beat_index


#print(forecast.loc[0,'polygon_vertices'][0])
#beat_index=get_beat_from_coordinates(forecast,forecast.loc[0,'polygon_vertices'][0])
#print(beat_index,type(beat_index)) 
#print(forecast.iloc[forecast.index==beat_index,:])
#print(forecast.loc[forecast.index==beat_index,'probability'].values)
#print(forecast.loc[forecast.index==beat_index,'primary_type_per_tally'].values[0])


# Create info control.
def get_info(coordinates=[],forecast=forecast):
    header = [html.H4("Beat")]
    if not coordinates:
        return header + ["Click over a colored beat"]
    #return header + [html.B(feature["properties"]["name"]), html.Br(),
                     #"{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]
    else:
        beat_index=get_beat_from_coordinates(coordinates,forecast)
        
        #return header + [html.Div(children=str(forecast.loc[forecast.index==beat_index,'primary_type_per_tally'].values[0]))]
        beat_number=forecast.loc[forecast.index==beat_index,'beat'].values[0]
        beat_primary_type=forecast.loc[forecast.index==beat_index,'primary_type'].values[0]
        beat_primary_type_crime_tally=forecast.loc[forecast.index==beat_index,'primary_type_per_tally'].values[0]
        beat_primary_type_probability=forecast.loc[forecast.index==beat_index,'probability'].values[0]
        info_control_data=[html.H4("Beat {}".format(beat_number)),
                           html.H5('Primary type: {}'.format(str(beat_primary_type).title())),
                           html.H5('Crime count {}'.format(beat_primary_type_crime_tally)),
                           html.H5('Crime probability {:.2f}'.format(beat_primary_type_probability))
                          ]
        return info_control_data

"""
# Create info control.
def get_info(coordinates=[]):
    header = [html.H4("Beat")]
    if not coordinates:
        return header + ["Click over a colored beat"]
    #return header + [html.B(feature["properties"]["name"]), html.Br(),
                     #"{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]
    else:
        return header + [html.Div(children=str(coordinates))]
"""

# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "11px", "left": "55px", "z-index": "1000"})

#Create geolocation control. Find my current position.
my_geolocaiton=dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}})


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'] 


# Create app.
#app = JupyterDash(__name__,external_stylesheets=external_stylesheets) # Jupyter notebook inline server run
app=dash.Dash(__name__,external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    
    html.H1(
        children='R.A.D.A.R'#,
        #style={
        #    'textAlign': 'left',
        #    'color': colors['text']
        #}
    ),

    html.Div(children='An AI powered predictive policing system'),
    
    html.Br(),

    html.Div(
      dl.Map([
      dl.LayersControl(
         [dl.BaseLayer(dl.TileLayer(url=url_template[keys.index(key)]), 
                        name=key, checked=key == "Light") for key in keys] +
                        
                        list(overlays.values())
        
      )
      ,info,my_geolocaiton],id='map', zoom=12, center=(29.0730, -110.9559)), style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}
    ),

    html.Div(children=[html.H6(children='Map test run')])

]
,style={'color':colors['background']}                     
)




@app.callback(Output("info", "children"),
              [Input("map", "click_lat_lng")])
def map_click(click_lat_lng):
  #click_lat_lng (list of numbers; optional): Dash callback property. Receives [lat, lng] upon click.
  #coordinates="({:.3f}, {:.3f})".format(click_lat_lng[0],click_lat_lng[1])
  coordinates=click_lat_lng#[click_lat_lng[0],click_lat_lng[1]]
  #print(type(click_lat_lng)) #python class list
  return get_info(coordinates)





if __name__ == '__main__':
    app.run_server(debug=True, port=8150)
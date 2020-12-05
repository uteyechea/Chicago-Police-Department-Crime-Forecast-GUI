#from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_leaflet as dl
import numpy as np
import pandas as pd
import dash #Use for standalone window server

import os
from pathlib import Path
import sys

path = Path(os.getcwd())
sys.path.append(os.path.join(path.parent,'libs'))

import fake_forecast as fk 


forecast=fk.fake_forecast(number_of_predictions=20)

#Generate map polygons per crime per beat
overlays={}
for primary_type in forecast['primary_type'].unique():

    columns=forecast.loc[forecast['primary_type']==primary_type]
   
    polygons=dl.Polygon(positions=list(columns['polygon_vertices'])[:],color=str(columns['color'].unique()[0]))
    
    overlays[str(primary_type)]=dl.Overlay(dl.LayerGroup(polygons),name=primary_type,checked=True)



colors={
    'background':'#ffffff',
    'text':'#280330'
}

hermosillo_coordinates = (29.0730,-110.9559)


burglary={}
for i in range(0,10):

    latitude=np.random.randn()*.025+hermosillo_coordinates[0]
    longitude=np.random.randn()*.025+hermosillo_coordinates[1]
    top_left=[latitude,longitude]
    top_right=[latitude,longitude+0.005]
    bottom_left=[latitude-0.005,longitude+0.005]
    bottom_right=[latitude-0.005,longitude]
    
    burglary[i]=dl.Polygon(positions=[ top_left ,top_right,bottom_left,bottom_right ],color='purple')

murder={}
for i in range(0,4):

    latitude=np.random.randn()*.025+hermosillo_coordinates[0]
    longitude=np.random.randn()*.025+hermosillo_coordinates[1]
    top_left=[latitude,longitude]
    top_right=[latitude,longitude+0.005]
    bottom_left=[latitude-0.005,longitude+0.005]
    bottom_right=[latitude-0.005,longitude]
    
    murder[i]=dl.Polygon(positions=[ top_left ,top_right,bottom_left,bottom_right ],color='blue')

kidnapping={}
for i in range(0,6):

    latitude=np.random.randn()*.025+hermosillo_coordinates[0]
    longitude=np.random.randn()*.025+hermosillo_coordinates[1]
    top_left=[latitude,longitude]
    top_right=[latitude,longitude+0.005]
    bottom_left=[latitude-0.005,longitude+0.005]
    bottom_right=[latitude-0.005,longitude]
    
    kidnapping[i]=dl.Polygon(positions=[ top_left ,top_right,bottom_left,bottom_right ],color='red')
    
    

colors={
    'background':'#white',
    'text':'black'
}


# Some shapes.
#markers = [dl.Marker(position=[56, 10]), dl.CircleMarker(center=[55, 10])]
#polygon = dl.Polygon(positions=[[57, 10], [57, 11], [56, 11], [57, 10]])
#polygon2 = dl.Polygon(positions=[ [29.1,-110.955] ,[29.1,-110.95],[29.095,-110.95],[29.095,-110.955] ],color='red') 
#positions=[[top_left],[top_right],[bottom_right],[bottom_left]]
#polygon3 = dl.Polygon(positions=[ [29.160,-110.970] ,[29.160,-110.965],[29.155,-110.965],[29.155,-110.970] ]) 


# Some tile urls.
keys = ["Historical", "Live"]


# Create info control.
def get_info():
    header = [html.H4("Zone")]
    return header + [html.B(id='coordinates_output'), html.Br()]

    #if not feature:
    #    return header + ["Hoover over a colored square"]
    #return header + [html.B(feature["properties"]["name"]), html.Br(),
                     #"{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]
    #return header + [html.B(id='coordinates_output'), html.Br(),
    #                 "{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]

# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "11px", "left": "55px", "z-index": "1000"})

#Create geolocation control.
my_geolocaiton=dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}})


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']


# Create app.
#app = JupyterDash(__name__,external_stylesheets=external_stylesheets)
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
    
    html.Div(children=[html.H1(id='stats')]),

    html.Div(
      dl.Map([
      dl.LayersControl(
         [dl.BaseLayer(dl.TileLayer(), 
                        name=key, checked=key == "Live") for key in keys] +
                        
                        list(overlays.values())
        
      )
      ,info,my_geolocaiton],id='map', zoom=12, center=(29.0730, -110.9559)), style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}
    ),

    html.Div(children=[html.H6(children='Map test run')])

]
,style={'color':colors['background']}                     
)


@app.callback(Output(component_id='coordinates_output', component_property='children'),
              Output(component_id='stats', component_property='children'),
              [Input("map", "click_lat_lng")])
def map_click(click_lat_lng):
  #click_lat_lng (list of numbers; optional): Dash callback property. Receives [lat, lng] upon click.
  coordinates="({:.3f}, {:.3f})".format(*click_lat_lng)
  return coordinates,coordinates

@app.callback(Output("info", "children"), [Input("map", "click_lat_lng")])
def info_hover():
    return get_info()

if __name__ == '__main__':
    app.run_server(debug=True, port=8150)
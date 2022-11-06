import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import pydeck as pdk

number_of_vehicles = 0

st.set_page_config(
    page_title="Public transport Dashboard",
    page_icon="🚎",
    layout="wide")

st.title("🚎🚂 API Dashboard")

st.subheader('Tracking Public transport movements in NL 🇳🇱')
st.text('This dashboard is a proof of concept by Peter van Doorn. The hypothesis was: Can we obtain reliable public transport data and plot it on a map?')
st.text('the answer it turns out: YES!🎉')
st.text('Stay tuned for part 2 of this project 🥳')
with st.empty():
    while True:
        try:
            df = pd.pandas.read_json('https://bussie.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/API/V1/get_vehicles', orient='index')
            df = pd.DataFrame(df,columns=['latitude', 'type_vehicle','dataownercode', 'timestamp', 'longitude','vehiclenumber', 'speed'])
            
            bus_train = df[df.type_vehicle.eq('BusOrTram')]
            bus_train['type_vehicle'] = bus_train['type_vehicle'].replace(['BusOrTram'], '🚌')
            ns = df[df.type_vehicle.eq('Train')]
            ns['type_vehicle'] = ns['type_vehicle'].replace(['Train'], '🚂')



            
            #df['timestamp'] = df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %X'))
            st.pydeck_chart(pdk.Deck(
                tooltip ={
                    "html":
                        "<h4 style='color:black'>{type_vehicle} {dataownercode}</h4><b>Vehicle Number:</b> {vehiclenumber}  <br><b> Speed: </b>{speed} km/h <br><b> Latitude: </b> {latitude} <br> <b> longitude: </b> {longitude}<br> <b> Last Update:</b> {timestamp} <br> ",
                    "style": {
                        "backgroundColor": "lightgrey",
                        "color": "black",
                    }},
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=52.3676,
                    longitude=4.9041,
                    zoom=12,
                    pitch=35,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=bus_train,
                        get_position='[longitude, latitude]',
                        radius_scale=6,
                        radius_min_pixels=10,
                        radius_max_pixels=5,
                        line_width_min_pixels=1,
                        get_fill_color=[136, 136, 136],
                        get_line_color=[8, 136, 0],
                        pickable=True

                    ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=ns,
                        get_position='[longitude, latitude]',
                        radius_scale=6,
                        radius_min_pixels=10,
                        radius_max_pixels=5,
                        line_width_min_pixels=1,
                        get_fill_color=[136, 8, 8],
                        get_line_color=[8, 136, 0],
                        pickable=True

                    ),
                ],
            ))
            time.sleep(5)
        except Exception as e: 
            print(e)
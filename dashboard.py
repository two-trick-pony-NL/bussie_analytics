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
st.text('This dashboard is a proof of concept by Peter van Doorn.')

with st.empty():
    while True:
        response = requests.get("https://bussie.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/API/V1/get_all_vehicle_information")
        response = response.json()
        df = pd.DataFrame.from_dict(response)
        df = df.T
        df = pd.DataFrame(df,columns=['latitude', 'longitude','vehiclenumber', 'dataownercode', 'timestamp'])
        df.dropna(how='all')  
        df = df[pd.to_numeric(df['latitude'], errors='coerce').notnull()]
        df = df[pd.to_numeric(df['longitude'], errors='coerce').notnull()]

        st.pydeck_chart(pdk.Deck(
                tooltip ={
                    "html":
                        "<h4 style='color:black'>{vehiclenumber} {dataownercode}</h4><b>Vehicle Number:</b> {vehiclenumber}  <br><b> Speed: </b>{speed} km/h <br><b> Latitude: </b> {latitude} <br> <b> longitude: </b> {longitude}<br> <b> Last Update:</b> {timestamp} <br> ",
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
                        data=df,
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
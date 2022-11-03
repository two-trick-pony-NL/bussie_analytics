import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import pydeck as pdk

number_of_vehicles = 0

st.set_page_config(
    page_title="Bussie Dashboard",
    page_icon="🚎",
    layout="wide")

st.title("Bussie API Dashboard")

st.subheader('Tracking Public transport movements 🇳🇱')

with st.empty():
    while True:
        try:
            df = pd.pandas.read_json('https://bussie.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/API/V1/get_vehicles', orient='index')
            df = pd.DataFrame(df,columns=['latitude', 'timestamp', 'longitude','dataownercode','lineplanningnumber','journeynumber','userstopcode','vehiclenumber'])
            df['timestamp'] = df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d %X'))
            st.pydeck_chart(pdk.Deck(
                tooltip ={
                    "html":
                        "<b>Line:</b> {lineplanningnumber} from operator: {dataownercode}<br/><b>Vehicle number: </b> {vehiclenumber} <br><b>To stationnumber:</b> {userstopcode} <br> <b>Journey</b> {journeynumber}<br/> <b>Updated:</b> {timestamp} ",
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
        except Exception as e: 
            print(e)
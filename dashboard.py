import pandas as pd
import streamlit as st
import requests
import time
from datetime import datetime
import pydeck as pdk

st.set_page_config(
    page_title="Public transport Dashboard",
    page_icon="🚎",
    layout="wide"
)

st.title("🚎🚂 API Dashboard")

st.subheader('Tracking Public transport movements in NL 🇳🇱')
st.text('This dashboard is a proof of concept by Peter van Doorn.')

# Sample custom SVG icons representing emojis for vehicles and stations
bus_icon_url = "data:image/png;base64,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"
station_icon_url = "data:image/png;base64,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"

with st.empty():
    while True:
        response_vehicles = requests.get("https://bussie.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/api/vehicles/inradius?center_longitude=52&center_latitude=5&radius=500&radius_unit=km")
        data_vehicles = response_vehicles.json()

        # Extract the "vehiclesInYourArea" list from the JSON response
        vehicles = data_vehicles.get("vehiclesInYourArea", [])

        # Convert the list to a pandas DataFrame for vehicles
        df_vehicles = pd.DataFrame(vehicles, columns=["vehiclenumber", "coordinates"])

        # Split the "coordinates" list into "latitude" and "longitude" columns
        df_vehicles[["latitude", "longitude"]] = pd.DataFrame(df_vehicles["coordinates"].to_list(), index=df_vehicles.index)
        df_vehicles.rename(columns={"vehiclenumber": "name"}, inplace=True)

        # Drop unnecessary columns and add the current time as "timestamp" for vehicles
        df_vehicles.drop(columns=["coordinates"], inplace=True)
        df_vehicles["timestamp"] = datetime.now().isoformat()

        # Drop rows with missing latitude or longitude values for vehicles
        df_vehicles.dropna(subset=["latitude", "longitude"], inplace=True)

        # Fetch station data only once if the station DataFrame is empty
        if "df_stations" not in st.session_state:
            response_stations = requests.get("https://bussie.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/api/stations/inradius?center_longitude=52&center_latitude=5&radius=500&radius_unit=km")
            data_stations = response_stations.json()

            # Extract the "stations" list from the JSON response
            stations = data_stations.get("stations", [])

            # Convert the list to a pandas DataFrame for stations
            df_stations = pd.DataFrame(stations, columns=['name', "coordinates"])

            # Split the "coordinates" list into "latitude" and "longitude" columns
            df_stations[["latitude", "longitude"]] = pd.DataFrame(df_stations["coordinates"].to_list(), index=df_stations.index)

            # Drop unnecessary columns for stations
            df_stations.drop(columns=["coordinates"], inplace=True)

            # Store the station DataFrame in the session state
            st.session_state.df_stations = df_stations

        else:
            # Retrieve the station DataFrame from the session state
            df_stations = st.session_state.df_stations

        # Add custom icons for vehicles and stations
        df_vehicles["icon_data"] = [{"url": bus_icon_url, "width": 100, "height": 100, "anchorY": 100}] * len(df_vehicles)
        df_stations["icon_data"] = [{"url": station_icon_url, "width": 100, "height": 100, "anchorY": 100}] * len(df_stations)

        # Initialize the deck with an empty DataFrame and an IconLayer for both vehicles and stations
        st.pydeck_chart(pdk.Deck(
            tooltip={
                "html":
                    "<h4 style='color:black'>{name}</h4><b><br><b> Latitude: </b> {latitude} <br> <b> longitude: </b> {longitude}<br> <b> Last Update:</b> {timestamp} <br> ",
                "style": {
                    "backgroundColor": "lightgrey",
                    "color": "black",
                }},
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=52.3676,
                longitude=4.9041,
                zoom=6,
                pitch=35,
            ),
            layers=[
                pdk.Layer(
                    'IconLayer',
                    data=df_vehicles,
                    get_icon="icon_data",
                    get_position='[longitude, latitude]',
                    size_scale=15,
                    size_min_pixels=10,
                    pickable=True,
                    auto_highlight=True,
                    tooltip={
                        "style": {
                            "backgroundColor": "lightgrey",
                            "color": "black",
                        }
                    }
                ),
                pdk.Layer(
                    'IconLayer',
                    data=df_stations,
                    get_icon="icon_data",
                    get_position='[longitude, latitude]',
                    size_scale=50,
                    size_min_pixels=10,
                    pickable=True,
                    auto_highlight=True,
                    tooltip={
                        "style": {
                            "backgroundColor": "lightgrey",
                            "color": "black",
                        }
                    }
                ),
            ],
        ))

        # Wait for 5 seconds before updating the map
        time.sleep(5)

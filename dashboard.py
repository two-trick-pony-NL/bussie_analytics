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
bus_icon_url = "https://raw.githubusercontent.com/two-trick-pony-NL/bussie_analytics/main/assets/train.png"
station_icon_url = "https://raw.githubusercontent.com/two-trick-pony-NL/bussie_analytics/main/assets/station.png"

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
                    size_scale=25,
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
                    size_scale=35,
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

import pandas as pd
import streamlit as st
import requests
import time
from datetime import datetime
import pydeck as pdk

st.subheader('Tracking Public transport movements in NL 🇳🇱')
st.text('This dashboard is a proof of concept by Peter van Doorn.')

# Create an initial empty DataFrame and an empty deck
df = pd.DataFrame(columns=["vehiclenumber", "latitude", "longitude"])
deck = pdk.Deck()

while True:
    response = requests.get("https://bussie.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/api/vehicles/inradius?center_longitude=52&center_latitude=5&radius=500&radius_unit=km")
    data = response.json()

    # Extract the "vehiclesInYourArea" list from the JSON response
    vehicles = data.get("vehiclesInYourArea", [])

    # Convert the list to a pandas DataFrame
    new_df = pd.DataFrame(vehicles, columns=["vehiclenumber", "coordinates"])

    # Split the "coordinates" list into "latitude" and "longitude" columns
    new_df[["latitude", "longitude"]] = pd.DataFrame(new_df["coordinates"].to_list(), index=new_df.index)

    # Drop unnecessary columns and add the current time as "timestamp"
    new_df.drop(columns=["coordinates"], inplace=True)
    new_df["timestamp"] = datetime.now()

    # Drop rows with missing latitude or longitude values
    new_df.dropna(subset=["latitude", "longitude"], inplace=True)

    # Append the new data to the existing DataFrame
    df = pd.concat([df, new_df], ignore_index=True)

    # Update the deck with the new data
    deck = pdk.Deck(
        tooltip={
            "html":
                "<h4 style='color:black'>{vehiclenumber}</h4><b>Vehicle Number:</b> {vehiclenumber}  <br>"
                "<b> Latitude: </b> {latitude} <br> <b> Longitude: </b> {longitude}<br> "
                "<b> Last Update:</b> {timestamp} <br> ",
            "style": {
                "backgroundColor": "lightgrey",
                "color": "black",
            }
        },
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
    )

    # Display the updated deck in the Streamlit app
    st.pydeck_chart(deck)

    # Wait for 5 seconds before updating the map
    time.sleep(5)

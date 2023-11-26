import streamlit as st
import pandas as pd
import requests
import pydeck as pdk

# Function to load data from the API
@st.cache_data
def load_data():
    API_URL = 'https://bloomington.data.socrata.com/resource/aw6y-t4ix.json'
    response = requests.get(API_URL)
    data = response.json()
    return pd.DataFrame(data)

# Function to plot the map using PyDeck
def plot_map(dataframe):
    view_state = pdk.ViewState(
        latitude=dataframe['lat'].mean(),
        longitude=dataframe['long'].mean(),
        zoom=12,
        pitch=0
    )

    layer = pdk.Layer(
        'ScatterplotLayer',
        data=dataframe,
        get_position='[long, lat]',
        get_color='[200, 30, 0, 160]',
        get_radius=100,
    )

    return pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer]
    )

# Main Streamlit app
def main():
    st.title("Service Request Visualization App")
    st.write("This app displays service requests on a map based on their geolocation data.")

    df = load_data()

    # Convert latitude and longitude to numeric
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['long'] = pd.to_numeric(df['long'], errors='coerce')

    map = plot_map(df)

    st.pydeck_chart(map)

if __name__ == "__main__":
    main()

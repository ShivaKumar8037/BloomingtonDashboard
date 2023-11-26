import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
from datetime import datetime

# Function to load data
@st.cache_data
def load_data():
    data = pd.read_csv('Cleaned_Open311.csv')
    # # Convert datetime fields to datetime objects
    data['requested_datetime'] = pd.to_datetime(data['requested_datetime'])
    data['updated_datetime'] = pd.to_datetime(data['updated_datetime'])
    data['closed_date'] = pd.to_datetime(data['closed_date'])
    return data

# Function to calculate average response time
def calculate_avg_response_time(data):
    # Filter out data where either requested or closed date is missing
    filtered_data = data.dropna(subset=['requested_datetime', 'closed_date'])
    # Calculate response time in days
    response_time = (filtered_data['closed_date'] - filtered_data['requested_datetime']).dt.days
    return response_time.mean()

# def create_color_mapping(data_column):
#     unique_values = data_column.unique()
#     # Create a color palette with a distinct color for each unique value
#     colors = plt.cm.tab20(np.linspace(0, 1, len(unique_values)))
#     color_mapping = {value: colors[i].tolist() for i, value in enumerate(unique_values)}
#     # Convert colors from 0-1 range to 0-255 range and return mapping
#     return {key: [int(color * 255) for color in value] for key, value in color_mapping.items()}

# Main app
def main():
    st.title("City of Bloomington Service Request Dashboard")

    data = load_data()

    # Sidebar for filters
    st.sidebar.title("Filters")
    request_type = st.sidebar.multiselect("Select Request Type", options=data['service_name'].unique())

    # Ensure default dates are within the range of the data
    min_date = data['requested_datetime'].min().date()
    max_date = data['requested_datetime'].max().date()
    default_start = min_date
    default_end = max_date if max_date > min_date else min_date

    start_date = st.sidebar.date_input("Start Date", value=default_start, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", value=default_end, min_value=start_date, max_value=max_date)

    # Filtering data based on selection
    if request_type:
        data = data[data['service_name'].isin(request_type)]
    data = data[(data['requested_datetime'].dt.date >= start_date) & (data['requested_datetime'].dt.date <= end_date)]

    # Display summary statistics
    if not data.empty:

        # color_mapping = create_color_mapping(data['service_name'])
        # data['color'] = data['service_name'].apply(lambda x: color_mapping[x])

        st.header("Summary Statistics")

        # Total number of requests
        total_requests = len(data)
        st.metric(label="Total Number of Requests", value=total_requests)

        # Average response time (in days)
        avg_response_time = calculate_avg_response_time(data)
        st.metric(label="Average Response Time (Days)", value=f"{avg_response_time:.2f}")

        # Number of unique request types
        unique_request_types = data['service_name'].nunique()
        st.metric(label="Unique Request Types", value=unique_request_types)

        #Tooltip for map
        data['requested_datetime_str'] = data['requested_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        data['closed_date_str'] = data['closed_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        tooltip = {
        "html": "<b>Service Name:</b> {service_name}<br/>"
                "<b>Description:</b> {description}<br/>"
                "<b>Status:</b> {status_description}<br/>"
                "<b>Requested:</b> {requested_datetime_str}<br/>"
                "<b>Closed:</b> {closed_date_str}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
        

        # Map rendering
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v12',
            initial_view_state=pdk.ViewState(
                latitude=data['lat'].mean(),
                longitude=data['long'].mean(),
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=data,
                    get_position=['long', 'lat'],
                    get_color=[200, 30, 0, 160],
                    get_radius=100,
                    pickable = True
                ),
            ],
            tooltip=tooltip
        ))
    else:
        st.write("No data available for the selected filters.")

if __name__ == "__main__":
    main()

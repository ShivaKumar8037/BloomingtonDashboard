import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
from wordcloud import WordCloud
import altair as alt

# Function to load data
@st.cache_data
def load_data(start_date=None, end_date=None):
    # Load the dataset
    data = pd.read_csv('Cleaned_Open311.csv')
    # Convert datetime fields to datetime objects
    data['requested_datetime'] = pd.to_datetime(data['requested_datetime'])
    data['updated_datetime'] = pd.to_datetime(data['updated_datetime'])
    data['closed_date'] = pd.to_datetime(data['closed_date'])
    data['resolution_days'] = (data['closed_date'] - data['requested_datetime']).dt.days

    # Filter data based on the date range provided
    if start_date is not None and end_date is not None:
        data = data[(data['requested_datetime'].dt.date >= start_date) & 
                    (data['requested_datetime'].dt.date <= end_date)]
    else:
        # Default to loading data from the current year
        current_year = datetime.now().year
        data = data[data['requested_datetime'].dt.year == current_year]

    return data

# Function to generate a word cloud from the request descriptions
def generate_word_cloud(data, column='description'):
    text = ' '.join(description for description in data[column].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(text)
    
    # Display the generated WordCloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt) 

# Function to calculate average response time
def calculate_avg_response_time(data):
    # Filter out data where either requested or closed date is missing
    filtered_data = data.dropna(subset=['requested_datetime', 'closed_date'])
    # Calculate response time in days
    response_time = (filtered_data['closed_date'] - filtered_data['requested_datetime']).dt.days
    return response_time.mean()


# Main app
def main():
    st.title("City of Bloomington Service Request Dashboard")

    # Sidebar for data loading options
    st.sidebar.title("Data Loading Options")
    min_date = datetime(1995, 1, 1)
    max_date = datetime.now()

    # Set default start date to the beginning of the current year
    default_start_date = datetime(datetime.now().year, 1, 1)

    start_date = st.sidebar.date_input("Start Date", value=default_start_date, min_value=min_date, max_value=max_date, key='start_date')
    end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date, key='end_date')

    # Load data based on selected date range or default to the current year
    data = load_data(start_date, end_date)

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

    #Heatmap
    st.sidebar.title("Map Type")
    use_heatmap = st.sidebar.checkbox("Show Heatmap")
    # Display 
    if not data.empty:
        # Tooltip configuration for the map
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

        # Define layers based on heatmap checkbox
        layers = []
        if use_heatmap:
            # Create a heatmap layer if the checkbox is checked
            heatmap_layer = pdk.Layer(
                "HeatmapLayer",
                data=data,
                get_position=['long', 'lat'],
                opacity=0.5,
                get_weight="resolution_days",  # Weight based on resolution days
                color_range=[
            [0, 0, 255],     # Blue for lowest values
            [0, 255, 0],     # Green for low to medium values
            [255, 255, 0],   # Yellow for medium to high values
            [255, 0, 0]      # Red for the highest values
        ],
        threshold=0.05,    # Fine-tune this for your data
        radius_pixels=30,
            )
            layers.append(heatmap_layer)
        else:
            # Create a scatterplot layer if the checkbox is not checked
            scatterplot_layer = pdk.Layer(
                'ScatterplotLayer',
                data=data,
                get_position=['long', 'lat'],
                get_color=[200, 30, 0, 160],
                get_radius=50,
                pickable=True
            )
            layers.append(scatterplot_layer)

        # Map rendering with layers
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v12',
            initial_view_state=pdk.ViewState(
                latitude=data['lat'].mean(),
                longitude=data['long'].mean(),
                zoom=11,
            ),
            layers=layers,  # Use layers list here
            tooltip=tooltip
        ))

    else:
        st.write("No data available for the selected filters.")
    # Summary statistics
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

    # Interactive bar chart of number of requests by service type
    st.header("Number of Requests by Service Type")
    requests_by_service_type = data['service_name'].value_counts().reset_index()
    requests_by_service_type.columns = ['service_name', 'count']
    requests_by_service_type = requests_by_service_type.sort_values('count', ascending=False)

    chart = alt.Chart(requests_by_service_type).mark_bar().encode(
        y=alt.Y('count:Q', title='Number of Requests'),
        x=alt.X('service_name:N', title='Service Type', sort='-y')  # Sort bars based on the count
    ).properties(
        width=alt.Step(20)  # Adjust the step width for bar thickness
    )

    st.altair_chart(chart, use_container_width=True)


    if st.checkbox('Show Word Cloud'):
        generate_word_cloud(data, column='description')
if __name__ == "__main__":
    main()
#check
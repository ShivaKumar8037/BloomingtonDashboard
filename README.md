# City of Bloomington Service Request Dashboard

## Overview

The City of Bloomington Service Request Dashboard is an advanced web application designed to analyze and visualize service request data from the City of Bloomington. This interactive dashboard is developed as part of a master's project in data visualization, using a dataset that has undergone extensive exploratory data analysis (EDA) and cleaning processes.

## Data Source and Preparation

- **Original Dataset URL**: Data obtained from Bloomington's Open311 system.
- **Data Cleaning and EDA**: Performed in a Jupyter notebook, enhancing data quality by addressing inconsistencies, missing values, and outliers.
- **Cleaned Dataset**: 'Cleaned_Open311.csv' with 111K rows and 17 columns, including fields like service_request_id, requested_datetime, updated_datetime, closed_date, status_description, and service_name.
- **Service Report Page**: Bloomington uReport for public access to service requests.

## Key Features

1. **Dynamic Data Loading**: Users can select a date range to load data, enhancing performance through batch processing.
2. **Interactive Filters**: Tailor the dashboard view with filters based on service request types.
3. **Map-Based Interaction**: Features interactive geospatial visualizations like heatmaps and scatterplots using PyDeck.
4. **Summary Statistics**: Displays metrics such as total requests, average response time, and unique request types.
5. **Temporal Analysis**: Includes visualizations like Service Requests Over Time, Average Response Time by Month, and Requests by Service Type.
6. **Word Cloud Visualization**: Generates a word cloud from service request descriptions to highlight common themes and issues.

## Technology Stack

- **Python Libraries**: Streamlit, Pandas, Numpy, PyDeck, Matplotlib, Altair, WordCloud, and Datetime.
- **Data Analysis and Cleaning**: Conducted in a Jupyter notebook using Python.

## Application Structure

- `load_data`: Efficiently handles data loading with caching.
- `plot_service_requests_over_time`: Generates time-series visualizations.
- `plot_avg_response_time_by_month`: Creates bar charts for average response times.
- `generate_word_cloud`: Produces word clouds from request descriptions.
- `calculate_avg_response_time`: Computes average response time for service requests.
- `main`: Core function for configuring and running the Streamlit application.

## User Interaction

The dashboard offers an intuitive interface for data exploration, allowing users to select visualization options, apply filters, and interact with dynamic charts and maps. This approach enhances the understanding of service request data.

## Conclusion

The City of Bloomington Service Request Dashboard is a pivotal tool in public administration, promoting civic engagement, informed decision-making, and transparency. By leveraging a thoroughly cleaned and analyzed dataset, this application highlights the impact of data-driven insights in public service management. It's an exemplary project for a master's degree in data visualization.

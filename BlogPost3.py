import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

data = pd.read_csv('accident_data.csv')
data = data.drop(columns = ['Unnamed: 0'])

st.title('Fatal Car Crashes in Utah')

tabs = st.tabs(['Variables', 'Raw Data Table', 'Day of Week Graph', 'Weather Graph', 'Lighting and Population Graph'])
tab1, tab2, tab3, tab4, tab5 = tabs

st.sidebar.header('Filter Data')

with tab1:
    st.title('Variables in dataset')
    st.markdown('city: City in Utah where crash took place<br>county: County in Utah where crash took place<br>year: Year crash took place<br>day_of_week: Day of week (Sunday-Saturday) on which crash occured<br>hospital: Whether passengers involved in crash were transported to hospital<br>lighting: How area of road was lit<br>population_type: What type of area crash took place in (Urban or Rural)<br>weather: Weather conditions at time of crash<br>fatalities: Number of fatalities resulting from crash', unsafe_allow_html = True)

with tab2:
    city = st.sidebar.multiselect('City', options = data['city'].unique(), default = [])
    
    filtered_data = data[
        (data['city'].isin(city))
    ]

    st.header('Data by City')
    st.dataframe(filtered_data)

with tab3:
    crashes_by_day = data.groupby('day_of_week')['fatalities'].sum().reset_index()

    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    crashes_by_day['day_of_week'] = pd.Categorical(crashes_by_day['day_of_week'], categories = ordered_days, ordered = True)
    crashes_by_day = crashes_by_day.sort_values('day_of_week')

    chart = alt.Chart(crashes_by_day).mark_line(point = True).encode(
        x = 'day_of_week',
        y = 'fatalities',
        tooltip = ['day_of_week', 'fatalities']
    ).properties(
        title='Number of Fatalities by Day of the Week'
    )

    st.altair_chart(chart, use_container_width = True)

color_scale_2 = alt.Scale(domain = ['Clear', 'Cloudy', 'Rain', 'Fog, Smog, Smoke', 'Snow', 'Severe Crosswinds', 'Blowing Snow', 'Sleet or Hail'],
                          range = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#8A2BE2', '#FF4500', '#8B4513', '#40E0D0'])

with tab4:
    st.header(f'Average Fatalities by Weather Type')
    
    weather_categories = {
        'Clear': 'Mild',
        'Cloudy': 'Mild',
        'Rain': 'Moderate',
        'Fog, Smog, Smoke': 'Moderate',
        'Snow': 'Moderate',
        'Severe Crosswinds': 'Severe',
        'Blowing Snow': 'Severe',
        'Sleet or Hail': 'Severe'
    }

    data['weather_category'] = data['weather'].map(weather_categories)

    category_options = ['Mild', 'Moderate', 'Severe']
    selected_category = st.sidebar.radio('Select Weather Category', category_options, index = 0)

    filtered_data = data[data['weather_category'] == selected_category]

    fatalities_by_weather = filtered_data.groupby('weather')['fatalities'].mean().reset_index()

    chart = alt.Chart(fatalities_by_weather).mark_bar().encode(
    x = alt.X('weather', sort='-y'),  # Sort the bars by the average fatalities
    y = 'fatalities',
    color=alt.Color('weather', scale = color_scale_2),
    tooltip = ['weather', 'fatalities'])
    
    st.altair_chart(chart, use_container_width=True)

color_scale = alt.Scale(domain = ['Daylight', 'Dark - Lighted', 'Dark - Not Lighted', 'Dawn', 'Dusk'],
                        range = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])

with tab5:
    st.header(f'Fatalities by Lighting Condition and Population Type')

    selected_population_type = st.sidebar.radio('Select Population Type',
                                                options = data['population_type'].unique(),
                                                index = 0)

    filtered_by_population = data[data['population_type'] == selected_population_type]

    chart_data = filtered_by_population.groupby('lighting')['fatalities'].sum().reset_index()

    chart = alt.Chart(chart_data).mark_bar().encode(
        x = alt.X('lighting', sort=['Daylight', 'Dark - Lighted', 'Dark - Not Lighted', 'Dawn', 'Dusk']),
        y = 'fatalities',
        color=alt.Color('lighting', scale=color_scale),
        tooltip = ['lighting', 'fatalities'])
    
    st.altair_chart(chart, use_container_width=True)


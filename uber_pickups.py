# Port number = 8505
# Port server = https://coding.ai-camp.org/7f8de42c-82ae-468d-9553-1ec9f3c41b82/server/8505/ 

import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pickups in NYC BEFORE PANDEMIC")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
# amazonaws.com = Amazon web-services

# Python Decorator changes the function's behavior, and the input parameter is a function. 
@st.cache # st.cache stands for streamlit.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
    
# write a dataframe.
st.write(data)

# Generating histogram
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

# NOW WE do a MAP!
st.subheader('Map of all pickups')
st.map(data)


# NOW WE do a FILTERED MAP!
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter] # Look at the Date Column/Raw Data, only looking at time (dt) and hour, for all these rows, true or false, because the hour is going to be equal to 17 or not. Only show map on filtered data.

st.markdown(f'Map of all pickups at **{hour_to_filter}:00**')
st.map(filtered_data)

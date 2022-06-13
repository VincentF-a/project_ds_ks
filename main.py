import streamlit as st
import pandas as pd
import re

from process.data_process import retrieve_cities, retrieve_years
from content import display

# Streamlit states

if 'past_migrations' not in st.session_state:
    st.session_state['past_migrations'] = False

st.sidebar.title('Welcome to our project')

st.sidebar.markdown('This project is aimed at displaying the **demographic evolution** inside South Korea and predict its future evolutions.')
list_cities = st.sidebar.multiselect('Select the cities and provinces',retrieve_cities(),default=retrieve_cities())

start_year_col, end_year_col = st.sidebar.columns(2)
list_years = retrieve_years()
with start_year_col:
    start_year = st.selectbox('Select the start year', options=list_years)
with end_year_col:
    updated_years = list_years[list_years.index(start_year):]
    end_year = st.selectbox('Select the end year', options=updated_years, index=len(updated_years)-1)

if st.sidebar.button('Visualize the migrations') or st.session_state['past_migrations']:
    st.session_state['past_migrations'] = True
    display(list_cities, start_year, end_year)


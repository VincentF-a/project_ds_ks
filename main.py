import streamlit as st
import pandas as pd
import re

from data_process import data_process as dp

st.sidebar.title('Welcome to our project')

st.sidebar.markdown('This project is aimed at displaying the **demographic evolution** inside South Korea and predict its future evolutions.')
st.sidebar.multiselect('Select the cities and provinces',dp.list_cities,default=dp.list_cities)

start_year_col, end_year_col = st.sidebar.columns(2)
with start_year_col:
    start_year = st.selectbox('Select the start year', options=dp.list_years)
with end_year_col:
    updated_years = dp.list_years[dp.list_years.index(start_year):]
    end_year = st.selectbox('Select the end year', options=updated_years, index=len(updated_years)-1)

if st.sidebar.button('Visualize the results'):
    st.markdown('todo')


st.dataframe(dp.df_migration)
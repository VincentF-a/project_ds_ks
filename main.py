import streamlit as st
import pandas as pd
import re

from process.data_process import retrieve_cities, retrieve_years
from content import display

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

if st.sidebar.button('Visualize the results'):
    display(list_cities, start_year, end_year)


"""st.dataframe(dp.df_migration)

df_cities = pd.read_csv('data/cities.csv')

st.map(df_cities)

df_migration_test = dp.formatting_df_years(dp.df_migration_net, 1970, 1998)
st.dataframe(df_migration_test)"""

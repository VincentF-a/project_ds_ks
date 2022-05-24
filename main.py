import streamlit as st
import pandas as pd

from data_process import data_process as dp

st.sidebar.title('Welcome to our project')

list_cities = [city for city in dp.list_cities_out if city in dp.list_cities_in]

st.dataframe(dp.df_migration)
st.markdown(dp.df_migration.shape)

st.markdown(dp.list_cities_in)
st.markdown(dp.list_cities_out)
st.markdown(list_cities)
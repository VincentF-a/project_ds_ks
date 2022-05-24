import streamlit as st
import pandas as pd
import re

from data_process import data_process as dp

st.sidebar.title('Welcome to our project')

st.sidebar.markdown('This project is aimed at displaying the **demographic evolution** inside South Korea and predict its future evolutions.')
st.sidebar.multiselect('Select the cities',dp.list_cities)

st.sidebar.slider('Select a time frame', min_value=dp.list_quarters[0], max_value=dp.list_quarters[-1], value=dp.list_quarters)

st.dataframe(dp.df_migration)
st.markdown(dp.df_migration.shape)

st.markdown(dp.list_cities_in)
st.markdown(dp.list_cities_out)
st.markdown(dp.list_cities)

st.markdown(dp.raw_list_quarters)
st.markdown(dp.list_quarters)
import streamlit as st
import altair as alt
import pandas as pd
from st_aggrid import AgGrid

from process import data_retrieve as dr
from process import data_process as dp
from process.data_visualization import plot_korea_viz

def display_analyze(list_cities: list, year_start: int, year_end: int):
    df_migration = dp.pre_processing(dr.df_migration)
    df_migration = dp.formatting_df_years(df_migration,year_start, year_end, list_cities)
    
    data_choice = st.selectbox('Please select the data type', ['Past data', 'Prediction data'])

    df_positions = dr.df_positions

    if data_choice == "Past data":

        year_selected = st.slider('Please select a year', year_start, year_end, step=1)

        df_migration_filtered = df_migration[
            (df_migration[
                'By district to move-out'
                ] == 'Whole Country') & (df_migration['By district to move-in'] != 'Whole Country')]
        
        df_migration_filtered.drop(columns=df_migration_filtered.columns[0], axis=1, inplace=True)

        df_migration_filtered.rename(columns={'By district to move-in':'name'}, inplace=True)

        df_migration_filtered = pd.merge(df_migration_filtered, df_positions, on=['name'], how='left')  

        df_migration_filtered[str(year_selected)] = df_migration_filtered[(year_selected)].apply(pd.to_numeric)

        df_migration_to_plot = dp.assign_neg_from_col(df_migration_filtered[[str(year_selected),'latitude', 'longitude']])
        df_migration_to_plot = df_migration_to_plot.sort_values(by=['positive'])

        df_migration_to_plot.rename(columns = {str(year_selected):'values'}, inplace = True)

        st.pydeck_chart(plot_korea_viz(df_migration_to_plot))

        if st.button('Verify the data'):
            AgGrid(df_migration_filtered[['name', str(year_selected)]])
    
    else:
        df_migration = dp.formatting_predictions(dr.df_predictions)

        df_migration = dp.concat_years_pred(df_migration)

        year_selected = st.slider('Please select a year', int(list(df_migration)[1]), int(list(df_migration)[-1]), step=1)

        df_migration_to_plot = df_migration.rename(columns = {'city':'name', str(year_selected):'values'})
        df_migration_to_plot = pd.merge(df_migration_to_plot, df_positions, on=['name'], how='left')
        
        df_migration_to_plot['values'] = df_migration_to_plot['values'].apply(pd.to_numeric)

        st.pydeck_chart(plot_korea_viz(df_migration_to_plot))

        if st.button('Verify the data'):
            AgGrid(df_migration[['city', str(year_selected)]])
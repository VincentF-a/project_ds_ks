import streamlit as st
import altair as alt
import pandas as pd
from st_aggrid import AgGrid

from process import data_retrieve as dr
from process.data_process import pre_processing, formatting_df_years, remove_neg_from_col
from process.data_visualization import plot_korea_viz

def display(list_cities: list, year_start: int, year_end: int):
    df_migration = pre_processing(dr.df_migration)
    df_migration = formatting_df_years(df_migration,year_start, year_end, list_cities)
    
    df_positions = dr.df_positions

    df_migration_filtered = df_migration[
        (df_migration[
            'By district to move-out'
            ] == 'Whole Country') & (df_migration['By district to move-in'] != 'Whole Country')]
    
    df_migration_filtered.drop(columns=df_migration_filtered.columns[0], axis=1, inplace=True)

    df_migration_filtered.rename(columns={'By district to move-in':'name'}, inplace=True)

    df_migration_filtered = pd.merge(df_migration_filtered, df_positions, on=['name'], how='left')

    st.dataframe(df_migration_filtered)

    year_selected = st.selectbox("Please select a year", [*range(year_start, year_end+1, 1)])

    df_migration_filtered[str(year_selected)] = df_migration_filtered[(year_selected)].apply(pd.to_numeric)

    """chart_cities = alt.Chart(df_migration_filtered).mark_point().encode(
        latitude='latitude',
        longitude='longitude',
        color=str(year_selected)
    )
    st.dataframe(df_migration_filtered)

    st.altair_chart(chart_cities,use_container_width=True)"""

    df_migration_to_plot = remove_neg_from_col(df_migration_filtered[[str(year_selected),'latitude', 'longitude']])
    st.dataframe(df_migration_to_plot)

    st.pydeck_chart(plot_korea_viz(df_migration_to_plot))

    """st.markdown('Positive Migration')
    st.pydeck_chart(plot_korea_viz(df_positive[['latitude', 'longitude']]))
    st.markdown('Negative Migration')
    st.pydeck_chart(plot_korea_viz(df_negative[['latitude', 'longitude']]))"""

    if st.button('Verify the data'):
        AgGrid(df_migration_filtered[['name', str(year_selected)]])
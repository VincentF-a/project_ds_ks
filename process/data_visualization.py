import pydeck as pdk
import numpy as np
import pandas as pd

def plot_korea_viz(df: pd.DataFrame):
    return pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=35.352376,
            longitude=128.090598,
            zoom=6,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ColumnLayer',
                data=df,
                get_position='[longitude, latitude]', 
                get_elevation='values/100',
                extruded=True,
                radius=4000,
                elevation_scale=50,
                get_fill_color='positive',
            ),
        ],
    )
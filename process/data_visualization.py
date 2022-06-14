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
                get_elevation=df.columns[0],
                radius=2000,
                elevation_scale=50,
                pickable=True,
                auto_highlight=True,
                get_fill_color=df.columns[-1],
            ),
        ],
    )
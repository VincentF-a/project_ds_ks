import pandas as pd
import re
from datetime import datetime as dt

from process.data_retrieve import df_migration

from zmq import device

def pre_processing(df_migration: pd.DataFrame) -> pd.DataFrame:
    df_migration_net = df_migration[df_migration['Item']=="Net migrants[Person]"]
    return df_migration_net

def retrieve_cities(df_migration: pd.DataFrame = df_migration) -> list:
    list_cities_out = df_migration['By district to move-out'].unique()
    list_cities_in = df_migration['By district to move-in'].unique()
    list_cities = [city for city in list_cities_out if city in list_cities_in]
    return list_cities

def retrieve_years(df_migration: pd.DataFrame = df_migration) -> list:
    raw_list_quarters = df_migration.columns.values.tolist()
    list_quarters = [quarter for quarter in raw_list_quarters if re.match(r'[1-2][0-9][0-9][0-9]',quarter)]
    list_years = list(set([int(quarter[:4]) for quarter in list_quarters]))
    return list_years

def formatting_df_years(df_migration: pd.DataFrame, year_start: int, year_end: int, list_cities:list) -> pd.DataFrame:
    df_migration = df_migration.fillna(0)
    list_years = [*range(year_start, year_end+1, 1)]
    list_cols_index = ['By district to move-out', 'By district to move-in', 'Item', 'UNIT']
    list_cols = list_cols_index + [
            year_col for year_col in list(df_migration)[4:] if int(year_col[:4]) in list_years]
    df_migration = df_migration[list_cols]
    for year in list_years:
        if year == 2022:
            list_quarters = ['2022.1/4']
            df_migration[list_quarters] = df_migration[list_quarters].apply(pd.to_numeric)
            df_migration[year] = df_migration[list_quarters[0]].map(int)
        else:
            list_quarters = [f"{year}.{i+1}/4" for i in range(4)]
            df_migration[list_quarters] = df_migration[list_quarters].apply(pd.to_numeric)
            df_migration[year] = df_migration[list_quarters[0]].map(int) + df_migration[list_quarters[1]].map(int) + df_migration[list_quarters[2]].map(int) + df_migration[list_quarters[3]].map(int)
    df_migration = df_migration[list_cols_index+list_years]
    df_migration = df_migration[df_migration['By district to move-in'].isin(list_cities)]
    return df_migration

import pandas as pd
import re
from datetime import datetime as dt

from process.data_retrieve import df_migration

from zmq import device

import streamlit as st

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

def assign_neg_from_col(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df[df.columns[0]]!=0]
    df['positive'] = df[df.columns[0]].apply(return_pos_neg)
    df = df.apply(abs)
    return df

def return_pos_neg(value: int) -> bool:
    return value > 0

def formatting_predictions(df: pd.DataFrame) -> pd.DataFrame:
    col_cities = [city for city in df.columns if "predicted" in city]
    return df.pivot_table(columns='Date', values=col_cities).rename_axis('city').reset_index()

def concat_years_pred(df: pd.DataFrame) -> pd.DataFrame:
    list_years =[year_col[:4] for year_col in list(df) if 'city' not in year_col]
    for year in list_years:
        if year == '2020':
            list_months = ['2020-11-01', '2020-12-01']
        else:    
            list_months = [f"{year}-0{i+1}-01" for i in range(9)] + [f'{year}-10-01', f'{year}-11-01', f'{year}-12-01']
            if year == '2070':
                list_months.pop()
        df[year] = df[list_months].sum(axis=1)
    
    list_cols_keep = [col for col in list(df) if "-" not in col]
    df['city'] = df['city'].map(lambda x: x.rstrip('_predicted'))
    return df[list_cols_keep]
    #return df[[cols_keep]]

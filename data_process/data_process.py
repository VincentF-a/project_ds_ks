import pandas as pd
import re
from datetime import datetime as dt

from zmq import device

df_migration = pd.read_csv('data/dataset_past_migrations.csv')
df_positions = pd.read_csv('data/cities.csv')

df_migration.drop(df_migration.columns[len(df_migration.columns)-1], axis=1, inplace=True)

list_cities_out = df_migration['By district to move-out'].unique()
list_cities_in = df_migration['By district to move-in'].unique()

list_cities = [city for city in list_cities_out if city in list_cities_in]

raw_list_quarters = df_migration.columns.values.tolist()
list_quarters = [quarter for quarter in raw_list_quarters if re.match(r'[1-2][0-9][0-9][0-9]',quarter)]
list_years = list(set([int(quarter[:4]) for quarter in list_quarters]))


# df migrations filtering and formatting 

df_migration_net = df_migration[df_migration['Item']=="Net migrants[Person]"]



def formatting_df_years(df_migration: pd.DataFrame, year_start: int, year_end: int):
    df_migration = df_migration.fillna(0)
    list_years = [*range(year_start, year_end+1, 1)]
    list_cols_index = ['By district to move-out', 'By district to move-in', 'Item', 'UNIT']
    list_cols = list_cols_index + [
            year_col for year_col in list(df_migration)[4:] if int(year_col[:4]) in list_years]
    df_migration = df_migration[list_cols]
    for year in list_years:
        list_quarters = [f"{year}.{i+1}/4" for i in range(4)]
        df_migration[list_quarters] = df_migration[list_quarters].apply(pd.to_numeric)
        df_migration[year] = df_migration[list_quarters[0]].map(int) + df_migration[list_quarters[1]].map(int) + df_migration[list_quarters[2]].map(int) + df_migration[list_quarters[3]].map(int)
    df_migration = df_migration[list_cols_index+list_years]
    return df_migration


import pandas as pd
import re
from datetime import datetime as dt

df_migration = pd.read_csv('data/dataset_past_migrations.csv')

list_cities_out = df_migration['By district to move-out'].unique()
list_cities_in = df_migration['By district to move-in'].unique()

list_cities = [city for city in list_cities_out if city in list_cities_in]

raw_list_quarters = df_migration.columns.values.tolist()
list_quarters = [quarter for quarter in raw_list_quarters if re.match(r'[1-2][0-9][0-9][0-9]',quarter)]
list_years = list(set([int(quarter[:4]) for quarter in list_quarters]))

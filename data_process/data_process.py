import pandas as pd

df_migration = pd.read_csv('data/dataset_past_migrations.csv')

list_cities_out = df_migration['By district to move-out'].unique()
list_cities_in = df_migration['By district to move-in'].unique()
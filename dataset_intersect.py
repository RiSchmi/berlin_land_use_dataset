# full dataframe imputed, merge with pollution data (based on ID) & meteorological (based on time step)
import pandas as pd 

sites_coord = pd.read_csv('datasets/df_spatial_only.csv')
sites_coord['id'] = sites_coord['id'].apply(lambda x : x.lower().replace(' ', '')[:5])

# load and merge pollution data
NO2_hourly = pd.read_csv('datasets/df_pollution_2023_berlin_imputed.csv')
df_2023_imputed = pd.merge(NO2_hourly, sites_coord, on = 'id', how= 'outer') # bind

# load and merge meteorological data (w/ imputed missing values)
meteorological_hourly = pd.read_csv('datasets/df_meteorological_impute.csv')
df_2023_imputed = pd.merge(df_2023_imputed, meteorological_hourly, on = 'MESS_DATUM', how= 'inner') # bind

df_2023_imputed.to_csv('datasets/df_2023_imputed.csv', index = False)
df_2023_imputed.head(3)


# full dataframe with missing values, merge with pollution data (based on ID) & meteorological (based on time step)

# load and merge pollution data
NO2_hourly = pd.read_csv('datasets/df_pollution_2023_berlin_na.csv')
df_2023_na = pd.merge(NO2_hourly, sites_coord, on = 'id', how= 'outer') # bind

# load and merge meteorological data (w/ imputed missing values)
meteorological_hourly = pd.read_csv('datasets/df_meteorological_na.csv')
df_2023_na = pd.merge(df_2023_na, meteorological_hourly, on = 'MESS_DATUM', how= 'inner') # bind

df_2023_na.to_csv('datasets/df_2023_na.csv', index = False)
df_2023_na.head(3)
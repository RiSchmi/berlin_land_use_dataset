# full dataframe imputed, merge with pollution data (based on ID) & meteorological (based on time step)
import pandas as pd 
from utilities.engineering import free_wind


lai_hourly = pd.read_csv('datasets/df_lai_factor.csv')
main_traffic = pd.read_csv('datasets/df_traffic_hours.csv')


sites_coord = pd.read_csv('datasets/df_spatial_only.csv')
sites_coord['id'] = sites_coord['id'].apply(lambda x : x.lower().replace(' ', '')[:5])

# load and merge pollution data
NO2_hourly = pd.read_csv('datasets/df_pollution_2023_berlin_imputed.csv')
df_2023_imputed = pd.merge(NO2_hourly, sites_coord, on = 'id', how= 'outer') # bind

# load and merge meteorological data (w/ imputed missing values)
meteorological_hourly = pd.read_csv('datasets/df_meteorological_impute.csv')
hourly = pd.merge(main_traffic, meteorological_hourly, on = 'time_step', how= 'inner')
df_2023_imputed = pd.merge(df_2023_imputed, hourly, on = 'time_step', how= 'inner') # bind



# merge leaf area data
df_2023_imputed = pd.merge(df_2023_imputed, lai_hourly, on = 'time_step', how= 'inner') # bind

# add boolean if wind can access (based on wind direction & street canyon)
df_2023_imputed = free_wind(main_df = df_2023_imputed, 
                            df_canyon= pd.read_csv('datasets/df_street_canyon_per_site.csv')).__getitem__()


df_2023_imputed.to_csv('datasets/df_2023_imputed.csv', index = False)


# full dataframe with missing values, merge with pollution data (based on ID) & meteorological (based on time step)

# load and merge pollution data
NO2_hourly = pd.read_csv('datasets/df_pollution_2023_berlin_na.csv')
df_2023_na = pd.merge(NO2_hourly, sites_coord, on = 'id', how= 'outer') # bind

# load and merge meteorological data (w/ imputed missing values)
meteorological_hourly = pd.read_csv('datasets/df_meteorological_na.csv')
hourly = pd.merge(main_traffic, meteorological_hourly, on = 'time_step', how= 'inner')
df_2023_na = pd.merge(df_2023_na, hourly, on = 'time_step', how= 'inner') # bind



# merge lai
df_2023_na = pd.merge(df_2023_na, lai_hourly, on = 'time_step', how= 'inner') # bind

# add boolean if wind can access (based on wind direction & street canyon)
df_2023_na = free_wind(main_df = df_2023_na, 
                        df_canyon= pd.read_csv('datasets/df_street_canyon_per_site.csv')).__getitem__()

df_2023_na.to_csv('datasets/df_2023_na.csv', index = False)

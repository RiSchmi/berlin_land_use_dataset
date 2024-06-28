# 0 load dependencies
from utilities.engineering import canyon, green, emitter

import geopandas as gpd
import pandas as pd

# 1. load coordinates in berlin to construct land use features
sites_coord = gpd.read_file('data/monitoring_station/monitoring_station.shp')[['id', 'geometry']]

# 1.1. check coordinate reference system        
if sites_coord.crs != 'EPSG:25833':
    print('Converting Coordinate System to EPSG:25833, double check correct transformation!')
    sites_coord.to_crs(crs='EPSG:25833')


# 2. construct 'prop_intercept_200', 'prop_intercept_50', border_values
features_canyon = canyon(path_building='data/building_polygon/building_polygon.shp', 
                         coordinates=sites_coord['geometry'], 
                         radius=200 # adjust if needed
                         ).calc_valley()



# 3. Green Volume Index (GVI_{radius}) for radius in radii
features_green = green(path_greenery = 'data/green_volume/green_volume.shp', 
                        coordinates=sites_coord['geometry'], 
                        gvi_radii= [25, 50, 100, 200] # adjust if needed
                        ).__getitem__()
    

# 4. emitter related features, traffic volume index (tvi_{radis}), proportion heavy vehicle, nearest street, nearest intersection, population
features_emitter = emitter(coordinates = sites_coord['geometry'], 
                        path_traffic_volume = 'data/traffic_volume_2019/traffic_volume_dtv_2019.shp',
                        tvi_radii = [25, 50, 100, 200], # adjust if needed
                        prop_main_radii = [200], # adjust if needed
                        path_population ='data/population/population.shp', 
                        population_radii = [25, 50, 100, 200] # adjust if needed
                        ).__getitem__()


sites_coord = pd.concat([sites_coord, features_canyon, features_green, features_emitter], axis=1)

# 5. save
sites_coord.drop(['geometry'], axis = 1).to_csv('datasets/df_spatial_only.csv')
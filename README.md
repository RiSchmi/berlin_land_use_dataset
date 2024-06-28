This repository provides the developed feature engineering for the construction of a land use dataset for Berlin, Germany. 
Therefore, arbitrary coordinates are intersected with geological point of interest characteristics provided by Berlin Geoportal 
and can be adjusted to other destinations for your purpose (within Berlin). The data source is further detailed in the Acknowledgment. 
The utilized script was initially proposed for the description of the local surroundings of air pollution monitoring sites in Berlin 
and thereby build the foundation of my data science master thesis on air pollution prediction. The dataset contains temporal consistent 
features of surrounding greenery, traffic volume, nearest street and intersection, population, and architecture (street canyon), 
and interpolated to hourly sequential meteorological and pollution data. 
A detailed feature description can be found in the Section Dataset and Feature Engineering of my thesis.

Structure of the Repository:
-	Notebook_feature_engineering: detailed and annotated description of engineering per feature 
-	main_dataset_construct.py: construction of non-temporal dataset based on coordinates specified in data/monitoring_station/monitoring_station.shp
-	utilities_feature_engineering: python files accessed by main_dataset_construct.py
-	data: original source data (the shapefile for buildings can be accessed through the Berlin Geoportal and is not included (filesize constraints))

-	datasets: all constructed datasets:  
1.  df_spatial_only.csv : no temporal features, only spatial characteristics
2.	df_2023_na.csv : air pollution, meteorological and land use data for 2023, missing values not imputed
3.	df_2023_imputed.csv : air pollution, meteorological and land use data for 2023, missing values imputed (see utilities_feature_engineering>encode_pollution.ipynb & repository: MLbased_meteorological_data_imputation)
4.	df_meteorological_2023_berlin.csv
5.  df_pollution_2023_berlin.csv
 	
Requirements:
-	Used python packages are specified in requirements.txt
-	Other coordinates: if applied to other locations (inside Berlin), the new coordinates must be specified as .shape file in the column geometry with EPSG:25833 (Coordinate Reference System)

<p> This repository provides the developed feature engineering for the construction of a land use dataset for Berlin, Germany. 
Therefore, arbitrary coordinates are intersected with geological 'point of interest' characteristics provided by Berlin Geoportal 
and can be adjusted to other destinations for your purpose (within Berlin). The data source is further detailed in the Acknowledgment. </p>

<p> The utilized script was initially proposed for the description of the local surroundings of air pollution monitoring sites in Berlin 
and thereby build the foundation of my data science master thesis on air pollution prediction. </p>

<p> The dataset contains temporal consistent features of <strong>surrounding greenery, traffic volume, nearest street and intersection, population, and architecture (street canyon)</strong>, and interpolated to <strong>hourly sequential meteorological and pollution data</strong>. A detailed feature description can be found in the Section Dataset and Feature Engineering of my thesis. </p>

<p> NOTE: Not all source files are included in this repository due to file size constrains. Please check out the according descriptions at (<em> data/building_polygon </em>)[https://github.com/RiSchmi/berlin_land_use_dataset/blob/main/data/building_polygon/note.md] and (<em>data/lai</em>)[https://github.com/RiSchmi/berlin_land_use_dataset/blob/main/data/lai/note.md] <p>

<h2> Structure of the Repository: </h2>

- <em> dataset_feature_engineering.pdf </em>: excerpt master thesis on dataset construction
-	<em> Notebook_feature_engineering </em>: detailed and annotated description of engineering per feature 
-	<em> spatial_feature_construct.py </em>: construction of non-temporal dataset based on coordinates specified in data/monitoring_station/monitoring_station.shp
-	<em> utilities_feature_engineering </em>: python files accessed by main_dataset_construct.py
-	<em> data </em>: original source data (the shapefile for buildings can be accessed through the Berlin Geoportal and is not included (filesize constraints))

<h2> all constructed datasets:  </h2>	

1. <em> df_spatial_only.csv </em>: no temporal features, only spatial characteristics
2.	<em> df_2023_na.csv </em>: air pollution, meteorological and land use data for 2023, missing values not imputed
3.	<em> df_2023_imputed.csv </em>: air pollution, meteorological and land use data for 2023, missing values imputed (see <em> utilities_feature_engineering>encode_pollution.ipynb </em> & repository: MLbased_meteorological_data_imputation)
4.	<em> df_meteorological_2023_berlin.csv </em>
5. <em> df_pollution_2023_berlin.csv </em>

 	
Requirements:
-	Used python packages are specified in requirements.txt
-	Other coordinates: if applied to other locations (inside Berlin), the new coordinates must be specified as .shape file in the column geometry with EPSG:25833 (Coordinate Reference System)

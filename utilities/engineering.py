from shapely import geometry
import numpy
import geopandas 
import pandas as pd


class canyon:
    def __init__(self, path_building,coordinates, radius):
        
        self.coordinates = coordinates
        self.radius = radius
        self.building = geopandas.read_file(path_building)     

    def object_intersect_scan(self, coordinate, intersect_polygon):
        '''
        create spatial echo with lines distributed in all directions and cute if intersected with building polygon
        --
        Input: 
            center_point: geometry - coordinate (geo point) of center 
            radius: int - radius 
            intersect_polygone: geometry of surroundings obstacle

        Return: 
            full_rays: Linestring (n=360) geometry
            distances: list (n=360) - length of lines [0, radius]

        '''
        #create rays (linestring) in 360 degree starting at north, doing counterclockwise
        rays = [geometry.LineString([
                coordinate, 
                geometry.Point(
                    coordinate.x + numpy.sin(-angle) * self.radius, 
                    coordinate.y + numpy.cos(-angle) * self.radius
                )]) 
                for angle in numpy.linspace(0, 2 * numpy.pi, 360, endpoint=False)]

        distances = [] # list hold distance between center and closest polygon (building) for all lines
        full_rays = [] # keep only lines which reach border

        for ray in rays:
            min_distance = numpy.inf
            for polygon in intersect_polygon:
                if ray.intersects(polygon):
                    intersection_point = ray.intersection(polygon)
                    distance = coordinate.distance(intersection_point)
                    if distance < min_distance:
                        min_distance = distance 

            # store the only linestrings which intersects with border (length radius)      
            if min_distance == numpy.inf: 
                full_rays.append(ray)
            
            distances.append(min_distance if min_distance != numpy.inf else 0)
        
        return full_rays, distances
    
        
    def calc_valley(self):
        '''
        SPATIAL ECHO obstacle detection
        ---
        Input:
            coordinate: geopoint (monitoring site)
            radius: int
            id: str- name of site
            plot: boolean 
        '''

        results = []
        for coordinate in self.coordinates:
            buffer = geopandas.GeoDataFrame(geometry=[coordinate.buffer(self.radius)], crs=self.building.crs)
            in_buffer_one = geopandas.overlay(self.building, buffer, how='intersection')
            
            prop_intersect_50 = round(1 - len(self.object_intersect_scan(coordinate, intersect_polygon=in_buffer_one['geometry'])[0]) / 360, 3)
            full_rays, len_rays = self.object_intersect_scan(coordinate, intersect_polygon=in_buffer_one['geometry'])
            prop_intersect_radius = round(1 - len(full_rays) / 360, 3)
            
            results.append((prop_intersect_radius, prop_intersect_50))

        
        print('finished features street canyon')
        return pd.DataFrame(results, columns=[f'prop_intercept_{self.radius}', 'prop_intercept_50'])
        

class green:
    def __init__(self, path_greenery, coordinates, gvi_radii):
        
        self.coordinates = coordinates
        self.greenery = geopandas.read_file(path_greenery)
        self.gvi_radii = gvi_radii

    def calc_GVI(self, coordinate, radius):
        buffer  = geopandas.GeoDataFrame(geometry= [coordinate.buffer(radius)], crs=self.greenery.crs) # create polygon with buffer region around monitoring point
        in_buffer_one = geopandas.overlay(self.greenery, buffer, how='intersection') # intersect block areas (with vegetation volume) with radius polygon to reduce block areas inside the radius 
        
        # calculate weighted mean of vegetation volume inside each circle
        in_buffer_one['area'] = in_buffer_one['geometry'].area # area for each block inside circle  
        in_buffer_one['factor_greenery'] = in_buffer_one['area'] / in_buffer_one['area'].sum() # weight= relative proportion of subarea from total area inside circle (sum == 1)
        in_buffer_one['weighted_greenery'] = (in_buffer_one['factor_greenery']) * in_buffer_one['vegvol2020'] # weight
        current_GVI = round(in_buffer_one['weighted_greenery'].sum(),3) # absolute VVI as sum of weighted area index
        return current_GVI

    def __getitem__(self):
        results = []
        for coordinate in self.coordinates:
            current_location = []
            # create gvi for each radius
            for radius in self.gvi_radii:
                current_location.append(self.calc_GVI(coordinate = coordinate, radius= radius))
            
            results.append(current_location)

        print('finished feature greenery')
        return pd.DataFrame(results, columns=[f'gvi_{radius}' for radius in self.gvi_radii])            
    
class emitter:
    def __init__(self, coordinates, path_traffic_volume, path_population, tvi_radii, prop_main_radii, population_radii):
        self.coordinates = coordinates
        
        self.traffic = geopandas.read_file(path_traffic_volume)
        self.tvi_radii = tvi_radii
        self.prop_main_radii = prop_main_radii


        first_coord = self.traffic['geometry'].apply(lambda x: geometry.Point(list(x.coords)[0]))
        last_coord = self.traffic['geometry'].apply(lambda x: geometry.Point(list(x.coords)[-1]))
        self.intersection_points = pd.concat([first_coord, last_coord])
        del(first_coord, last_coord)

        self.population = geopandas.read_file(path_population)
        self.population['original_area'] = self.population['geometry'].area
        self.population_radii = population_radii
        
    

    def calc_tvi(self, coordinate, radius, mode = 'tvi'):
        buffer  = geopandas.GeoDataFrame(geometry= [coordinate.buffer(radius)], crs=self.traffic.crs) # create polygon with buffer region around monitoring point
        in_buffer_one = geopandas.overlay(self.traffic, buffer, how='intersection') # intersect linestring (traffic road) with radius polygon to reduce to inside the radius 
        
        # calculate traffic volume index
        in_buffer_one['new_length'] = in_buffer_one['geometry'].length # calculate new length (within radius) per street
        in_buffer_one['main_emitter'] = in_buffer_one['lkw']   + in_buffer_one['linienbuss'] +  in_buffer_one['reisebusse'] # count main emitter to calc prop.
        in_buffer_one['volume_x_len'] = in_buffer_one['new_length'] * in_buffer_one['dtv']
        in_buffer_one['relative_street_len'] = in_buffer_one['new_length']/ in_buffer_one['new_length'].sum()
        tvi = in_buffer_one['volume_x_len'].sum()/(10000 * radius) # normalized by range
        prop_main_emitter = (in_buffer_one['main_emitter']/ in_buffer_one['dtv'] * in_buffer_one['relative_street_len']).sum()
        if mode == 'tvi':
            return tvi
        elif mode == 'prop_main_emitter':
            return prop_main_emitter

    # 2. calculate nearest point / street intersection
    def distance_nearest_intersection(self, point):
        return self.intersection_points.apply(lambda x: point.distance(x)).min()

    # 3. calculate distance between monitoring site and nearest street
    def distance_nearest_street(self, point):
        return self.traffic['geometry'].apply(lambda x: point.distance(x)).min()

    # 4. find total population per radius
    def get_popu_per_radius(self, coordinate, radius):
        buffer  = geopandas.GeoDataFrame(geometry= [coordinate.buffer(radius)], crs=self.traffic.crs) # create polygon with buffer region around monitoring point
        in_buffer = geopandas.overlay(self.population, buffer, how='intersection') # intersect and keep only those polygons inside radius area
        in_buffer['weighted_pop'] = round((in_buffer['geometry'].area)/ in_buffer['original_area'] *in_buffer['ew2022'])
        return in_buffer['weighted_pop'].sum()

    
    def __getitem__(self):
        results = []
        for coordinate in self.coordinates:
            
            current_location = []

            # create tvi for each radius
            for radius in self.tvi_radii:
                current_location.append(self.calc_tvi(coordinate= coordinate, radius = radius))
            
            for radius in self.prop_main_radii:
                current_location.append(self.calc_tvi(coordinate= coordinate, radius = radius, mode = 'prop_main_emitter'))

            # create distance to nearest intersection and nearest street
            current_location.append(self.distance_nearest_intersection(point = coordinate))
            current_location.append(self.distance_nearest_street(point = coordinate))

            # create population for each radius
            for radius in self.population_radii:
                current_location.append(self.get_popu_per_radius(coordinate = coordinate, radius = radius))

            # Append current_location to results
            results.append(current_location)

        # Define column names
        column_names = (
            [f'tvi_{radius}' for radius in self.tvi_radii] +
            [f'prop_main_emitter_{radius}' for radius in self.prop_main_radii] +
            ['distance_nearest_intersection', 'distance_nearest_street'] +
            [f'population_{radius}' for radius in self.population_radii]
        )

        # Return DataFrame
        print('finished feature greenery')
        return pd.DataFrame(results, columns=column_names)            
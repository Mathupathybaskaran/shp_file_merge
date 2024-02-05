import os
import geopandas as gpd
import pandas as pd
from pathlib import Path
import glob
 

"""
This script used for merge the all shapefiles inside the fmb folder in input path

"""


def process_shapefile(shapefile):


    try:
        gdf = gpd.read_file(shapefile)
        new_crs = 'EPSG:4326'
        gdf = gdf.to_crs(new_crs)
        p = Path(shapefile)
        gdf['district_code'] = p.parts[3]
        gdf['taluk_code'] = p.parts[4]
        gdf['village_code'] = p.parts[5]
        gdf['file_path'] = shapefile
        gdf['phase'] = p.parts[5]
        return gdf
    except Exception as e:
        print('An exceptional thing happened - {} - on file - {}'.format(e, shapefile))
        return None
"""
In this above part parts 3 is district code in input path.parts 4 is taluk code in input path.
parts 5 is village code in input path

"""

def merge_shapefiles(input_path, output_file):
    merged_gdf = gpd.GeoDataFrame()

    # Find all shapefiles in the root directory
    shapefiles = glob.glob(os.path.join(input_path, '**', 'georef', '*.shp'), recursive=True)

    for shapefile in shapefiles:
        gdf = process_shapefile(shapefile)
        if gdf is not None:
            merged_gdf = pd.concat([merged_gdf, gdf], ignore_index=True)
            print(f"Processed: {shapefile}")

    # Write the merged GeoDataFrame to a new shapefile
    merged_gdf.to_file(output_file)

    print("Shapefiles merged successfully!")

if __name__ == '__main__':
    input_path = r"D:/set1"
    output_file = r"D:/set1/merged_fmb.shp"
    
    merge_shapefiles(input_path, output_file)

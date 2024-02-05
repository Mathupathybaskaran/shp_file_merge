import os
import geopandas as gpd
import pandas as pd

"""
This script used to merge all shp files on vector folder in input path

"""

def merge_shapefiles(input_path, output_file):
    merged_gdf = gpd.GeoDataFrame()

    for root, dirs, files in os.walk(input_path):
        if "vector" in dirs:
            vector_folder = os.path.join(root, "vector")
            for file in os.listdir(vector_folder):
                if file.endswith(".shp"):
                    file_path = os.path.join(vector_folder, file)
                    gdf = gpd.read_file(file_path)

                    # Extract folder details
                    folder_names = root.split(os.sep)
                    district_code = None
                    taluk_code = None
                    village_code = None

                    if len(folder_names) >= 10:
                        district_code = folder_names[-10]
                        taluk_code = folder_names[-9]
                        village_code = folder_names[-7]

                    """
                    In above section -10 th place is district code,-9 th place is taluk code,
                    -7 th place is village code on input path

                    """
                    # Add folder details to columns
                    gdf["input_path"] = input_path
                    gdf["district_code"] = district_code
                    gdf["taluk_code"] = taluk_code
                    gdf["village_code"] = village_code

                    merged_gdf = pd.concat([merged_gdf, gdf], ignore_index=True)

                    print(f"Processed: {file_path}")  # Print processed file name

    # Write the merged GeoDataFrame to a new shapefile
    merged_gdf.to_file(output_file)

    print("Shapefiles merged successfully!")

input_path = r"D:\phase1 and 2 fmb\01_Tiruvallur\01_Tiruvallur"
output_file = r"D:\phase1 and 2 fmb\merged.shp"

merge_shapefiles(input_path, output_file)

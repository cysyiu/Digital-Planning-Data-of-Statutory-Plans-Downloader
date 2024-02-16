import requests
import os
import zipfile
import pandas as pd
import wget
import geopandas as gpd



# Create "DEV_PLAN_Data" file to store OZP and Download OZP data
try:
   os.mkdir("DEV_PLAN_Data")
except FileExistsError:
   # directory already exists
   pass

# Create "DEV_PLAN_Result" file to store merged OZP
try:
   os.mkdir("DEV_PLAN_Result")
except FileExistsError:
   # directory already exists
   pass


# URL for OZP
url = "https://www.pland.gov.hk/pland_en/info_serv/digital_planning_data/Metadata/DEV_PLAN_SHP.json"


def readjson():
    response = requests.get("https://www.pland.gov.hk/pland_en/info_serv/digital_planning_data/Metadata/DEV_PLAN_SHP.json")
    if response.status_code == 200:
        get = response.json()
        url = pd.DataFrame(get)['SHP_LINK']
        print(len(url))
        for i in url:
            file_path = ("DEV_PLAN_Data")
            wget.download(i, out=file_path)
    else:
        print("Faied to connect!")


#Run
readjson()

##########################################################

# Extract ZIP files
extension = ".zip"
directory = "DEV_PLAN_Data"

for item in os.listdir(directory):
    if item.endswith(extension):
        zip_file = os.path.join(directory, item)  # Get the full path of the zip file

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(directory)  # Extract the contents of the zip file to the directory
            zip_ref.close()

        os.remove(zip_file)  # Delete the zip file


###########################################################
#Schema Area
def merge_schema_area(directory):
    PlanSchemeArea_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "PLAN_SCHEME_AREA.shp":
                file_path = os.path.join(root, file)
                PlanSchemeArea_files.append(file_path)

    gdf_schema_area = gpd.GeoDataFrame()
    
    for file in PlanSchemeArea_files:
        gdf = gpd.read_file(file)
        gdf_schema_area = pd.concat([gdf_schema_area, gdf], ignore_index=True)
    
    gdf_schema_area.to_file("./DEV_PLAN_Result/PLAN_SCHEME_AREA_master.shp")

###########################################################
#Zone
def merge_zone(directory):
    Zone_files = []

    for root, dir, files in os.walk(directory):
        for file in files:
            if file == "ZONE.shp":
                file_path = os.path.join(root, file)
                Zone_files.append(file_path)

    gdf_zone = gpd.GeoDataFrame()
    
    for file in Zone_files:
        gdf = gpd.read_file(file)
        gdf_zone = pd.concat([gdf_zone, gdf], ignore_index=True)
    
    gdf_zone.to_file("./DEV_PLAN_Result/Zone_master.shp")


###########################################################
#BHC
def merge_bhc(directory):
    BHC_files = []

    for root, dir, files in os.walk(directory):
        for file in files:
            if file == "BHC.shp":
                file_path = os.path.join(root, file)
                BHC_files.append(file_path)

    gdf_bhc = gpd.GeoDataFrame()
    
    for file in BHC_files:
        gdf = gpd.read_file(file)
        gdf_bhc = pd.concat([gdf_bhc, gdf], ignore_index=True)
    
    gdf_bhc.to_file("./DEV_PLAN_Result/BHC_master.shp")

# ###########################################################
#Amendment
def merge_amendment(directory):
    Admendment_files = []

    for root, dir, files in os.walk(directory):
        for file in files:
            if file == "BHC.shp":
                file_path = os.path.join(root, file)
                Admendment_files.append(file_path)

    gdf_admendment = gpd.GeoDataFrame()
    
    for file in Admendment_files:
        gdf = gpd.read_file(file)
        gdf_admendment = pd.concat([gdf_admendment, gdf], ignore_index=True)
    
    gdf_admendment.to_file("./DEV_PLAN_Result/Admendment_master.shp")

###########################################################

# Example usage
merge_schema_area(directory)
merge_zone(directory)
merge_bhc(directory)
merge_amendment(directory)

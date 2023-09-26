import json
import requests
import codecs
import os
from zipfile import ZipFile


#Create Temp File
try:
   os.mkdir("Data")
except FileExistsError:
   # directory already exists
   pass

#Download ZIP Data
os.chdir("Data")
r = requests.get("https://www.pland.gov.hk/pland_en/info_serv/digital_planning_data/Metadata/OZP_PLAN_SHP.json")

decoed_data = codecs.decode(r.text.encode(), 'utf-8-sig')
data = json.loads(decoed_data)

for i, dt in enumerate(data):
    response = requests.get(dt['SHP_LINK'])
    name = os.path.basename(dt['SHP_LINK'])
    open("{}".format(name), "wb").write(response.content)

#Extract ZIP files
extension = ".zip"

for item in os.listdir(): # loop through items in dir
    if item.endswith(extension): # check for ".zip" extension
        file_name = os.path.abspath(item) # get full path of files
        zip_ref = ZipFile(file_name) # create zipfile object
        zip_ref.extractall() # extract file to dir
        zip_ref.close() # close file
        os.remove(file_name) # delete zipped file


#Merging SHP
import arcpy
import os
from pathlib import Path

arcpy.env.workspace = 'Data'
directories = os.listdir('Data')

#SCHEMA_AREA
SCHEMA_AREA_LOCATION = r'\Plan GIS Data SHP\PLAN_SCHEME_AREA.shp'

directories_scheme_area = [dir + SCHEMA_AREA_LOCATION for dir in directories]
directories_scheme_area_exist = []

for schema_area_shp in directories_scheme_area:
    if arcpy.Exists(schema_area_shp):
        directories_scheme_area_exist.append(schema_area_shp)

arcpy.Merge_management(directories_scheme_area, r"PLAN_SCHEME_AREA_master.shp")

#ZONE
ZONE_LOCATION = r'\Plan GIS Data SHP\ZONE.shp'

directories_zone = [dir + ZONE_LOCATION for dir in directories]
directories_zone_exist = []

for zone_shp in directories_zone:
    if arcpy.Exists(zone_shp):
        directories_zone_exist.append(zone_shp)

arcpy.Merge_management(directories_zone, r"ZONE_master.shp")

#BHC
BHC_LOCATION = r'\Plan GIS Data SHP\BHC.shp'

directories_bhc = [dir + BHC_LOCATION for dir in directories]
directories_bhc_exist = []

for bhc_shp in directories_bhc:
    if arcpy.Exists(bhc_shp):
        directories_bhc_exist.append(bhc_shp)

arcpy.Merge_management(directories_bhc_exist, "BHC_master.shp")

#AENDMENT
AMENDMENT_LOCATION = r'\Plan GIS Data SHP\AMENDMENT.shp'

directories_amendment = [dir + AMENDMENT_LOCATION for dir in directories]
directories_amendment_exist = []

for amendment_shp in directories_amendment:
    if arcpy.Exists(amendment_shp):
        directories_amendment_exist.append(amendment_shp)

arcpy.Merge_management(directories_amendment_exist, "Amendment_master.shp")   

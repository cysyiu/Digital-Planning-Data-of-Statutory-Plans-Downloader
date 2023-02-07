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



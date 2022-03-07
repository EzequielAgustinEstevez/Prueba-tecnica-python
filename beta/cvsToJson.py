import csv
import json
import uuid
import zipfile
import urllib
import urllib.request


#import requests
# Download
print('Download jodi_gas_csv_beta.zip')
url = r'https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip'
extract_dir = './'
output = r'./jodi_gas_csv_beta.zip'

#UnZip
print('Unziping')
zip_path, _ = urllib.request.urlretrieve(url)
with zipfile.ZipFile(zip_path, "r") as f:
    f.extractall(extract_dir)

# Program
def csv_to_json(csvFilePath, jsonFilePath):
    print('Interpret csv data to code')
    
    # Open csv file
    with open(csvFilePath, encoding='utf-8') as csvf:
        # read csv file data using the csv library's dictionary delimiter by ","
        csvReader = csv.reader(csvf, delimiter=',')
        # Ignore first line
        next(csvReader)
        # for loop to
        outPutData = []
        for row in csvReader:
            data = {}
            points = []
            fields = {}
            
            # row 'REF_AREA'
            key1 = row[0]
            # row 'ENERGY_PRODUCT'
            key2 = row[2]
            # Generate a unique series id
            id = str(uuid.uuid4().hex)
            # combining to make sense id it is identifying
            series_id = id + "-" + key1 + "-" + key2
            # Set the id to data
            data['series_id'] = series_id

            # Load row TIME_PERIOD and enter the first day's date
            period = row[1] + "-01"
            # The TIME_PERIOD and OBS_VALUE row are appended to the points array
            points.append([period, row[5]])
            # Set the points to data
            data['points'] = points

            # Load additional metadata rows to field
            fields['REF_AREA'] = row[0]
            fields['ENERGY_PRODUCT'] = row[2]
            fields['FLOW_BREAKDOWN'] = row[3]
            fields['UNIT_MEASURE'] = row[4]
            fields['ASSESSMENT_CODE'] = row[6]
            # Set the field to data
            data['fields'] = fields
            # Add data to outPutData
            outPutData.append(data)

    # open jsonFile on writer and dumps outPutData
    print('Writing data.json')
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(outPutData, indent=4)
        jsonf.write(jsonString)
        print('data.json ready')


csvFilePath = r'./jodi_gas_beta.csv'
jsonFilePath = r'./data.json'
csv_to_json(csvFilePath, jsonFilePath)
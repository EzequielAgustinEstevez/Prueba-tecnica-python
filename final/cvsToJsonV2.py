import csv
import json
import uuid
import requests
import zipfile

# Download
print('Download jodi_gas_csv_beta.zip')
url = r'https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip'
output = r'./jodi_gas_csv_beta.zip'

r = requests.get(url)
with open(output, 'wb') as f:
    f.write(r.content)

# Unzip
print('Unzip jodi_gas_beta.csv')
destination = '.'

with zipfile.ZipFile(output) as zf:
    zf.extractall(destination)

# Program


def csv_to_json(csvFilePath, jsonFilePath):
    print('Processing output csv data to json')
    # Open the json file to enter line by line the result of the loop for
    dataJson = open(jsonFilePath, 'w')

    # Open csv file
    with open(csvFilePath, encoding='utf-8') as csvf:
        # read csv file data using the csv library, delimiter by","
        csvReader = csv.reader(csvf, delimiter=',')
        # Ignore first line
        next(csvReader)
        # for loop to
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
            series_id = id + "_" + key1 + "_" + key2
            # Set the id to data
            data['series_id'] = series_id

            # Load row TIME_PERIOD and enter the first day's date
            period = row[1] + "-01"
            # The TIME_PERIOD and OBS_VALUE row are appended to the pointsarray
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

            # Add data to dataJson using the json library
            json.dump(data, dataJson)
            # New line to add and persist with the last line
            dataJson.write('\n')

    dataJson.close()


csvFilePath = r'./jodi_gas_beta.csv'
jsonFilePath = r'./data.json'
csv_to_json(csvFilePath, jsonFilePath)

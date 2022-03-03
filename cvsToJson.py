import csv
import json
import uuid


def csv_to_json(csvFilePath, jsonFilePath):

    # read csv file
    with open(csvFilePath, encoding='utf-8') as csvf:
        # load csv file data using csv library's dictionary reader
        csvReader = csv.reader(csvf, delimiter=',')
        next(csvReader)
        # convert each csv row into python dict
        superdata = []
        for rows in csvReader:
            data = {}
            points = []
            fields = {}

            # be the primary key 'REF_AREA'
            key = rows[0]
            # generate a unique series id
            id = str(uuid.uuid4().hex)
            # combining to make sense to the series it is identifying
            series_id = id + "-" + key
            # Set the id to data
            data['series_id'] = series_id

            # Load row TIME_PERIOD and enter the first day's date
            period = rows[1] + "-01"
            # The TIME_PERIOD and OBS_VALUE rows are appended to the points array.
            points.append([period, rows[5]])
            # Set the points to data
            data['points'] = points

            fields['ENERGY_PRODUCT'] = rows[2]
            fields['FLOW_BREAKDOWN'] = rows[3]
            fields['UNIT_MEASURE'] = rows[4]
            fields['ASSESSMENT_CODE'] = rows[6]
            data['fields'] = fields

            superdata.append(data)

    # convert python jsonObjet to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(superdata, indent=4)
        jsonf.write(jsonString)


csvFilePath = r'.\jodi_gas_beta.csv'
jsonFilePath = r'data.json'
csv_to_json(csvFilePath, jsonFilePath)

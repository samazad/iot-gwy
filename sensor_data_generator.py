#!/usr/bin/env python3

import json
import random

def sensor_data(sid, type):
    """Builds JSON Payload for Panduit Sensors - Temperature, Humidity, Vibration"""

    data = {}

    if type == "Temperature":
        data['SensorID'] = 100000 + sid
    elif type == "Humidity":
        data['SensorID'] = 200000 + sid
    elif type == "Vibration":
        data['SensorID'] = 300000 + sid

    if type == "Temperature":
        data['ApplicationID'] = '2'
    elif type == "Humidity":
        data['ApplicationID'] = '43'
    elif type == "Vibration":
        data['ApplicationID'] = '95'

    data['CSNetID'] = '4'

    if type == "Temperature":
        data['SensorName'] = 'Temperature - ' + str(100000 + sid)
    elif type == "Humidity":
        data['SensorName'] = 'Humidity - ' + str(200000 + sid)
    elif type == "Vibration":
        data['SensorName'] = 'Vibration - ' + str(300000 + sid)

    data['LastCommunicationDate'] = '/Date(1507706467000)/' 
    data['NextCommunicationDate'] = '/Date(-62135596800000)/' 
    data['LastDataMessageMessageGUID'] = '176788a7-8e22-450f-9da5-356c517c96c3'
    data['PowerSourceID'] = '2'
    data['Status'] = '1'
    data['CanUpdate'] = 'True'

    if type == "Temperature":
        data['CurrentReading'] = str(random.randint(75, 85)) + '.' + str(random.randint(0, 9)) + '.. F'
    elif type == "Humidity":
        data['CurrentReading'] = str(random.randint(0, 99)) + '.' + str(random.randint(0, 99)) + '% @ ' \
                                + str(random.randint(75, 85)) + '.' + str(random.randint(0, 9)) + '.. F'   
    elif type == "Vibration":
        data['CurrentReading'] = 'X-Axis ' + str(random.randint(0, 10)) + '.' + str(random.randint(0, 9)) \
                                + ' mm/s 22 Hz, Y-Axis ' + str(random.randint(0, 10)) + '.' + \
                                str(random.randint(0, 9)) + ' mm/s 9 Hz, Z-Axis ' + \
                                str(random.randint(0, 10)) + '.' + str(random.randint(0, 9)) + \
                                ' mm/s 9 Hz, Duty Cycle 100 %'

    data['BatteryLevel'] = '100'
    data['SignalStrength'] = '100'
    data['AlertsActive'] = 'True'
    data['CheckDigit'] = 'ASZJ'
    data['AccountID'] = '2'

    json_data = json.dumps(data)
    return json_data

from flask import Flask, jsonify, request
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
import json
import random
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)

auth = HTTPBasicAuth()

user = "admin"
password = "admin"

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return 'Welcome to the Panduit Gateway Simulator'

@app.route('/json/GetAuthToken')
@auth.login_required
def get_auth_token():
    print(request)
    print(request.args)
    uname = request.args.get('username')
    pwd = request.args.get('password')
    print("Username supplied: " + uname)
    print("Password supplied: " + pwd)
    token = generate_auth_token()
    return jsonify(token.decode('ascii'))

def generate_auth_token():
    s = Serializer('cisco123', expires_in = 600)
    return s.dumps({'id': 1})

def verify_auth_token(token):
    print("Verifying if the token is valid")
    s = Serializer('cisco123')
    try:
        data = s.loads(token)
    except SignatureExpired:
        print("Token has expired")
        return None # valid token, but expired
    except BadSignature:
        print("Invalid Token")
        return None # invalid token
    return True

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    if verify_auth_token(username_or_token):
        print("Token is Valid")
        return True 
    else:
        # try to authenticate with username/password
        if username_or_token != "admin":
            print("Username is Incorrect")
            return False    
        if password != "admin": 
            print("Password is Incorrect")
            return False
        print("User is Authenticated")
        return True

@app.route('/api/sensor_list')
@auth.login_required
def get():

    d = []
    for i in range(1,34): 
        d.append(sensor_data(i, "Temperature"))
        d.append(sensor_data(i, "Humidity"))
        d.append(sensor_data(i, "Vibration"))

    return jsonify(d)

def sensor_data(sid, type):
    """Builds JSON Payload for Panduit Sensors - Temperature, Humidity, Vibration"""

    data = {}

    if type == "Temperature":
        data['SensorID'] = 100000 + sid
    elif type == "Humidity":
        data['SensorID'] = 200000 + sid
    elif type == "Vibration":
        data['SensorID'] = 300000 + sid

    data['ApplicationID'] = '2'
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
        data['CurrentReading'] = str(random.randint(75, 85)) + '.' + str(random.randint(0,9)) + '.. F'
    elif type == "Humidity":
        data['CurrentReading'] = str(random.randint(0, 99)) + '.' + str(random.randint(0, 99)) + '% @ ' \
                              + str(random.randint(75, 85)) + '.' + str(random.randint(0,9)) + '.. F'   
    elif type == "Vibration":
        data['CurrentReading'] = 'X-Axis ' + str(random.randint(0, 10)) + '.' + str(random.randint(0,9)) \
                                + ' mm/s 22 Hz, Y-Axis ' + str(random.randint(0, 10)) + '.' + \
                                str(random.randint(0,9)) + ' mm/s 9 Hz, Z-Axis ' + \
                                str(random.randint(0, 10)) + '.' + str(random.randint(0,9)) + \
                                ' mm/s 9 Hz, Duty Cycle 100 %'

    data['BatteryLevel'] = '100'
    data['SignalStrength'] = '100'
    data['AlertsActive'] = 'True'
    data['CheckDigit'] = 'ASZJ'
    data['AccountID'] = '2'

    json_data = json.dumps(data)
    return json_data

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5010)

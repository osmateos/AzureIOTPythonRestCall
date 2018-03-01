''' This example shows how to connect with the IOT hub and send events just using the API
    and sending a bytearray to the endpoint using the sas token
    No sdk library is needed
'''

import time
from datetime import datetime
import requests
import random
import httplib, urllib, base64, json

iotHub = "osmateosiothub"
deviceId = "MyFirstPythonDevice"  # This should be the name for you registered device
api = "2016-02-03" 
restUriPost = "https://" + iotHub + ".azure-devices.net/devices/" + deviceId + "/messages/events?api-version=" + api
sas = "xxx"

# sas format should look like 
# "SharedAccessSignature sr=osmateosiothub.azure-devices.net&sig=xxxxskn=iothubowner"
# It can be generated trought the azure cli with this command 
# az iot hub generate-sas-token --hub-name osmateosiothub


headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Authorization': sas,
}

def getFlowValues(mydateTime):
'''This function return a formatted text with some random values 
   from temperature,flow or humidity
   input mydatetime is a timestamp
'''
    deviceValue = random.randint(1, 100)
    deviceParameterList = ['Flow', 'Temperature','Humidity']
    deviceId = 'SensorDevice'
    MSG_TXT = "{\"deviceValue\":  %.2f ,\"deviceParameter\": \"%s\" , \"deviceId\": \"%s\" , \"datetime\": \"%s\" }"
    msg_txt_formatted = MSG_TXT % ( deviceValue,random.choice(deviceParameterList),deviceId,mydateTime)
    return msg_txt_formatted

conn = httplib.HTTPSConnection(iotHub + ".azure-devices.net")
try:
    while True:
        mydateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sensordata = getFlowValues(mydateTime)
        conn.request("POST", restUriPost,bytearray(sensordata,'utf8'), headers)
        response = conn.getresponse()
        print(response.status)    
        conn.close()
except Exception as e:
    print(e)


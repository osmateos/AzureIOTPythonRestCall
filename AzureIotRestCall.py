import time
from datetime import datetime
import requests
import random
import httplib, urllib, base64, json

iotHub = "osmateosiothub";
deviceId = "MyFirstPythonDevice";
api = "2016-02-03" 
restUriPost = "https://" + iotHub + ".azure-devices.net/devices/" + deviceId + "/messages/events?api-version=" + api
sas = "SharedAccessSignature sr=osmateosiothub.azure-devices.net&sig=WWKYesM0tQrRhodI3KOgggSN3qdqx%2FhaFjQY24Eo%2BLk%3D&se=1519921120&skn=iothubowner"
headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Authorization': sas,
}

def getFlowValues(mydateTime):
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


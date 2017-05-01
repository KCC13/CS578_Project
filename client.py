import requests
import json
import time

headers = {'content-type': 'application/json'}

print "add new position"
url = 'http://127.0.0.1:5000/api/v1/add_pos'
payload = {'device_id': '123', 'lng': 79.123456, 'lat': 84.567890}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

print "\nget latest position"
url = 'http://127.0.0.1:5000/api/v1/get_pos'
payload = {'device_id': '123'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

print "\nadd another new position"
url = 'http://127.0.0.1:5000/api/v1/add_pos'
payload = {'device_id': '123', 'lng': 80.123456, 'lat': 85.567890}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

print "\nget latest position"
url = 'http://127.0.0.1:5000/api/v1/get_pos'
payload = {'device_id': '123'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

print "\ndo whatever query you want, here we try to get all positions(localhost only)"
url = 'http://127.0.0.1:5000/api/v1/do_query'
payload = {'query': 'select * from gps_records', 'args': []}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

print "\nadd phonecall record"
url = 'http://127.0.0.1:5000/api/v1/add_call'
payload = {'device_id': '123', 'phone_num': '0987654321', 'called_time': '1987-12-31 23:05:07'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

print "\nadd another phonecall record"
url = 'http://127.0.0.1:5000/api/v1/add_call'
payload = {'device_id': '123', 'phone_num': '0912345678', 'called_time': '1999-02-01 13:35:55'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

print "\nget phonecall records"
url = 'http://127.0.0.1:5000/api/v1/get_call'
payload = {'device_id': '123'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

print "\nsend sms message"
url = 'http://127.0.0.1:5000/api/v1/send_msg'
payload = {'phone_num': '0987654321'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

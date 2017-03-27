import requests
import json
import time

headers = {'content-type': 'application/json'}

url = 'http://127.0.0.1:5000/api/v1/add_pos'
payload = {'device_id': 123, 'lng': 79.123456, 'lat': 84.567890}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

url = 'http://127.0.0.1:5000/api/v1/get_pos'
payload = {'device_id': 123}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

url = 'http://127.0.0.1:5000/api/v1/add_pos'
payload = {'device_id': 123, 'lng': 80.123456, 'lat': 85.567890}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

url = 'http://127.0.0.1:5000/api/v1/get_pos'
payload = {'device_id': 123}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

url = 'http://127.0.0.1:5000/api/v1/do_query'
payload = {'query': 'select * from records', 'args': []}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

time.sleep(1)

url = 'http://127.0.0.1:5000/api/v1/send_msg'
payload = {'phone_num': '0937954300'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content

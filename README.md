# CS578_Project 

[Introduction](#introduction)  
[中文簡介](#簡介)

## Introduction
A simple server made by flask+sqlite3, support multithreading
### Prerequisites
```
python 2.7
flask
requests
```
```requests``` is not really necessary, it is only used for testing API in our case.

### Installing

#### python 2.7
https://www.python.org/downloads/

#### flask
```
pip install flask
```

#### requests
```
pip install requests
```

### Running the server
```
python server.py
```
The default ip address is ```127.0.0.1``` and the default port is ```5000```, you can change them in ```const.py```. Set ip address to ```0.0.0.0``` to have the server available externally.  
The error and info messages would be saved in ```server.log```.
Also, remember to change the username and password of SMS in ```const.py``` if you want to use the API to send short message(here I use service of [SMS King](http://www.kotsms.com.tw/)).

### Example of using APIs
Make sure that you use post to make every requests, and follow the data type of example.  
Here I use ```requests``` to demonstrate how to use the APIs, You can also see them in ```client.py```.  
First, you need to import ```requests```:
```python
import requests
```
#### 1. Adding position
Devices can report positions by ```add_pos```.
```python
url = 'http://127.0.0.1:5000/api/v1/add_pos'
payload = {'device_id': 123, 'lng': 79.123456, 'lat': 84.567890}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content
```

#### 2. Getting position
App can get the latest position of the device by ```get_pos```.
```python
url = 'http://127.0.0.1:5000/api/v1/get_pos'
payload = {'device_id': 123}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content
```

#### 3. Doing query(Localhost only)
Other applications(in localhost) can fetch the data by sending any query to ```do_query```.
```python
url = 'http://127.0.0.1:5000/api/v1/do_query'
payload = {'query': 'select * from records', 'args': []}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content
```
Parameter arg in payload should be remained even if it's empty, just like the example shows.

#### 4. Sending message
Devices can use ```send_msg``` to send the short messages to the target phone.
```python
url = 'http://127.0.0.1:5000/api/v1/send_msg'
payload = {'phone_num': '0987654321'}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content
```

### Reference
[Flask Docs](http://flask.pocoo.org/docs/0.12/)  
[簡訊王非官方API](https://github.com/fuyuanli/kotsms.py)

### License
This project is licensed under the MIT License


## 簡介
一個以flask+sqlite3做的簡易server，支援multithreading

### 需要環境
```
python 2.7
flask
requests
```
```requests```在此只是拿來測試api用，並非必要

### 安裝

#### python 2.7
https://www.python.org/downloads/

#### flask
```
pip install flask
```

#### requests
```
pip install requests
```

### 啟動server
```
python server.py
```
ip的初始值是```127.0.0.1```，port則是```5000```，你可以在```const.py```改動他們。把ip設為```0.0.0.0```則可將server對外開放。錯誤和運行訊息會存在```server.log```。  
另外要注意的是如果要使用server的傳送簡訊功能，需在```const.py```設定SMS帳號密碼，這裡我是使用[簡訊王的SMS](http://www.kotsms.com.tw/)。

### API使用簡介
注意，任何request都須以post傳送，並且遵守範例中的data型式  
這裡我用```requests```示範如何使用這些API，你可以在```clinet.py```看到完整的範例，首先你得import ```requests```
```python
import requests
```
#### 1. Adding position
裝置可以藉由```add_pos```回報他們的位置。
```python
url = 'http://127.0.0.1:5000/api/v1/add_pos'
payload = {'device_id': 123, 'lng': 79.123456, 'lat': 84.567890}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content
```

#### 2. Getting position
App可以藉由```get_pos```獲取裝置最新的位置.
```python
url = 'http://127.0.0.1:5000/api/v1/get_pos'
payload = {'device_id': 123}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content
```

#### 3. Doing query(Localhost only)
Localhost下的其他程式可以藉由```do_query```問任何query以獲取自己想要的data。
```python
url = 'http://127.0.0.1:5000/api/v1/do_query'
payload = {'query': 'select * from records', 'args': []}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content
```
在payload中，參數args就算是空的也要留著，如同範例所示

#### 4. Sending message
裝置可以藉由```send_msg```傳送簡訊至目標手機.
```python
url = 'http://127.0.0.1:5000/api/v1/send_msg'
payload = {'phone_num': '0987654321'}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
print r.content
```

### 參考資料
[Flask Docs](http://flask.pocoo.org/docs/0.12/)  
[簡訊王非官方API](https://github.com/fuyuanli/kotsms.py)

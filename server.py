# -*- coding: utf-8 -*-
import os
import sqlite3
import json
import kotsms
import const
import logging
from threading import Lock
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Nothing here, get out!'

@app.route('/api/v1/add_pos', methods=['POST'])
def add_pos():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		lng = info["lng"]
		lat = info["lat"]
		insert_gps(device_id, lng, lat)
		return "Sucess."
	except:
		return "Fail."

@app.route('/api/v1/get_pos', methods=['POST'])
def get_pos():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		coord = query_db("SELECT lng, lat, saved_time FROM gps_records WHERE device_id = ? ORDER BY saved_time DESC", [device_id])[0]
		if coord is not None:
			return jsonify({'lng': coord[0], 'lat': coord[1], "time":coord[2]})
		else:
			return "No record found."
	except:
		return "Bad request."

@app.route('/api/v1/get_2_pos', methods=['POST'])
def get_2_pos():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		coords = query_db("SELECT lng, lat, saved_time FROM gps_records WHERE device_id = ? ORDER BY saved_time DESC", [device_id])
		if coords is not None:
			if len(coords) >= 2:
				return jsonify({'lng_new': coords[0][0], 'lat_new': coords[0][1], 'time_new': coords[0][2], 'lng_old' : coords[1][0], 'lat_old' : coords[1][1], 'time_old': coords[1][2]})
			else:
				return jsonify({'lng_new': coords[0][0], 'lat_new': coords[0][1], 'time_new': coords[0][2], 'lng_old' : coords[0][0], 'lat_old' : coords[0][1], 'time_old': coords[0][2]})
		else:
			return "No record found."
	except:
		return "Bad request."

@app.route('/api/v1/get_all_pos', methods=['POST'])
def get_all_pos():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		coords = query_db("SELECT lng, lat, saved_time FROM gps_records WHERE device_id = ? ORDER BY saved_time DESC", [device_id])
		if coords is not None:
			history = [{"lng": coord[0], "lat": coord[1], "time":coord[2]} for coord in coords]
			return jsonify(history)

		else:
			return "No record found."
	except:
		return "Bad request."

@app.route('/api/v1/add_call', methods=['POST'])
def add_call():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		phone_num = info["phone_num"]
		called_time = info["called_time"]
		insert_call(device_id, phone_num, called_time)
		return "Sucess."
	except:
		return "Fail."

@app.route('/api/v1/get_call', methods=['POST'])
def get_call():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		calls = query_db("SELECT phone_num, called_time FROM phonecall_records WHERE device_id = ? ORDER BY saved_time DESC", [device_id])
		if calls is not None:
			nums = []
			times = []
			for call in calls:
				nums.append(call[0])
				times.append(call[1])
			return jsonify({'phone_num': nums, 'called_time': times})
		else:
			return "No record found."
	except:
		return "Bad request."

@app.route('/api/v1/do_query', methods=['POST'])
def do_query():	
	if request.remote_addr == '127.0.0.1':
		try:
			info = request.get_json(silent=True)
			query = info['query']
			args = info['args']
			return jsonify(query_db(query, args))
		except:
			return 'Bad request.'
	else:
		return 'Localhost only.'

@app.route('/api/v1/send_msg', methods=['POST'])
def send_msg():
	try:
		info = request.get_json(silent=True)
		phone_num = info["phone_num"]
		return sms.sendMsg(phone_num, u"您的家人在找您")
	except:
		return "Bad request."

def insert_gps(device_id, lng, lat):
	with lock:
		db.execute("INSERT INTO gps_records (device_id, lng, lat) VALUES (?, ?, ?)", (device_id, lng, lat))

def insert_call(device_id, phone_num, called_time):
	with lock:
		db.execute("INSERT INTO phonecall_records (device_id, phone_num, called_time) VALUES (?, ?, ?)", (device_id, phone_num, called_time))

def query_db(query, args=()):
	with lock:
		cur = db.execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return rv

def init_db():
	with app.app_context():
		tmp = sqlite3.connect('mem.db')
		with app.open_resource('schema.sql', mode='r') as f:
			tmp.cursor().executescript(f.read())
		query = "".join(line for line in tmp.iterdump())
		tmp.close()
		db = sqlite3.connect(':memory:', check_same_thread=False)
		db.cursor().executescript(query)
		return db

def close_connection():
	os.remove('mem.db')
	query = "".join(line for line in db.iterdump())
	tmp = sqlite3.connect('mem.db')
	tmp.executescript(query)
	tmp.close()
	db.close()

if __name__ == '__main__':
	logging.basicConfig(filename="sever.log", level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
	db = init_db()
	lock = Lock()
	sms = kotsms.kotsms()
	sms.login(const.SMS_USERNAME, const.SMS_PASSWORD)
	app.run( 
		host=const.HOST,
		port=const.PORT,
		threaded=True
	)
	close_connection()

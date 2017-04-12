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
		insert_db(device_id, lng, lat)
		return "Sucess."
	except:
		return "Fail."

@app.route('/api/v1/get_pos', methods=['POST'])
def get_pos():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		coord = query_db("SELECT lng, lat FROM records WHERE device_id = ? ORDER BY saved_time DESC", [device_id])[0]
		if coord is not None:
			return jsonify({'lng': coord[0], 'lat': coord[1]})
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

def insert_db(device_id, lng, lat):
	with lock:
		db.execute("INSERT INTO records (device_id, lng, lat) VALUES (?, ?, ?)", (device_id, lng, lat))

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

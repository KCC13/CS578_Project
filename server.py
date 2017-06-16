# -*- coding: utf-8 -*-
import os
import sqlite3
import json
import kotsms
import const
import logging
from threading import Lock
from datetime import timedelta
from flask import Flask, request, jsonify, make_response, current_app
from functools import update_wrapper

app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/')
def hello_world():
    return 'Nothing here, get out!'

@app.route('/api/v1/add_pos', methods=['POST'])
@crossdomain(origin='*')
def add_pos():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		lng = info["lng"]
		lat = info["lat"]
		insert_gps(device_id, lng, lat)
		return "Sucess."
	except Exception,e:
		logging.error(str(e))
		return "Fail."

@app.route('/api/v1/get_pos', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=const.headers)
def get_pos():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		coord = query_db("SELECT lng, lat, saved_time FROM gps_records WHERE device_id = ? ORDER BY saved_time DESC", [device_id])[0]
		if coord is not None:
			return jsonify({'lng': coord[0], 'lat': coord[1], "time":coord[2]})
		else:
			return "No record found."
	except Exception,e:
		logging.error(str(e))
		return "Bad request."

@app.route('/api/v1/get_2_pos', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=const.headers)
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
	except Exception,e:
		logging.error(str(e))
		return "Bad request."

@app.route('/api/v1/get_all_pos', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=const.headers)
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
	except Exception,e:
		logging.error(str(e))
		return "Bad request."

@app.route('/api/v1/add_call', methods=['POST'])
def add_call():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		phone_num = info["phone_num"]
		called_to = info["called_to"]
		called_time = info["called_time"]
		insert_call(device_id, phone_num, called_to, called_time)
		return "Sucess."
	except Exception,e:
		print str(e)
		logging.error(str(e))
		return "Fail."

@app.route('/api/v1/get_call', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=const.headers)
def get_call():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		calls = query_db("SELECT phone_num, called_to, called_time FROM phonecall_records WHERE device_id = ? ORDER BY saved_time DESC", [device_id])
		if calls is not None:
			history = [{"phone_num": call[0], "called_to": call[1], "called_time": call[2]} for call in calls]
			return jsonify(history)
		else:
			return "No record found."
	except Exception as e:
		print str(e)
		logging.error(str(e))
		return "Bad request."

@app.route('/api/v1/add_bettary', methods=['POST'])
def add_bettary():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		bettary = info["bettary"]
		insert_bettary(device_id, bettary)
		return "Sucess."
	except Exception,e:
		print str(e)
		logging.error(str(e))
		return "Fail."

@app.route('/api/v1/get_bettary', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=const.headers)
def get_bettary():
	try:
		info = request.get_json(silent=True)
		device_id = info["device_id"]
		bettary = query_db("SELECT bettary FROM bettary_records WHERE device_id = ?", [device_id])[0]
		if bettary is not None:
			history = {"bettary": bettary[0]}
			return jsonify(history)
		else:
			return "No record found."
	except Exception as e:
		print str(e)
		logging.error(str(e))
		return "Bad request."

@app.route('/api/v1/do_query', methods=['POST'])
def do_query():	
	if request.remote_addr == '127.0.0.1':
		try:
			info = request.get_json(silent=True)
			query = info['query']
			args = info['args']
			return jsonify(query_db(query, args))
		except Exception,e:
			logging.error(str(e))
			return 'Bad request.'
	else:
		return 'Localhost only.'

@app.route('/api/v1/send_msg', methods=['POST'])
def send_msg():
	try:
		info = request.get_json(silent=True)
		phone_num = info["phone_num"]
		return sms.sendMsg(phone_num, u"您的家人在找您")
	except Exception,e:
		logging.error(str(e))
		return "Bad request."

def insert_gps(device_id, lng, lat):
	with lock:
		db.execute("INSERT INTO gps_records (device_id, lng, lat) VALUES (?, ?, ?)", (device_id, lng, lat))

def insert_call(device_id, phone_num, called_to, called_time):
	with lock:
		db.execute("INSERT INTO phonecall_records (device_id, phone_num, called_to, called_time) VALUES (?, ?, ?, ?)", (device_id, phone_num, called_to, called_time))

def insert_bettary(device_id, bettary):
	with lock:		
		db.execute("REPLACE INTO bettary_records (device_id, bettary) VALUES (?, ?)", (device_id, bettary))

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

CREATE TABLE IF NOT EXISTS gps_records 
(db_id 		INTEGER 					PRIMARY KEY, 
device_id 	TEXT			NOT NULL, 
lng 		DECIMAL(9, 6) 	NOT NULL, 
lat 		DECIMAL(9, 6) 	NOT NULL, 
saved_time 	TIMESTAMP		NOT NULL  	DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS phonecall_records 
(db_id 		INTEGER 					PRIMARY KEY, 
device_id 	TEXT 			NOT NULL, 
phone_num 	TEXT		 	NOT NULL, 
called_time TIMESTAMP 		NOT NULL, 
saved_time 	TIMESTAMP		NOT NULL  	DEFAULT CURRENT_TIMESTAMP);
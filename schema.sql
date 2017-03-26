CREATE TABLE IF NOT EXISTS records 
(db_id 		INTEGER 					PRIMARY KEY, 
device_id 	INTEGER 		NOT NULL, 
lng 		DECIMAL(9, 6) 	NOT NULL, 
lat 		DECIMAL(9, 6) 	NOT NULL, 
saved_time 	TIMESTAMP		NOT NULL  	DEFAULT CURRENT_TIMESTAMP);
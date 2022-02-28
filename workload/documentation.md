##### main.py -> dbsqlite.py
-  init_db_sqlite3()
-  get_db_sqlite3()
-  insert_record_sqlite3(r)
-  query_record_sqlite3()

##### main.py -> dbmongo.py
-  get_db_mongo()
-  insert_record_mongo(r)
-  query_record_mongo(page)

##### Simulator.py -> gps.py
-  load_gps_paths()

##### Simulator.py -> waves.py
-  load_wave()

##### Simulator.py -> settings.py
-  load_sensors_settings()
-  load_schedule_settings(path)
-  get_collection_and_configuration()

##### Simulator.py -> sensor.py
-  init_sensor(simulator, id, config)
-  run_sensor(simulator, id, config)
-  start_sensors(simulator, new_sensors, configs)
-  stop_sensors(simulator, new_sensors)

##### Simulator.py -> sensormsgs.py
-  send_sensor_msg(session, url, msg)
-  get_device_sensor_msg(sensor)
-  get_temp_sensor_msg(sensor)
-  get_gps_sensor_msg(sensor)
-  get_camera_sensor_msg(sensor)
-  get_asd_sensor_msg(sensor)

##### Simulator.py -> db.py
-  insertToDB(collection, item)

##### sensormsgs.py -> sensors.device.py
- get_device_sensor_msg(sensor)

##### sensormsgs.py -> sensors.gps.py
- get_gps_sensor_msg(sensor)

##### sensormsgs.py -> sensors.sensor.py
- stop_sensors(simulator, new_sensors)
- start_sensors(simulator, new_sensors, configs)
- run_sensor(simulator, id, config)
- init_sensor(simulator, id, config)

##### sensormsgs.py -> sensors.sensormsgs.py

##### sensormsgs.py -> sensors.temperature.py
- get_temp_sensor_msg(sensor)

##### sensormsgs.py -> sensors.camera.py
- get_camera_sensor_msg(sensor)

#### Simulator.py -> statistics.py
- do_statistics(simulator, interval, collection)

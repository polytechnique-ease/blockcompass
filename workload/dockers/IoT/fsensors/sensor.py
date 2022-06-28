import asyncio
import aiohttp
import fsensors.sensormsgs
import fsensors.temperature
import fsensors.gps
import fsensors.device
import fsensors.asd
import fsensors.camera
import random
import time
import __main__ as Simulator

# Initialize the sensor
def init_sensor(simulator, id, config):
    session = aiohttp.ClientSession()
    t = {
        "url": simulator["url"],
        "session": session,
        "id": config[0] + "_" + str(id),
        "seqno": 0
    }
    if config[0] == "device":
        t["mean"] = float(config[1])
        t["sigma"] = float(config[2])
        t["func"] = fsensors.device.get_device_sensor_msg
    elif config[0] == "temp":
        t["interval"] = float(config[1])
        t["mean"] = random.uniform(-30, 50)
        t["func"] = fsensors.temperature.get_temp_sensor_msg
    elif config[0] == "gps":
        t["interval"] = float(config[1])
        t["dir"] = True
        t["spot"] = random.randrange(0, len(Simulator.gps_paths), 1)
        t["func"] = fsensors.gps.get_gps_sensor_msg
    elif config[0] == "camera":
        t["fps"] = int(config[1])
        t["bitrate"] = int(config[2])
        t["motion"] = (random.choice([0, 1]) == 1)
        t["motion_time"] = float(random.uniform(1, 10))
        t["cur_time"] = 0
        t["func"] = fsensors.camera.get_camera_sensor_msg
    elif config[0] == "asd":
        t["sps"] = int(config[1])
        t["spot"] = random.randrange(0, len(Simulator.wave_data), 1)
        t["func"] = fsensors.asd.get_asd_sensor_msg
    else:
        Simulator.L.error("Sensor %d: No such type" % id)
    return t

# Run the id-th sensor
async def run_sensor(simulator, id, config):
    Simulator.L.info("Sensor %d: Start %s" % (id, str(config)))
    sensor = init_sensor(simulator, id, config)
    metrics = simulator["metrics"]

    while (id < simulator["cur_sensors"]):
        msg, st = sensor["func"](sensor)
        # L.info("Sensor %d: Send %d bytes, Sleep %.2f" % (id, len(msg), st))
        starttime = time.time()
        success = await fsensors.sensormsgs.send_sensor_msg(sensor["session"], sensor["url"], msg)
        endtime = time.time()

        if success:
            # send request
            metrics[0] += 1
            # latency
            metrics[2] += endtime - starttime
        else:
            # error request
            metrics[1] += 1

        diff = st - (endtime - starttime)
        if diff > 0:
            await asyncio.sleep(st)

    await sensor["session"].close()
    Simulator.L.info("Sensor %d: Exit" % id)


# Start new sensors
def start_sensors(simulator, new_sensors, configs):
    num_configs = len(configs)
    old_sensors = simulator["cur_sensors"]
    simulator["cur_sensors"] = new_sensors
    for i in range(old_sensors, new_sensors):
        config = configs[i % num_configs]
        task = simulator["loop"].create_task(run_sensor(simulator, i, config))
        # simulator["tasks"].append(task)


# Stop current sensors
def stop_sensors(simulator, new_sensors):
    simulator["cur_sensors"] = new_sensors
    # old_tasks = []
    # for i in range(len(simulator["tasks"]), new_sensors, -1):
    #    old_tasks.append(simulator["tasks"].pop())
    # return old_tasks

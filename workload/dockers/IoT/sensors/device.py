import __main__ as Simulator
import random
import time
import json

# Generate messages from device sensor
# ON / OFF
def get_device_sensor_msg(sensor):
    val = random.choice(["OFF", "ON"])
    valString = str(val)
    for i in range(Simulator.size):
        valString += valString

    msg = {
        "dev_id": str(sensor["id"]),
        "ts": round(time.time(), 5),
        "seq_no": sensor["seqno"],
        "data_size": len(valString),
        "sensor_data": str(valString)
    }
    sensor["seqno"] += 1
    st = random.gauss(sensor["mean"], sensor["sigma"])
    return json.dumps(msg), st
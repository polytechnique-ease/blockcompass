import __main__ as Simulator
import random
import time
import json

# Generate messages from temperature sensor
# the temperature value
def get_temp_sensor_msg(sensor):
    val = str(round(random.normalvariate(sensor["mean"], 10), 1))
    valString = str(val)
    for i in range(Simulator.size):
        valString += valString
    valString += " C"
    msg = {
        "dev_id": str(sensor["id"]),
        "ts": round(time.time(), 5),
        "seq_no": sensor["seqno"],
        "data_size": len(valString),
        "sensor_data": str(valString)
    }
    sensor["seqno"] += 1
    st = sensor["interval"]
    return json.dumps(msg), st
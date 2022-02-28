import __main__ as Simulator
import time
import json

# Generate messages from gps sensor
# the position value
def get_gps_sensor_msg(sensor):
    j = sensor["spot"]
    val = "(%f,%f)" % (Simulator.gps_paths[j][0], Simulator.gps_paths[j][1])
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
    if sensor["dir"]:
        j += 1
        if j >= len(Simulator.gps_paths):
            j = len(Simulator.gps_paths) - 2
            sensor["dir"] = False
    else:
        j -= 1
        if j < 0:
            j = 1
            sensor["dir"] = True
    sensor["spot"] = j
    st = sensor["interval"]

    return json.dumps(msg), st
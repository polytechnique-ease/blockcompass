import __main__ as Simulator
import json
import time

# Generate messages from ASD sensor
# Sound value
def get_asd_sensor_msg(sensor):
    j = sensor["spot"]
    val = str(Simulator.wave_data[j])
    for i in range(Simulator.size):
        val += str(val)
    msg = {
        "dev_id": str(sensor["id"]),
        "ts": round(time.time(), 5),
        "seq_no": sensor["seqno"],
        "data_size": len(val),
        "sensor_data": str(val)
    }
    sensor["seqno"] += 1
    st = 1 / sensor["sps"]
    sensor["spot"] = (j + round(120 / sensor["sps"])) % len(Simulator.wave_data)

    return json.dumps(msg), st
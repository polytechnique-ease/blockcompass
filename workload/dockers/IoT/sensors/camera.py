import __main__ as Simulator
import random
import os
import time
import json

# Generate messages from camera value
# NO_MOTION or video value
def get_camera_sensor_msg(sensor):
    new_motion = False
    if sensor["motion"]:
        fps = sensor["fps"]
        bitrate = int(random.uniform(sensor["bitrate"] / 4, sensor["bitrate"]))
        val = os.urandom(int(bitrate / 8 / fps))
        st = float(1.0 / fps)
        sensor["cur_time"] += st
        if sensor["cur_time"] > sensor["motion_time"]:
            new_motion = True
    else:
        val = "NO_MOTION"
        st = sensor["motion_time"]
        new_motion = True

    if new_motion:
        sensor["motion"] = (random.choice([0, 1]) == 1)
        sensor["motion_time"] = float(random.uniform(1, 10))
        sensor["cur_time"] = 0

    valString = str(val)
    for i in range(Simulator.size):
        valString += valString
    msg = {
        "dev_id": str(sensor["id"]),
        "ts": round(time.time(), 5),
        "seq_no": sensor["seqno"],
        "data_size": len(valString),
        "sensor_data": valString
    }
    sensor["seqno"] += 1
    return json.dumps(msg), st
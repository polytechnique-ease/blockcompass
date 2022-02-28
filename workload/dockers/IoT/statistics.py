import __main__ as Simulator
import time
import asyncio
import pytz
import db
from datetime import datetime

# Do statistics and output
async def do_statistics(simulator, interval, collection):
    metrics = simulator["metrics"]
    with open("run/metrics.csv", "w") as f:
        f.write("Time,Sensors,Requests,success,ErrorRate,AvgLatency\n")
        while simulator["running"]:
            await asyncio.sleep(interval)

            avgLatency = metrics[2] / metrics[0] * \
                1000 if metrics[0] > 0 else 0.0
            allRequests = metrics[0] + metrics[1]
            succRequests = metrics[0]
            errorRate = metrics[1] / allRequests if allRequests > 0 else 0.0

            Simulator.L.info(
                "METRIC: %d sensors, %.2f seconds, %d requests, %d success , Error Rate: %.2f, Average Latency: %.2f ms" %
                (simulator["cur_sensors"], interval, allRequests, succRequests, errorRate, avgLatency))

            t = time.localtime()
            f.write("%02d:%02d:%02d,%d,%d,%d,%.2f,%.2f\n" % (t.tm_hour, t.tm_min, t.tm_sec,
                                                             simulator["cur_sensors"],
                                                             allRequests, succRequests, errorRate, avgLatency))
            tz = pytz.timezone(Simulator.timezone)
            data = {
                "time": datetime.now(tz),
                "sensors": simulator["cur_sensors"],
                "allRequests": allRequests,
                "succRequests": succRequests,
                "errorRate": errorRate,
                "avgLatency": avgLatency

            }
            db.insertToDB(collection, data)
            metrics[0] = 0
            metrics[1] = 0
            metrics[2] = 0.0
import sys
import logging
import gps
import waves
import asyncio
import settings
import statistics
import fsensors.sensor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

# Init vars
global L
L = logging.getLogger()
global gps_paths 
gps_paths = []
wave_data = []
global size
size = 1
global timezone
timezone = "Africa/Tunis"

async def run_scheduler(simulator, schedules, sensors, collection):
    simulator["loop"].create_task(statistics.do_statistics(simulator, 10, collection))
    for sched in schedules:
        L.info("%d sensors in %d seconds" % sched)

        if simulator["workload_type"] == "transactional":
            if sched[0] > simulator["cur_sensors"]:
                fsensors.sensor.start_sensors(simulator, sched[0], sensors)
            else:
                fsensors.sensor.stop_sensors(simulator, sched[0])
            await asyncio.sleep(sched[1])

        elif simulator["workload_type"] == "batch":
            num_batches = sched[1]
            for _ in range(num_batches):
                # Send a batch of requests equal to sched[0] (number of sensors)
                await send_batch_requests(simulator, sched[0], sensors)
                await asyncio.sleep(1)  # Wait for 1 second before sending the next batch

    tasks = fsensors.sensor.stop_sensors(simulator, 0)
    simulator["running"] = False
    await asyncio.sleep(12)

async def send_batch_requests(simulator, num_requests, sensors):
    fsensors.sensor.start_sensors(simulator, num_requests, sensors)
    await asyncio.sleep(0.1)  # Give a short time for the requests to be sent
    fsensors.sensor.stop_sensors(simulator, num_request


def main(argv):
    if len(argv) != 3:
        L.error("Usage: %s server_url workload_type" % argv[0])
        return
    server_url = argv[1]
    workload_type = argv[2]

    if workload_type not in ['transactional', 'batch']:
        L.error("Invalid workload type. Expected 'transactional' or 'batch'.")
        return

    collection = settings.get_collection_and_configuration()
    gps.load_gps_paths()
    waves.load_wave()
    sensors = settings.load_sensors_settings("run/users.list")
    schedules = settings.load_schedule_settings("run/schedule.list")
    loop = asyncio.get_event_loop()
    metrics = [0, 0, 0.0]
    simulator = {
        "url": server_url,
        "loop": loop,
        "cur_sensors": 0,
        "tasks": [],
        "metrics": metrics,
        "running": True,
        "workload_type": workload_type  # add workload type to the simulator dictionary
    }
    loop.run_until_complete(run_scheduler(simulator, schedules, sensors, collection))
    loop.close()

if __name__ == "__main__":
    main(sys.argv)

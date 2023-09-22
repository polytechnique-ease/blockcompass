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

# Run the scheduler
async def run_scheduler(simulator, schedules, sensors, collection):
    simulator["loop"].create_task(statistics.do_statistics(simulator, 10, collection))
    for sched in schedules:
        L.info("%d sensors in %d seconds" % sched)
        if sched[0] > simulator["cur_sensors"]:
            fsensors.sensor.start_sensors(simulator, sched[0], sensors)
        else:
            fsensors.sensor.stop_sensors(simulator, sched[0])
        await asyncio.sleep(sched[1])
    tasks = fsensors.sensor.stop_sensors(simulator, 0)
    simulator["running"] = False
    await asyncio.sleep(12)


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

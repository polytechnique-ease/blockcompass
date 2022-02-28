import __main__ as Simulator
import pymongo
import yaml

# Load settings of sensors from path
# File format: Each line:
# sensor_type sensor_settings
def load_sensors_settings(path):
    sensors = []
    with open(path) as f:
        for line in f.readlines():
            ss = line.strip().split(" ")
            if (len(ss) >= 1):
                sensors.append(ss)
    return sensors

# Load settings of schedule from path
# File format: Each line:
# num_sensors runtime
def load_schedule_settings(path):
    scheds = []
    with open(path) as f:
        for line in f.readlines():
            ss = line.strip().split(" ")
            if (len(ss) == 2):
                scheds.append((int(ss[0]), int(ss[1])))
            # elif(len(ss) != 0):
            #    L.warning("Schedule configs: Unsupported format: " + str(ss))

    return scheds

# get blockchain.yaml file
def get_collection_and_configuration():
    connection_string = []
    with open("/configuration/blockchain.yaml", 'r') as stream:
        try:
            loaded_config = yaml.safe_load(stream)
            if loaded_config['replicaSet']:
                connection_string = loaded_config['replicaSet']
            global timezone
            if loaded_config['timezone']:
                timezone = loaded_config['timezone']
            global size
            if loaded_config['dataSize']:
                size = loaded_config['dataSize']
        except yaml.YAMLError as exc:
            Simulator.L.error(exc)
    try:
        #connection_string = ['service.localhost:27011','service.localhost:27012', 'service.localhost:27013']
        client = pymongo.MongoClient(connection_string, replicaSet='rs0')
        collection = client.benchmarker.performance
        return collection
    except Exception as error:
        Simulator.L.error(error)
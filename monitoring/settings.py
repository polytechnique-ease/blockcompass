import yaml
import pytz
import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    def __init__(self,configurationFile):
        self.configuration_file = configurationFile
        self.connection_string = ""
        self.blockchain = ""
        self.delay = 0
        self.log_monitor_file = "resource-metrics.csv"
        self.timezone = pytz.timezone('Canada/Central')
        self.targets = []
    def import_setting(self,delay):
        self.delay = delay
        with open(self.configuration_file, 'r') as stream:
            try:
                loaded_config = yaml.safe_load(stream)
                if (loaded_config['replicaSet']):
                    self.connection_string = loaded_config['replicaSet']
                    print(self.connection_string)
                    self.blockchain = loaded_config["blockchain"]["type"]
                    self.targets = os.getenv(self.blockchain).split(',')

                if loaded_config['timezone']:
                    timezone = loaded_config['timezone']
                else:
                    timezone = 'Canada/Central'
                self.timezone = pytz.timezone(timezone)

            except yaml.YAMLError as exc:
                print(exc)


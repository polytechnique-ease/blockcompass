from dockerMonitoring import DockerMonitoring
from mongoDB import MongoDB
from settings import Settings
import time

def main():
    settings = Settings("../configuration/blockchain.yaml")
    settings.import_setting(10)
    database = MongoDB(settings.connection_string)
    docker_monitor = DockerMonitoring(database, settings)
    # write target containers names to file
    docker_monitor.writeNamesToFile()
    while True:
        start_time = time.time()
        print("INFO:\tStart checking ...")
        docker_monitor.get_measurements()
        end_time = time.time()
        sleep_time = settings.delay - (end_time - start_time)
        print("INFO:\tFinish checking. Sleeping %.2f seconds ...\n" % sleep_time)
        if sleep_time > 0:
            time.sleep(sleep_time)



if __name__ == "__main__":
    main()
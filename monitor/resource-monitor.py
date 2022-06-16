import time
import os
import sys
import getopt
import pytz
import re
import time
from datetime import datetime

import yaml
import pymongo

check_interval = 10
connection_string = []
blockchain = ""
timezone = "Africa/Tunis"
log_cpu_path = "resource-metrics.csv"


def getName(target):
    pattern = re.compile(r".*%s.*" % target)
    patternDev = re.compile(r".*%s.*" % "dev")
    order = re.compile(r".*%s.*" % "order")
    orderCa = re.compile(r".*%s.*" % "ca")
    registry_tp = re.compile(r".*%s.*" % "registry-tp")
    names = []
    with os.popen("sudo docker stats --no-stream") as f:
        for s in f.readlines():
            ss = s.split()
            if (pattern.match(ss[1]) or order.match(ss[1])) and (
                    not patternDev.match(ss[1]) and not orderCa.match(ss[1]) and not registry_tp.match(ss[1]) ):
                names.append(ss[1].replace("example.com", ""))
    return names


def read_configuration():
    with open("../configuration/blockchain.yaml", 'r') as stream:
        try:
            loaded_config = yaml.safe_load(stream)
            if (loaded_config['replicaSet']):
                global connection_string
                connection_string = loaded_config['replicaSet']
                print(connection_string)
                global blockchain
                blockchain = loaded_config["blockchain"]["type"]
            global timezone
            if loaded_config['timezone']:
                timezone = loaded_config['timezone']

        except yaml.YAMLError as exc:
            print(exc)


def get_collection():
    client = pymongo.MongoClient(connection_string
                                 , replicaSet='rs0')
    collection = client.benchmarker.resource
    # collection.drop()
    return collection


def insertToDB(collection, item):
    collection.insert_one(item)


def check_utilization(target, collection):
    cpus = []
    mems = []
    net_is = []
    net_os = []
    names = []
    pattern = re.compile(r".*%s.*" % target)
    patternDev = re.compile(r".*%s.*" % "dev")
    order = re.compile(r".*%s.*" % "order")
    orderCa = re.compile(r".*%s.*" % "ca")
    registry_tp = re.compile(r".*%s.*" % "registry-tp")

    with os.popen("docker stats --no-stream") as f:
        for s in f.readlines():
            ss = s.split()
            if len(ss) >= 3 and pattern.match(ss[1]) and (
                    not patternDev.match(ss[1]) and not orderCa.match(ss[1]) and not registry_tp.match(ss[1])):
                name = ss[1].replace("example.com", "")
                names.append(name)
                cu = float(ss[2].replace("%", ""))
                cpus.append(cu)
                mem = float(ss[6].replace("%", ""))
                mems.append(mem)
                net_i = toBytes(ss[7])
                net_o = toBytes(ss[9])
                if net_o is None:
                    net_o = 0
                if net_i is None:
                    net_i = 0
                net_is.append(net_i)
                net_os.append(net_o)

                print("INFO: container %s: cpu %.2f%%, mem %.2f%%, net_i %d B, net_o %d B" % (
                    name, cu, mem, net_i, net_o))

    num = len(cpus)
    avg_cpu = sum(cpus) / num if num > 0 else -1
    avg_mem = sum(mems) / num if num > 0 else -1
    avg_net_i = sum(net_is) / num if num > 0 else -1
    avg_net_o = sum(net_os) / num if num > 0 else -1

    tz = pytz.timezone(timezone)

    data = {
        "time": datetime.now(tz),
        "avgCPU": avg_cpu,
        "avgMEM": avg_mem,
        "avgNetI": avg_net_i,
        "avgNetO": avg_net_o,
        "containers": []
    }

    for i in range(len(names)):
        data["containers"].append({
            "name": names[i],
            "cpu": cpus[i],
            "mem": mems[i],
            "netI": net_is[i],
            "netO": net_os[i]
        })

    insertToDB(collection, data)

    writeToFile(num, avg_cpu, avg_mem, avg_net_i, avg_net_o, cpus, mems, net_is, net_os)


def writeToFile(num, avg_cpu, avg_mem, avg_net_i, avg_net_o, cpus, mems, net_is, net_os):
    log_file = open(log_cpu_path, "a")
    log_file.write((datetime.now().strftime("%H:%M:%S"),
                                                   num, avg_cpu, avg_mem, avg_net_i, avg_net_o,
                                                   ",".join( (
                                                       cpus[i], mems[i], net_is[i], net_os[i]) for i in
                                                            range(num))))
    log_file.close()


def toBytes(transform):
    r = re.compile("([-+]?\d*\.\d+|\d+)([a-zA-Z]+)")
    match = r.match(transform)

    if match:
        value = match.group(1)
        unit = match.group(2)
        unit = unit.lower()
        if value is None:
            return 0
        if unit == "kb":
            return float(value) * 1000
        if unit == "mb":
            return float(value) * 1000000
        if unit == "gb":
            return float(value) * 1000000
    else:
        raise Exception("error formation %s", transform)


def main():
    read_configuration()
    collection = get_collection()
    global source
    print(blockchain)
    if blockchain in ["sawtooth-pbft", "sawtooth-raft", "sawtooth-poet"]:
        source = "validator"
    elif blockchain == "fabric":
        source = "peer"
    elif blockchain == "ethereum-clique" or blockchain == "ethereum-pow":
        source = "miner"
    else:
        print("target must be sawtooth-pbft, sawtooth-raf ,sawtooth-poet, fabric or ethereum-clique or ethereum-pow")
        exit(0)

    log_file = open(log_cpu_path, "w")
    names = getName(source)
    headline = "Time,Num,AvgCPU,AvgMEM,AvgNetI,AvgNetO,"
    for name in names:
        headline += name + "-CPU" + "," + name + "-mem" + "," + name + "-netI" + "," + name + "-netO" + ","
    headline = headline[:-1]
    headline += "\n"
    log_file.write(headline)
    log_file.close()
    while True:
        start_time = time.time()
        print("INFO:\tStart checking ...")
        check_utilization(source, collection)
        end_time = time.time()
        sleep_time = check_interval - (end_time - start_time)
        print("INFO:\tFinish checking. Sleeping %.2f seconds ...\n" % sleep_time)
        if sleep_time > 0:
            time.sleep(sleep_time)


if __name__ == "__main__":
    main()

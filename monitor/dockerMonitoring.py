import time
import os
import sys
import getopt
import pytz
import re
import time
from datetime import datetime
from dotenv import load_dotenv
from monitoring import Monitoring
from untils import toBytes

load_dotenv()


class DockerMonitoring(Monitoring):
    def __init__(self, database, settings):
        super().__init__(database)
        self.settings = settings
        self.nb_containers = 0
        self.net_os = []
        self.net_is = []
        self.cpus = []
        self.names = []
        self.memories = []
        self.avg_cpu = 0.00
        self.avg_mem = 0.00
        self.avg_net_i = 0.00
        self.avg_net_o = 0.00

    def check_pattern(self, container):
        for target in self.settings.targets:
            pattern = re.compile(r".*%s.*" % target)
            if pattern.match(container):
                return True
        False

    def get_names(self):
        names = []
        with os.popen("sudo docker stats --no-stream") as f:
            for s in f.readlines():
                ss = s.split()
                if self.check_pattern(ss[1]):
                    names.append(ss[1].replace("example.com", ""))
        return names

    def get_measurements(self):

        with os.popen("docker stats --no-stream") as f:
            for s in f.readlines()[1:]:
                ss = s.split()
                if len(ss) >= 3 and self.check_pattern(ss[1]):
                    name = ss[1].replace("example.com", "")
                    self.names.append(name)
                    cu = float(ss[2].replace("%", ""))
                    self.cpus.append(cu)
                    mem = float(ss[6].replace("%", ""))
                    self.memories.append(mem)
                    net_i = toBytes(ss[7])
                    net_o = toBytes(ss[9])
                    if net_o is None:
                        net_o = 0
                    if net_i is None:
                        net_i = 0
                    self.net_is.append(net_i)
                    self.net_os.append(net_o)
                    print("INFO: container %s: cpu %.2f%%, mem %.2f%%, net_i %d B, net_o %d B" % (
                        name, cu, mem, net_i, net_o))





        num = len(self.cpus)
        self.avg_cpu = sum(self.cpus) / num if num > 0 else -1
        self.avg_mem = sum(self.memories) / num if num > 0 else -1
        self.avg_net_i = sum(self.net_is) / num if num > 0 else -1
        self.avg_net_o = sum(self.net_os) / num if num > 0 else -1

        data = {
            "time": datetime.now(self.settings.timezone),
            "avgCPU": self.avg_cpu,
            "avgMEM": self.avg_mem,
            "avgNetI": self.avg_net_i,
            "avgNetO": self.avg_net_o,
            "containers": []
        }

        for i in range(len(self.names)):
            data["containers"].append({
                "name": self.names[i],
                "cpu": self.cpus[i],
                "mem": self.memories[i],
                "netI": self.net_is[i],
                "netO": self.net_os[i]
            })

        self.database_insertion(data)

        self.writeToFile(num, self.avg_cpu, self.avg_mem, self.avg_net_i, self.avg_net_o,
                         self.cpus, self.memories, self.net_is, self.net_os)

    def writeToFile(self, num, avg_cpu, avg_mem, avg_net_i, avg_net_o, cpus, memories, net_is, net_os):
        log_file = open(self.settings.log_monitor_file, "a")
        log_file.write("%s,%d,%.2f,%.2f,%d,%d,%s\n" % (datetime.now().strftime("%H:%M:%S"),
                                                       num, avg_cpu, avg_mem, avg_net_i, avg_net_o,
                                                       ",".join("%.2f,%.2f,%.3f,%.3f" % (
                                                           cpus[i], memories[i], net_is[i], net_os[i]) for i in
                                                                range(num))))

    def writeNamesToFile(self):
        log_file = open(self.settings.log_monitor_file, "w")
        names = self.get_names()
        headline = "Time,Num,AvgCPU,AvgMEM,AvgNetI,AvgNetO,"
        for name in names:
            headline += name + "-CPU" + "," + name + "-mem" + "," + name + "-netI" + "," + name + "-netO" + ","
        headline = headline[:-1]
        headline += "\n"
        log_file.write(headline)
        log_file.close()

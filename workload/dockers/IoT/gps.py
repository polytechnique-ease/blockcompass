import csv
import __main__ as Simulator

def load_gps_paths():
    with open('gps_path.txt', 'r') as gpsfile:
        p = csv.reader(gpsfile, delimiter='\t')
        for row in p:
            if len(row) >= 3:
                r = [float(row[0]), float(row[1]), float(row[2])]                
                Simulator.gps_paths.append(r)
    Simulator.L.info("GPS paths: %d rows" % len(Simulator.gps_paths))


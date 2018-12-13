import os
import glob
import time
import math
from cachetools import cached, TTLCache
 
# Enable One Wire Interface 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
cache = TTLCache(maxsize=1, ttl=300)
 
def read_sensor():
    lines = ["" for i in range(2)]
    while lines[0].strip()[-3:] != 'YES':
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        time.sleep(0.2)
    return lines

@cached(cache)
def read_temp():
    lines = read_sensor()
    temp_line = lines[1]
    t_pos = temp_line.find('t=')
    if t_pos != -1:
        temp_string = lines[1][t_pos+2:] # Read the raw value
        temp_c = float(temp_string) / 1000.0 # Convert to Celcius
        temp_f = math.floor(temp_c * 9.0 / 5.0 + 32.0) # Convert to Farenheit and floor
        return temp_f


if __name__ == "__main__":
    f = read_temp()
    str = "Temperature - F: {0}".format(f)
    print(str)

    
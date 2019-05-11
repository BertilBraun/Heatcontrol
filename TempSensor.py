import os
import glob
import time

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')

def read_temp_raw(i):
    f = open(device_folder[i] + '/w1_slave', 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(i):
    lines = read_temp_raw(i)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp = round(float(temp_string) / 1000.0, 1)
        return temp

#!/usr/bin/env python
import sys
import commands
import signal
import time
import multiprocessing
import simplejson as json

stop_event = multiprocessing.Event()

def stop(signum, frame):
    stop_event.set()

signal.signal(signal.SIGTERM, stop)

bandwidthpre = 0
bandwidthnew = 0
bandwidthtotal = 0

if __name__ == '__main__':
    while not stop_event.is_set():
	cpu = commands.getoutput("zabbix_get -s 127.0.0.1 -I 127.0.0.1 -k system.cpu.util[all,idle,avg1]")
	load = commands.getoutput("zabbix_get -s 127.0.0.1 -I 127.0.0.1 -k system.cpu.load[all,avg1]")
	bandwidth = commands.getoutput("zabbix_get -s 127.0.0.1 -I 127.0.0.1 -k net.if.out[bond0]")
	cpu = 100.0 - float(cpu)
	bandwidthnew = float(bandwidth)
	bandwidthtotal = (float(bandwidthnew) - float(bandwidthpre))/3
	data = json.dumps({'cpu': int(float(cpu)), 'load': int(float(load)), 'bandwidth': int(float(bandwidthtotal)) }, sort_keys=True, indent=4 * ' ')
	f = open ('zabbix_data.json','w+')
	f.write(data)
	f.close()
	bandwidthpre = float(bandwidth)
        time.sleep(3)

#!/bin/env python2.7
# desc: simple way to extract metrics from logs and store into statsd (influx/graphite)
import os
import statsd
import eventlet
from eventlet.green.socket import *

HOST = ('aurek.aurebesh.net', 8125)

# bind udp port 1055, which will receive log lines from rsyslog
def server():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', 1055))
    while True:
        eventlet.spawn(handle_client, sock.recvfrom(4096))

# send every request/logline as an increment to statsd service
def handle_client(data):
    try:
        c = statsd.StatsClient(HOST[0],HOST[1])
        key = "%s%s" % (os.uname()[1], ".req")
        c.incr(key,1)
        c.incr(key + str(data[0].split()[6]),1)
        print key
    except Exception as E:
        print E
        pass
if __name__ == "__main__":
    server()

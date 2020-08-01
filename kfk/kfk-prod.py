#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2020 Jul 17 10:07:59 PM

#import os
#import sys 
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from kafka import KafkaProducer as kp

now = int(time.time())
today = int(now+8*3600)/86400*86400-8*3600
dayts = 86400
hourts = 3600
mints = 60
yesterday = today - dayts

def YMD(ts):
    return time.strftime("%Y%m%d", time.localtime(ts))

def YM(ts):
    return time.strftime("%Y%m", time.localtime(ts))

def DAY(ts):
    return time.strftime("%d", time.localtime(ts))

kafka_hosts = ["localhost:9092"]
kafka_topic = "new_topic"
msg = "again"
#kafka_group = "group_test"

c = kp(bootstrap_servers=kafka_hosts)

def main():
    c.send(kafka_topic, msg)


if __name__ == "__main__":
    main()


#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2020 Jul 17 10:04:36 PM

#import os
#import sys 
#sys.path.append(os.path.abspath("../../"))
import time
from kafka import KafkaConsumer as kc

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
kafka_group = "group_test"
kafka_topic = "multipart"
def main():
    cons = kc(bootstrap_servers=kafka_hosts,group_id=kafka_group)
    cons.subscribe(kafka_topic)
    for m in cons:
        print m

if __name__ == "__main__":
    main()


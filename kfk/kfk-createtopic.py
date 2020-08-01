#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: user
# Date  : 2020 Jul 17 10:16:35 PM

import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from kafka import KafkaAdminClient as kac
from kafka.admin import NewTopic
from lib.decorator.safe_run import safe_run

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

kafka_host = ["localhost:9092"]
kafka_topic_name = "new_topic"
partitions = 3

def main():
    run()
    print "ok"

@safe_run
def run():
    c = kac(bootstrap_servers=kafka_host)
    kl = []
    kl.append(NewTopic(name=kafka_topic_name, num_partitions=partitions,replication_factor=1))
    c.create_topics(new_topics=kl)

if __name__ == "__main__":
    main()


#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: sansna
# Date  : 2020 Nov 05 10:24:41

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import time
import datetime
from kafka import KafkaConsumer as kc, TopicPartition, OffsetAndMetadata
from decorator.safe_run import safe_run_wrap

# App Config
# XXX: https://stackoverflow.com/questions/3536620/how-to-change-a-module-variable-from-another-module
#if __name__ == "__main__":
#    import config.base
#    if not config.base.Configured:
#        config.base.Configured = True
#        config.base.App = "lib/kfk"
#        config.base.Env = config.base.ENV_PRODUCTION

now = int(time.time())
today = int(now+8*3600)/86400*86400-8*3600
dayts = 86400
hourts = 3600
mints = 60
yesterday = today - dayts
nowdate = datetime.datetime.fromtimestamp(now)
Year = nowdate.year
Month = nowdate.month
Day = nowdate.day
BeginOfCurrentMonth = datetime.date(Year, Month, 1)
BeginOfLastMonth = (BeginOfCurrentMonth - datetime.timedelta(1)).replace(day=1)
BeginOfCurrentYear = BeginOfCurrentMonth.replace(month=1)
BeginOfLastYear = (BeginOfCurrentYear - datetime.timedelta(1)).replace(month=1, day=1)
BeginOfCurrentMonth = int(time.mktime(BeginOfCurrentMonth.timetuple()))
BeginOfLastMonth = int(time.mktime(BeginOfLastMonth.timetuple()))
BeginOfCurrentYear = int(time.mktime(BeginOfCurrentYear.timetuple()))
BeginOfLastYear = int(time.mktime(BeginOfLastYear.timetuple()))

def YMD(ts):
    return time.strftime("%Y%m%d", time.localtime(ts))

def YM(ts):
    return time.strftime("%Y%m", time.localtime(ts))

def DAY(ts):
    return time.strftime("%d", time.localtime(ts))

@safe_run_wrap
def KfkConnect(kafka_topic="", kafka_hosts=["localhost:9092"], kafka_group="python_test"):
    cons = kc(bootstrap_servers=kafka_hosts,group_id=kafka_group,max_poll_interval_ms=300000,max_poll_records=500)
    return conn

@safe_run_wrap
def KfkCons(kafka_topic="", kafka_hosts=["localhost:9092"], kafka_group="python_test"):
    """
    This wrap consumes too slow. And also does not choose its partitions of the same topic.
    """
    cons = KfkConnect(kafka_topic=kafka_topic, kafka_hosts=kafka_hosts, kafka_group=kafka_group)
    cons.subscribe(kafka_topic)
    return cons

@safe_run_wrap
def KfkPartitions(cons, topic):
    """
    生成指定topic的tps
    returns list of partitions numbers
    e.g. [ i for i in xrange(0,16) ]
    """
    return list(cons.partitions_for_topic(topic))

@safe_run_wrap
def KfkGetTps(topic, parts=[0]):
    """
    示例用法：
    tps = KfkGetTps(topic, KfkPartitions(cons, topic))
    """
    return [ TopicPartition(topic, i) for i in parts ]

@safe_run_wrap
def KfkAssign(tps, kafka_topic="", kafka_hosts=["localhost:9092"], kafka_group="python_test"):
    """
    消费指定topic下面的指定partitions
    tps: KfkGetTps() 返回值
    """
    cons = KfkConnect(kafka_topic=kafka_topic, kafka_hosts=kafka_hosts, kafka_group=kafka_group)
    cons.assign(tps)
    return cons

@safe_run_wrap
def GetLatestOffsets(cons, tps):
    """
    获取指定partitions的log offset map
    in: [ TopicPartition(topic, part) ]
    out: dict( tp: offset )
    """
    return cons.end_offsets(tps)

@safe_run_wrap
def KfkToLatest(cons, tps):
    offsets = GetLatestOffsets(cons, tps)
    dic = {}
    for tp, offset in offsets.iteritems():
        dic.update({tp:OffsetAndMetadata(offset,None)})
    cons.commit(dic)

def main():
    for m in KfkCons("online_topic"):
        print m
        # 消息data
        print m.value
        break

if __name__ == "__main__":
    main()


#!/bin/python
import bson
import redis
import argparse
import json
import time
import math
import sys
import pymongo

p = argparse.ArgumentParser(conflict_handler='resolve')
p.add_argument("-h", type=str, default='172.20.20.1',help='mgodb host')
p.add_argument("-p", type=int, default=27065, help='mgo port')
#p.add_argument("-r", type=str, default='',help='mgodb host')
#p.add_argument("-l", type=int, default=6379, help='mgo port')
args = p.parse_args()
conn = pymongo.MongoClient(host=args.h, port=args.p, read_preference=pymongo.read_preferences.ReadPreference.SECONDARY_PREFERRED)
c = redis.StrictRedis(host='172.20.20.2', password='', port=6379)

t = conn['user']['zone_footprint']
t.drop()

cursor = 0
x={}
i=0
while True:
    r = c.scan(match='*user_zone_visit*',cursor=cursor)

    for k in r[1]:
        c.delete(k)


    cursor = r[0]
    if cursor == 0:
        break

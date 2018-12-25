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
p.add_argument("-h", type=str, default='172.16.2.156',help='mgodb host')
p.add_argument("-p", type=int, default=27047, help='mgo port')
#p.add_argument("-r", type=str, default='',help='mgodb host')
#p.add_argument("-l", type=int, default=6379, help='mgo port')
args = p.parse_args()
conn = pymongo.MongoClient(host=args.h, port=args.p, read_preference=pymongo.read_preferences.ReadPreference.SECONDARY_PREFERRED)
c = redis.StrictRedis(host='r-uf6db21c0dd00ee4.redis.rds.aliyuncs.com', password='')

t = conn['record']['adm_record_square']

cursor = 0
x={}
i=0
while True:
    r = c.zscan('record_rds_all_score', cursor=cursor)
    for k in r[1]:
        pid = k[0]
        info = t.find_one({"pid":bson.Int64(pid)})
        if info == None:
            c.zrem('record_rds_all_score',pid)
            #print pid
            continue
        i+=1
        disp = info.get('disp',0)
        view = info.get('detail',0)
        like = info.get('like',0)
        rep1 = info.get('reply',0)
        rep2 = info.get('replyL2',0)
        ct = info.get('ct',0)
        now = int(time.time())
        dura = (now-ct)*1.0/(60*30)
        time_rate = 1/(1+math.exp(-1*((48-dura)/12)))
        score = 0.0
        if (disp > 0):
            score = (0.1*view + 1.5*rep1 + 0.8*rep2 + 1.2*like)/disp
            newscore = score * time_rate
            x[pid] = [newscore,info.get('score',0)]
            #c.zadd('record_rds_all_score', newscore, pid)
            #if newscore < 0.01:
            #    continue
            #print pid, newscore


    cursor = r[0]
    if cursor == 0:
        break

keys = x.keys()
keys.sort()
print i
for k in keys:
    #print k,x[k]
    c.zadd('record_rds_all_score', x[k][0], k)
    #break

#y = sorted(x.items(), key=lambda x:x[0], reverse=False)
#
#for k,v in y:
#    print v, k
#    #c.zadd('record_rds_all_score', v[1], k)

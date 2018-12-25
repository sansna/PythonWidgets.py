#!/bin/python
import redis
import json
import time
import math

c = redis.StrictRedis(host='r-uf6db21c0dd00ee4.redis.rds.aliyuncs.com', password='')

cursor = 0
while True:
    r = c.zscan('record_rds_all_score', cursor=cursor)
    for k in r[1]:
        pid = k[0]
        info = c.get('adm_record_score_%s' % pid)
        if info == None:
            continue
        info = json.loads(info)
        disp = info.get('v',0)
        view = info.get('detail',0)
        like = info.get('u',0)
        rep1 = info.get('r',0)
        rep2 = info.get('r2',0)
        ct = info.get('ct','null')
        now = int(time.time())
        dura = (now-ct)*1.0/(60*30)
        time_rate = 1/(1+math.exp(-1*((48-dura)/12)))
        score = 0.0
        if (disp > 0):
            score = (0.1*view + 1.5*rep1 + 0.8*rep2 + 1.2*like)/disp
            newscore = score * time_rate
            #c.zadd('record_rds_all_score', newscore, pid)
            print pid, newscore
            

        cursor = r[0]
        if cursor == 0:
            break

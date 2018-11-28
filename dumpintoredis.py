#!/usr/bin/python
import sys
import pymongo
import argparse
import time
import datetime
import bson
import redis

p = argparse.ArgumentParser(conflict_handler='resolve')
p.add_argument("-h", type=str, default='localhost',help='mgodb host')
p.add_argument("-p", type=int, default=27047, help='mgo port')
#p.add_argument("-r", type=str, default='',help='mgodb host')
#p.add_argument("-l", type=int, default=6379, help='mgo port')
args = p.parse_args()
conn = pymongo.MongoClient(host=args.h, port=args.p, read_preference=pymongo.read_preferences.ReadPreference.SECONDARY_PREFERRED)

t = conn['record']['record_square']
t2 = conn['record']['adm_record_square']
r = redis.StrictRedis(host="localhost", port=6379, db=0, password="passwd")
i = 0
for doc in t.find({"targer_disp_count":0,"stat.disp":{"$gt":450},"status":1}):
    founddoc = t2.find_one({"pid":bson.Int64(doc['_id'])})
    if (founddoc==None):
        continue
    i=i+1
    doc['pid'] = bson.Int64(doc['_id'])
    doc.pop('_id', None)
    doc.pop('targer_disp_count', None)
    pid = doc["pid"]
    #doc['status'] = bson.Int64(1)
    doc["forbid"] = bson.Int64(0)
    doc["stage"] = bson.Int64(3)
    if 'stat' in doc:
        doc["disp"] = bson.Int64(doc['stat']['disp'])
        doc["like"] = bson.Int64(doc['stat']['like'])
        doc["dislike"] = bson.Int64(doc['stat']['dislike'])
        doc["reply"] = bson.Int64(doc['stat']['reply'])
        doc["ctr"] = doc['stat']['ctr']
        doc["detail_square"] = bson.Int64(doc['stat']['detail_square'])
        doc["detail_friend"] = bson.Int64(doc['stat']['detail_friend'])
        doc["detail"] = bson.Int64(doc['stat']['detail'])
        doc.pop('stat', None)
    t2.insert(doc)
    #t2.find_and_modify(query={"pid":pid},update={"$set":{"stage":bson.Int64(3),"forbid":bson.Int64(0)}})
    if 'city_code' in doc:
        table_all_city="record_rds_all_city_"+doc['city_code']
        #print doc['pid'], doc['ct'], doc['city_code']
        r.zadd(table_all_city,doc['pid'],doc['ct'])
    table_all="record_rds_all_score"
    #print doc['pid'], doc['score']
    r.zadd(table_all, doc['pid'],doc['score'])
print i

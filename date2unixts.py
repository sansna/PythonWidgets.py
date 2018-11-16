#!/usr/local/bin/python
import sys
import pymongo
import argparse
import time
import datetime
from calendar import monthrange

p = argparse.ArgumentParser(conflict_handler='resolve')
p.add_argument("-h", type=str, default='localhost', help='mgodb host')
p.add_argument("-p", type=int, default=27047, help='mgodb port')
p.add_argument("-y", type=int, default=2018, help='year')
p.add_argument("-m", type=int, default=10, help='month')
p.add_argument("-n", type=int, default=None, help='dump limit')
args = p.parse_args()

conn = pymongo.MongoClient(host=args.h, port=args.p, read_preference=pymongo.read_preferences.ReadPreference.SECONDARY_PREFERRED)

t = conn['post']['posts']

cnt = 0
for i in range(1,monthrange(args.y, args.m)[1]):
    df = datetime.date(args.y, args.m, i)
    dt = datetime.date(args.y, args.m, i+1)
    utf = time.mktime(df.timetuple())
    utt = time.mktime(dt.timetuple())
    print args.y,args.m,i, t.find({"ct":{"$gt":utf,"$lt":utt},"c_type":13}).count()
    sys.stdout.flush()

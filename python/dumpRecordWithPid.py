#!/usr/local/bin/python3
import sys
import pymongo
import argparse

p = argparse.ArgumentParser(conflict_handler='resolve')
p.add_argument("-h", type=str, default='172.16.2.157', help='mgodb host')
p.add_argument("-p", type=int, default=27047, help='mgodb port')
p.add_argument("-i", type=int, default=0, help='pid')
p.add_argument("-n", type=int, default=None, help='dump limit')
args = p.parse_args()

conn = pymongo.MongoClient(host=args.h, port=args.p, read_preference=pymongo.read_preferences.ReadPreference.SECONDARY_PREFERRED)

t = conn['record']['record_square']

cnt = 0
for i in t.find({"_id":args.i}):
    if args.n != None and cnt >= args.n:
        break
    cnt += 1
    if cnt % 1000 == 0:
        sys.stderr.write('lines: %d\n' % cnt)

    print cnt, i.get('_id', 0), i.get('mid', 0), i.get('tid', 0), i.get('ct', 0), i.get('ut', 0), i.get('status', 0), i.get('score', 0.0), i.get('targer_disp_count', 0), i.get('stat', 'none')
    sys.stdout.flush()

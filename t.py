# Note: do not name this file as time.py
# Otherwise the following import will import itself
import time
import datetime
# date to string
print(time.strftime("%Y-%m-%d",time.localtime(time.time()-24*60*60)))
print(time.strftime("%Y%m%d,%H:%M:%S",time.localtime(time.time())))

# date to timestamp
a = datetime.date(2018,1,1)
j = time.mktime(a.timetuple())
print int(j)

# timestamp to string
ts = 1172969203
c = time.ctime(ts)
print c

# timestamp to date obj
ts = 1172969203
d = datetime.datetime.fromtimestamp(ts)
print d.year, d.month, d.day

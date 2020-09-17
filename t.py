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

# weekday
print d.weekday()

# change between unixtimestamp & iso8601 format: 2006-01-02T15:04:05Z07:00
## To iso8601
import pytz
tz = pytz.timezone('Asia/Shanghai')
print datetime.datetime.fromtimestamp(1600334632, tz).isoformat()

## To Unix timestamp
import iso8601
ts = int(time.mktime(iso8601.parse_date('2020-09-17T17:23:52+08:00').timetuple()))
print ts

# Note: do not name this file as time.py
# Otherwise the following import will import itself
import time
print(time.strftime("%Y-%m-%d",time.localtime(time.time()-24*60*60)))
print(time.strftime("%Y%m%d,%H:%M:%S",time.localtime(time.time())))

# Note the python-crontab/crontab module manipulate system crontab file.
#+ To do python world's crontab, use sched.
import sched
import time
from datetime import datetime, timedelta

scheduler = sched.scheduler(timefunc=time.time)

def reschedule():
    new_target = datetime.now().replace(
            second=0, microsecond=0
            )
    # every whole minute
    new_target += timedelta(minutes=1)
    #print("next at: %s"%new_target)
    scheduler.enterabs(
            time=new_target.timestamp(), priority=0, action=saytime)

def saytime():
    # body
    print(time.ctime(),flush=True)
    # body end
    reschedule()

# write sched
reschedule()

try:
    # start sched
    scheduler.run(blocking=True)
except KeyboardInterrupt:
    print('stopped')

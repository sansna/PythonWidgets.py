from datetime import datetime
from chinese_calendar import is_workday, is_holiday
import chinese_calendar as cc

rest_hours=set()
weekend_hours=set()
holiday_hours=set()


# Retval: True/False
# Strict
def IsWorkHour(do):
  hour = do.hour
  if hour >= 10 and hour < 12:
        return True
  if hour >= 14 and hour < 18:
        return True
  if hour >= 19 and hour < 21:
        return True
  return False

# Less strict Version
def IsWorkHourV2(do):
  hour = do.hour
  minu = do.minute
  if hour < 10:
    return False
  if hour == 12 and minu >= 30:
    return False
  if hour == 13:
    return False
  if hour == 18 and minu >= 10:
    return False
  if hour == 21 and minu >= 30:
    return False
  if hour > 21:
    return False
  return True

with open("info", 'r') as f:
  lines = f.readlines()
  for l in lines:
    #l = l[:-1]
    do = datetime.strptime(' '.join(l[:-1].split(' ')), '%a %b %d %H:%M:%S %Y')
    #print do

    hour = do.hour
    day = do.day
    month = do.month
    year = do.year
    info = str(year)+"/"+str(month)+"/"+str(day)+" "+str(hour)
    
    # no tiaoxiu is included.
    if is_workday(do):
        #print ("work", do)
        if IsWorkHourV2(do):
            pass
            #print("work*0", do)
        else:
            #print("rest*1.5", do, info)
            rest_hours.add(info)
    elif cc.get_holiday_detail(do)[0] and cc.get_holiday_detail(do)[1] is not None:
        #print ("holiday*3", do, info)
        holiday_hours.add(info)
    else:
        #print ("weekend*2", do, info)
        weekend_hours.add(info)
print(len(weekend_hours))
print(len(rest_hours))
print(len(holiday_hours))
commit_hours = 2*float(len(weekend_hours))+3*float(len(holiday_hours))+1.5*float(len(rest_hours))
print(commit_hours*125)

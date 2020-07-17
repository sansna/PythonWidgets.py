import yagmail as yg
import time
import datetime

now = int(time.time()-86400)
d = datetime.datetime.fromtimestamp(now)
yesterday="%04d-%02d-%02d"%(d.year,d.month,d.day)
#yesterday=str(d.year)+'-'+str(d.month)+'-'+str(d.day)
f='./data/'+yesterday+'.csv'

yg=yg.SMTP(user='sender',password='pass',host='smtp.exmail.qq.com')
yg.send(['recver'],'subject',attachments=[f])

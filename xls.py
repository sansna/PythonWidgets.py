import xlrd
import time
strtime=time.strftime("%Y-%m-%d",time.localtime(time.time()-24*60*60))
book=xlrd.open_workbook("temp.xlsx")
sh = book.sheet_by_index(0)
sss="总："+strtime+'，公司总收件量：'
zl1=''
zh2=''
sd1=''
sd2=''
nx1=''
nx2=''
hj1=''
hj2=''
hj3=''
bd1=''
bd2=''
for rx in range(sh.nrows):
    if sh.cell_value(rx,0)=='浙江湖州织里公司':
        zl1=sh.cell_value(rx,1)
        zl1=str(zl1)
        zl2=sh.cell_value(rx,2)
        zl2=str(zl2)
    if sh.cell_value(rx,0)=='浙江湖州市东营业厅':
        sd1=sh.cell_value(rx,1)
        sd1=str(sd1)
        sd2=sh.cell_value(rx,2)
        sd2=str(sd2)
    if sh.cell_value(rx,0)=='浙江湖州八里店公司':
        bd1=sh.cell_value(rx,1)
        bd1=str(bd1)
        bd2=sh.cell_value(rx,2)
        bd2=str(bd2)
    if sh.cell_value(rx,0)=='浙江湖州南浔公司':
        nx1=sh.cell_value(rx,1)
        nx1=str(nx1)
        nx2=sh.cell_value(rx,2)
        nx2=str(nx2)
    if sh.cell_value(rx,0)=='合 计':
        hj1=sh.cell_value(rx,1)
        hj1=str(hj1)
        hj2=sh.cell_value(rx,2)
        hj2=str(hj2)
        hj3=sh.cell_value(rx,4)
        hj3=str(hj3)
sss = sss + hj1 + '票，总派件量：'+hj2+'票，直营片区：市东 收件量：'+sd1+'票，派件量：'+sd2+'票；'+'八里店 收件量:'+bd1+'票，派件量：'+bd2+'票；南浔 收件量：'+nx1+'票，派件量：'+nx2+'票；织里 收件量：'+zl1+'票，派件量：'+zl2+'票。公司整体签收率：'+hj3+'%'
ass = "安" +sss
wss = "汪" +sss
print(ass)
print()
print(wss)
print()
print(hj1)
print(hj2)
print('{:.4f}'.format(float(hj3)/100))
print()
print(zl1)
print(zl2)
print()
print(bd1)
print(bd2)
print()
print(nx1)
print(nx2)
print()
print(sd1)
print(sd2)

import os
os.system('pause')

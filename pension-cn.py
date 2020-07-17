# -*- coding:utf-8 -*-
# 可以通过北京市2019年职工养老保险社保基数范围确定北京市平均工资
# 因为基数范围是avg的0.6~3倍，反推2019年平均应为7K，湖州(浙江省通用)应为5.5K
# Analyzing pension factors.
years=int(input("How many years did you worked?\n"))
# income * 0.8 is paid, but cannot be larger than 1885, or less than 289 in Beijing.
income=float(input("How much income are you expected to have?\n"))
local_income=float(input("What is the avg income of your retired place?\n"))
# times >= 0.6 and times <= 3
times=float(input("How hard to you think you worked than others? (Base at 1.0)\n"))

paid = income*0.08
if paid > 1889:
    paid = 1889
elif paid < 289:
    paid = 289
p1=years*12*paid/139
p2=(local_income*times+local_income)/2*years*0.01
print p1,p2,(p1+p2)

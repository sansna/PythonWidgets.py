# !/usr/bin/python
# -*-coding: utf-8 -*-

import sys
import os
import subprocess
from datetime import *

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

import pymysql
from odps import ODPS

# reload(sys)
# sys.setdefaultencoding('utf8')

AccessKeyID = ''
AccessKeySecret = ''
odps_db = ODPS(AccessKeyID, AccessKeySecret, '')

host = ''
user = ''
password = ''
db = ''

# query_date = datetime.now().date() + timedelta(days=-1)
# ts_string = str(query_date ).replace('-', '')

table_name = ''

#def query_from_odps(query_sql):
#    print(query_sql)
#    with odps_db.execute_sql(query_sql).open_reader() as reader:
#        print(reader.count)
#        record_list = list()
#        for record in reader:
#            record_list.append(dict(record))
#    record_pd = pd.DataFrame(record_list)
#    return record_pd
def get_from_shell(quary_date):
    ret_tab = pd.DataFrame(np.array([ret_disturbed[0], ret_disturbed[1], ret_banned, ret_prevlock_info[0], ret_prevlock_info[1], 0, 0, 0]), columns=['chat_disturbed_cnt', 'chat_disturbed_avg', 'banned_cnt', 'prevlock_cnt', 'mis_prevlock_rate', 'report_delay', 'report_cnt', 'report_validate_rate'])
    return ret_tab

def insert_into_mysql(temp_pd, table_name):
    mysql_url = 'mysql+pymysql://' + user + ':' + password + '@' + host + '/' + db + '?charset=utf8'
    engine = create_engine(mysql_url, echo=True)
    temp_pd.to_sql(name=table_name,
                   con=engine,
                   index=False,
                   if_exists='append')
    print("insert %s data to table %s" %(temp_pd,table_name))

def tab(table_name,quary_date):
    tab_pd = get_from_shell(quary_date)
    print(tab_pd)
    insert_into_mysql(tab_pd,table_name)



if __name__ == '__main__':

    
    #start_date_string = '2019-01-31'
    #start_date = datetime.strptime(start_date_string, '%Y-%m-%d').date()
    #end_date = start_date + timedelta(days = 158)
    #while start_date <= end_date:
    #    #print(start_date)
    #    print("statring data of %s" %start_date)
        #print(str(start_date).replace("-",""))
    tab(table_name,0)
        #start_date = start_date + timedelta(days = 1)

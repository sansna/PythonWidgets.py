#encoding: utf-8
import pymongo
import time
import sys
from odps import ODPS
#import dateutil
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

conn = pymongo.MongoClient()

tSpark=conn['ascore']['spark_record']


def get_odps():
    return ODPS('',
                '',
                '',
                endpoint='http://odps-ext.aliyun-inc.com/api')


def odps_run_sql(odps_conn, sql, read_ret=True):
    #print('start run odps sql:' + sql)
    sys.stdout.flush()

    instance = odps_conn.execute_sql(sql, hints={"odps.sql.submit.mode" : "script"})
    records = []
    if not read_ret:
        return records
    with instance.open_reader() as reader:
        if reader is not None:
            for record in reader:
                records.append(record)
    return records

def odps_select_as_df(odps_conn, sql, tmp_table_pre='hanabi'):
    dt = datetime.now()
    table_name = '{tmp_table_pre}_tmp_{dt}'.format(tmp_table_pre=tmp_table_pre, dt=dt.strftime('%Y%m%d%H%M%S_')+str(dt.microsecond))
    sql_create = 'create table {table_name} LIFECYCLE 1  as {sql_select}'.format(
        table_name=table_name, sql_select=sql)
    odps_run_sql(odps_conn, sql_create, False)
    return odps_conn.get_table(table_name).to_df()







clk_exp=0
clk_tst=0
rec_exp=0
rec_tst=0

def try_insert(df, r, row, col, name):
    if row == 9:
        return
    if col in r:
        v = r.get_by_name(col)
        df[name][[row]] = v

def main():
    delta=0
    date_obj = datetime.fromtimestamp(int(time.time())-86400*(delta+1))
    year,mon,day,hour=date_obj.year,date_obj.month,date_obj.day,date_obj.hour
    ym=str(year).zfill(4)+str(mon).zfill(2)
    day=str(day).zfill(2)
    hour=str(hour).zfill(2)

    #print df

   #print "日期：", ym+day
    # effect_chat
   #print "####有效会话数据####"
    sql_clk = "\
            SELECT  ct\
                    ,GET_JSON_OBJECT(data, '$.session_info.BigMid') AS mid\
                    ,GET_JSON_OBJECT(data, '$.session_info.SmallMid') AS uid\
            FROM    hanabi_actionlog\
            WHERE   atype = 'other-other'\
            AND     type = 'chat'\
            AND     stype = 'bizspam'\
            AND     (\
                            GET_JSON_OBJECT(data, CONCAT( '$.session_info.UsersMsgCount.', GET_JSON_OBJECT(data, '$.session_info.BigMid'))) >= 15\
                        AND GET_JSON_OBJECT(data, CONCAT( '$.session_info.UsersMsgCount.', GET_JSON_OBJECT(data, '$.session_info.SmallMid'))) = 15\
                    )\
            OR      (\
                            GET_JSON_OBJECT(data, CONCAT( '$.session_info.UsersMsgCount.', GET_JSON_OBJECT(data, '$.session_info.BigMid'))) = 15\
                        AND GET_JSON_OBJECT(data, CONCAT( '$.session_info.UsersMsgCount.', GET_JSON_OBJECT(data, '$.session_info.SmallMid'))) >= 15\
                    )\
    ".format(ym=ym,day=day,ymd=ym+day)
    ret = odps_run_sql(get_odps(), sql_clk)
    for r in ret:
       #print "分类：",r.get_by_name('type'), "有效会话占比：",r.get_by_name('effective_percent'), "人均有效会话数：", r.get_by_name('avg_effect')
       mid = r.get_by_name('mid')
       uid = r.get_by_name('uid')
       ct = r.get_by_name('ct')
       tSpark.insert_one({"mid":mid,"uid":uid,"ct":ct,"ut":ut})

if __name__ == '__main__':
    main()

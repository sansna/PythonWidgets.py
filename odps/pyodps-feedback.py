#encoding: utf-8
import time
import sys
from odps import ODPS
#import dateutil
from datetime import datetime, timedelta


def get_odps():
    return ODPS('',
                '',
                '',
                endpoint='http://odps-ext.aliyun-inc.com/api')


def odps_run_sql(odps_conn, sql, read_ret=True):
    #print('start run odps sql:' + sql)
    sys.stdout.flush()

    instance = odps_conn.execute_sql(sql)
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







#class TblDateUtil(object):
#    def __init__(self, dt):
#        self.dt = dt
#
#    def ym(self):
#        return self.dt.strftime('%Y%m')
#
#    @property
#    def day(self):
#        return self.dt.day
#
#    def p_date(self):
#        return self.dt.strftime('%Y-%m-%d')

clk_exp=0
clk_tst=0
rec_exp=0
rec_tst=0

def run(delta=0):
    date_obj = datetime.fromtimestamp(int(time.time())-3600*(delta+1))
    year,mon,day,hour=date_obj.year,date_obj.month,date_obj.day,date_obj.hour
    ym=str(year).zfill(4)+str(mon).zfill(2)
    day=str(day).zfill(2)
    hour=str(hour).zfill(2)

    sql_clk = "\
    SELECT  c.mid as mid\
            ,b.ddd as ct\
            ,case when c.gender = 1 then '男'\
            WHEN c.gender = 2 then '女'\
            else '未知'\
            end as gender\
            ,b.content as cont_array\
            ,b.url as feedback_url\
    FROM    hanabi_usermetadata AS c INNER\
    JOIN    (\
                SELECT  a.mid AS mid\
                        ,TO_CHAR(FROM_UNIXTIME(a.cct*60),'yyyy-mm-dd hh:mi:ss') AS ddd\
                        ,COLLECT_LIST(CONCAT(GET_JSON_OBJECT(a.data,'$.content'),\"。\" )) AS content\
                        ,CONCAT(\
                            \"http://op.iupvideo.net/op/details/chatdetails/\"\
                            ,GET_JSON_OBJECT(a.data,'$.session_id') \
                        ) AS url\
                FROM    (\
                            SELECT  *\
                                    ,CAST(ct/60 AS INT ) AS cct\
                            FROM    im_chat\
                            WHERE   ymd >= '2019-11-09'\
                            AND     ymd <= '2019-11-15'\
                            AND     type = 'chat_create'\
                            AND     stype = 'chat'\
                            AND     GET_JSON_OBJECT(data, '$.app_name') = 'hanabi'\
                            AND     GET_JSON_OBJECT(data, '$.mtype') = 1\
                            AND     GET_JSON_OBJECT(data, '$.touser') = \"100006\"\
                        ) AS a\
                GROUP BY a.mid\
                         ,a.cct\
                         ,GET_JSON_OBJECT(data,'$.session_id')\
            ) AS b\
    ON      c.mid = b.mid\
    ".format(ym=ym,day=day,ymd=ym+day)
    ret = odps_run_sql(get_odps(), sql_clk)
    for r in ret:
        #if r.get_by_name('result'):
        #    clk_exp=r.get_by_name('pv')
        #else:
        #    clk_tst=r.get_by_name('pv')
        print(r.get_by_name('mid'),r.get_by_name('ct'),r.get_by_name('gender'),r.get_by_name('cont_array'),r.get_by_name('feedback_url'))

def main():
    #for i in range(50,-1,-1):
    #    run(i)
    run()

if __name__ == '__main__':
    main()

#encoding: utf-8
import sys
from odps import ODPS
#import dateutil
from datetime import datetime, timedelta


def get_odps():
    return ODPS('',
                '',
                'db',
                endpoint='')


def odps_run_sql(odps_conn, sql, read_ret=True):
    print('start run odps sql:' + sql)
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

def odps_select_as_df(odps_conn, sql, tmp_table_pre=''):
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

def main():
    sql = "\
    select concat(ym,day,lpad(cast(cast((cast(ct as int)/3600+8)%24 as int) as string), 2, '0')) as ymd, count(*) as pv, (cast(mid as int)%5)=3 as result from actionlog\
    where ym > '201908'\
    and type = ''\
    and stype = ''\
    and frominfo = ''\
    and concat(ym,day) > '20190823' \
    group by concat(ym,day,lpad(cast(cast((cast(ct as int)/3600+8)%24 as int) as string), 2, '0')), (cast(mid as int)%5)=3\
    "
    ret = odps_run_sql(get_odps(), sql)
    for r in ret:
        print(r.get_by_name('ymd'),r.get_by_name('pv'),r.get_by_name('result'))
    #print(ret)

if __name__ == '__main__':
    main()

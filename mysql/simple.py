import pymysql
from sqlalchemy import create_engine

def get_conn():
    # u:pw@ip/dbname?..
    engine=create_engine('mysql+pymysql://root:pw@127.0.0.1/mytest?host=localhost?port=3306',echo=True)
    return engine.connect()

# Do any sql sentences.
def sql_do():
    conn = get_conn()
    # table name
    result = conn.execute("select * from my_test;")
    # as a tuple eg. (1,2)
    #for r in result:
    #    print r
    for r in result:
        print getattr(r, 'col_name')

    # do update
    result = conn.execute("update my_test set col1=100 where id=1;")

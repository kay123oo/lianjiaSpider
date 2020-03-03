# coding:utf-8
import sys
from lianjiaSpider.ipprocy.config import DB_CONFIG
from lianjiaSpider.ipprocy.util.exception import Con_DB_Fail


try:
    if DB_CONFIG['DB_CONNECT_TYPE'] == 'pymongo':
        from lianjiaSpider.ipprocy.db.MongoHelper import MongoHelper as SqlHelper
    elif DB_CONFIG['DB_CONNECT_TYPE'] == 'redis':
        from lianjiaSpider.ipprocy.db.RedisHelper import RedisHelper as SqlHelper
    else:
        from lianjiaSpider.ipprocy.db.SqlHelper import SqlHelper as SqlHelper
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
except Exception as e:
    raise Con_DB_Fail


def store_data(queue2, db_proxy_num):
    '''
    读取队列中的数据，写入数据库中
    :param queue2:
    :return:
    '''
    successNum = 0
    failNum = 0
   # print('外面数据读入：')
    while True:
        try:
            proxy = queue2.get(timeout=300)
            #print("数据读入:")
            #print(proxy)
            if proxy:
                print(proxy)
                sqlhelper.insert(proxy)
                successNum += 1
                print('successNum++')
                print(successNum)
            else:
                failNum += 1
                #print('failNum++')
                #print(failNum)
            #str = 'IPProxyPool----->>>>>>>>Success ip num :%d,Fail ip num:%d' % (successNum, failNum)
            #sys.stdout.write(str + "\r")
            #sys.stdout.flush()
        except BaseException as e:
            print(e)
            if db_proxy_num.value != 0:
                successNum += db_proxy_num.value
                db_proxy_num.value = 0
                str = 'IPProxyPool----->>>>>>>>Success ip num :%d,Fail ip num:%d' % (successNum, failNum)
                sys.stdout.write(str + "\r")
                sys.stdout.flush()
                successNum = 0
                failNum = 0



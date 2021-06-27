# -*- coding:utf8 -*-


import pymysql
from dbutils.PooledDB import PooledDB


class MysqlTools(object):
    __instance = None
    __db_list = []
    __pool = None

    def __init__(self, host, user, password, db, charset, port):
        try:
            self.host = host
            self.user = user
            self.password = password
            self.db = db
            self.charset = charset
            self.port = port
            self.conn = MysqlTools.__get_conn(host=self.host, user=self.user, password=self.password, db=self.db,
                                              charset=self.charset, port=self.port)
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            print(e.args)

    @staticmethod
    def __get_conn(host, user, password, db, charset, port):
        if MysqlTools.__pool is None:
            __pool = PooledDB(creator=pymysql,
                              mincached=1, maxcached=5, maxconnections=20, blocking=True, host=host, port=port,
                              user=user,
                              passwd=password,
                              db=db, charset=charset)
        return __pool.connection()

    def query_sql(self, sql, param_data=None):
        try:
            if param_data is not None:
                self.cursor.execute(sql, param_data)
            else:
                self.cursor.execute(sql)
            resource = self.cursor.fetchall()
            counts = self.cursor.rowcount
            sql = sql.split(" ")
            if sql[0].lower() == "select":
                return resource
            else:
                return_result = counts
                return return_result
        except Exception as e:
            return e.args

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self.conn.commit()
        else:
            self.conn.rollback()

    def close_connect(self):
        if self.cursor:
            self.cursor.close()
        self.conn.close()

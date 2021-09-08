import pymysql
import traceback


class db():
    # host = "13bfc66f81062088.natapp.cc"  # 小邵笔记本
    # host = "127.0.0.1"
    host = "127.0.0.1"
    user = "root"
    password = "123456"

    port = 3306

    # port = 8888

    def __init__(self, db='weibo'):
        self.db = db

    def get_conn(self):
        """
        :return: 连接，游标
        """
        # 创建连接
        conn = pymysql.connect(host=self.host,
                               user=self.user,
                               password=self.password,
                               db=self.db,
                               port=self.port,
                               charset="utf8mb4")
        # 创建游标
        cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        return conn, cursor

    def close_conn(self, conn, cursor):
        """
        关闭链接
        :param conn:
        :param cursor:
        :return:
        """
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    def query(self, sql, *args):
        """
        封装通用查询
        :param sql:
        :param args:
        :return: 返回查询到的结果，((),(),)的形式
        """

        conn, cursor = self.get_conn()
        cursor.execute(sql, args)
        res = cursor.fetchall()
        self.close_conn(conn, cursor)
        return res

    def exec_(self, sql):
        cursor = None
        conn = None
        try:
            conn, cursor = self.get_conn()
            cursor.execute(sql)
            conn.commit()  # 提交事务 update delete insert操作
        except:
            traceback.print_exc()
        finally:
            self.close_conn(conn, cursor)

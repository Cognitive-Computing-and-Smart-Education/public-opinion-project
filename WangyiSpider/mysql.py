# encoding: utf-8
# Author    : 1476776320@qq.com
# Datetime  : 2021/07/27 9:24
# User      : TianXin
# Product   : PyCharm
# Project   : WangyiSpider
# File      : mysql.py
# Explain   : 备注

import pymysql

import traceback


def get_conn():
    """
    链接数据库
    :return: 连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="localhost",
                           port=3306,
                           user="root",
                           password="0125",
                           db="spider",  # 数据库名字
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


def close_conn(conn, cursor):
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


def query(sql, *args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，((),(),)的形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


def exec_(sql):
    cursor = None
    conn = None
    try:
        conn, cursor = get_conn()
        cursor.execute(sql)
        conn.commit()  # 提交事务 update delete insert操作
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

# if __name__ == '__main__':
#     sql = "select * from student" #mysql查询语句
#     res = query(sql)
#     print(res)

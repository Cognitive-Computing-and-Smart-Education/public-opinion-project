# coding:utf-8
import json
import requests
import re
from weibo import db
import time

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Host': 'm.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.75 Safari/537.36',
    'Cookie': 'SCF=AqXAEhlSMyrGIXnlBHjJmmK7cp32TYkKKmD1f_mp18VDOpCcBNiV_3sveSOdJJYTTdSljIPqywWqHLs-__Grhxo.; '
              'SUB=_2A25N87gYDeRhGeBP61QQ8CrOyj-IHXVvH9hQrDV6PUJbktCOLUOtkW1NRZQcmVLb-PHpYcX2QauHgVNOjf2lT6Kk; '
              'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhsUrMIY8fkXPb9CT.pEwbZ5NHD95QceK5ceK5Xeo20Ws4DqcjQ-8HFxEH8SC'
              '-4eF-ReEH81CHF1FHWeCH8SCHFeF-RxbH8SE-41CHFx5tt; _T_WM=88789922234; WEIBOCN_FROM=1110006030; MLOGIN=1; '
              'XSRF-TOKEN=fc100c; M_WEIBOCN_PARAMS=lfid%3D1076031283148795%26luicode%3D20000174%26uicode%3D20000174 '
}


def get_user(uid):
    # 用户基本信息
    user_url = 'https://m.weibo.cn/profile/info?uid=%s' % uid
    print(user_url)
    # uid = 5044281310

    params = {"uid": uid}

    get_text = requests.get(user_url, headers=headers, params=params, allow_redirects=False).text

    # print(get_text)
    get_text = json.loads(get_text)
    ok = get_text.get('ok')
    UserItem = {}

    # print(get_text)
    if ok:
        data = get_text.get('data')
        # 用户信息
        user = data.get('user')

        # 用户id
        UserItem['uid'] = uid

        # 用户名
        UserItem['uname'] = user.get("screen_name")

        # 关注数
        UserItem['follow_count'] = user.get('follow_count')

        # 粉丝数
        UserItem['followers_count'] = user.get("followers_count")

        # 微博总数
        UserItem['statuses_count'] = user.get("statuses_count")

        if user.get("verified"):
            # 是否为微博认证
            UserItem['verified'] = 1
        else:
            UserItem['verified'] = 0

        # 粉丝列表id
        UserItem['fans_list_id'] = re.findall(r'id=(\d+)', data.get('fans'))[0]

        # 微博列表id
        UserItem['more_list_id'] = re.findall(r'^/p/(\d+)', data.get('more'))[0]

    return UserItem


def insert_user(UserItem):
    update_sql = "update user set `uname`='%s',`follow_count`='%s',`followers_count`='%s',`statuses_count`='%s',`verified`='%s',`fans_list_id`='%s',`more_list_id`='%s' where `uid`='%s'" % (
        UserItem['uname'], UserItem['follow_count'], UserItem['followers_count'], UserItem['statuses_count'],
        UserItem['verified'], UserItem['fans_list_id'], UserItem['more_list_id'], UserItem['uid'])
    print(update_sql)
    db.exec_(update_sql)


def create_uid():
    sql = "select auth_id from title where isCrawled=1 group by auth_id;"
    query = db.query(sql)

    for i in query:
        uid = i[0]
        into_sql = "insert into user(`uid`) value('%s')" % uid
        db.exec_(into_sql)


def main():
    sql = "select `uid` from user where `uname` is null "
    sql = "select `uid` from user "
    query = db.query(sql)
    for i in query:
        uid = i[0]

        UserItem = get_user(uid)
        if UserItem:
            insert_user(UserItem)
        time.sleep(1)


if __name__ == '__main__':
    # 文章爬取后才开放
    # create_uid()

    main()

    # 测试内容
    # useritem = get_user(1283148795)
    # print(useritem)

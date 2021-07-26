# coding:utf-8
import json
import requests
import re
# from weibo import db
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


def userTitle(more_list_id):
    # 用户基本信息
    # user_url = 'https://m.weibo.cn/profile/info?uid=%s' % uid
    # print(user_url)
    # uid = 5044281310

    userTitle_url = f"https://m.weibo.cn/api/container/getIndex?containerid={more_list_id}_-_WEIBO_SECOND_PROFILE_WEIBO_ORI&page_type=03"

    params = {'containerid': f'{more_list_id}_-_WEIBO_SECOND_PROFILE_WEIBO_ORI',
              'page_type': '03',
              }
    get_text = requests.get(userTitle_url, headers=headers, params=params, allow_redirects=False).text
    # print(get_text)
    get_text = json.loads(get_text)
    original_count = get_text.get("data").get('cardlistInfo').get("total")

    return original_count


def update_userTittle(uid, original_count):
    sql = f"update user set `original_count`={original_count} where `uid` ={uid}"
    db.exec_(sql)


def main():
    sql = "select `uid`,`more_list_id` from user"
    more_list = db.query(sql)
    for i in more_list:
        uid = i[0]
        more_list_id = i[1]
        original_count = userTitle(more_list_id)
        print(uid, original_count)
        update_userTittle(uid, original_count)
        time.sleep(1)


if __name__ == '__main__':
    main()

# uid = 1828509247
# more_list_id = 2304131828509247
#
# count = userTitle(more_list_id)

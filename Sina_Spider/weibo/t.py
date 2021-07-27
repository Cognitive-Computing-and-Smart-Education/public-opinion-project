# coding:utf-8
import random
import json
import requests
import re
# from weibo import db
import db
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


def get_fans(uid, fans_list_id):
    # 用户基本信息
    # user_url = 'https://m.weibo.cn/profile/info?uid=%s' % uid
    # print(user_url)
    # uid = 5044281310
    page = 1

    # 粉丝数
    followers_count = 0

    # 活跃粉丝用户
    activeFans_count = 0

    # 男性粉丝
    mFans_count = 0

    # 女性粉丝
    fFans_count = 0

    # 粉丝中大V数量（认证粉丝数量）
    verifiedFans_count = 0
    item = {}

    while True:
        "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_5873877634&since_id=0"
        fans_url = f"https://m.weibo.cn/api/container/getSecond?containerid={fans_list_id}_-_FANS&page={page}"
        params = {'containerid': fans_list_id + '_-_FANS', 'page': page}
        get_text = requests.get(fans_url, headers=headers, params=params, allow_redirects=False).text
        get_text = json.loads(get_text)
        ok = get_text.get("ok")
        if ok:
            fans_list = get_text.get('data').get("cards")
            followers_count = get_text.get('data').get('count')
            for fans in fans_list:
                user = fans.get('user')
                fans_id = user.get('id')
                ifans_name = user.get("screen_name")
                # 是否为认证用户
                verified = user.get("verified")
                sex = user.get('gender')
                # print(sex)
                # if re.findall(r'^用户\d+$', ifans_name):
                #     actived = 0
                # else:
                #     actived = 1

                if sex == 'm':
                    mFans_count += 1
                else:
                    fFans_count += 1
                if verified:
                    verifiedFans_count += 1
                activeFans_count += 1
                # print(fFans_count, mFans_count)

            page += 1
            # sleepTime = random.randint(1, 5)
            # time.sleep(1)
        else:
            break
    # 粉丝数
    item['uid'] = uid
    # item['followers_count'] = followers_count

    # 活跃粉丝用户
    item['activeFans_count'] = activeFans_count

    # 男性粉丝
    # item['mFans_count'] = mFans_count

    # 女性粉丝
    # item['fFans_count'] = fFans_count

    # 粉丝中大V数量（认证粉丝数量）
    item['verifiedFans_count'] = verifiedFans_count
    print(item, page)
    return item


def inset_fans_info(item):
    sql = f"update user set activeFans_count={item['activeFans_count']},verifiedFans_count={item['verifiedFans_count']} where uid ={item['uid']}"
    db.exec_(sql)


def main():
    sql = "select uid,fans_list_id from user where `activeFans_count` is NULL "
    uid_list = db.query(sql)
    for i in uid_list:
        uid = i[0]
        fans_list_id = i[1]
        print(uid)
        item = get_fans(uid, fans_list_id)
        inset_fans_info(item)
        time.sleep(1)
    # uid = '1312806234'
    # item = get_fans(uid)

    # uid = '1071006415'
    # fans_list_id = '1005051071006415'
    #
    # get_fans(uid, fans_list_id)


if __name__ == '__main__':
    main()

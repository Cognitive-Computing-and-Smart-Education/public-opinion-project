from weibo import db
import re
from pymysql.converters import escape_string
from sqlalchemy import create_engine, text

keys = ['教育', '教学', '体育教育', '智慧教育', '科技', '体育', '国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', "婴儿教育", "幼儿教育", '艺术培训', '远程教育',
        '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]

# sql = "select `title_id`,`key` from title where instr(`title`,'高考' ) ;"
# query = db.query(sql)

id_sql = "select `title_id`,`title`,`key` from title"
id_query = db.query(id_sql)
item = {}
data = []
for i in id_query:
    id = i[0]
    title = escape_string(i[1])
    title = re.sub(r'%', '', title)
    keyWords = []
    for key in keys:
        sql = f"select `title_id` from title where `title_id`='{id}' and '%%{title}%%' like '%%{key}%%';"
        # print(sql)
        if db.query(sql):
            keyWords.append(key)

    if i[2] not in keyWords:
        keyWords.append(i[2])

    item['id'] = id

    keyWords = ",".join(keyWords)
    item['key'] = keyWords
    print(item)
    sql = f"update title set `key`='{item['key']}' where `title_id` ='{item['id']}'"
    print(sql)
    db.exec_(sql)

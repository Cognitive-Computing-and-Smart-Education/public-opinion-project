from weibo import db
from pymysql.converters import escape_string
from sqlalchemy import create_engine, text

keys = ['教育', '教学', '体育教育', '智慧教育', '科技', '体育', '国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', "婴儿教育", "幼儿教育", '艺术培训', '远程教育',
        '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]

# sql = "select `title_id`,`key` from title where instr(`title`,'高考' ) ;"
# query = db.query(sql)

id_sql = "select title_id,title from title"
id_query = db.query(id_sql)
item = {}
data = []
for i in id_query:
    id = i[0]
    title = escape_string(i[1])
    keyWords = []
    for key in keys:

        if key in title:
            keyWords.append(key)
    keyWords = ",".join(keyWords)
    item['id'] = id
    item['key'] = keyWords
    print(item)
    # data

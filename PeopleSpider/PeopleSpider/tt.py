from PeopleSpider.db import db

a = db(db='people')

redis_sql = "select * from people"
a.db = 'redis'
query = a.query(redis_sql)
print(query)

# keys = ['教育', '教学', '体育教育', '智慧教育', '科技', '体育', '国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', "婴儿教育", "幼儿教育", '艺术培训', '远程教育',
#         '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]
# # print(",".join(keys))
import re

name = '千空2002'
res = re.findall(r'(用户\d+)', name)
print(res)

"""
{'followers_count': 129, 'fans_id': 6455574545, 'fans_name': 'JVE千慕雾化中心', 'verified': False, 'sex': 'm', 'actived': 1}
{'followers_count': 129, 'fans_id': 7572255870, 'fans_name': '用户7572255870', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 7519538178, 'fans_name': '千空2002', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 7520133818, 'fans_name': '用户7520133818', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 7293236458, 'fans_name': '轻度网瘾患者', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 6476357348, 'fans_name': '用户6476357348', 'verified': False, 'sex': 'f', 'actived': 0}
{'followers_count': 129, 'fans_id': 7519409413, 'fans_name': 'Uuu077', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 7519921959, 'fans_name': '用户7519921959', 'verified': False, 'sex': 'f', 'actived': 0}
{'followers_count': 129, 'fans_id': 7519405534, 'fans_name': '用户7519405534', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 6970026006, 'fans_name': '孤城03081', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 6455574545, 'fans_name': 'JVE千慕雾化中心', 'verified': False, 'sex': 'm', 'actived': 1}
{'followers_count': 129, 'fans_id': 7572255870, 'fans_name': '用户7572255870', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 7519538178, 'fans_name': '千空2002', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 7520133818, 'fans_name': '用户7520133818', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 7293236458, 'fans_name': '轻度网瘾患者', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 6476357348, 'fans_name': '用户6476357348', 'verified': False, 'sex': 'f', 'actived': 0}
{'followers_count': 129, 'fans_id': 7519409413, 'fans_name': 'Uuu077', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 7519921959, 'fans_name': '用户7519921959', 'verified': False, 'sex': 'f', 'actived': 0}
{'followers_count': 129, 'fans_id': 7519405534, 'fans_name': '用户7519405534', 'verified': False, 'sex': 'm', 'actived': 0}
{'followers_count': 129, 'fans_id': 6970026006, 'fans_name': '孤城03081', 'verified': False, 'sex': 'm', 'actived': 0}
"""

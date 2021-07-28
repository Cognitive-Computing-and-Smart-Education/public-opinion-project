import {success,pageSuccess} from '@/mock/bean'

export default pageSuccess(
        [
            {
                id:'@guid',
                "userId": /[A-Z]\d{6}/,
                "userName": '@cname',
                "jurisdiction|1":  [
                    "超级管理员",
                    "一般管理员",
                    "低级管理员"
                ],
                "contacts":  '@cname',
                "contactsPhone|+1": 18315673430,
                "officePhone|+1": 6543211,
                "usageState|+1": [
                    "启用",
                    "禁用"
                ]
            }
        ]
    )

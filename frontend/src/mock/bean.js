import Constant from '@/lib/constant'
import {Random} from 'mockjs'
export function success(data,message) {
    return {
        code: Constant.SUCCESS,
        message: message || '操作成功',
        data:data
    }
}

export function pageSuccess(data,message,limit = 10) {
    let result = {
        code: Constant.SUCCESS,
        message: message || '查询成功',
        total: function () {
            let total = this.data.length
            if(total === limit){
                return Random.integer(this.data.length,500)
            }else{
                return total
            }
        }
    }

    result['data|'+limit] = data

    return result
}

import axios from 'axios'
import {Loading, Message, MessageBox} from 'element-ui'
import {stripObject} from './utils'

class HttpRequest {
    constructor(options) {
        this.baseUrl = '/api'
        this.queue = {}
    }
    getInsideConfig() {
        const config = {
            baseURL: this.baseUrl,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            timeout: 3000
        }
        return config
    }
    interceptors(instance) {
        instance.interceptors.request.use(config => {
            // console.log(config)
            // 添加全局去除空格
            // if(!config.noTrim){
            //     //全局去除空格 可以用noTrim 来控制不进行全局去除空格
            //     stripObject(config.params || config.data)
            // }

            // 添加全局loading...
            if(config.loading === undefined || config.loading){//全局遮罩层处理
                if(!instance.loading){
                    instance.loading = {total:1,obj:
                            Loading.service({
                                fullscreen: true,lock: true,
                                background: 'rgba(0, 0, 0, 0.05)'
                            })}
                }else{
                    instance.loading.total++
                }
                config.loading = true
            }

            return config

        },error => {
            Message({
                message: error.message,
                type: 'error',
                duration: 5 * 1000
            })
            return Promise.reject(error)
        })
        instance.interceptors.response.use(res => {

            if(res.config.loading){
                if(instance.loading.total>1){//遮罩层处理
                    instance.loading.total--
                }else{
                    instance.loading.obj.close()
                    instance.loading = undefined
                }
            }
            // console.log(res)
            return res
        },error => {
            if(!error.config || error.config.loading){
                if(instance.loading){
                    if(instance.loading.total>1){//遮罩层处理
                        instance.loading.total--
                    }else{
                        instance.loading.obj.close()
                        instance.loading = undefined
                    }
                }

            }
            // console.log('error',error)
            Message({
                message: error.message,
                type: 'error',
                duration: 5 * 1000
            })
            return Promise.reject(error)
        })
    }
    request(options) {
        const instance = axios.create()
        options = Object.assign(this.getInsideConfig(),options)
        this.interceptors(instance)
        return instance(options)
    }
}

export default HttpRequest

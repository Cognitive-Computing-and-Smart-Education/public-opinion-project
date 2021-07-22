const webpack = require('webpack')

const path = require('path')

const resolve = dir => {
    return path.join(__dirname, dir)
}

const BASE_URL = process.env.NODE_ENV === 'production' ? '/iview-admin/' : '/'

module.exports = {
    devServer: {
        open: false, //是否自动打开。
        port: 8091, //打开系统的端口号。
        https: false,
        disableHostCheck: true
    },
    lintOnSave: false,
    baseUrl: BASE_URL,
    chainWebpack: config => {
        config.resolve.alias
            .set('@', resolve('src'))
    },
    configureWebpack: {
        externals: {
            'AMap': 'AMap' // 高德地图配置
        }
    }
}

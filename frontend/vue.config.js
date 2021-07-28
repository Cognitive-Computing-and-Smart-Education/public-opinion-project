const webpack = require('webpack')

const path = require('path')

const resolve = dir => {
    return path.join(__dirname, dir)
}

const BASE_URL = process.env.NODE_ENV === 'production' ? '/iview-admin/' : '/'

module.exports = {
    outputDir: process.env.outputDir,
    devServer: {
        open: false, //是否自动打开。
        port: 8091, //打开系统的端口号。
        https: false,
        disableHostCheck: true,
        // proxy: 'http://localhost:8091'
        proxy: {
            '/api': {
                target: 'http://localhost:8091',
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    },
    lintOnSave: false,
    baseUrl: '/',
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

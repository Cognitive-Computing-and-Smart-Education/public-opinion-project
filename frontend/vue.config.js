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
                // target: 'http://172.18.40.39:800',
                // target: 'http://172.18.40.20:800',
                // target: 'http://172.18.40.52:8000',
                target: 'http://172.18.40.131:8000',
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    },
    lintOnSave: false,
    publicPath: './',
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

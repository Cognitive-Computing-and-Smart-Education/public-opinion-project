import Vue from 'vue'
import App from './App.vue'
import router from './router';
import store from './store';
import AMap from 'AMap' // 引入高德地图
Vue.use(AMap); //设置elementUI。
require('./mock/index')

Vue.config.productionTip = false

//添加element ui组件
import elementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(elementUI); //设置elementUI。

// element loading组件
import { Loading } from 'element-ui';
Vue.prototype.openLoading = function() {
  const loading = this.$loading({           // 声明一个loading对象
    lock: true,                             // 是否锁屏
    text: '正在加载...',                     // 加载动画的文字
    spinner: 'el-icon-loading',             // 引入的loading图标
    background: 'rgba(0, 0, 0, 0.3)',       // 背景颜色
    target: '.sub-main',                    // 需要遮罩的区域
    body: true,
    customClass: 'mask'                     // 遮罩层新增类名
  })
  setTimeout(function () {                  // 设定定时器，超时5S后自动关闭遮罩层，避免请求失败时，遮罩层一直存在的问题
    loading.close();                        // 关闭遮罩层
  },5000)
  return loading;
}

import axios from 'axios';
Vue.prototype.axios = axios;

import * as echarts from 'echarts'

Vue.prototype.$echarts = echarts

import * as math from 'mathjs'
Vue.prototype.$math = math;

/*import VueAMap from 'vue-amap';
Vue.use(VueAMap);
VueAMap.initAMapApiLoader({
  key: 'df83e5e653753bb0ce4e9a5e673fdfca',
  plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor'],
  // 默认高德 sdk 版本为 1.4.4
  v: '1.4.4'
});*/




new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')

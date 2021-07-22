import Vue from 'vue'
import App from './App.vue'
import router from './router';
import store from './store';
import AMap from 'AMap' // 引入高德地图
Vue.use(AMap); //设置elementUI。

Vue.config.productionTip = false

//添加element ui组件
import elementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(elementUI); //设置elementUI。

import axios from 'axios';
Vue.prototype.axios = axios;

import * as echarts from 'echarts'

Vue.prototype.$echarts = echarts

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

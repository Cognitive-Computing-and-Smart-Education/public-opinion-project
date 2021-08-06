import Vue from 'vue'
import Vuex from 'vuex'
import home from './modules/home'



Vue.use(Vuex)

export default new Vuex.Store({
    // strict: true,
    state: {
        styleName: '' //风格名称。
    },
    getters: {

    },
    mutations: {

    },
    modules: {
        home
    },
    actions: {

    }
})

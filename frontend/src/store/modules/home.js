// import common from "../common"


export default {
    state: {
        Area_name: '全国'
    },
    getters: {
        homeAreaName(state) {
            return state.Area_name;
        }
    },
    mutations: {
        changeHomeAreaName(state, payload) {
            state.Area_name = payload;
        }
    },
    actions: {

    }
}

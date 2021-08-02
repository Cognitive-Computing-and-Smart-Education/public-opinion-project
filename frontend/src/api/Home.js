import axios from './index'
import el from "element-ui/src/locale/lang/el";

export const getCeShi = ({userId}) => {
    return axios.request({
        url: '/member-manage/businessMember/get',
        method: "get",
        data: {
            userId: userId
        }
    })
}

// 事件检索api
export const getNews = ({keyword}) => {
    return axios.request({
        url: '/get_news/',
        method: "post",
        data: {
            Keyword: keyword || ''
        }
    })
}


// 文章影响力api
export const getNewsInfluence = ({Area_name}) => {
    return axios.request({
        url: '/get_news_influence/',
        method: "post",
        data: {
            Area_name: Area_name || '全国'
        }
    })
}


// 顶部监控数据量
export const getNewsNum = ({Area_name}) => {
    if(!Area_name) {
        return axios.request({
            url: "/get_news_num/?type=num&province=全国",
            method: "get",
            data: {
                Area_name: '全国'
            }
        })
    }else {
        return axios.request({
            url: "/get_news_num/?type=num&province=" + Area_name,
            method: "get",
            data: {
                Area_name: Area_name
            }
        })
    }
}


// 地图文章地理分布
export const getNewsMap = () => {
    return axios.request({
        url: '/get_news_map/',
        method: "get",
        data: {
            // Area_name: Area_name || ''
        }
    })
}


// 细分行业声量
export const getAreaNewsIndustry = ({Area_name}) => {
    return axios.request({
        url: '/get_area_news_industry/',
        method: "post",
        data: {
            Area_name: Area_name || '全国'
        }
    })
}


// 地区的舆情趋势
export const getAreaNewsTre = ({Area_name}) => {
    return axios.request({
        url: '/get_area_news_tre/',
        method: "post",
        data: {
            Area: Area_name || '全国'
        }
    })
}


// 地区的信息来源
export const getAreaNewsSource = ({Area_name}) => {
    return axios.request({
        url: '/get_area_news_source/',
        method: "post",
        data: {
            Area_name: Area_name || '全国'
        }
    })
}


// 地区的媒体影响力
export const getAreaSourceInfluence = ({Area_name}) => {
    return axios.request({
        url: '/get_area_source_influence/',
        method: "post",
        data: {
            Area_name: Area_name || '全国'
        }
    })
}


// 热门词云
export const getAreaHotWord = ({Area_name}) => {
    return axios.request({
        url: '/get_area_hot_word/',
        method: "post",
        data: {
            Area_name: Area_name || '全国'
        }
    })
}

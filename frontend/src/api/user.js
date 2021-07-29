import axios from './index'

export const getUserInfo = ({userId}) => {
    return axios.request({
        url: '/member-manage/businessMember/get',
        method: "get",
        data: {
            userId: userId
        }
    })
}

export const getCeshi = ({keyword}) => {
    return axios.request({
        url: '/get_news/',
        method: "post",
        data: {
            Keyword: keyword
        }
    })
}

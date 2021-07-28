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

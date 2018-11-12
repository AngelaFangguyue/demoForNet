import * as types from '../mutation-types'
import axios from "axios/index";

const state = {
    name: "",
    email: "",
    nickname: "",
}

const actions = {
    getUserBaseInfo({commit}){      // 获得当前用户基础信息
        axios.post("/api/user/base")
            .then(function(response){
                commit(types.SET_USER_BASE_INFO, response.data)
            })
            .catch(function (error) {
                console.log(error)
            })
    },
}


const mutations = {
    [types.SET_USER_BASE_INFO] (state, data){
        state.name = data.name
        state.email = data.email
        state.nickname = data.nickname
    },
}

export default {
    state,
    actions,
    mutations
}
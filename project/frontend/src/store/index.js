import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './action'
import mutations from "./mutations"
import user from "./modules/user"

Vue.use(Vuex)

const state = {
}

export default new Vuex.Store({
    actions,
    state,
    mutations,
    modules: {
        user,
    }
})


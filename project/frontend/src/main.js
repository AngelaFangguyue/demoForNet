// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import 'element-ui/lib/theme-chalk/base.css';
import axios from 'axios'
import store from "./store"
import "url-search-params-polyfill"

Vue.config.productionTip = false
Vue.use(ElementUI)

Vue.prototype.$http = axios

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
    store,
  template: '<App/>',
  components: { App }
})

// axios的拦截器
axios.interceptors.response.use(function(response){
    return response
}, function(error){
    if(error.response && error.response.data && error.response.data === 'LOGIN REQUIRED'){
        window.location.href = "/login"
    }
    return Promise.reject(error)
})


import Vue from 'vue'
import Router from 'vue-router'

import HelloWorld from "../components/HelloWorld"


Vue.use(Router)

const routes = [
    {path: "/", component: HelloWorld},
    {path: "*", redirect: "/"}

]

export default new Router({
    mode: "history",
    routes: routes,
})

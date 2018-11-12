import Vue from 'vue'
import Router from 'vue-router'

import HelloWorld from "../components/HelloWorld"
import Setting from "../components/Setting"

Vue.use(Router)

const routes = [
    {path: "/", redirect: "/index"},
    {path: "/index", component: HelloWorld},
    {path: "/setting", component: Setting},
    {path: "*", redirect: "/index"}
]

export default new Router({
    mode: "history",
    routes: routes,
})

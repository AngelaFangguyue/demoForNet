<template>
    <el-menu
            :default-active="activeIndex"
            mode="horizontal"
            @select="handleSelect"
            ref="topMenu"
            :router="true"
            id="topMenu"
            class="top-menu-bar"
    >
            <el-menu-item index="0" style="margin-right: 50px;">
                <a href="http://qa.pangu.netease.com/homePage/">
                    <img src="../../assets/img/homeLogoBlack.png" style="width: 130px" ondragstart="return false">
                </a>
            </el-menu-item>
            <el-menu-item index="/index">分页一</el-menu-item>
            <el-menu-item index="/setting">设置</el-menu-item>


        <el-submenu index="uxv1" class="right-sub-menu">
            <template slot="title">
                {{ username }}
            </template>
            <a href="/logout">
                <el-menu-item index="uxv1-0"><span class="my-span glyphicon glyphicon-off" aria-hidden="true"></span>退出登录</el-menu-item>
            </a>
        </el-submenu>

    </el-menu>
</template>

<script>
    export default {
        name: "top-bar",
        data(){
            return {
                activeIndex: this.$route.path.split("/")[1],
            }
        },
        computed: {
            username(){
                return this.$store.state.user.name
            },
            currentPath: function(){
                return this.$route.path
            },
        },
        watch: {
            currentPath(){
                let curPath = "/" + this.$route.path.split("/")[1]
                if(curPath !== this.$refs.topMenu.activeIndex){
                    this.$refs.topMenu.activeIndex = curPath
                }
            },

        },
        methods: {
            handleSelect(key, path){
                if(key.indexOf('uxv') >= 0){
                    this.$refs.topMenu.activeIndex = this.activeIndex
                } else {
                    this.activeIndex = this.$refs.topMenu.activeIndex
                }
            },

        },
        mounted: function(){
            let curPath = "/" + this.$route.path.split("/")[1]
            if(curPath !== this.$refs.topMenu.activeIndex){
                this.$refs.topMenu.activeIndex = curPath
            }
        }
    }
</script>

<style lang="less">

    .right-sub-menu{
        float: right !important;
        width: 160px;
        margin-right: 10px !important;
        .el-menu-item{
            min-width: 0;
            text-align: center;
        }
    }

    .my-span{
        padding-right: 20px;
        padding-bottom: 2px;
    }

    .el-menu--horizontal{
        ul{
            min-width: 0 !important;
            width: 160px;
        }
        li{
            text-align: center;
            user-select: none;
        }

    }

    .el-menu-horizontal{
        z-index: 10;
        position: fixed !important;
        width: 100%;
        top: 0;
        left: 0;
        right: 0;
    }

    .top-menu-bar{
        box-shadow: 0 1px 6px rgba(0,0,0,.117647), 0 1px 4px rgba(0,0,0,.117647);
        z-index: 10;
    }

</style>

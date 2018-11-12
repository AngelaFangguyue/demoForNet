<template>
  <div id="app">
      <TopBar></TopBar>
      <el-row id="body-outer-wrapper">
          <router-view></router-view>
      </el-row>

  </div>
</template>

<script>
    import TopBar from "./components/common/TopBar"
    export default {
        components: {TopBar},
        name: 'app',
        data(){
            return {
            }
        },
        computed: {
        },
        methods:{
            checkBrowserType(){
                // 检查浏览器类型
                let browser = this.getBrowserType()
                if(browser !== "Chrome"){
                    this.$notify.warning({
                        title: "浏览器检测",
                        message: "检测到您当前未使用Chrome浏览器，本站建议使用Chrome浏览器。其他浏览器不保证兼容性"
                    })
                }
            },

            getBrowserType(){
                let userAgent = navigator.userAgent
                let isOpera = userAgent.indexOf("Opera") > -1
                if(isOpera){
                    return "Opera"
                }
                if(userAgent.indexOf("Firefox") > -1) {
                    return "Firefox"
                }
                if(userAgent.indexOf("Edge") > -1){
                    return "Edge"
                }
                if(userAgent.indexOf("Chrome") > -1){
                    return "Chrome"
                }
                return "Others"
            },

        },
        created(){
            this.checkBrowserType()
        },
        beforeMount(){
            this.$store.dispatch("getUserBaseInfo")
        }
    }
</script>

<style lang="less">
    #app {
          font-family: "Hiragino Sans GB", "MicroSoft YaHei",'Avenir', Helvetica, Arial, sans-serif;
          -webkit-font-smoothing: antialiased;
          -moz-osx-font-smoothing: grayscale;
    }

    #body-outer-wrapper{
        position: absolute;
        top: 60px;
        bottom: 0;
        left: 0;
        right: 0;
        overflow-y: auto;
        background-color: rgb(238, 238, 238);
    }

</style>

<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
    name: 'app',
    created(){
        this.$store.dispatch("getUserBaseInfo")
    }
}
</script>

<style>
  #app {
      font-family: "Hiragino Sans GB", "MicroSoft YaHei",'Avenir', Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
  }
</style>

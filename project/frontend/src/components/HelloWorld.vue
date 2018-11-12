<template>
    <div class="body-wrapper">
        <p>Hello World!</p>
    </div>
</template>

<script>
export default {
    name: 'HelloWorld',
    computed: {
        username(){
            return this.$store.state.user.name
        },
        email(){
            return this.$store.state.user.email
        },
    },
    data () {
         return {

         }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
    @my-gray: #eee;

    .body-wrapper{
        background-color: @my-gray;
        height: 100%;
        width: 100%;
        text-align: center;

        p{
            font-weight: 600;
            font-size: 60px;
            margin-top: 200px;
        }
    }
</style>

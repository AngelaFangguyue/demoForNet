<template>
    <el-row style="width: 100%; height: 100%;">
        <el-row style="height: 100%; padding: 100px 0">
            <el-col :span="8" :offset="8" class="content-wrapper">
                <div style="margin-bottom: 30px">
                    <p v-if="nickname">欢迎，{{nickname}}</p>
                    <p v-else>您尚未设置昵称</p>
                </div>

                <el-form :model="form" label-width="100px" label-position="left" size="small">
                    <el-form-item label="昵称">
                        <el-input v-model="form.nickname" placeholder="请输入昵称" clearable></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button @click="onClickModifyBtn">修改昵称</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </el-row>
</template>

<script>
    export default {
        name: "setting",
        computed: {
            nickname(){
                return this.$store.state.user.nickname
            }
        },
        data(){
            return {
                form: {
                    nickname: "",
                }
            }
        },
        watch: {
            nickname(){
                this.form.nickname = this.nickname
            }
        },
        methods: {
            onClickModifyBtn(){
                let params = new URLSearchParams()
                params.append("nickname", this.form.nickname)
                this.$http.post("/api/user/nickname/modify", params)
                    .then(response => {
                        this.$message.success({
                            message: response.data
                        })
                        this.$store.dispatch("getUserBaseInfo")
                    })
                    .catch(error => {
                        console.log(error)
                        this.$message.error({
                            message: error.response.data
                        })
                    })
            }
        }
    }
</script>

<style lang="less" scoped>
    .content-wrapper{
        background-color: #fff;
        padding: 50px;
        height: 100%;

    }
</style>
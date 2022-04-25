<template>
  <el-row type="flex" align="center" justify="center">
    <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="100px" class="demo-ruleForm">
      <el-form-item label="用户名" prop="userName">
        <el-input v-model="ruleForm.login_account" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="ruleForm.login_password" type="password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">登陆</el-button>
      </el-form-item>
    </el-form>
  </el-row>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'Login',
  data() {
    return {
      ruleForm: {
        login_account: '',
        login_password: ''
      },
      rules: {
        login_account: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur' }
        ],
        login_password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 32, message: '长度在 6 到 32 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  created: function() {
    if (localStorage.getItem('token') != null) {
      this.$router.push({path:'/logout'})
    }
  },
  methods: {
    save2localstorage(token) {
      localStorage.setItem('token', token)
    },
    submitForm(formName) {
      var vm = this
      this.$refs[formName].validate(valid => {
        if (valid) {
          var form = this.ruleForm
          axios
            .post('http://localhost:8000/catalog/sign_in', qs.stringify(form))
            .then(function(response) {
              if (response.data.hasOwnProperty("err_msg")) {
                console.log(response.data["err_msg"])
                return false
              }
              vm.save2localstorage(response.data)
              vm.$message({
                message: '登陆成功',
                type: 'success'
              })
              var page = {
                type: '',
                count: 8,
                offset: 1
              }
              vm.$store.commit('getUserDetail')
              vm.$store.commit('getWouldLikeMovie', page)
              vm.$store.commit('getRates')
              vm.$router.push({ path: '/' })
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style lang="css" scoped>
.el-button {
  width: 100%;
}
</style>

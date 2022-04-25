<template>
  <el-row type="flex" align="center" justify="center">
    <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="100px" class="demo-ruleForm">
      <el-form-item label="用户名" prop="userName">
        <el-input v-model="ruleForm.reg_account" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="ruleForm.reg_password" type="password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">注册</el-button>
      </el-form-item>
    </el-form>
  </el-row>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
export default {
  name: 'Sign',
  data() {
    var validateName = (rule, value, callback) => {
      var form = {
        login_account: this.ruleForm.reg_account,
        login_password: this.ruleForm.reg_password
      }
      axios
        .post('http://localhost:8000/catalog/sign_in', qs.stringify(form))
        .then(function(response) {
          if (response.data.hasOwnProperty("err_msg")) {
              callback()
          } else {
            callback(new Error('用户名已注册'))
          }
        })
    }
    return {
      ruleForm: {
        reg_account: '',
        reg_password: ''
      },
      rules: {
        reg_account: [
          { validator: validateName, trigger: 'blur' },
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur' }
        ],
        reg_password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 32, message: '长度在 6 到 32 个字符', trigger: 'blur' }
        ]
      }
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
            .post('http://localhost:8000/catalog/sign_up', qs.stringify(form))
            .then(function(response) {
              if (response.data.hasOwnProperty("err_msg")) {
                console.log(response.data["err_msg"])
                return false
              }
              vm.save2localstorage(response.data)
              vm.$message({
                message: '注册成功,登录成功',
                type: 'success'
              })
              vm.$store.commit('getUserDetail')
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

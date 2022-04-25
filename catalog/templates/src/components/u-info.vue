<template>
  <el-row type="flex" justify="center">
    <el-col :span="6">
      <span class="label">用户名</span>
      <el-input v-model="userDetail.nick_name" />
      <span class="label">电话</span>
      <el-input v-model="userDetail.phone" />
      <span class="label">电子邮箱</span>
      <el-input v-model="userDetail.email" />
      <span class="label">年龄</span>
      <el-input v-model="userDetail.age" />
      <span class="label">性别 </span>
      <el-select v-model="userDetail.sex" @change="handleChange" placeholder="请选择">
        <el-option value="男" />
        <el-option value="女" />
      </el-select>
      <span class="label"> 职业 </span>
      <el-select v-model="userDetail.profession" @change="handleChange" filterable placeholder="请选择">
        <el-option value="学生" />
        <el-option value="工人" />
        <el-option value="教师"/>
        <el-option value="工程师"/>
        <el-option value="科学家"/>
        <el-option value="作家"/>
        <el-option value="售货员"/>
        <el-option value="其他"/>
      </el-select>
      <div style="text-align:center">
        <el-button  size="primary" @click="submitInfo(userDetail)">保存</el-button>                    
      </div>
    </el-col>
  </el-row>
</template>
<script>
import axios from 'axios'
import qs from 'qs'
export default {
  data() {
    return {
      userDetail: {}
    }
  },
  created: function() {
      if (localStorage.getItem('token') == null) {
        this.$message({
          message: '请登录！',
          type: 'warning'
        })
        this.$router.push({path: '/login'})
      }
      this.userDetail = this.$store.getters.getUser
      if (this.userDetail.sex == 'female') {
        this.userDetail.sex = '女'
      } else if (this.userDetail.sex == 'male') {
        this.userDetail.sex = '男'
      }
      return this.userDetail
  },
  methods: {
    addaxiosinterceptor() {
      axios.interceptors.request.use(
        function(config) {
          const authorization = localStorage.getItem('token')
          config.headers.Authorization = authorization
          return config
        },
        function(error) {
          return Promise.reject(error)
        }
      )
    },
    handleChange() {
      this.$forceUpdate()
    },
    submitInfo(user) {
      if (user == {} || user.nick_name == '') {
        this.$message.warning(`用户信息错误`)
      } else {
        this.addaxiosinterceptor()
        if (user.sex == '男') {
          user.sex = 'male'
        } else {
          user.sex = 'female'
        }
        axios
        .post(
          'http://localhost:8000/catalog/save_user_detail',
          qs.stringify(user)
        )
        .then(function(response) {
          console.log(response.data)
        })
        .catch(function(error) {
          console.log(error)
        })
      }
    }
  }
}
</script>

<style lang="css" scoped>
.el-input {
  margin-bottom: 10px;
}
.el-select {
  display: block;
  margin-bottom: 10px;
}
</style>

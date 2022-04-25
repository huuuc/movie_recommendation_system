<template>
  <el-row type="flex" align="center" justify="center">
    <el-col  :span="4">
      <span>
        您已登录，是否需要退出登录？
      </span>
      <div style="text-align:center">
        <el-button type="primary" @click="logout()">退出</el-button>
      </div>
    </el-col>
  </el-row>
</template>
<script>
export default {
  name: 'Logout',
  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$message({
        message: '退出成功！',
        type: 'success'
      })
      this.$router.push({path:'/login'})
    }
  }
}
</script>

<style lang="css" scoped>
span {
  display: block;
  font-size: 18px;
  margin-bottom: 20px;
}
</style>
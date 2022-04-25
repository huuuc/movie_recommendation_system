<template>
  <el-row type="flex" align="center" justify="center">
    <el-col :span="18">
      <el-menu :default-active="activeIndex" :router="true" class="el-menu-demo" mode="horizontal" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
        <el-menu-item index="/">主页</el-menu-item>
        <el-menu-item index="/movie/rec">推荐</el-menu-item>
        <el-menu-item index="/user/detail">个人</el-menu-item>
        <el-menu-item index="/collect">我的收藏</el-menu-item>
        <el-menu-item index="/login">登陆</el-menu-item>
        <el-menu-item index="/sign">注册</el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>
<script>
export default {
  data() {
    return {
      page: {
        type: '',
        country: '',
        context: '',
        count: 8,
        offset: 1
      }
    }
  },
  computed: {
    activeIndex() {
      return this.$route.path
    }
  },
  mounted() {
    this.$store.commit('getMovies', this.page)
    if (localStorage.getItem('token') !== null) {
      this.$store.commit('getWouldLikeMovie', this.page)
      this.$store.commit('getRates')
      this.$store.commit('getUserDetail')
    } else {
      this.$store.commit('initData')
    }
  }
}
</script>
<style lang="css" scoped>
</style>

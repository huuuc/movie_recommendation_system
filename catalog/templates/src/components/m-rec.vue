<template>
  <el-container>
    <el-main>
      <el-row justify="center">
        <el-col v-for="(movie, index) in MoviesPage[0]" :key="index" @click.native="$router.push({path:'/movie/'+movie.fields.movie_id})">
          <el-card :body-style="{ padding: '0px'}" shadow="hover">
            <img :src="getImage(movie.fields.movie_url)"  :onerror="defaultimg" class="image">
            <div class="movie">{{ movie.fields.name }}</div>
          </el-card>
        </el-col>
      </el-row>
      <el-row type="flex" align="center" justify="center">
        <el-col :span="16">
          <el-pagination background layout="prev, pager, next" @current-change="currentChangeHandler" :total="MoviesPage[1]" :page-size="recPage.count">
          </el-pagination>
        </el-col>
      </el-row>
    </el-main>
  </el-container>

</template>
<script>
export default {
  data() {
    return {
      recPage: {
        count: 10, 
        offset: 1
      },
      defaultimg:'this.src="'+require('../../../static/image/default.png')+'"'
    };
  },
  created: function() {
    if (localStorage.getItem('token') == null) {
      this.$message({
        message: '请登录！',
        type: 'warning'
      })
      this.$router.push({path: '/login'})
      return
    }
    this.$store.commit('getRec', this.recPage)
  },
  computed: {
    MoviesPage() {
      return this.$store.getters.getRecMovie
    }
  },
  methods: {
    getImage(url){
	    if(url !== undefined && url != ''){
		    return url.replace(/^(http)[s]*(\:\/\/)/,'https://images.weserv.nl/?url=');
	    }
      return url
    },
    currentChangeHandler(offset) {
      this.recPage.offset = offset
      this.$store.commit('getRec', this.recPage)
    },
  }
}
</script>
<style lang="css" scoped>
.el-main {
  margin-left: 185px;
}
.el-col {
  width: 180px;
  margin: 20px;
}
.el-row {
  margin-bottom: 20px;
  display:flex;
  flex-wrap: wrap;
 }
.el-row  .el-card {
  min-width: 100%;
  height: 100%; 
  margin-right: 20px;
  transition: all .5s;
}
a {
  text-decoration: none;
}
img {
  width: 160px;
  height: 220px;
  margin-top: 10px;
  margin-left: 10px;
  margin-right: 10px;
}
.movie {
  padding-bottom: 0px;
  text-align: center;
  font-size: 15px;
}
span {
  display: inline-block;
  width: 60px;
  height: 20px;
  font-size: 14px;
}
</style>

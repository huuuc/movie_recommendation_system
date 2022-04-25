<template>
  <el-container>
    <el-main>
      <el-row justify="center">
        <el-input style="width:80%;" v-model="page.context" placeholder="请输入">
	        <template slot="append">
		        <el-button type="primary" plain @click="searchMovie">搜索</el-button>
	        </template>
        </el-input>
        <el-col v-for="(movie, index) in MoviesPage[0]" :key="index" @click.native="$router.push({path:'/movie/'+movie.fields.movie_id})">
          <el-card :body-style="{ padding: '0px'}" shadow="hover">
            <img :src="getImage(movie.fields.movie_url)"  :onerror="defaultimg" class="image">
            <div class="movie">{{ movie.fields.name }}</div>
          </el-card>
        </el-col>
      </el-row>
      <el-row type="flex" align="center" justify="center">
        <el-col :span="16">
          <el-pagination background layout="prev, pager, next" @current-change="currentChangeHandler" :total="MoviesPage[1]" :page-size="page.count">
          </el-pagination>
        </el-col>
      </el-row>
    </el-main>
    <el-aside width="250px" style="margin-right:185px">
      <div>
        <h2>
          分类排行榜------------
        </h2>
        <span @click="currentChangeType('')">全部</span>
        <span @click="currentChangeType('剧情')">剧情</span>
        <span @click="currentChangeType('喜剧')">喜剧</span>
        <span @click="currentChangeType('动作')">动作</span>
        <br>
        <span @click="currentChangeType('爱情')">爱情</span>
        <span @click="currentChangeType('科幻')">科幻</span>
        <span @click="currentChangeType('动画')">动画</span>
        <span @click="currentChangeType('悬疑')">悬疑</span>
        <br>
        <span @click="currentChangeType('惊悚')">惊悚</span>
        <span @click="currentChangeType('恐怖')">恐怖</span>
        <span @click="currentChangeType('纪录片')">纪录片</span>
        <span @click="currentChangeType('短片')">短片</span>
        <br>
        <span @click="currentChangeType('情色')">情色</span>
        <span @click="currentChangeType('同性')">同性</span>
        <span @click="currentChangeType('音乐')">音乐</span>
        <span @click="currentChangeType('歌舞')">歌舞</span>
        <br>
        <span @click="currentChangeType('家庭')">家庭</span>
        <span @click="currentChangeType('儿童')">儿童</span>
        <span @click="currentChangeType('传记')">传记</span>
        <span @click="currentChangeType('历史')">历史</span>
        <br>
        <span @click="currentChangeType('战争')">战争</span>
        <span @click="currentChangeType('犯罪')">犯罪</span>
        <span @click="currentChangeType('西部')">西部</span>
        <span @click="currentChangeType('奇幻')">奇幻</span>
        <br>
        <span @click="currentChangeType('冒险')">冒险</span>
        <span @click="currentChangeType('灾难')">灾难</span>
        <span @click="currentChangeType('武侠')">武侠</span>
        <span @click="currentChangeType('古装')">古装</span>
        <br>
        <h2>
          地区排行榜------------
        </h2>
        <span @click="currentChangeCountry('')">全部</span>
        <span @click="currentChangeCountry('中国大陆')">中国大陆</span>
        <span @click="currentChangeCountry('美国')">美国</span>
        <span @click="currentChangeCountry('中国香港')">中国香港</span>
        <br>
        <span @click="currentChangeCountry('中国台湾')">中国台湾</span>
        <span @click="currentChangeCountry('日本')">日本</span>
        <span @click="currentChangeCountry('韩国')">韩国</span>
        <span @click="currentChangeCountry('英国')">英国</span>
        <br>
        <span @click="currentChangeCountry('法国')">法国</span>
        <span @click="currentChangeCountry('德国')">德国</span>
        <span @click="currentChangeCountry('意大利')">意大利</span>
        <span @click="currentChangeCountry('西班牙')">西班牙</span>
        <br>
        <span @click="currentChangeCountry('印度')">印度</span>
        <span @click="currentChangeCountry('泰国')">泰国</span>
        <span @click="currentChangeCountry('俄罗斯')">俄罗斯</span>
        <span @click="currentChangeCountry('伊朗')">伊朗</span>
        <br>
        <span @click="currentChangeCountry('加拿大')">加拿大</span>
        <span @click="currentChangeCountry('澳大利亚')">澳大利亚</span>
        <span @click="currentChangeCountry('爱尔兰')">爱尔兰</span>
        <span @click="currentChangeCountry('瑞典')">瑞典</span>
        <br>
      </div>
    </el-aside>

  </el-container>

</template>
<script>
const page = {
  type: "",
  country: "",
  context: "",
  count: 8, 
  offset: 1
}
export default {
  data() {
    return {
      page,
      defaultimg:'this.src="'+require('../../../static/image/default.png')+'"'
    };
  },
  computed: {
    MoviesPage() {
      return this.$store.getters.getMovieList
    }
  },
  methods: {
    searchMovie() {
      this.page.country = '',
      this.page.type = '',
      this.$store.commit('getMovies', this.page)
    },
    getImage(url){
	    if(url !== undefined && url != ''){
		    return url.replace(/^(http)[s]*(\:\/\/)/,'https://images.weserv.nl/?url=');
	    }
      return url
    },
    currentChangeHandler(offset) {
      this.page.offset = offset
      this.$store.commit('getMovies', this.page)
    },
    currentChangeType(type) {
      this.page.type = type
      this.$store.commit('getMovies', this.page)
    },
    currentChangeCountry(country) {
      this.page.country = country
      this.$store.commit('getMovies', this.page)
    }
  }
}
</script>
<style lang="css" scoped>
.el-main {
  margin-left: 185px;
}
.el-col {
  width: 180px;
  margin: 10px;
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
.el-input {
  margin-left: 70px;
  
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

<template>
<el-main>
  <el-row type="flex" justify="center">
    <el-col :span="8">
      <el-card :body-style="{ padding: '0px'}" shadow="hover">
        <div>
          <img :src="getImage(movie.fields.movie_url)" :onerror="defaultimg" v-if="movie" class="image">
        </div>
        <div class="right">
          <span>
            <span>名称</span>
            :
            <span>{{ movie.fields.name }}</span>
          </span>
          <br>
          <span>
            <span>导演</span>
            :
            <span>{{ movie.fields.director }}</span>
          </span>
          <br>
          <span>
            <span>主演</span>
            :
            <span>{{ movie.fields.stars }}</span>
          </span>
          <br>
          <span>
            <span>类型</span>
            :
            <span>{{ movie.fields.type }}</span>
          </span>
          <br>
          <span>
            <span>国家</span>
            :
            <span>{{ movie.fields.country }}</span>
          </span>
          <br>
          <span>
            <span>语言</span>
            :
            <span>{{ movie.fields.language }}</span>
          </span>
          <br>
          <span>
            <span>上映日期</span>
            :
            <span>{{ movie.fields.releas_time }}</span>
          </span>
          <br>
          <span>
            <span>片长</span>
            :
            <span>{{ movie.fields.length }} 分钟</span>
          </span>
          <br>
        </div>
        <div class="block right">
          {{ movie.fields.rate_num }} 人评价
          <el-rate  v-model="score" :disabled = "true" :max="10" text-color="#ff9900" :show-score="true" :allow-half="true" :colors="['#99A9BF', '#F7BA2A', '#FF9900']">
          </el-rate>
          你的评价
          <el-rate v-model="value" :disabled="isread" @change="changeHandler" text-color="#ff9900" :show-score="isread" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" >
          </el-rate>
        </div>
        <div class="collect">
          <el-button type="primary" float:left plain @click="collectMovie">收藏</el-button>
        </div>
      </el-card>
    </el-col>
  </el-row>
  <el-row type="flex" justify="center">
    <el-col :span="12">
      <div class="commentBox">
        <h3>评论区</h3>
        <p v-if="comment.length==0">暂无评论，我来发表第一篇评论！</p>
        <div v-else>
          <div class="comment" v-for="(item,index) in comment[0]" v-bind:index="index" >
            <b>
              {{ item.user_name }}
              <span>{{ item.time }}</span>
              <el-button type="primary" float:right plain @click="vote(item.tag_id)">
                <img :src="agreeImg">
                <div>{{ item.votes }}</div>
              </el-button>
            </b>
            <p>{{ item.content }}</p>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
  <el-row type="flex" align="center" justify="center">
    <el-col :span="12">
      <el-pagination background layout="prev, pager, next" @current-change="currentChangeHandler" :total="comment[1]" :page-size="tag_param.count">
      </el-pagination>
    </el-col>
  </el-row>
  <el-row type="flex" justify="center">
    <el-col :span="12">
      <div class="commentBox">
      <h3>发表评论</h3>
        <textarea name="" value="请填写评论内容" v-model="commentText"></textarea>
        <el-button  @click="addComment">发表</el-button>
      </div>
    </el-col>
  </el-row>
</el-main>
</template>
<script>
import axios from 'axios'
import qs from 'qs'
export default {
  created: function() {
    var param = {
      count: 10, 
      offset: 1,
      movie_id: this.$route.params.id
    }
    this.$store.commit('getComment', param)
  },
  data() {
    return {
      commentText: '',
      score: null,
      movie_id: 0,
      user_score: null,
      defaultimg:'this.src="'+require('../../../static/image/default.png')+'"',
      agreeImg: require('../../../static/image/agree.png'),
      tag_param: {
        count: 10, 
        offset: 1,
        movie_id: this.$route.params.id
      }
    }
  },
  computed: {
    movie() {
      var movie = this.$store.getters.getMovie(this.$route.params.id)
      this.score = Number(movie.fields.score)
      this.movie_id = movie.fields.movie_id
      return movie
    },
    comment() {
      return this.$store.getters.getComments
    },
    value: {
      get: function() {
        return this.$store.getters.getRate(this.$route.params.id)
      },
      set: function(newScore) {
        this.user_score = newScore
      }
    },
    isread() {
      if (this.value === null) {
        return false
      }
      return true
    }
  },
  methods: {
    changeHandler(value) {
      if (this.$store.getters.getRate(this.$route.params.id) === null) {
        this.changeHandlerMethod(value)
      }
    },
    vote(id) {
      let vm = this
      axios
        .post(
          'http://localhost:8000/catalog/vote_tag',
          qs.stringify({ vote_id: id})
        )
        .then(function(response) {
          if (response.data.hasOwnProperty("err_msg")) {
            console.log(response.data["err_msg"])
          }
          else {
            vm.$message.success('点赞成功！')
            vm.$router.push({path:'/movie/'+vm.$route.params.id})
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    addComment() {
      let vm = this
      if (this.commentText == '') {
        vm.$message.warning('评论信息不能为空！')
        return
      }
      this.addaxiosinterceptor()
      axios
        .post(
          'http://localhost:8000/catalog/comment_movie',
          qs.stringify({ movie_id: vm.movie.fields.movie_id,  comment: this.commentText})
        )
        .then(function(response) {
          if (response.data.hasOwnProperty("err_msg")) {
            console.log(response.data["err_msg"])
          }
          else {
            vm.$message({
              message: '评论成功!',
              type: 'success'
            })
            vm.commentText = ''
            vm.$forceUpdate()
          }
        })
        .catch(function(error) {
          vm.$message.error('认证失败，已跳转到登陆页面')
          console.log(error)
          vm.$router.push({ path: '/login' })
        })
    },
    collectMovie() {
      this.addaxiosinterceptor()
      let vm = this
      axios
        .post(
          'http://localhost:8000/catalog/add_would_like_movie',
          qs.stringify({ movie_id: vm.movie.fields.movie_id})
        )
        .then(function(response) {
          if (response.data.hasOwnProperty("err_msg")) {
            vm.$message({
              message: '已收藏！',
              type: 'warning'
            })
          }
          else {
            vm.$message({
              message: '添加成功!',
              type: 'success'
            })
          }
        })
        .catch(function(error) {
          vm.$message.error('认证失败，已跳转到登陆页面')
          console.log(error)
          vm.$router.push({ path: '/login' })
        })
    },
    currentChangeHandler(offset) {
      this.tag_param.offset = offset
      this.$store.commit('getComment', this.tag_param)
    },
    getImage(url){
	    if(url !== undefined && url != ''){
		    return url.replace(/^(http)[s]*(\:\/\/)/,'https://images.weserv.nl/?url=');
	    }
      return url
    },
    changeHandlerMethod(value) {
      this.addaxiosinterceptor()
      let vm = this
      axios
        .post(
          'http://localhost:8000/catalog/rate_movie',
          qs.stringify({ movie_id: vm.movie.fields.movie_id, rate: value})
        )
        .then(function(response) {
          console.log(response.data)
          if (response.data.hasOwnProperty("err_msg")) {
            vm.$message({
              message: '已评分！',
              type: 'warning'
            })
          } else {
            vm.$store.commit('getRates')
            vm.$message({
              message: '添加成功!',
              type: 'success'
            })
          }
        })
        .catch(function(error) {
          vm.$message.error('认证失败，已跳转到登陆页面')
          console.log(error)
          vm.$router.push({ path: '/login' })
        })
    },
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
    }
  }
}
</script>

<style lang="css" scoped>
.el-col {
  margin: 5px;
}
img {
  width: 160px;
  height: 220px;
  margin-top: 10px;
  margin-left: 10px;
  margin-right: 10px;
  float: left;
}
.el-button {
  margin-left: 55px;
  margin-top: 10px;
  margin-bottom: 10px;

}
.right {
  padding-top: 5px;
  float: right;
  width: 290px;
  font-size: 14px;
}
.commentBox {
  margin:20px;
}
.commentBox h3 {
  color: #634322;
  background: #e9e5df;
  padding: 8px 15px;
  text-align: left;
  font-size: 16px;
}
.comment p {
  font-size:16px;
  margin-bottom: 20px;
  color:#333;
}
.comment b span {
  color:#333;
  font-size:14px;
  margin-left:20px;
}
.comment b {
  color:#01553D;
  font-size:16px;
  display:block;
  margin:5px 0;
}
.commentBox textarea {
  overflow: auto; 
  width: 100%; 
  height: 95px; 
  outline: none; 
  resize: none;
}
.commentBox button {
  float:right; 
  background:#338FCC;
  color: #fff;
  margin-left:20px; 
  padding:5px 30px; 
  border-radius:5px; 
  font-size:16px;
}
.collect button {
  background:#338FCC;
  color: #fff;
}
.collect button:hover {
  color: #fff;
  background:#22B8DD;
}
.commentBox button:hover {
  color: #fff;
  background:#22B8DD;
}
.comment img {
  width: 20px;
  height: 20px;
}
.comment button {
  background:#FFA54F;
  color: #fff;
}
.comment + .comment {
  border-top:1px solid #ccc;
}
</style>

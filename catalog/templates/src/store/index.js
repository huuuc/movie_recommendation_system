import Vue from 'vue'
import vuex from 'vuex'
import axios from 'axios'
Vue.use(vuex)
export default new vuex.Store({
  state: {
    movies: [],
    // 用户评分数组
    rates: [],
    // 电影相关评论
    comments: [],
    user: {},
    // allRates: [],
    recommend: [],
    would_like: [],
    // 总页数
    would_like_total: 0,
    comment_total: 0,
    movies_total: 0,
    recommend_total: 0,
  },
  getters: {
    getMovie: state => id => {
      for (let x in state.movies) {
        if (state.movies[x].fields.movie_id == Number(id)) {
          return state.movies[x]
        }
      }
      for (let x in state.would_like) {
        if (state.would_like[x].fields.movie_id == Number(id)) {
          return state.would_like[x]
        }
      }
      for (let x in state.recommend) {
        if (state.recommend[x].fields.movie_id == Number(id)) {
          return state.recommend[x]
        }
      }
      return []
    },
    getRecMovie: state => {
      return [state.recommend, state.recommend_total]
    },
    getMovieList: state => {
      return [state.movies, state.movies_total]
    },
    getWouldLike: state => {
      return [state.would_like, state.would_like_total]
    },
    getComments: state => {
      return [state.comments, state.comment_total]
    },
    getRate: state => id => {
      for (let x in state.rates) {
        if (state.rates[x].movie_id == Number(id)) {
          return state.rates[x].rate
        }
      }
      return null
    },
    getUser: state => {
      return state.user
    }
  },
  mutations: {
    getMovies(state, obj) {
      axios.post('http://localhost:8000/catalog/get_type_list', JSON.stringify(obj)).then(function(response) {
        if (response.data.hasOwnProperty("err_msg")) {
          console.log(response.data["err_msg"])
          return false
        }
        state.movies = response.data["data"]
        state.movies_total = response.data.total
      })
    },
    getComment(state, obj) {
      axios.post('http://localhost:8000/catalog/get_tag_list', JSON.stringify(obj)).then(function(response) {
        if (response.data.hasOwnProperty("err_msg")) {
          console.log(response.data["err_msg"])
          return false
        }
        state.comments = response.data["data"]
        state.comment_total = response.data.total
      })
    },
    getWouldLikeMovie(state, obj) {
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
      obj.type = 1
      axios
        .post('http://localhost:8000/catalog/get_movie_list', JSON.stringify(obj)).then(function(respone) {
          if (respone.data.hasOwnProperty("err_msg")) {
            console.log(respone.data["err_msg"])
            return false
          }
          state.would_like = respone.data["data"]
          state.would_like_total = respone.data.total
        })
        .catch(function(error) {
          localStorage.removeItem('token')
          console.log(error)
        })  
    },
    getUserDetail(state) {
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
      axios
        .post('http://localhost:8000/catalog/get_user_detail').then(function(respone) {
          if (respone.data.hasOwnProperty("err_msg")) {
            console.log(respone.data["err_msg"])
            return false
          }
          state.user['nick_name'] = respone.data['nick_name']
          state.user['phone'] = respone.data['phone']
          state.user['email'] = respone.data['email']
          state.user['age'] = respone.data['age']
          state.user['sex'] = respone.data['sex']
          state.user['profession'] = respone.data['profession']
        })
        .catch(function(error) {
          localStorage.removeItem('token')
          console.log(error)
        })  
    },
    getRec(state, obj) {
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
      axios
        .post('http://localhost:8000/catalog/get_recommend_list', JSON.stringify(obj))
        .then(function(respone) {
          if (respone.data.hasOwnProperty("err_msg")) {
            console.log(respone.data["err_msg"])
            return false
          }
          state.recommend = respone.data["data"]
          state.recommend_total = respone.data.total
        })
        .catch(function(error) {
          localStorage.removeItem('token')
          console.log(error)
        })
    },
    getRates(state) {
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
      axios
        .get('http://localhost:8000/catalog/get_rate_list')
        .then(function(respone) {
          if (respone.data.hasOwnProperty("err_msg")) {
            console.log(respone.data["err_msg"])
            return false
          }
          state.rates = respone.data["data"]
        })
        .catch(function(error) {
          localStorage.removeItem('token')
          console.log(error)
        })
    }
  },
  initData(state) {
    state.rates = []
    state.user = {}
    state.recommend = []
    state.would_like = []
    state.would_like_total = 0
    state.recommend_total = 0
  },
  actions: {}
})

import Vue from 'vue'
import Router from 'vue-router'
import MList from '@/components/m-list'
import MRec from '@/components/m-rec'
import UInfo from '@/components/u-info'
import MInfo from '@/components/m-info'
import Login from '@/components/login'
import Sign from '@/components/sign'
import Logout from '@/components/logout'
import Collect from '@/components/collect'
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    { path: '/', name: 'MList', component: MList },
    { path: '/user/detail', name: 'UInfo', component: UInfo },
    { path: '/movie/rec', name: 'MRec', component: MRec },
    { path: '/movie/:id', name: 'MInfo', component: MInfo },
    { path: '/login', name: 'Login', component: Login },
    { path: '/sign', name: 'Sign', component: Sign },
    { path: '/logout', name: 'Logout', component: Logout },
    { path: '/collect', name: 'Collect', component: Collect }
  ]
})

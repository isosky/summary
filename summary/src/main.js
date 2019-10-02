// import Vue from 'vue/dist/vue.js'
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import task from './components/task.vue'
import analysis from './components/analysis.vue'
import VueRouter from 'vue-router'

Vue.use(ElementUI)
Vue.use(VueRouter)

const routes = [{
    path: '/task',
    component: task
  },
  {
    path: '/analysis',
    component: analysis
  }
]


const router = new VueRouter({
  routes
})

const app = new Vue({
  router,
  render: h => h(App),
  mounted: function () {
    this.gofirstpage()
  },
  methods: {
    gofirstpage: function (event) {
      this.$router.push('/task')
    }
  }
}).$mount('#app')

import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import task from './components/task.vue'
import analysis from './components/analysis.vue'
import schedule from './components/schedule.vue'
import VueRouter from 'vue-router'
import axios from 'axios'

Vue.use(ElementUI)
Vue.use(VueRouter)

const routes = [{
    path: '/task',
    component: task
  },
  {
    path: '/analysis',
    component: analysis
  },
  {
    path: '/schedule',
    component: schedule

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
    this.initschedule()
  },
  methods: {
    gofirstpage: function (event) {
      this.$router.push('/schedule')
    },
    initschedule: function (event) {
      axios.get("http://127.0.0.1:5000/initschedule").then(response => {
        if (response.status == 200) {
          // console.log(response);
          console.log(response);
          if (response.data.status == 1) {
            this.$message({
              message: response.data.message,
              type: "success"
            });
          }
        }
      });
    }
  }
}).$mount('#app')

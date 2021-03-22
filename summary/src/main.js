import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import task from './components/task.vue'
import person from './components/person.vue'
import count from './components/count.vue'
import schedule from './components/schedule.vue'
import syssetting from './components/syssetting.vue'
import VueRouter from 'vue-router'

import axios from 'axios'

Vue.use(ElementUI)
Vue.use(VueRouter)

const routes = [{
    path: '/task',
    component: task
  },
  {
    path: '/schedule',
    component: schedule

  },
  {
    path: '/person',
    component: person

  },
  {
    path: '/count',
    component: count

  },
  {
    path: '/syssetting',
    component: syssetting

  }
]

const router = new VueRouter({
  routes
})

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

axios.defaults.baseURL = 'http://localhost:5000';
// axios.defaults.baseURL = 'http://81.70.25.54:5000';

const app = new Vue({
  router,
  render: h => h(App),
  mounted: function () {
    this.gofirstpage()
    this.initschedule()
  },
  methods: {
    gofirstpage: function (event) {
      // 2020-07-05 从数据库中获得
      axios.get("/getfirstpage").then(response => {
        if (response.status == 200) {
          let temp = '/' + response.data.firstpage;
          this.$router.push(temp);
        }
      });
    },
    initschedule: function (event) {
      axios.get("/initschedule").then(response => {
        if (response.status == 200) {
          // console.log(response);
          // 添加完成后，需要重新刷新一下面板
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

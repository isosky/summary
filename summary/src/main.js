import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import task from './components/task.vue'
import analysis from './components/analysis.vue'
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
    path: '/analysis',
    component: analysis
  },
  {
    path: '/schedule',
    component: schedule

  },
  {
    path: '/syssetting',
    component: syssetting

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
      // 2020-07-05 从数据库中获得
      // TODO 搞个yys的题库，现在的这个命中率太丢人了
      axios.get("http://127.0.0.1:5000/getfirstpage").then(response => {
        if (response.status == 200) {
          // console.log(response);
          // 添加完成后，需要重新刷新一下面板
          let temp = '/' + response.data.firstpage
          this.$router.push(temp)
        }
      });

    },
    initschedule: function (event) {
      axios.get("http://127.0.0.1:5000/initschedule").then(response => {
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

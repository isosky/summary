import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import task from './components/task.vue';
import project from './components/project.vue';
import transaction from './components/transaction.vue';
import investmentReview from './components/investment_review.vue';
import marketWatchlist from './components/market_watchlist.vue';
import marketSyncOps from './components/market_sync_ops.vue';
import person from './components/person.vue';
import count from './components/count.vue';
import schedule from './components/schedule.vue';
// fund subpages archived: see summary/src/components/archive/
import syssetting from './components/syssetting.vue';
import typeanalysis from './components/typeanalysis.vue';
import travel from './components/travel.vue';
import activity from './components/activity.vue';
import activityRunSegmentAnalysis from './components/activity_run_segment_analysis.vue';
import activityRideSegmentAnalysis from './components/activity_ride_segment_analysis.vue';
import activitySettings from './components/activity_settings.vue';
// archived components removed: cycling, dft, nga, nga_setting
import VueRouter from 'vue-router';

import axios from 'axios';

Vue.use(ElementUI);
Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    redirect: '/task'
  },
  {
    path: '/task',
    component: task
  },
  {
    path: '/project',
    component: project
  },
  {
    path: '/transaction',
    component: transaction
  },
  {
    path: '/investment_review',
    component: investmentReview
  },
  {
    path: '/market_watchlist',
    component: marketWatchlist
  },
  {
    path: '/market_sync_ops',
    component: marketSyncOps
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
    path: '/typeanalysis',
    component: typeanalysis
  },
  {
    path: '/travel',
    component: travel
  },
  {
    path: '/activity',
    component: activity
  },
  {
    path: '/activity_run_segment_analysis',
    component: activityRunSegmentAnalysis
  },
  {
    path: '/activity_ride_segment_analysis',
    component: activityRideSegmentAnalysis
  },
  {
    path: '/activity_settings',
    component: activitySettings
  },

  {
    path: '/syssetting',
    component: syssetting
  }
];

const router = new VueRouter({
  routes
});

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err);
};
// 动态根据当前页面主机名设置后端地址，避免浏览器中 localhost 指向错误主机
axios.defaults.baseURL = (function () {
  const host = window.location.hostname || 'localhost';
  return 'http://' + host + ':5000';
})();

new Vue({
  router,
  render: h => h(App),
  mounted: function () {
    this.initschedule();
  },
  methods: {
    initschedule: function (event) {
      axios.get('/initschedule').then(response => {
        if (response.status === 200) {
          // console.log(response);
          // 添加完成后，需要重新刷新一下面板
          if (response.data.status === 1) {
            this.$message({
              message: response.data.message,
              type: 'success'
            });
          }
        }
      });
    }
  }
}).$mount('#app');

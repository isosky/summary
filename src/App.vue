<template>
  <div id="app">
    <el-row v-if="islogin">
      <el-col :span="1" v-if="islogin">
        <div>
          <el-menu :default-active="defaultactive" class="el-menu-vertical-demo" :collapse="isCollapse"
            :default-openeds="defaultOpeneds" @select="moveto">
            <el-menu-item index="/task">
              <i class="el-icon-s-claim"></i>
              <span slot="title">任务管理</span>
            </el-menu-item>
            <el-menu-item index="/project">
              <i class="el-icon-collection"></i>
              <span slot="title">项目分析</span>
            </el-menu-item>
            <el-menu-item index="/transaction">
              <i class="el-icon-data-analysis"></i>
              <span slot="title">财务分析</span>
            </el-menu-item>
            <el-menu-item index="/investment_review">
              <i class="el-icon-data-line"></i>
              <span slot="title">投资复盘</span>
            </el-menu-item>
            <el-menu-item index="/market_watchlist">
              <i class="el-icon-view"></i>
              <span slot="title">观察池管理</span>
            </el-menu-item>
            <el-menu-item index="/market_sync_ops">
              <i class="el-icon-refresh"></i>
              <span slot="title">市场同步运维</span>
            </el-menu-item>
            <el-menu-item index="/count">
              <i class="el-icon-s-data"></i>
              <span slot="title">统计</span>
            </el-menu-item>
            <el-menu-item index="/person">
              <i class="el-icon-user"></i>
              <span slot="title">人员信息</span>
            </el-menu-item>
            <el-menu-item index="/schedule">
              <i class="el-icon-time"></i>
              <span slot="title">定时任务</span>
            </el-menu-item>
            <el-menu-item index="/typeanalysis">
              <i class="el-icon-monitor"></i>
              <span slot="title">类型分析</span>
            </el-menu-item>
            <el-menu-item index="/travel">
              <i class="el-icon-s-promotion"></i>
              <span slot="title">出行</span>
            </el-menu-item>
            <el-submenu index="/activity_menu">
              <template slot="title">
                <i class="el-icon-bicycle"></i>
                <span>运动分析</span>
              </template>
              <el-menu-item index="/activity">运动总览</el-menu-item>
              <el-menu-item index="/activity_run_segment_analysis">跑步路段分析</el-menu-item>
              <el-menu-item index="/activity_ride_segment_analysis">骑行路段分析</el-menu-item>
              <el-menu-item index="/activity_settings">设置</el-menu-item>
            </el-submenu>
            <el-menu-item index="/syssetting">
              <i class="el-icon-setting"></i>
              <span slot="title">系统设置</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-col>
      <el-col :span="23">
        <div>
          <router-view></router-view>
        </div>
      </el-col>
    </el-row>
    <el-row v-if="!islogin">
      <el-input v-model="todo_user_name" placeholder="请输入内容"></el-input>
      <el-input placeholder="请输入密码" v-model="todo_user_pass" show-password></el-input>
      <el-button type="primary" @click="login">确 定</el-button>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      // TODO 考虑一下是否将gofirstpage放到这个地方
      defaultactive: '/task',
      defaultOpeneds: ['/activity_menu'],
      isCollapse: true,
      islogin: false,
      todo_user_name: '',
      todo_user_pass: ''
      // routers: ["/task", "/yysyh", "/yyshero", "/schedule", "/syssetting"]
    };
  },
  mounted: function () {
    // console.log(axios.defaults.headers.common["Authorization"]);
    if (typeof axios.defaults.headers.common['Authorization'] === 'undefined') {
      this.islogin = false;
    } else {
      this.islogin = true;
      this.defaultactive = this.$route.path || '/task';
    }
  },
  watch: {
    '$route.path': function (val) {
      this.defaultactive = val || '/task';
    }
  },
  methods: {
    moveto: function (index) {
      this.$router.push(index);
    },
    login: function (event) {
      axios
        .post('/login', {
          user_name: this.todo_user_name,
          user_pass: this.todo_user_pass
        })
        .then((response) => {
          if (response.data.code === 200) {
            axios.defaults.headers.common['Authorization'] =
              response.data.token;
            this.islogin = true;
            this.defaultactive = '/task';
            this.$router.push('/task');
            // console.log(axios.defaults.headers.common);
          }
        });
    }
  }
};
</script>

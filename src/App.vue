<template>
  <div id="app">
    <el-row v-if="islogin">
      <el-col :span="1" v-if="islogin">
        <div>
          <el-menu :default-active="defaultactive" class="el-menu-vertical-demo" :collapse="isCollapse"
            @select="moveto">
            <el-menu-item index="/task">
              <i class="el-icon-s-claim"></i>
              <span slot="title">任务管理</span>
            </el-menu-item>
            <el-menu-item index="/project">
              <i class="el-icon-collection"></i>
              <span slot="title">项目分析</span>
            </el-menu-item>
            <el-menu-item index="/dft">
              <i class="el-icon-data-board"></i>
              <span slot="title">dft</span>
            </el-menu-item>
            <el-menu-item index="/transaction">
              <img src="@/assets/wallet.png">
              <span slot="title">财务分析</span>
            </el-menu-item>
            <el-menu-item index="/count">
              <i class="el-icon-s-data"></i>
              <span slot="title">统计</span>
            </el-menu-item>
            <el-menu-item index="/person">
              <i class="el-icon-user"></i>
              <span slot="title">人员信息</span>
            </el-menu-item>
            <el-submenu index="/fund_estimate">
              <template slot="title">
                <i class="el-icon-money"></i>
                <span>基金</span>
              </template>
              <el-menu-item index="/fund_estimate">
                <i class="el-icon-view"></i>
                <span>基金估值</span>
              </el-menu-item>
              <el-menu-item index="/fund_total">
                <i class="el-icon-view"></i>
                <span>基金统计</span>
              </el-menu-item>
              <el-menu-item index="/fund_review">
                <i class="el-icon-view"></i>
                <span>基金复盘</span>
              </el-menu-item>
              <el-menu-item index="/fund_orders"><i class="el-icon-view"></i>
                <span>基金买卖</span>
              </el-menu-item>
              <el-menu-item index="/fund_treemap_label"><i class="el-icon-view"></i>
                <span>基金分布</span>
              </el-menu-item>
              <el-menu-item index="/fund_setting"><i class="el-icon-view"></i>
                <span>基金设置</span>
              </el-menu-item>
            </el-submenu>
            <!-- <el-submenu index="/nga">
              <template slot="title">
                <i class="el-icon-chat-dot-square"></i>
                <span>NGA</span>
              </template> -->
            <el-menu-item index="/nga">
              <i class="el-icon-chat-dot-square"></i>
              <span slot="title">NGA</span>
            </el-menu-item>
            <!-- <el-menu-item index="/nga_setting">
                <i class="el-icon-setting"></i>
                <span slot="title">NGA设置</span>
              </el-menu-item>
            </el-submenu> -->
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
            <el-menu-item index="/cycling">
              <i class="el-icon-bicycle"></i>
              <span slot="title">骑行</span>
            </el-menu-item>
            <!-- <el-menu-item index="/cycling_strava">
              <i class="el-icon-bicycle"></i>
              <span slot="title">骑行strava</span>
            </el-menu-item> -->
            <el-submenu>
              <template slot="title">
                <i class="el-icon-setting"></i>
                <span>设置</span>
              </template>
              <el-menu-item index="/syssetting">
                <i class="el-icon-setting"></i>
                <span slot="title">系统设置</span>
              </el-menu-item>
              <el-menu-item index="/nga_setting">
                <i class="el-icon-setting"></i>
                <span slot="title">NGA设置</span>
              </el-menu-item>
            </el-submenu>
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
import axios from "axios";
export default {
  data() {
    return {
      // TODO 考虑一下是否将gofirstpage放到这个地方
      defaultactive: "1",
      isCollapse: true,
      islogin: false,
      todo_user_name: "",
      todo_user_pass: "",
      // routers: ["/task", "/yysyh", "/yyshero", "/schedule", "/syssetting"]
    };
  },
  mounted: function () {
    // console.log(axios.defaults.headers.common["Authorization"]);
    if (typeof axios.defaults.headers.common["Authorization"] === "undefined") {
      this.islogin = false;
    } else this.islogin = true;
  },
  methods: {
    moveto: function (index) {
      this.$router.push(index);
    },
    login: function (event) {
      axios
        .post("/login", {
          user_name: this.todo_user_name,
          user_pass: this.todo_user_pass,
        })
        .then((response) => {
          if (response.data.code == 200) {
            axios.defaults.headers.common["Authorization"] =
              response.data.token;
            this.islogin = true;
            this.$router.push("/task");
            // console.log(axios.defaults.headers.common);
          }
        });
    },
  },
};
</script>

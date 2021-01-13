<template>
  <div id="app">
    <el-row>
      <el-col :span="1">
        <div>
          <el-menu
            default-active="3"
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
            @select="moveto"
          >
            <el-menu-item index="1">
              <i class="el-icon-s-claim"></i>
              <span slot="title">任务管理</span>
            </el-menu-item>
            <el-menu-item index="2">
              <i class="el-icon-time"></i>
              <span slot="title">定时任务</span>
            </el-menu-item>
            <el-menu-item index="3">
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      isCollapse: true,
      // routers: ["/task", "/yysyh", "/yyshero", "/schedule", "/syssetting"]
      routers: ["/task", "/schedule", "/syssetting"],
    };
  },
  methods: {
    moveto: function (index) {
      this.$router.push(this.routers[index - 1]);
    },
  },
};
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>
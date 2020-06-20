<template>
  <div id="app">
    <el-row :gutter="5">
      <el-col :span="6">
        <el-tabs v-model="yys_yhtypescore_bar_select" @tab-click="roleclick">
          <el-tab-pane label="scrapy" name="scrapy">scrapy</el-tab-pane>
          <el-tab-pane label="吃糖了" name="吃糖了">吃糖了</el-tab-pane>
          <el-tab-pane label="ploit" name="ploit">ploit</el-tab-pane>
          <el-tab-pane label="葛神棍" name="葛神棍">葛神棍</el-tab-pane>
        </el-tabs>
      </el-col>
      <el-col :span="18">
        <div id="yys_yhscore_line" style="height:300px"></div>
      </el-col>
    </el-row>
    <el-row :gutter="5">
      <el-col :span="16">
        <div id="yys_yhtypescore_bar" style="height:300px"></div>
      </el-col>
      <el-col :span="4">
        <div id="yys_yhtypenum_radar" style="height:300px"></div>
      </el-col>
      <el-col :span="4">
        <div id="yys_yhtype_sunburst" style="height:300px"></div>
      </el-col>
    </el-row>
  </div>
</template>


<script>
import axios from "axios";
var echarts = require("echarts");
export default {
  data() {
    return {
      yys_yhscore_line_chart: "",
      yys_yhscore_line_option: {
        tooltip: {
          trigger: "axis"
        },
        legend: {
          left: "left"
        },
        xAxis: {
          type: "category",
          splitLine: { show: false },
          data: []
        },
        yAxis: {
          type: "value",
          min: "dataMin"
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        series: []
      },
      yys_yhtypescore_bar_select: "scrapy",
      yys_yhtypescore_bar_chart: "",
      yys_yhtypescore_bar_chart_data: "",
      yys_yhtypescore_bar_option: {
        tooltip: {
          trigger: "axis"
        },
        xAxis: {
          type: "category",
          axisLabel: { rotate: 45 },
          data: []
        },
        yAxis: {
          type: "value"
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        series: [
          {
            label: {
              show: true,
              position: "top"
            },
            type: "bar",
            data: []
          }
        ]
      }
    };
  },
  mounted: function() {
    this.yys_yhscore_line_chart = echarts.init(
      document.getElementById("yys_yhscore_line"),
      "white",
      { renderer: "canvas" }
    );
    this.yys_yhtypescore_bar_chart = echarts.init(
      document.getElementById("yys_yhtypescore_bar"),
      "white",
      { renderer: "canvas" }
    );
    this.freshall();
  },
  methods: {
    freshyhscore: function() {
      axios.get("http://127.0.0.1:5000/yys_getyhscore").then(response => {
        if (response.status == 200) {
          // console.log(response);
          this.yys_yhscore_line_option.legend.data = response.data.legend;
          this.yys_yhscore_line_option.xAxis.data = response.data.axis;
          this.yys_yhscore_line_option.series = response.data.series;
          // console.log(this.yys_yhscore_line_option);
          this.yys_yhscore_line_chart.setOption(this.yys_yhscore_line_option);
          this.yys_yhtypescore_bar_chart.setOption(
            this.yys_yhtypescore_bar_option
          );
        }
      });
    },
    freshyhtypescore: function() {
      axios.get("http://127.0.0.1:5000/yys_getyhtypescore").then(response => {
        if (response.status == 200) {
          // console.log(response);
          this.yys_yhtypescore_bar_option.xAxis.data = response.data.axis;
          this.yys_yhtypescore_bar_chart_data = response.data.series;
          this.yys_yhtypescore_bar_option.series[0].data = this.yys_yhtypescore_bar_chart_data[
            this.yys_yhtypescore_bar_select
          ];
          // console.log(this.yys_yhtypescore_bar_option);
          this.yys_yhtypescore_bar_chart.setOption(
            this.yys_yhtypescore_bar_option
          );
        }
      });
    },
    freshall: function() {
      this.freshyhscore();
      this.freshyhtypescore();
    },
    roleclick(tab, event) {
      // console.log(tab, event);
      this.yys_yhtypescore_bar_option.series[0].data = this.yys_yhtypescore_bar_chart_data[
        this.yys_yhtypescore_bar_select
      ];
      this.yys_yhtypescore_bar_chart.setOption(this.yys_yhtypescore_bar_option);
    }
  }
};
</script>

<style>
</style>
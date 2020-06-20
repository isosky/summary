<template>
  <div id="app">
    <el-row :gutter="5">
      <el-col :span="4">
        <div>role_info</div>
      </el-col>
      <el-col :span="20">
        <div id="yys_yh_score_line" style="height:300px"></div>
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
      yys_yh_score_line_chart: "",
      yys_yh_score_line_option: {
        tooltip: {
          trigger: "axis"
        },
        legend: {
          left: "left"
        },
        xAxis: {
          type: "category",
          name: "x",
          splitLine: { show: false },
          data: []
        },
        // dataZoom: [{ start: 80 }],
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        yAxis: {
          type: "value",
          min: "dataMin"
        },
        series: []
      }
    };
  },
  mounted: function() {
    console.log(this);
    this.yys_yh_score_line_chart = echarts.init(
      document.getElementById("yys_yh_score_line"),
      "white",
      { renderer: "canvas" }
    );
    this.freshall();
  },
  methods: {
    freshall: function() {
      axios.get("http://127.0.0.1:5000/yys_getyhscore").then(response => {
        if (response.status == 200) {
          // console.log(response);
          this.yys_yh_score_line_option.legend.data = response.data.legend;
          this.yys_yh_score_line_option.xAxis.data = response.data.axis;
          this.yys_yh_score_line_option.series = response.data.series;
          // console.log(this.yys_yh_score_line_option);
          this.yys_yh_score_line_chart.setOption(this.yys_yh_score_line_option);
        }
      });
    }
  }
};
</script>

<style>
</style>
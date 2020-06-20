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
        <el-row :gutter="5">
          <div id="yys_yhtypescore_bar" style="height:300px"></div>
        </el-row>
        <el-row :gutter="5">
          <el-col :span="6">
            <div id="yys_yhtypenum_radar" style="height:300px"></div>
          </el-col>
          <el-col :span="18">
            <!-- <div id="yys_yhtypetop10" style="height:300px"></div> -->
            <el-tabs v-model="yys_yhtypetop10" @tab-click="roleclick">
              <el-tab-pane label="一号位" name="一号位">一号位</el-tab-pane>
              <el-tab-pane label="二号位" name="二号位">二号位</el-tab-pane>
              <el-tab-pane label="三号位" name="三号位">三号位</el-tab-pane>
              <el-tab-pane label="四号位" name="四号位">四号位</el-tab-pane>
              <el-tab-pane label="五号位" name="五号位">五号位</el-tab-pane>
              <el-tab-pane label="六号位" name="六号位">六号位</el-tab-pane>
            </el-tabs>
          </el-col>
        </el-row>
      </el-col>

      <el-col :span="8">
        <div id="yys_yhtype_sunburst" style="height:600px">123</div>
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
          left: "2%",
          right: "2%",
          bottom: "5%",
          top: "5%",
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
      },
      yys_yhtypescore_bar_option_select: "雪幽魂",
      yys_yhtypenum_radar_chart: "",
      yys_yhtypenum_radar_chart_data: "",
      yys_yhtypenum_radar_option: {
        title: {
          text: ""
        },
        radar: {
          // name: {
          //   textStyle: {
          //     color: "#fff",
          //     backgroundColor: "#999",
          //     borderRadius: 3,
          //   }
          // },
          indicator: [
            { name: "一号位" },
            { name: "二号位" },
            { name: "三号位" },
            { name: "四号位" },
            { name: "五号位" },
            { name: "六号位" }
          ]
        },
        series: [
          {
            type: "radar",
            // areaStyle: {normal: {}},
            data: [
              {
                value: []
              }
            ]
          }
        ]
      },
      yys_yhtypetop10: "一号位"
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
    this.yys_yhtypenum_radar_chart = echarts.init(
      document.getElementById("yys_yhtypenum_radar"),
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
    freshyhtypenum: function() {
      axios.get("http://127.0.0.1:5000/yys_getyhtypenum").then(response => {
        if (response.status == 200) {
          console.log(response);
          console.log(this.yys_yhtypenum_radar_option);
          this.yys_yhtypenum_radar_chart_data = response.data.series;
          console.log(this.yys_yhtypenum_radar_chart_data);
          this.yys_yhtypenum_radar_option.title.text = this.yys_yhtypescore_bar_option_select;
          this.yys_yhtypenum_radar_option.title.subtext = "14个";
          this.yys_yhtypenum_radar_option.series[0].data[0].value = this.yys_yhtypenum_radar_chart_data[
            this.yys_yhtypescore_bar_select
          ][this.yys_yhtypescore_bar_option_select];

          console.log(this.yys_yhtypenum_radar_option);
          this.yys_yhtypenum_radar_chart.setOption(
            this.yys_yhtypenum_radar_option
          );
        }
      });
    },
    freshall: function() {
      this.freshyhtypenum();
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
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
        <div id="yys_yhtype_sunburst" style="height:600px"></div>
      </el-col>
    </el-row>
  </div>
</template>


<script>
import axios from "axios";
import AppVue from "../App.vue";
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
      yys_yhtypenum_radar_title_data: "",
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
      yys_yhtype_sunburst_chart: "",
      yys_yhtype_sunburst_chart_data: "",
      yys_yhtype_sunburst_option: {
        tooltip: {},
        series: {
          type: "sunburst",
          // highlightPolicy: 'ancestor',
          data: [],
          radius: [0, "90%"],
          label: {
            rotate: "radial"
          }
        }
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
    this.yys_yhtype_sunburst_chart = echarts.init(
      document.getElementById("yys_yhtype_sunburst"),
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
          this.yys_yhtypenum_radar_title_data = response.data.yh_type_nums;
          this.yys_yhtypescore_bar_chart_data = response.data.series;
          this.yys_yhtypescore_bar_option.xAxis.data = response.data.axis;
          this.yys_yhtypescore_bar_option.series[0].data = this.yys_yhtypescore_bar_chart_data[
            this.yys_yhtypescore_bar_select
          ];
          this.yys_yhtypescore_bar_chart.setOption(
            this.yys_yhtypescore_bar_option
          );
          // 其实就是增加一个指向就好了，不然下面的this用的是echarts，不是vue的this
          let _this = this;
          this.yys_yhtypescore_bar_chart.on("click", function(params) {
            // console.log(_this);
            _this.yys_yhtypescore_bar_option_select = params.name;
            // console.log(_this.yys_yhtypescore_bar_option_select);
          });
        }
      });
    },
    freshyhtypenum: function() {
      axios.get("http://127.0.0.1:5000/yys_getyhtypenum").then(response => {
        if (response.status == 200) {
          // console.log(response);
          this.yys_yhtypenum_radar_chart_data = response.data.series;
          this.yys_yhtypenum_radar_option.title.text = this.yys_yhtypescore_bar_option_select;
          this.yys_yhtypenum_radar_option.title.subtext =
            this.yys_yhtypenum_radar_title_data[
              this.yys_yhtypescore_bar_select
            ][this.yys_yhtypescore_bar_option_select] + "个";
          this.yys_yhtypenum_radar_option.series[0].data[0].value = this.yys_yhtypenum_radar_chart_data[
            this.yys_yhtypescore_bar_select
          ][this.yys_yhtypescore_bar_option_select];
          this.yys_yhtypenum_radar_chart.setOption(
            this.yys_yhtypenum_radar_option
          );
        }
      });
    },
    freshyhtypesunburst: function() {
      axios
        .get("http://127.0.0.1:5000/yys_getyhtypesunburst")
        .then(response => {
          if (response.status == 200) {
            console.log(response);
            this.yys_yhtype_sunburst_chart_data = response.data.series;
            this.yys_yhtype_sunburst_option.series.data = this.yys_yhtype_sunburst_chart_data[
              this.yys_yhtypescore_bar_select
            ][this.yys_yhtypescore_bar_option_select];
            this.yys_yhtype_sunburst_chart.setOption(
              this.yys_yhtype_sunburst_option
            );
          }
        });
    },
    freshall: function() {
      this.freshyhscore();
      this.freshyhtypescore();
      this.freshyhtypenum();
      this.freshyhtypesunburst();
    },
    roleclick(tab, event) {
      // console.log(tab, event);
      this.yys_yhtypescore_bar_option.series[0].data = this.yys_yhtypescore_bar_chart_data[
        this.yys_yhtypescore_bar_select
      ];
      this.yys_yhtypescore_bar_chart.setOption(this.yys_yhtypescore_bar_option);
    }
  },
  watch: {
    yys_yhtypescore_bar_option_select: function(val) {
      // console.log(
      //   this.yys_yhtypescore_bar_select,
      //   this.yys_yhtypescore_bar_option_select
      // );
      // console.log(this.yys_yhtypenum_radar_chart_data);
      this.yys_yhtypenum_radar_option.title.text = this.yys_yhtypescore_bar_option_select;
      this.yys_yhtypenum_radar_option.title.subtext =
        this.yys_yhtypenum_radar_title_data[this.yys_yhtypescore_bar_select][
          this.yys_yhtypescore_bar_option_select
        ] + "个";
      this.yys_yhtypenum_radar_option.series[0].data[0].value = this.yys_yhtypenum_radar_chart_data[
        this.yys_yhtypescore_bar_select
      ][this.yys_yhtypescore_bar_option_select];
      this.yys_yhtypenum_radar_chart.setOption(this.yys_yhtypenum_radar_option);
      // 更新右边的图
      this.yys_yhtype_sunburst_option.series.data = this.yys_yhtype_sunburst_chart_data[
        this.yys_yhtypescore_bar_select
      ][this.yys_yhtypescore_bar_option_select];
      this.yys_yhtype_sunburst_chart.setOption(this.yys_yhtype_sunburst_option);
    }
  }
};
</script>

<style>
</style>
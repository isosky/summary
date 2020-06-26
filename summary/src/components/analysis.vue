<template>
  <div id="app">
    <el-row :gutter="5">
      <el-col :span="6">
        <el-tabs v-model="role_name" @tab-click="roleclick">
          <!-- TODO 原本这个地方想用组件来实现，结果发现直接在下面重新声明一个div就好了 -->
          <el-tab-pane label="scrapy" name="scrapy"></el-tab-pane>
          <el-tab-pane label="吃糖了" name="吃糖了"></el-tab-pane>
          <el-tab-pane label="ploit" name="ploit"></el-tab-pane>
          <el-tab-pane label="葛神棍" name="葛神棍"></el-tab-pane>
          <!-- <div>asd</div> -->
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="grid-content bg-purple" align="center">6星式神:{{sixss}}</div>
            </el-col>
            <el-col :span="8">
              <div class="grid-content bg-purple-light" align="center">6星御魂:{{sixyh}}</div>
            </el-col>
            <el-col :span="8">
              <div class="grid-content bg-purple" align="center">御魂总分:{{yhsum}}</div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="4" v-for="item in yys_role_now" :key="item.id">
              <!-- <span class="demonstration">{{ fit }}</span> -->
              <el-image style="width: 40px; height: 40px;left:10px" :src="item.rurl" :fit="full"></el-image>
              <div class="grid-content bg-purple" align="center">{{item.value}}</div>
              <div class="grid-content bg-purple-light" align="center">{{item.zc}}</div>
            </el-col>
          </el-row>
          <el-row :gutter="5"></el-row>
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
      sixss: "123",
      sixyh: "234",
      yhsum: "123",
      yys_role_data: "",
      /**
       * { id: 1, v: 1, url: require("../assets/suit/300007.png") },
       * { id: 2, v: 2, url: require("../assets/suit/300002.png") },
       * { id: 3, v: 3, url: require("../assets/suit/300003.png") },
       * { id: 4, v: 4, url: require("../assets/suit/300004.png") },
       * { id: 5, v: 5, url: require("../assets/suit/300008.png") },
       * { id: 6, v: 6, url: require("../assets/suit/300006.png") }
       */
      yys_role_now: [],
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
      role_name: "scrapy",
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
              color: "#000",
              position: "top"
            },
            type: "bar",
            data: []
          }
        ]
      },
      yh_name: "雪幽魂",
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
                value: [],
                label: {
                  show: true,
                  formatter: function(params) {
                    return params.value;
                  }
                }
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
          sort: null,
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
            this.role_name
          ];
          this.yys_yhtypescore_bar_chart.setOption(
            this.yys_yhtypescore_bar_option
          );
          // 其实就是增加一个指向就好了，不然下面的this用的是echarts，不是vue的this
          let _this = this;
          this.yys_yhtypescore_bar_chart.on("click", function(params) {
            // console.log(_this);
            _this.yh_name = params.name;
            // console.log(_this.yh_name);
          });
        }
      });
    },
    freshyhtypenum: function() {
      axios.get("http://127.0.0.1:5000/yys_getyhtypenum").then(response => {
        if (response.status == 200) {
          // console.log(response);
          this.yys_yhtypenum_radar_chart_data = response.data.series;
          this.yys_yhtypenum_radar_option.title.text = this.yh_name;
          this.yys_yhtypenum_radar_option.title.subtext =
            this.yys_yhtypenum_radar_title_data[this.role_name][this.yh_name] +
            "个";
          this.yys_yhtypenum_radar_option.series[0].data[0].value = this.yys_yhtypenum_radar_chart_data[
            this.role_name
          ][this.yh_name];
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
            // console.log(response);
            this.yys_yhtype_sunburst_chart_data = response.data.series;
            this.yys_yhtype_sunburst_option.series.data = this.yys_yhtype_sunburst_chart_data[
              this.role_name
            ][this.yh_name];
            this.yys_yhtype_sunburst_chart.setOption(
              this.yys_yhtype_sunburst_option
            );
          }
        });
    },
    setrole: function() {
      // console.log(this.yys_role_data);
      this.sixss = this.yys_role_data[this.role_name].sixss;
      this.sixyh = this.yys_role_data[this.role_name].sixyh;
      this.yhsum = this.yys_role_data[this.role_name].yhsum;
      this.yys_role_now = this.yys_role_data[this.role_name].speed;
    },
    initrole: function() {
      axios.get("http://127.0.0.1:5000/yys_getyysrole").then(response => {
        if (response.status == 200) {
          console.log(response);
          this.yys_role_data = response.data.res;
          console.log("**********");
          for (let i in this.yys_role_data) {
            // console.log(i);
            this.yys_role_data[i].speed.forEach(item => {
              item.rurl = require("../assets/suit/" + item.url);
              // console.log(item);
            });
          }
          this.setrole();
        }
      });
    },
    freshall: function() {
      this.initrole();
      this.freshyhscore();
      this.freshyhtypescore();
      this.freshyhtypenum();
      this.freshyhtypesunburst();
    },
    roleclick(tab, event) {
      // console.log(tab, event);
      this.yys_yhtypescore_bar_option.series[0].data = this.yys_yhtypescore_bar_chart_data[
        this.role_name
      ];
      this.yys_yhtypescore_bar_chart.setOption(this.yys_yhtypescore_bar_option);
      this.setrole();
    }
  },
  watch: {
    yh_name: function(val) {
      // console.log(
      //   this.role_name,
      //   this.yh_name
      // );
      // console.log(this.yys_yhtypenum_radar_chart_data);
      this.yys_yhtypenum_radar_option.title.text = this.yh_name;
      this.yys_yhtypenum_radar_option.title.subtext =
        this.yys_yhtypenum_radar_title_data[this.role_name][this.yh_name] +
        "个";
      this.yys_yhtypenum_radar_option.series[0].data[0].value = this.yys_yhtypenum_radar_chart_data[
        this.role_name
      ][this.yh_name];
      this.yys_yhtypenum_radar_chart.setOption(this.yys_yhtypenum_radar_option);
      // 更新右边的图
      this.yys_yhtype_sunburst_option.series.data = this.yys_yhtype_sunburst_chart_data[
        this.role_name
      ][this.yh_name];
      this.yys_yhtype_sunburst_chart.setOption(this.yys_yhtype_sunburst_option);
    }
  }
};
</script>

<style>
</style>
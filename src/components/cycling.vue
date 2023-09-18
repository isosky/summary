<template>
  <div id="app">
    <el-col :span="24">
      <div id="cycling_div" style="height: 900px; position: relative"></div>
    </el-col>
  </div>
</template>

<script>
import axios from "axios";
var echarts = require("echarts");
import "echarts/extension/bmap/bmap";
import mapConfig from "../data/map-config.json";
export default {
  data() {
    return {
      cycling_chart: "",
      bmap: {},
      cycling_chart_option: {
        bmap: {
          center: [116.46, 39.92],
          zoom: 11,
          roam: true,
          mapStyle: {
            styleJson: mapConfig,
          },
        },
        series: [
          {
            type: "lines",
            coordinateSystem: "bmap",
            data: [],
            polyline: true,
            silent: true,
            lineStyle: {
              // color: '#c23531',
              // color: 'rgb(200, 35, 45)',
              opacity: 0.7,
              width: 1,
            },
            progressiveThreshold: 5000,
            progressive: 2000,
          },
          {
            type: "lines",
            coordinateSystem: "bmap",
            data: [],
            polyline: true,
            lineStyle: {
              width: 0,
            },
            effect: {
              constantSpeed: 20,
              show: true,
              trailLength: 0.2,
              symbolSize: 2,
            },
            zlevel: 2,
          },
        ],
      },
    };
  },
  mounted: function () {
    this.init();
  },
  methods: {
    init: function () {
      this.cycling_chart = echarts.init(
        document.getElementById("cycling_div"),
        "white",
        {
          renderer: "canvas",
        }
      );
      axios.get("/getcycling").then((response) => {
        if (response.status == 200) {
          console.log(response);
          this.cycling_chart_option.series[0].data = response.data.cycling_data;
          this.cycling_chart_option.series[1].data = response.data.cycling_data;
          this.cycling_chart.setOption(this.cycling_chart_option);
        }
      });
    },
  },
};
</script>
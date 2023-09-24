<template>
  <div id="app">
    <el-col :span="24">
      <div id="travel_div" style="height: 900px; position: relative"></div>
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
      travel_chart: "",
      bmap: {},
      travel_chart_option: {
        bmap: {
          center: [116.46, 39.92],
          zoom: 5,
          roam: true,
          mapStyle: {
            styleJson: mapConfig,
          },
        },
        series: [
          {
            type: "lines",
            coordinateSystem: "bmap",
            polyline: false,
            data: [],
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
            polyline: false,
            data: [],
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
          {
            type: "effectScatter",
            coordinateSystem: "bmap",
            data: [],
            label: {
              formatter: "{b}",
              position: "top",
              show: true,
            },
            symbolSize: 3,
            itemStyle: {
              color: "#f4e925",
              shadowBlur: 10,
              shadowColor: "#333",
            },
            zlevel: 1,
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
      console.log(this.bmap);
      this.travel_chart = echarts.init(
        document.getElementById("travel_div"),
        "white",
        {
          renderer: "canvas",
        }
      );
      axios.get("/gettravel").then((response) => {
        if (response.status == 200) {
          console.log(response);
          this.travel_chart_option.series[0].data = response.data.travel_data;
          this.travel_chart_option.series[1].data = response.data.travel_data;
          this.travel_chart_option.series[2].data = response.data.res_city;
          this.travel_chart.setOption(this.travel_chart_option);
        }
      });
    },
  },
};
</script>
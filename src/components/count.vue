<template>
  <div id="app">
    <el-col :span="24">
      <el-tabs
        v-model="activeName"
        :lazy="true"
        style="height: 940px"
        @tab-click="handleClick"
      >
        <el-tab-pane
          label="任务情况-时间分布"
          name="first"
          style="height: 940px"
        >
          <el-row>
            <div id="treemap_type_chart_div" style="height: 920px"></div>
          </el-row>
        </el-tab-pane>
        <el-tab-pane label="专精-时间分布" name="second" style="height: 940px">
          <el-row>
            <div id="treemap_dir_chart_div" style="height: 920px"></div>
          </el-row>
        </el-tab-pane>
        <el-tab-pane label="进度表" name="third" style="height: 940px">
          <el-row>
            <div id="bar_progress_chart_div" style="height: 920px"></div>
          </el-row>
        </el-tab-pane>
        <el-tab-pane label="sankey" name="forth" style="height: 940px">
          <el-row>
            <div id="sankey_chart_div" style="height: 920px"></div>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-col>
    <el-dialog
      title="提示"
      :visible.sync="dialogtaskVisible"
      width="40%"
      :before-close="handleClose"
    >
      <el-row :span="5">
        <el-tag type="success">{{ main_click }}</el-tag>
        <el-tag type="success">{{ sub_click }}</el-tag>
      </el-row>
      <el-row :span="5">
        <el-table :data="dialogtask" style="width: 100%" :height="300">
          <el-table-column prop="task_id" label="任务id" width="80">
          </el-table-column>
          <el-table-column prop="task_name" label="任务名称" width="280">
          </el-table-column>
          <el-table-column prop="hours" label="耗时" width="120">
          </el-table-column>
          <el-table-column prop="ftime" label="完成时间" width="180">
          </el-table-column>
        </el-table>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
var echarts = require("echarts");
var formatUtil = echarts.format;
export default {
  data() {
    return {
      activeName: "first",
      bar_progress_chart: "",
      main_click: "",
      sub_click: "",
      dialogtask: [],
      dialogtaskVisible: false,
      bar_progress_chart_option: {
        dataset: {
          dimensions: ["dirs", "value", "ccc"],
          source: [],
        },
        title: {
          text: "进度表",
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        yAxis: { type: "value", max: 5000 },
        xAxis: {
          type: "category",
          axisLabel: {
            interval: 0,
            rotate: 45,
          },
        },
        visualMap: {
          // Map the score column to color
          dimension: "ccc",
          show: false,
          min: 0,
          max: 100,
          // TODO 颜色啊
          inRange: {
            color: ["blue", "yellow", "gray", "red"],
          },
        },
        series: [
          {
            type: "bar",
            label: {
              show: true,
              position: "top",
              formatter: function (num) {
                if (num.value == 0) {
                  return "";
                }
              },
            },
            encode: {
              x: "dirs",
              y: "value",
            },
          },
        ],
      },
      treemap_type_chart: "",
      treemap_type_chart_option: {
        title: {
          text: "任务类型-时间分布",
        },
        tooltip: {
          formatter: function (info) {
            var value = info.value;
            var treePathInfo = info.treePathInfo;
            var treePath = [];

            for (var i = 1; i < treePathInfo.length; i++) {
              treePath.push(treePathInfo[i].name);
            }

            return [
              '<div class="tooltip-title">' +
                formatUtil.encodeHTML(treePath.join("/")) +
                "</div>",
              "总工作时间: " + formatUtil.addCommas(value) + " 小时",
            ].join("");
          },
        },
        series: [
          {
            type: "treemap",
            label: {
              show: true,
              formatter: "{b}\n{c}小时",
            },
            levels: [
              {
                itemStyle: {
                  borderWidth: 0,
                  gapWidth: 5,
                },
              },
              {
                itemStyle: {
                  gapWidth: 1,
                },
              },
              {
                colorSaturation: [0.35, 0.5],
                itemStyle: {
                  gapWidth: 1,
                  borderColorSaturation: 0.6,
                },
              },
            ],
            data: [],
          },
        ],
      },
      treemap_dir_chart: "",
      treemap_dir_chart_option: {
        title: {
          text: "专精-时间分布",
        },
        tooltip: {
          formatter: function (info) {
            var value = info.value;
            var treePathInfo = info.treePathInfo;
            var treePath = [];

            for (var i = 1; i < treePathInfo.length; i++) {
              treePath.push(treePathInfo[i].name);
            }

            return [
              '<div class="tooltip-title">' +
                formatUtil.encodeHTML(treePath.join("/")) +
                "</div>",
              "总工作时间: " + formatUtil.addCommas(value) + " 小时",
            ].join("");
          },
        },
        series: [
          {
            type: "treemap",
            label: {
              show: true,
              formatter: "{b}\n{c}小时",
            },
            levels: [
              {
                itemStyle: {
                  borderWidth: 0,
                  gapWidth: 5,
                },
              },
              {
                itemStyle: {
                  gapWidth: 1,
                },
              },
              {
                colorSaturation: [0.35, 0.5],
                itemStyle: {
                  gapWidth: 1,
                  borderColorSaturation: 0.6,
                },
              },
            ],
            data: [],
          },
        ],
      },
      sankey_chart: "",
      sankey_chart_option: {
        title: {
          text: "关联图",
        },
        series: [
          {
            type: "sankey",
            data: [],
            links: [],
            emphasis: {
              focus: "adjacency",
            },
            levels: [
              {
                depth: 0,
                itemStyle: {
                  color: "#ec6867",
                },
                lineStyle: {
                  color: "target",
                  opacity: 0.4,
                },
              },
              {
                depth: 1,
                itemStyle: {
                  color: "#5e7bd7",
                },
                lineStyle: {
                  color: "target",
                  opacity: 0.4,
                },
              },
              {
                depth: 2,
                itemStyle: {
                  color: "green",
                },
                lineStyle: {
                  color: "target",
                  opacity: 0.4,
                },
              },
              {
                depth: 3,
                itemStyle: {
                  color: "#a86ac4",
                },
                lineStyle: {
                  color: "target",
                  opacity: 0.4,
                },
              },
              {
                depth: 4,
                itemStyle: {
                  color: "#fedc67",
                },
                lineStyle: {
                  color: "target",
                  opacity: 0.4,
                },
              },
            ],
            lineStyle: {
              curveness: 0.5,
            },
          },
        ],
      },
      pickerOptions: {
        shortcuts: [
          {
            text: "最近一周",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "最近一个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "最近三个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            },
          },
        ],
      },
    };
  },
  mounted: function () {
    let that = this;
    // this.bar_progress_chart = echarts.init(
    //   document.getElementById("bar_progress_chart_div"),
    //   "white",
    //   {
    //     renderer: "canvas",
    //   }
    // );
    this.treemap_type_chart = echarts.init(
      document.getElementById("treemap_type_chart_div"),
      "white",
      {
        renderer: "canvas",
      }
    );
    this.treemap_type_chart.on("click", function (params) {
      axios
        .post("/gettreetask", {
          type: "type",
          main: params.treePathInfo[1]["name"],
          sub: params.treePathInfo[2]["name"],
        })
        .then((response) => {
          that.main_click = params.treePathInfo[1]["name"];
          that.sub_click = params.treePathInfo[2]["name"];
          that.dialogtask = response.data.datas;
          that.dialogtaskVisible = true;
        });
    });
    // this.treemap_dir_chart = echarts.init(
    //   document.getElementById("treemap_dir_chart_div"),
    //   "white",
    //   {
    //     renderer: "canvas",
    //   }
    // );

    this.init();
  },
  methods: {
    handleClick(tab, event) {
      if (this.activeName == "second") {
        let that = this;
        if (this.treemap_dir_chart == "") {
          setTimeout(() => {
            this.treemap_dir_chart = echarts.init(
              document.getElementById("treemap_dir_chart_div"),
              "white",
              {
                renderer: "canvas",
              }
            );
            this.treemap_dir_chart.on("click", function (params) {
              // console.log(params);
              axios
                .post("/gettreetask", {
                  type: "dir",
                  main: params.treePathInfo[1]["name"],
                  sub: params.treePathInfo[2]["name"],
                })
                .then((response) => {
                  that.main_click = params.treePathInfo[1]["name"];
                  that.sub_click = params.treePathInfo[2]["name"];
                  that.dialogtask = response.data.datas;
                  that.dialogtaskVisible = true;
                });
            });
            axios.post("/gettreemapdata", {}).then((response) => {
              this.treemap_dir_chart_option.series[0].data =
                response.data.treemap_dir_data;
              this.treemap_dir_chart.setOption(this.treemap_dir_chart_option);
            });
          }, 500);
        } else {
          axios.post("/gettreemapdata", {}).then((response) => {
            this.treemap_dir_chart_option.series[0].data =
              response.data.treemap_dir_data;
            this.treemap_dir_chart.setOption(this.treemap_dir_chart_option);
          });
        }
      }
      if (this.activeName == "third") {
        // console.log(document.getElementById("sankey_chart_div"));
        if (this.bar_progress_chart == "") {
          setTimeout(() => {
            this.bar_progress_chart = echarts.init(
              document.getElementById("bar_progress_chart_div"),
              "white",
              {
                renderer: "canvas",
              }
            );
            axios.post("/getprogressdata", {}).then((response) => {
              this.bar_progress_chart_option.dataset.source =
                response.data.progress_data;
              this.bar_progress_chart.setOption(this.bar_progress_chart_option);
            });
          }, 500);
        } else {
          axios.post("/getprogressdata", {}).then((response) => {
            this.bar_progress_chart_option.dataset.source =
              response.data.progress_data;
            this.bar_progress_chart.setOption(this.bar_progress_chart_option);
          });
        }
      }
      if (this.activeName == "forth") {
        // console.log(document.getElementById("sankey_chart_div"));
        if (this.sankey_chart == "") {
          setTimeout(() => {
            this.sankey_chart = echarts.init(
              document.getElementById("sankey_chart_div"),
              "white",
              {
                renderer: "canvas",
              }
            );
            axios.post("/getsankeydata", {}).then((response) => {
              // console.log(response.data);
              this.sankey_chart_option.series[0].data = response.data.nodes;
              this.sankey_chart_option.series[0].links = response.data.links;
              this.sankey_chart.setOption(this.sankey_chart_option);
            });
          }, 500);
        } else {
          axios.post("/getsankeydata", {}).then((response) => {
            // console.log(response.data);
            this.sankey_chart_option.series[0].data = response.data.nodes;
            this.sankey_chart_option.series[0].links = response.data.links;
            this.sankey_chart.setOption(this.sankey_chart_option);
          });
        }
      }
    },
    init: function () {
      axios.post("/gettreemapdata", {}).then((response) => {
        this.treemap_type_chart_option.series[0].data =
          response.data.treemap_type_data;

        this.treemap_type_chart.setOption(this.treemap_type_chart_option);
      });
    },
    handleClose: function () {
      this.dialogtask = [];
      this.main_click = "";
      this.sub_click = "";
      this.dialogtaskVisible = false;
    },
  },
};
</script>


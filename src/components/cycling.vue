<template>
  <div id="app">
    <el-col :span="12">
      <el-row :gutter="5">
        <el-select
          label="标题"
          :label-width="formLabelWidth"
          v-model="cycling_type_selected"
          clearable
          filterable
          @change="updatelabeloption"
          default-first-option
          placeholder="请选择"
          style="width: 220px"
        >
          <el-option
            v-for="item in cycling_type_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-row>
      <div class="grid-content">
        <el-table
          :data="cyclingdata"
          border
          height="855"
          style="width: 100%"
          :default-sort="{ prop: 'date', order: 'descending' }"
        >
          <el-table-column
            prop="date"
            sortable
            label="日期"
            width="180"
          ></el-table-column>
          <el-table-column
            prop="strava_id"
            label="strava_id"
            width="120"
          ></el-table-column>
          <el-table-column
            prop="name"
            label="名称"
            width="110"
          ></el-table-column>
          <el-table-column
            prop="avg_hr"
            label="平均心率"
            width="60"
          ></el-table-column>
          <el-table-column
            prop="max_hr"
            label="最大心率"
            width="60"
          ></el-table-column>
          <el-table-column
            prop="np"
            label="标准功率"
            width="60"
          ></el-table-column>
          <el-table-column
            prop="intensity"
            label="强度"
            width="60"
          ></el-table-column>
          <el-table-column
            prop="efficiency"
            label="效率"
            width="60"
          ></el-table-column>
          <el-table-column
            prop="avg_cadence"
            label="踏频"
            width="60"
          ></el-table-column>
          <el-table-column prop="adr" label="解耦" width="60"></el-table-column>
          <el-table-column
            prop="remark"
            label="备注"
            width="120"
          ></el-table-column>
        </el-table>
      </div>
    </el-col>
    <el-col :span="12">
      <div id="cycling_charts" style="height: 240px">图零</div>
      <div id="cycling_line_charts1" style="height: 380px">图一</div>
      <div id="cycling_line_charts2" style="height: 380px">图二</div>
    </el-col>
  </div>
</template>

<script>
import axios from "axios";
var echarts = require("echarts");

export default {
  data() {
    return {
      formLabelWidth: "100px",
      cyclingdata: [],
      cycling_type_option: [],
      cycling_type_selected: "",
      cycling_charts1: "",
      charts1_option: {
        tooltip: {
          trigger: "axis",
        },
        legend: {
          data: ["平均心率", "最大心率", "踏频"],
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          data: [],
        },
        yAxis: [
          {
            type: "value",
            min: "dataMin",
          },
          {
            type: "value",
            min: "dataMin",
          },
        ],
        series: [
          {
            name: "平均心率",
            type: "line",
            data: [],
            label: {
              show: true,
            },
          },
          {
            name: "最大心率",
            type: "line",
            data: [],
            label: {
              show: true,
            },
          },
          {
            name: "踏频",
            type: "line",
            yAxisIndex: 1,
            data: [],
            label: {
              show: true,
            },
          },
        ],
      },
      cycling_charts2: "",
      charts2_option: {
        tooltip: {
          trigger: "axis",
        },
        legend: {
          data: ["强度", "效率", "解耦"],
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          data: [],
        },
        yAxis: [
          {
            type: "value",
            min: 0.6,
          },
          {
            type: "value",
          },
        ],
        series: [
          {
            name: "强度",
            type: "line",
            data: [],
            label: {
              show: true,
            },
          },
          {
            name: "效率",
            type: "line",
            data: [],
            label: {
              show: true,
            },
          },
          {
            name: "解耦",
            type: "bar",
            yAxisIndex: 1,
            data: [],
            label: {
              show: true,
            },
          },
        ],
      },
    };
  },
  mounted: function () {
    this.init();
    this.cycling_charts1 = echarts.init(
      document.getElementById("cycling_line_charts1"),
      "white",
      {
        renderer: "canvas",
      }
    );
    this.cycling_charts2 = echarts.init(
      document.getElementById("cycling_line_charts2"),
      "white",
      {
        renderer: "canvas",
      }
    );
  },
  methods: {
    init: function () {
      axios
        .post("/getcycling", {
          cycling_type_selected: this.cycling_type_selected,
        })
        .then((response) => {
          this.cyclingdata = response.data.tabledata;
        });
      this.getcycoption();
    },
    getcycoption: function () {
      axios.get("/get_cycling_name").then((response) => {
        this.cycling_type_option = response.data.data;
      });
    },
    updatelabeloption: function () {
      axios
        .post("/getcycling", {
          cycling_type_selected: this.cycling_type_selected,
        })
        .then((response) => {
          this.cyclingdata = response.data.tabledata;
          this.charts1_option.xAxis.data = response.data.yaxis;
          this.charts1_option.series[0].data = response.data.avg_hr;
          this.charts1_option.series[1].data = response.data.max_hr;
          this.charts1_option.series[2].data = response.data.avg_cadence;
          this.cycling_charts1.setOption(this.charts1_option);
          this.charts2_option.xAxis.data = response.data.yaxis;
          this.charts2_option.series[0].data = response.data.intensity;
          this.charts2_option.series[1].data = response.data.efficiency;
          this.charts2_option.series[2].data = response.data.adr;
          this.cycling_charts2.setOption(this.charts2_option);
        });
    },
  },
};
</script>


<style>
.formlabelwidth {
  width: 120px;
}
.el-table {
  overflow: visible !important;
}
</style>
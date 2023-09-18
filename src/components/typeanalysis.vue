<template>
  <div id="app">
    <el-row>
      <el-col :span="3">
        <el-select
          @change="updatesuboption"
          clearable
          filterable
          allow-create
          default-first-option
          v-model="task_select"
          placeholder="请选择"
        >
          <el-option
            v-for="item in task_select_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-col>
      <el-col :span="4">
        <el-select
          v-model="task_sub_select"
          filterable
          clearable
          allow-create
          default-first-option
          placeholder="请选择"
        >
          <el-option
            v-for="item in task_sub_select_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-col>
      <el-col :span="4">
        <el-select
          v-model="person_id"
          filterable
          :filter-method="personFilter"
          clearable
          default-first-option
          placeholder="请选择相关人员"
        >
          <el-option
            v-for="item in person_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-col>
      <el-col :span="3"
        ><el-button type="primary" @click="freshscatter"
          >查询</el-button
        ></el-col
      >
    </el-row>
    <el-row>
      <el-col :span="20">
        <div id="scatter_persontype_chart_div" style="height: 900px"></div>
      </el-col>
      <el-col :span="4">
        <el-row>
          <span>积极性评价</span>
        </el-row>
        <el-row>
          <el-table :data="scoreactivity" style="width: 100%">
            <el-table-column prop="stype" label="项目"> </el-table-column>
            <el-table-column prop="pic" label="负责人"> </el-table-column>
            <el-table-column prop="pe" label="参与者"> </el-table-column>
            <el-table-column prop="po" label="其他"> </el-table-column>
          </el-table>
        </el-row>
        <el-row> <span>批判性评价</span></el-row>
        <el-row>
          <el-table :data="scorecritical" style="width: 100%">
            <el-table-column prop="stype" label="项目"> </el-table-column>
            <el-table-column prop="pic" label="负责人"> </el-table-column>
            <el-table-column prop="pe" label="参与者"> </el-table-column>
            <el-table-column prop="po" label="其他"> </el-table-column>
          </el-table>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>



<script>
import axios from "axios";
import PinyinMatch from "pinyin-match";
var echarts = require("echarts");
export default {
  data() {
    return {
      scoreactivity: [
        { stype: "初始", pic: 1.5, pe: 0, po: -2.5 },
        { stype: "延期", pic: 0, pe: -1.5, po: -2.5 },
        { stype: "有追踪", pic: "+0.5", pe: "+0.5", po: "+0.5" },
      ],
      scorecritical: [
        { stype: "初始", pic: 1.5, pe: 0, po: -2.5 },
        { stype: "有效质疑", pic: "0", pe: "+1.5", po: "+1" },
        { stype: "有效答疑", pic: "+0.5", pe: "0", po: "0" },
        { stype: "无效答疑", pic: "-0.5", pe: "0", po: "0" },
        { stype: "有效建议", pic: "0", pe: "+0.5", po: "+0.5" },
      ],

      // 一级分类
      task_select: "",
      task_select_option: [],
      // 二级分类
      task_sub_select: "",
      task_sub_select_option: [],
      task_sub_all_option: [],
      type: "项目",
      sub_type: "集团",
      person_id: "",
      person_option: [],
      copyperson_option: [],
      scatter_persontype_chart: "",
      scatter_persontype_chart_option: {
        xAxis: { min: -5, max: 5, name: "积极性" },
        yAxis: { min: -5, max: 5, name: "批判性" },
        legend: {
          left: "1%",
          top: "3%",
          orient: "vertical",
        },
        tooltip: {
          formatter: function (params) {
            return (
              params.seriesName +
              ": 积极性为" +
              params.data[0] +
              ",批判性为" +
              params.data[1]
            );
          },
        },
        series: [],
      },
    };
  },
  mounted: function () {
    this.scatter_persontype_chart = echarts.init(
      document.getElementById("scatter_persontype_chart_div"),
      "white",
      {
        renderer: "canvas",
      }
    );
    this.init();
  },
  methods: {
    freshscatter: function () {
      axios
        .post("/getscatterdata", {
          type: this.task_select,
          sub_type: this.task_sub_select,
          person_id: this.person_id,
        })
        .then((response) => {
          let temp_data = response.data.scatter_data;
          this.scatter_persontype_chart_option =
            this.$options.data().scatter_persontype_chart_option;
          this.scatter_persontype_chart.clear();
          if (JSON.stringify(temp_data) != "{}") {
            for (let i in temp_data) {
              let temp_option = {
                type: "scatter",
                symbolSize: 20,
                label: {
                  show: true,
                  position: "top",
                  formatter: function (params) {
                    return (
                      params.seriesName +
                      ":" +
                      params.data[0] +
                      ";" +
                      params.data[1]
                    );
                  },
                },
              };
              temp_option["name"] = temp_data[i]["name"];
              temp_option["data"] = temp_data[i]["datas"];
              this.scatter_persontype_chart_option.series.push(temp_option);
            }
          }
          this.scatter_persontype_chart.setOption(
            this.scatter_persontype_chart_option
          );
        });
      this.getperson_option();
    },
    initoption: function (event) {
      axios.get("/initoption").then((response) => {
        if (response.status == 200) {
          // console.log(response);
          this.task_sub_all_option = [];
          this.task_sub_all_option = response.data.task_sub_all_option;
          this.task_select_option = [];
          this.task_select_option = response.data.task_select_option;
          this.updatesuboption();
        }
      });
    },
    getperson_option: function () {
      axios.get("/getperson_option").then((response) => {
        // console.log(response);
        this.person_option = response.data;
        this.copyperson_option = Object.assign(this.person_option);
      });
    },
    personFilter: function (val) {
      if (val) {
        this.person_option = this.copyperson_option.filter((item) => {
          // 如果直接包含输入值直接返回true
          if (item.label) {
            if (item.label.toUpperCase().indexOf(val.toUpperCase()) != -1) {
              return true;
            }
            // 输入值拼音d
            return PinyinMatch.match(item.label, val);
          }
        });
      } else {
        this.person_option = this.copyperson_option;
      }
    },
    updatesuboption: function (event) {
      // console.log('update option');
      this.task_sub_select = "";
      if (this.task_select != "" && this.task_sub_all_option != []) {
        this.task_sub_select_option = [];
        let temp = this.task_sub_all_option[this.task_select];
        // console.log(temp);
        if (temp) {
          this.task_sub_select_option = [];
          for (let i in temp) {
            // console.log(temp[i]);
            this.task_sub_select_option.push({
              value: temp[i],
              label: temp[i],
            });
          }
        }
      }
    },
    init: function () {
      this.freshscatter();
      this.initoption();
      this.getperson_option();
    },
  },
};
</script>


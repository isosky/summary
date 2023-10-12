<template>
  <div id="app">
    <el-col :span="10">
      <el-row>
        <el-button type="primary" @click="getfundtable" icon="el-icon-refresh"
          >刷新
        </el-button>
        <el-button
          type="primary"
          @click="getfryfundtable"
          icon="el-icon-refresh"
          >只看鱼塘
        </el-button>
        <el-button type="primary" @click="getfundalldata" icon="el-icon-refresh"
          >查看所有
        </el-button>
        <el-select
          label="标题"
          :label-width="formLabelWidth"
          v-model="label_select"
          clearable
          filterable
          @change="updatelabeloption"
          default-first-option
          placeholder="请选择"
          style="width: 220px"
        >
          <el-option
            v-for="item in labeloption"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-row>
      <el-row>
        <el-table
          :data="
            fundnowdata.filter(
              (v) => v.fund_label.includes(label_select) || !label_select
            )
          "
          show-summary
          :summary-method="getSummaries"
          style="width: 100%"
          height="850"
          :cell-style="pricestyle"
          ref="fundnowdata"
          @row-click="changefundchart"
          :default-sort="{ prop: 'holding_return_rate', order: 'descending' }"
        >
          <el-table-column prop="fund_name" label="基金名称" width="220">
          </el-table-column>
          <el-table-column
            prop="holding_amount"
            sortable
            label="持有金额"
            width="100"
          >
          </el-table-column>
          <el-table-column prop="fund_label" label="行业" width="140">
          </el-table-column>
          <el-table-column
            prop="cumulative_profit"
            sortable
            label="累计收益"
            width="100"
          >
          </el-table-column>
          <el-table-column
            prop="holding_profit"
            sortable
            label="持有收益"
            width="100"
          >
          </el-table-column>
          <el-table-column
            prop="holding_return_rate"
            sortable
            label="收益率"
            width="100"
          >
          </el-table-column>
          <!-- <el-table-column prop="earn_total" label="累计收益">
              </el-table-column> -->
          <!-- <el-table-column prop="cost" label="持仓成本"> </el-table-column> -->
          <el-table-column label="操作" width="60">
            <template slot-scope="scope">
              <el-button
                @click="diashowreview(scope.row)"
                type="text"
                size="small"
                >复盘</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="14">
      <el-row>
        <div id="div_one_remain" style="height: 370px"></div>
      </el-row>
      <el-row :span="5">
        <el-button type="primary" @click="getfundnow" icon="el-icon-refresh"
          >实时
        </el-button>
        <!-- <el-button type="primary" @click="revertwatch" icon="el-icon-back">
            </el-button> -->
        <el-button type="primary" @click="shownewmarkline" icon="el-icon-view">
        </el-button>
        <el-input v-model="watch_label" style="width: 220px"></el-input>
        <!-- <el-button
              type="primary"
              @click="shownewmarkline"
              icon="el-icon-view"
              >屏蔽买卖
            </el-button>
            <el-button
              type="primary"
              @click="shownewmarkline"
              icon="el-icon-view"
              >移除线
            </el-button> -->
      </el-row>
      <el-row>
        <div id="div_one_total" style="height: 480px"></div>
      </el-row>
    </el-col>
    <el-dialog :visible.sync="dialogreviewFormVisible" width="30%">
      <el-form :model="reviewform">
        <el-row :span="5">
          <el-form-item label="基金代码" :label-width="formLabelWidth">
            <el-input
              v-model="reviewform.fund_name"
              disabled
              style="width: 450px"
            ></el-input>
          </el-form-item>
          <el-form-item label="复盘日期" :label-width="formLabelWidth">
            <el-date-picker
              v-model="reviewform.fund_review_time"
              value-format="yyyy-MM-dd"
              type="date"
              placeholder="选择日期"
              @change="get_fund_review(true)"
            >
            </el-date-picker>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="走势预期" :label-width="formLabelWidth">
            <el-slider
              :min="-10"
              :max="10"
              :step="2.5"
              show-input
              show-stops
              v-model="reviewform.fund_review_attitude"
              style="width: 450px"
            ></el-slider>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="操作想法" :label-width="formLabelWidth">
            <el-radio-group v-model="reviewform.operation" size="medium">
              <el-radio label="退场"></el-radio>
              <el-radio label="低吸"></el-radio>
              <el-radio label="观望"></el-radio>
              <el-radio label="加仓"></el-radio>
              <el-radio label="止盈"></el-radio>
            </el-radio-group>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="review" :label-width="formLabelWidth">
            <el-input
              type="textarea"
              v-model="reviewform.fund_review"
              :autosize="{ minRows: 5 }"
            ></el-input>
          </el-form-item>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogreviewFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="add_fund_review">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>
  
  
<script>
import axios from "axios";
var echarts = require("echarts");
export default {
  data() {
    return {
      formLabelWidth: "100px",
      label_select: "",
      labeloption: [],
      fundnowdata: [],
      watch_label: "",
      dialogreviewFormVisible: false,
      reviewform: {
        fund_code: "",
        fund_name: "",
        fund_review_time: "",
        fund_review_attitude: 0,
        fund_review: "",
        operation: "观望",
        fund_label: null,
      },
      fundnamesearch: "",
      title: "qqq",
      watch_list: [
        {
          name: "",
          lineStyle: { color: "black" },
          label: { formatter: "{b}" },
          coord: [],
        },
        {
          coord: [],
        },
      ],
      click_fund_code: "",
      click_fund_name: "",
      one_remain_option: {
        title: [
          {
            text: "",
            left: "10%",
          },
          {
            text: "",
            left: "60%",
          },
          {
            text: "",
            textAlign: "center",
            left: "23%",
            top: "15%",
            textStyle: {
              fontSize: 25,
            },
          },
          {
            text: "",
            textAlign: "center",
            left: "53%",
            top: "15%",
            textStyle: {
              fontSize: 25,
            },
          },
          {
            text: "",
            textAlign: "center",
            left: "83%",
            top: "15%",
            textStyle: {
              fontSize: 25,
            },
          },
        ],
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            crossStyle: {
              color: "#999",
            },
          },
        },
        xAxis: [
          {
            type: "category",
            data: [],
          },
        ],
        yAxis: [
          {
            type: "value",
            name: "份额",
            // splitNumber: 5,
            min: 0,
            max: "",
            interval: "",
          },
          {
            type: "value",
            name: "净值",
            // splitNumber: 5,
            min: "",
            max: "",
            interval: "",
          },
        ],
        series: [
          {
            name: "份额",
            type: "bar",
            data: [],
          },
          {
            name: "净值",
            type: "line",
            yAxisIndex: 1,
            data: [],
            markLine: {
              data: [
                {
                  label: { formatter: "{b},{c}" },
                  yAxis: "",
                  name: "Now",
                  lineStyle: {
                    color: "red",
                  },
                },
              ],
            },
          },
        ],
      },
      one_total_option: {
        title: {
          text: "",
          left: "10%",
        },
        legend: {
          left: "center",
          data: ["K", "MA5", "MA10", "MA20", "MA30"],
        },
        tooltip: {
          trigger: "axis",
        },
        xAxis: {
          type: "category",
          data: [],
        },
        yAxis: {
          type: "value",
          min: function (value) {
            return (value.min * 0.99).toFixed(4);
          },
        },
        dataZoom: [
          {
            show: true,
            startValue: "",
          },
          {
            type: "inside",
            show: true,
            startValue: "",
          },
        ],
        series: [
          {
            name: "K",
            data: [],
            type: "line",
            markLine: {
              label: { formatter: "{b},{c}" },
              lineStyle: { color: "red" },
              data: [],
            },
            markPoint: {
              data: "",
            },
          },
          {
            name: "MA5",
            type: "line",
            data: null,
            smooth: true,
            lineStyle: {
              opacity: 0.5,
            },
          },
          {
            name: "MA10",
            type: "line",
            data: null,
            smooth: true,
            lineStyle: {
              opacity: 0.5,
            },
          },
          {
            name: "MA20",
            type: "line",
            data: null,
            smooth: true,
            lineStyle: {
              opacity: 0.5,
            },
          },
          {
            name: "MA30",
            type: "line",
            data: null,
            smooth: true,
            lineStyle: {
              opacity: 0.5,
            },
          },
        ],
      },
      total_history_chart: "",
      one_remain_chart: "",
    };
  },
  mounted: function () {
    let that = this;
    this.init();
    this.one_remain_chart = echarts.init(
      document.getElementById("div_one_remain"),
      "white",
      {
        renderer: "canvas",
      }
    );
    this.one_remain_chart.on("click", function (params) {
      that.one_remain_option.title[1].text = params.name;
      that.one_remain_option.title[2].text =
        "盈利:" + that.one_remain_chart_datail[params.name]["res_earn"];
      that.one_remain_option.title[3].text =
        "份额:" + that.one_remain_chart_datail[params.name]["res_remain_share"];
      that.one_remain_option.title[4].text =
        that.one_remain_chart_datail[params.name]["res_earn_percent"];
      that.one_remain_chart.setOption(that.one_remain_option);
    });
    this.one_total_chart = echarts.init(
      document.getElementById("div_one_total"),
      "white",
      {
        renderer: "canvas",
      }
    );
    this.one_total_chart.on("click", function (params) {
      if (params.componentType != "series") {
        console.log("不是控制点");
        return;
      }
      // console.log(params);
      if (that.watch_click == 1) {
        that.watch_list[0]["coord"] = [];
        that.watch_list[0]["coord"].push(params.name);
        that.watch_list[0]["coord"].push(
          that.one_total_option.series[0].data[
            that.one_total_option.xAxis.data.indexOf(params.name)
          ][1]
        );
        that.watch_label = params.name;
        that.watch_click = 2;
      } else {
        that.watch_list[1]["coord"] = [];
        that.watch_list[1]["coord"].push(params.name);
        that.watch_list[1]["coord"].push(
          that.one_total_option.series[0].data[
            that.one_total_option.xAxis.data.indexOf(params.name)
          ][1]
        );
        that.watch_label = that.watch_label + "-----" + params.name;
        that.watch_list[0]["name"] = (
          ((that.watch_list[1]["coord"][1] - that.watch_list[0]["coord"][1]) /
            that.watch_list[1]["coord"][1]) *
          100
        ).toFixed(2);
        that.watch_click = 1;
      }
    });
  },
  methods: {
    init() {
      this.getfundtable();
    },
    getfundtable() {
      axios.get("/get_fund_total_data").then((response) => {
        this.fundnowdata = response.data.data;
        let temp_label = [];
        this.labeloption = [];
        this.fundnowdata.forEach((i) => {
          if (temp_label.indexOf(i.fund_label) == -1) {
            this.labeloption.push({ value: i.fund_label, label: i.fund_label });
            temp_label.push(i.fund_label);
          }
        });
        this.click_fund_code = this.fundnowdata[0].fund_code;
        this.click_fund_name = this.fundnowdata[0].fund_name;
        this.setoneremainchart();
        this.setonetotalchart();
      });
    },
    getfryfundtable() {
      axios.get("/getfryfundtable").then((response) => {
        this.fundnowdata = response.data.data;
        this.click_fund_code = this.fundnowdata[0].fund_code;
        this.click_fund_name = this.fundnowdata[0].fund_name;
        this.setoneremainchart();
        this.setonetotalchart();
      });
    },
    getfundalldata() {
      axios.get("/getfundalldata").then((response) => {
        this.fundnowdata = response.data.data;
        this.click_fund_code = this.fundnowdata[0].fund_code;
        this.click_fund_name = this.fundnowdata[0].fund_name;
        this.setoneremainchart();
        this.setonetotalchart();
      });
    },
    updatelabeloption() {
      // console.log(this.label_select);
      if (this.label_select != "") {
        this.fundnowdata.forEach((v) => {
          if (v.fund_label == this.label_select) {
            this.click_fund_code = v.fund_code;
            this.click_fund_name = v.fund_name;
            this.setoneremainchart();
            this.setonetotalchart();
            return;
          }
        });
      } else {
        this.click_fund_code = this.fundnowdata[0].fund_code;
        this.click_fund_name = this.fundnowdata[0].fund_name;
        this.setoneremainchart();
        this.setonetotalchart();
      }
    },
    getSummaries(param) {
      const { columns, data } = param;
      const sums = [];
      columns.forEach((column, index) => {
        if (index === 0) {
          sums[index] = "总价";
          return;
        }
        if (index === 2 || index === 6 || index === 7) {
          sums[index] = "";
          return;
        }
        if (index === 5) {
          sums[5] =
            Math.round((sums[4] / (sums[1] - sums[4])) * 10000) / 100 + "%";
          return;
        }
        const values = data.map((item) => Number(item[column.property]));
        if (!values.every((value) => isNaN(value))) {
          sums[index] = values.reduce((prev, curr) => {
            const value = Number(curr);
            if (!isNaN(value)) {
              return prev + curr;
            } else {
              return prev;
            }
          }, 0);
          sums[index] = sums[index].toFixed(2);
        }
      });
      return sums;
    },
    pricestyle({ row, column, rowIndex, columnIndex }) {
      // console.log(columnIndex);
      if (columnIndex > 1 && columnIndex < 5) {
        if (row[column.property] > 0) {
          return "color : Red";
        } else if (row[column.property] < 0) {
          return "color : Green";
        } else {
          return "color : Black";
        }
      }
      if (columnIndex == 5) {
        if (row.holding_return_rate > 0) {
          return "color : Red";
        } else if (row.holding_return_rate < 0) {
          return "color : Green";
        } else {
          return "color : Black";
        }
      }
    },
    changefundchart(row, event, column) {
      this.click_fund_code = row.fund_code;
      this.click_fund_name = row.fund_name;
      this.setoneremainchart();
      this.setonetotalchart();
    },
    setoneremainchart() {
      axios
        .post("/get_fund_remain_chart_data", {
          fund_code: this.click_fund_code,
        })
        .then((response) => {
          if (response.data == "404") {
            this.one_remain_chart.clear();
          } else {
            this.one_remain_option.xAxis[0].data = response.data.xaxis;
            this.one_remain_option.series[0].data = response.data.xaxisdata;
            this.one_remain_option.yAxis[0].max = response.data.xmax;
            this.one_remain_option.yAxis[0].interval = response.data.xinterval;
            this.one_remain_option.yAxis[1].min = response.data.ymin;
            this.one_remain_option.yAxis[1].max = response.data.ymax;
            this.one_remain_option.yAxis[1].interval = response.data.yinterval;
            this.one_remain_option.series[1].data = response.data.yaxisdata;
            this.one_remain_option.series[1].markLine.data[0].yAxis =
              response.data.ymarkline;
            this.one_remain_option.title[0].text =
              this.click_fund_name + "持仓情况";
            this.one_remain_option.title[1].text = "";
            this.one_remain_option.title[2].text = "";
            this.one_remain_option.title[3].text = "";
            this.one_remain_option.title[4].text = "";
            // console.log(this.one_remain_option);
            this.one_remain_chart_datail = response.data.details;
            this.one_remain_chart.setOption(this.one_remain_option);
          }
        });
    },
    setonetotalchart() {
      axios
        .post("/get_fund_total_chart_data", {
          fund_code: this.click_fund_code,
        })
        .then((response) => {
          this.one_total_option.xAxis.data = response.data.xAxisdata;
          this.one_total_option.series[0].data = response.data.seriesdata;
          this.one_total_option.title.text =
            this.click_fund_name + "近90天走势";
          this.one_total_option.title.subtext =
            "最新数据：" + response.data.maxdatatime;
          this.one_total_option.dataZoom[0].startValue =
            response.data.xaxisrange;
          this.one_total_option.dataZoom[1].startValue =
            response.data.xaxisrange;
          this.one_total_option.series[0].markPoint.data = response.data.mps;
          this.one_total_option.series[0].markLine.data = [];
          if (response.data.mkl.yAxis != null) {
            this.one_total_option.series[0].markLine.data.push(
              response.data.mkl
            );
          }
          // console.log(response);
          let k_data = response.data.seriesdata;
          this.one_total_option.series[1].data = this.calculateMA(5, k_data);
          this.one_total_option.series[2].data = this.calculateMA(10, k_data);
          this.one_total_option.series[3].data = this.calculateMA(20, k_data);
          this.one_total_option.series[4].data = this.calculateMA(30, k_data);
          // console.log(this.one_total_option);
          this.one_total_chart.setOption(this.one_total_option);
        });
    },
    getfundnow() {
      // console.log(this.click_fund_code);
      axios
        .post("/getfundnow", {
          click_fund_code: this.click_fund_code,
        })
        .then((response) => {
          // console.log(response.data);
          // 判断今天是否已经加过了
          if (
            this.one_total_option.xAxis.data.indexOf(response.data[0]) == -1
          ) {
            this.one_total_option.xAxis.data.push(response.data[0]);
            this.one_total_option.series[0].data.push(response.data);
          } else {
            this.one_total_option.series[0].data.pop();
            this.one_total_option.series[0].data.push(response.data);
          }

          let k_data = this.one_total_option.series[0].data;
          this.one_total_option.series[1].data = this.calculateMA(5, k_data);
          this.one_total_option.series[2].data = this.calculateMA(10, k_data);
          this.one_total_option.series[3].data = this.calculateMA(20, k_data);
          this.one_total_option.series[4].data = this.calculateMA(30, k_data);
          this.one_total_chart.setOption(this.one_total_option);
        });
    },
    shownewmarkline() {
      if (this.watch_list[0]["coord"][0] < this.watch_list[1]["coord"][0]) {
        this.one_total_option.series[0].markLine.data.push(this.watch_list);
        this.one_total_chart.setOption(this.one_total_option);
      }
    },
    diashowreview: function (event) {
      // console.log(event);
      let y = new Date().getFullYear() + "-";
      let m =
        new Date().getMonth() + 1 < 10
          ? "0" + (new Date().getMonth() + 1) + "-"
          : new Date().getMonth() + 1 + "-";
      let d =
        new Date().getDate() < 10
          ? "0" + new Date().getDate()
          : new Date().getDate();
      let currentDate = y + m + d;
      this.reviewform.fund_code = event.fund_code;
      this.reviewform.fund_name = event.fund_name;
      this.reviewform.fund_review_time = currentDate;
      this.get_fund_review(true);
      this.dialogreviewFormVisible = true;
    },
    add_fund_review: function () {
      // console.log(this.reviewform);
      axios
        .post("/add_fund_review", {
          reviewform: this.reviewform,
        })
        .then((response) => {
          this.reviewform = this.$options.data().reviewform;
          this.dialogreviewFormVisible = false;
        });
    },
    get_fund_review: function (event) {
      // console.log(event);
      axios
        .post("/get_fund_review", {
          reviewform: this.reviewform,
          oneday: event,
        })
        .then((response) => {
          // console.log(response);
          if (response.data.response_code == 200) {
            // console.log("aaaaaaaaaaaaa");
            this.reviewform.fund_review_attitude =
              response.data.res.fund_review_attitude;
            this.reviewform.fund_review = response.data.res.fund_review;
            this.reviewform.operation = response.data.res.operation;
          } else {
            this.reviewform.fund_review_attitude = 0;
            this.reviewform.fund_review = "";
            this.reviewform.operation = "观望";
          }
        });
    },
    calculateMA: function (dayCount, k_data) {
      var result = [];
      for (var i = 0, len = k_data.length; i < len; i++) {
        if (i < dayCount) {
          result.push("-");
          continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
          sum += k_data[i - j][1];
        }
        result.push(+(sum / dayCount).toFixed(3));
      }
      return result;
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
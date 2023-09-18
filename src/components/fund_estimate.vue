<template>
  <div id="app">
    <el-col :span="14"><el-row>
        <el-button type="primary" icon="el-icon-refresh" @click="get_fund_estimate_data">刷新
        </el-button>
        <el-button type="primary" icon="el-icon-refresh" @click="getestimatenow">获取净值
        </el-button>
      </el-row>
      <el-row>
        <el-table :data="estimatedata" style="width: 100%" :cell-style="estimatepricestyle" show-summary
          :summary-method="getestimateSummaries" @row-click="changeestimate" height="900"
          :default-sort="{ prop: 'net_change', order: 'descending' }">
          <el-table-column prop="fund_name" label="基金名称" width="220"></el-table-column>
          <el-table-column prop="fund_label" sortable label="行业" width="140"></el-table-column>
          <el-table-column prop="operation_label" sortable label="标签" width="80"></el-table-column>
          <el-table-column prop="holding_amount" sortable label="持有金额" width="100"></el-table-column>
          <el-table-column prop="holding_profit" sortable label="持收" width="100"></el-table-column>
          <el-table-column prop="holding_return_rate" sortable label="收益率" width="100"></el-table-column>
          <el-table-column prop="net_change" sortable label="预估" width="100"></el-table-column>
          <el-table-column prop="estimate_profit" sortable label="预估收益" width="100"></el-table-column>
          <el-table-column prop="net_value_time" label="预估时间" width="160"></el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="10">
      <el-row>
        <el-table :data="estimatebuydata" style="width: 100%" height="370" :default-sort="{ prop: 'trade_time' }">
          <el-table-column prop="trade_time" label="交易时间" width="220"></el-table-column>
          <el-table-column prop="order_amount" label="订单金额" width="220"></el-table-column>
          <el-table-column prop="remain_volume" label="份额" width="220"></el-table-column>
        </el-table>
      </el-row>
      <el-row>
        <div id="div_estimate_total" style="height: 480px"></div>
      </el-row>
    </el-col>
  </div>
</template>


<script>
import axios from "axios";
var echarts = require("echarts");
export default {
  data() {
    return {
      estimatedata: [],
      estimatebuydata: [],
      estimate_total_chart: "",
      estimate_total_option: {
        xAxis: {
          type: "category",
          data: [],
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            data: [],
            type: "line",
          },
        ],
      },
    };
  },
  mounted: function () {
    this.get_fund_estimate_data();
    this.estimate_total_chart = echarts.init(
      document.getElementById("div_estimate_total"),
      "white",
      {
        renderer: "canvas",
      }
    );
  },
  methods: {
    get_fund_estimate_data() {
      axios.get("/get_fund_estimate_data").then((response) => {
        this.estimatedata = response.data;
      });
    },
    getestimatenow: function () {
      axios.get("/collect_all_fund_net").then((response) => {
        console.log(response);
      });
    },
    estimatepricestyle: function ({ row, column, rowIndex, columnIndex }) {
      // console.log(columnIndex);
      if (columnIndex > 3 && columnIndex < 8) {
        if (row[column.property] > 0) {
          return "color : Red";
        } else if (row[column.property] < 0) {
          return "color : Green";
        } else {
          return "color : Black";
        }
      }
    },
    getestimateSummaries(param) {
      const { columns, data } = param;
      const sums = [];
      columns.forEach((column, index) => {
        if (index === 0) {
          sums[index] = "总价";
          return;
        }
        if (
          index === 1 ||
          index === 2 ||
          index === 5 ||
          index === 6 ||
          index === 8
        ) {
          sums[index] = "";
          return;
        }
        // if (index === 5) {
        //   sums[5] =
        //     Math.round((sums[4] / (sums[1] - sums[4])) * 10000) / 100 + "%";
        //   return;
        // }
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
    changeestimate: function (row, event, column) {
      this.click_estfund_code = row.fund_code;
      axios
        .post("/getestimatebuydata", { fund_code: this.click_estfund_code })
        .then((response) => {
          // console.log(response);
          this.estimatebuydata = response.data.data;
          this.estimate_total_option.xAxis.data = response.data.y;
          this.estimate_total_option.series[0].data = response.data.x;
          this.estimate_total_chart.setOption(this.estimate_total_option);
        });
    },
  },
};
</script>
<style>
.formlabelwidth {
  width: 120px;
}
</style>
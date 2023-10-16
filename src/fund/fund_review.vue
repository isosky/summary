<template>
  <div id="app">
    <el-col :span="10">
      <el-row :span="5">
        <el-col :span="5">
          <el-select
            v-model="fund_had_code_selected"
            @change="getcalendar"
            clearable
            filterable
            default-first-option
            placeholder="请选择基金"
          >
            <el-option
              v-for="item in fund_had_option"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option> </el-select></el-col
        ><el-col :span="4">
          <el-date-picker
            v-model="date_selected"
            type="month"
            value-format="yyyy-MM"
            @change="getcalendar"
            placeholder="选择月"
            style="width: 120px"
          >
          </el-date-picker
        ></el-col>
        <el-col :span="10">
          <el-button-group>
            <el-tooltip
              class="item"
              effect="dark"
              content="上个月"
              placement="bottom-end"
            >
              <el-button
                type="primary"
                @click="lastmonth"
                icon="el-icon-arrow-left"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="dark"
              content="下个月"
              placement="bottom-end"
            >
              <el-button
                type="primary"
                @click="nextmonth"
                icon="el-icon-arrow-right"
              ></el-button>
            </el-tooltip> </el-button-group
        ></el-col>
      </el-row>
      <el-row style="height: 450px">
        <el-col :span="6" v-show="showonefund == 1">
          <div>
            <el-statistic
              group-separator=","
              :precision="2"
              :value="sform.earn_history"
              style="
                height: 50px;
                margin-top: 30px;
                font-size: 30px;
                text-align: center;
              "
              title="历史收益"
            ></el-statistic>
            <el-statistic
              group-separator=","
              :precision="2"
              :value="sform.earn_sum"
              style="
                height: 50px;
                margin-top: 30px;
                font-size: 30px;
                text-align: center;
              "
              title="持有收益"
            ></el-statistic>
            <el-statistic
              group-separator=","
              :precision="2"
              :value="sform.earn_percent"
              style="
                height: 50px;
                margin-top: 30px;
                font-size: 30px;
                text-align: center;
              "
              title="持有收益率"
            ></el-statistic>
            <el-statistic
              title="基金行业"
              style="
                height: 50px;
                margin-top: 30px;
                font-size: 30px;
                text-align: center;
              "
            >
              <template slot="formatter">{{ sform.fund_label }}</template>
            </el-statistic>
          </div> </el-col
        ><el-col :span="18">
          <div id="calendar_div" style="height: 450px"></div>
        </el-col>
      </el-row>
      <el-row v-show="showonefund == 1">
        <div id="div_one_total" style="height: 450px"></div>
      </el-row>
    </el-col>
    <el-col :span="14">
      <el-row :span="5">
        <el-col :span="5">
          <el-select
            v-model="funder_selected"
            @change="filtertable"
            clearable
            filterable
            default-first-option
            placeholder="请选择作者"
          >
            <el-option
              v-for="item in funder_option"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option> </el-select
        ></el-col>
        <el-col :span="5">
          <el-select
            v-model="fund_label_selected"
            @change="filtertable"
            clearable
            filterable
            default-first-option
            placeholder="请选择行业"
          >
            <el-option
              v-for="item in fund_label_option"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option> </el-select></el-col
        ><el-button-group>
          <el-button type="primary" icon="el-icon-refresh"></el-button>
          <el-tooltip
            class="item"
            effect="dark"
            content="增加作者复盘"
            placement="bottom-end"
          >
            <el-button
              type="primary"
              icon="el-icon-plus"
              @click="showdialogfunderreview"
            ></el-button
          ></el-tooltip>
          <el-tooltip
            class="item"
            effect="dark"
            content="增加实盘"
            placement="bottom-end"
          >
            <el-button
              type="primary"
              icon="el-icon-coin"
            ></el-button></el-tooltip
        ></el-button-group>
      </el-row>
      <el-row>
        <el-table
          :data="reviewtabledata"
          style="width: 100%"
          height="700"
          :cell-style="pricestyle"
          ref="reviewtabledata"
        >
          <el-table-column
            prop="fund_label"
            label="行业"
            width="120"
          ></el-table-column>
          <el-table-column
            prop="fund_name"
            label="基金名称"
            sortable
            width="160"
          >
          </el-table-column>
          <el-table-column prop="funder_name" sortable label="作者" width="120">
          </el-table-column>
          <el-table-column
            prop="fund_review_attitude"
            label="走势预期"
            width="60"
          ></el-table-column>
          <el-table-column
            prop="operation"
            label="操作"
            width="60"
          ></el-table-column>
          <el-table-column
            prop="fund_review"
            label="总结"
            width="360"
          ></el-table-column>
          <el-table-column
            prop="isfirm"
            label="实盘"
            width="80"
            :formatter="isformat"
          >
          </el-table-column>

          <el-table-column
            prop="review_confidence"
            sortable
            label="可信度"
            width="100"
          >
          </el-table-column>
          <el-table-column label="操作" width="80">
            <template slot-scope="scope">
              <el-button
                @click="diashowreview(scope.row)"
                type="text"
                size="small"
                >修改</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-row>
      <!-- TODO 实盘怎么弄，待规划 -->
      <el-row v-if="false"
        ><el-header style="text-align: left; font-size: 20px"
          ><span>实盘</span></el-header
        >
        <el-table
          :data="reviewtabledata"
          style="width: 100%"
          height="400"
          :cell-style="pricestyle"
          ref="reviewtabledata"
        >
          <el-table-column
            prop="fund_label"
            label="行业"
            width="120"
          ></el-table-column>
          <el-table-column prop="apps" label="来源" width="80">
          </el-table-column>
          <el-table-column prop="funder_name" label="作者" width="120">
          </el-table-column>
          <el-table-column
            prop="fund_review_attitude"
            label="走势预期"
            width="60"
          ></el-table-column>
          <el-table-column
            prop="operation"
            label="操作"
            width="60"
          ></el-table-column>
          <el-table-column
            prop="fund_review"
            label="总结"
            width="300"
          ></el-table-column>
          <el-table-column prop="isfirm" label="实盘" width="80">
          </el-table-column>
          <el-table-column
            prop="earn_percent"
            sortable
            label="收益率"
            width="100"
          >
          </el-table-column>
          <el-table-column
            prop="review_confidence"
            sortable
            label="可信度"
            width="100"
          >
          </el-table-column>
          <el-table-column label="操作" width="80">
            <template slot-scope="scope">
              <el-button
                @click="diashowreview(scope.row)"
                type="text"
                size="small"
                >修改</el-button
              >
            </template>
          </el-table-column>
        </el-table>
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
          <el-form-item label="基金行业" :label-width="formLabelWidth">
            <el-input
              v-model="reviewform.fund_label"
              disabled
              style="width: 450px"
            ></el-input>
          </el-form-item>
          <el-form-item label="复盘日期" :label-width="formLabelWidth">
            <el-date-picker
              v-model="reviewform.fund_review_time"
              disabled
              value-format="yyyy-MM-dd"
              type="date"
              placeholder="选择日期"
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
        <el-button type="primary" @click="commitreview">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog :visible.sync="dialogfunderreviewFormVisible" width="50%">
      <el-form :model="funderreviewform">
        <el-row :span="5">
          <el-col :span="8">
            <el-form-item label="作者" :label-width="formLabelWidth">
              <el-input
                v-model="funderreviewform.funder_name"
                disabled
                style="width: 200px"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="复盘日期" :label-width="formLabelWidth">
              <el-date-picker
                v-model="funderreviewform.fund_review_time"
                value-format="yyyy-MM-dd"
                type="date"
                @change="getfunderreviewondday"
                placeholder="选择日期"
                style="width: 200px"
              >
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="基金行业" :label-width="formLabelWidth">
              <el-select
                v-model="funderreviewform.fund_label"
                clearable
                filterable
                allow-create
                default-first-option
                placeholder="请选择行业"
                style="width: 200px"
              >
                <el-option
                  v-for="item in fund_label_option"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :span="5">
          <el-col :span="12">
            <el-form-item label="走势预期" :label-width="formLabelWidth">
              <el-slider
                :min="-10"
                :max="10"
                :step="2.5"
                show-input
                show-stops
                v-model="temp_attitude"
                style="width: 350px"
              ></el-slider>
            </el-form-item>
          </el-col>
          <el-col :span="10">
            <el-form-item label="操作想法" :label-width="formLabelWidth">
              <el-radio-group v-model="temp_operation" size="mini">
                <el-radio-button label="退场"></el-radio-button>
                <el-radio-button label="低吸"></el-radio-button>
                <el-radio-button label="观望"></el-radio-button>
                <el-radio-button label="加仓"></el-radio-button>
                <el-radio-button label="止盈"></el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="2">
            <el-form-item>
              <el-button
                @click="addappendix"
                icon="el-icon-check"
                type="primary"
                size="mini"
              ></el-button>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :span="5">
          <el-form-item label="review" :label-width="formLabelWidth">
            <el-input
              type="textarea"
              v-model="temp_review"
              :autosize="{ minRows: 3 }"
            ></el-input>
          </el-form-item>
        </el-row>
        <el-row>
          <!-- <el-form-item label="结果表" :label-width="formLabelWidth"> -->
          <el-table
            :data="funderreviewform.funder_table"
            style="width: 90%; left: 5%; right: 5%"
          >
            <el-table-column prop="fund_label" label="行业"> </el-table-column>
            <el-table-column prop="fund_review_attitude" label="预期">
            </el-table-column>
            <el-table-column prop="operation" label="操作"> </el-table-column>
            <el-table-column prop="fund_review" label="review">
            </el-table-column>
            <el-table-column label="操作" width="170">
              <template slot-scope="dirscope">
                <el-button
                  @click="
                    ixdelete(dirscope.$index, funderreviewform.funder_table)
                  "
                  type="text"
                  size="small"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>
          <!-- </el-form-item> -->
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogfunderreviewFormVisible = false"
          >取 消</el-button
        >
        <el-button type="primary" @click="commitfunderreview">确 定</el-button>
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
      dialogreviewFormVisible: false,
      dialogfunderreviewFormVisible: false,
      reviewform: {},
      funderreviewform: {
        funder_id: null,
        funder_name: "",
        fund_review_time: "",
        fund_label: "",
        funder_table: [],
      },
      fund_label_option: [],
      showonefund: 1,
      showfirm: 0,
      temp_attitude: 0,
      temp_operation: "观望",
      temp_review: "",
      temp_funderreviewtable: [],
      reviewtabledata: [],
      orgreviewtabledata: [],
      fund_had_option: [],
      fund_had_list: "",
      fund_had_code_selected: "",
      fund_had_name_selected: "",
      funder_option: [],
      funder_option_list: [],
      funder_selected: "",
      fund_label_selected: "",
      date_selected: "",
      calendar_click: "",
      sform: {},
      calendar_chart: "",
      calendar_option: {
        tooltip: {
          formatter: function (params) {
            return "收益率: " + params.value[1].toFixed(2);
          },
        },
        // TODO 颜色这块还得研究研究
        visualMap: {
          show: false,
          splitNumber: 10,
          min: -5,
          max: 5,
          inRange: {
            color: [
              "#00ff16",
              "#5dff6b",
              "#8fff99",
              "#b3ffba",
              "#e0ffe3",
              "#ffffff",
              "#ffdfdf",
              "#ffb7b7",
              "#ffa9a9",
              "#ff9494",
              "#ff0000",
            ],
          },
          outOfRange: {
            color: ["green", "red"],
          },
        },
        calendar: {
          range: ["2023-03"],
          orient: "vertical",
          cellSize: [65, 65],
          seriesIndex: [2],
          yearLabel: {
            show: false,
          },
          dayLabel: {
            firstDay: 1, // 从周一开始
            show: false,
          },
          monthLabel: {
            show: false,
          },
        },
        series: [
          {
            type: "scatter",
            coordinateSystem: "calendar",
            symbolSize: 0,
            label: {
              show: true,
              formatter: function (params) {
                var d = echarts.number.parseDate(params.value[0]);
                return d.getDate() + "\n\n" + params.value[1] + "\n\n";
              },
              fontSize: 12,
              color: "#000",
            },
            data: [],
            silent: true,
          },
          {
            type: "scatter",
            coordinateSystem: "calendar",
            symbolSize: 0,
            label: {
              show: true,
              formatter: function (params) {
                return "\n\n\n" + (params.value[2] || "");
              },
              fontSize: 14,
              fontWeight: 700,
              color: "#a00",
            },
            data: [],
            silent: true,
          },
          {
            type: "heatmap",
            coordinateSystem: "calendar",
            data: [],
          },
        ],
      },
      one_total_chart: "",
      one_total_option: {
        title: {
          text: "",
          left: "10%",
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
        series: {
          data: [],
          type: "line",
          markLine: {
            label: { formatter: "{b},{c}" },
            data: "",
          },
          markPoint: {
            data: "",
          },
        },
      },
    };
  },
  mounted: function () {
    let that = this;
    this.calendar_chart = echarts.init(
      document.getElementById("calendar_div"),
      "white",
      {
        renderer: "canvas",
      }
    );
    this.calendar_chart.on("click", function (params) {
      that.calendar_click = params.data[0];
      that.getreviewtabledata();
    });
    this.one_total_chart = echarts.init(
      document.getElementById("div_one_total"),
      "white",
      {
        renderer: "canvas",
      }
    );
    this.init();
  },
  methods: {
    init: function () {
      //   console.log("temp");
      this.gethadfund();
      this.getfunder();
      this.getfundlabel();
    },
    getreviewtabledata: function () {
      if (this.calendar_click == "") {
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
        this.calendar_click = currentDate;
      }
      axios
        .post("/getreviewtabledata", {
          fund_code: this.fund_had_code_selected,
          fund_review_time: this.calendar_click,
        })
        .then((response) => {
          this.reviewtabledata = response.data;
          this.orgreviewtabledata = response.data;
        });
      return;
    },
    addappendix: function () {
      this.funderreviewform.funder_table.push({
        fund_label: this.funderreviewform.fund_label,
        fund_review_attitude: this.temp_attitude,
        operation: this.temp_operation,
        fund_review: this.temp_review,
      });
      this.funderreviewform.fund_label = null;
      this.temp_attitude = 0;
      this.temp_operation = "观望";
      this.temp_review = "";
    },
    getcalendar: function () {
      if (this.fund_had_code_selected != "" && this.date_selected != "") {
        // console.log("我的某个基金");
        this.showonefund = 1;
        axios
          .post("/getfundcalendar", {
            fund_code: this.fund_had_code_selected,
            mode: "fund",
          })
          .then((response) => {
            // console.log(response);
            this.calendar_option.series[0].data = response.data.bs_data;
            this.calendar_option.series[1].data = response.data.bs_data;
            this.calendar_option.series[2].data = response.data.data;
            this.calendar_option.calendar.range = this.date_selected;
            this.sform = response.data.sform;
            // console.log(this.calendar_option);
            this.calendar_chart.setOption(this.calendar_option);
            this.calendar_chart.resize();
          });
        this.setonetotalchart();
      }
      if (this.fund_had_code_selected == "" && this.date_selected != "") {
        this.showonefund = 0;
        // console.log("某个博主");
        axios
          .post("/getfundcalendar", {
            funder_selected: this.funder_selected,
            mode: "author",
          })
          .then((response) => {
            // console.log(response);
            this.calendar_option.series[0].data = response.data.bs_data;
            this.calendar_option.series[1].data = response.data.bs_data;
            this.calendar_option.series[2].data = response.data.data;
            this.calendar_option.calendar.range = this.date_selected;
            this.sform = response.data.sform;
            // console.log(this.calendar_option);
            this.calendar_chart.setOption(this.calendar_option);
            this.calendar_chart.resize();
          });
      }
    },
    gethadfund: function () {
      axios.get("/get_fund_info").then((response) => {
        this.fund_had_option = response.data.data;
        this.fund_had_list = response.data.listdata;
        this.fund_had_code_selected = this.fund_had_option[0]["value"];
        this.setonetotalchart();
        let y = new Date().getFullYear() + "-";
        let m =
          new Date().getMonth() + 1 < 10
            ? "0" + (new Date().getMonth() + 1)
            : new Date().getMonth() + 1;
        this.date_selected = y + m;
        this.getcalendar();
        this.getreviewtabledata();
      });
    },
    lastmonth: function () {
      let arr = this.date_selected.split("-");
      let year = arr[0]; //获取当前日期的年份
      let month = arr[1]; //获取当前日期的月份

      let year2 = year;
      let month2 = parseInt(month) - 1;
      if (month2 == 0) {
        //1月的上一月是前一年的12月
        year2 = parseInt(year2) - 1;
        month2 = 12;
      }

      if (month2 < 10) {
        //10月之前都需要补0
        month2 = "0" + month2;
      }
      let preMonth = year2 + "-" + month2;
      this.date_selected = preMonth;
      this.getcalendar();
    },
    nextmonth: function () {
      var arr = this.date_selected.split("-");
      let year = arr[0]; //获取当前日期的年份
      let month = arr[1]; //获取当前日期的月份

      let year2 = year;
      let month2 = parseInt(month) + 1;
      if (month2 == 13) {
        //12月的下月是下年的1月
        year2 = parseInt(year2) + 1;
        month2 = 1;
      }
      if (month2 < 10) {
        //10月之前都需要补0
        month2 = "0" + month2;
      }

      let nextMonth = year2 + "-" + month2;
      this.date_selected = nextMonth;
      this.getcalendar();
    },
    pricestyle: function ({ row, column, rowIndex, columnIndex }) {
      // console.log(columnIndex);
    },
    setonetotalchart: function () {
      axios
        .post("/get_fund_total_chart_data", {
          fund_code: this.fund_had_code_selected,
        })
        .then((response) => {
          this.one_total_option.xAxis.data = response.data.xAxisdata;
          this.one_total_option.series.data = response.data.seriesdata;
          this.fund_had_name_selected =
            this.fund_had_list[this.fund_had_code_selected];
          this.one_total_option.title.text =
            this.fund_had_name_selected + "近90天走势";
          this.one_total_option.dataZoom[0].startValue =
            response.data.xaxisrange;
          this.one_total_option.dataZoom[1].startValue =
            response.data.xaxisrange;
          this.one_total_option.series.markPoint.data = response.data.mps;
          this.one_total_option.series.markLine.data = response.data.mkl;
          this.one_total_chart.setOption(this.one_total_option);
        });
    },
    diashowreview: function (event) {
      // console.log(event);
      this.reviewform = event;
      this.dialogreviewFormVisible = true;
    },
    getfunder: function () {
      axios.get("/getfunder").then((response) => {
        this.funder_option_list = response.data.data_list;
        this.funder_option = response.data.data;
      });
    },
    getfundlabel: function () {
      axios.get("/getfundlabel").then((response) => {
        this.fund_label_option = response.data;
      });
    },
    showdialogfunderreview: function () {
      if (this.funder_selected == "") {
        this.$message.error("先选择一个作者");
        return;
      }
      this.funderreviewform.funder_name =
        this.funder_option_list[this.funder_selected];
      this.funderreviewform.funder_id = this.funder_selected;
      this.getfunderreview();
      this.dialogfunderreviewFormVisible = true;
    },
    ixdelete: function (index, rows) {
      // console.log(rows);
      rows.splice(index, 1);
    },
    commitreview: function () {
      // console.log(this.reviewform);
      axios
        .post("/add_fund_review", {
          reviewform: this.reviewform,
          isupdate: true,
        })
        .then((response) => {
          this.reviewform = this.$options.data().reviewform;
          this.dialogreviewFormVisible = false;
        });
    },
    commitfunderreview: function () {
      // console.log(this.funderreviewform);
      axios
        .post("/commitfunderreview", {
          funderreviewform: this.funderreviewform,
        })
        .then((response) => {
          this.funderreviewform = this.$options.data().funderreviewform;
          this.dialogfunderreviewFormVisible = false;
        });
    },
    getfunderreview: function () {
      // console.log(this.funderreviewform);
      axios
        .post("/getfunderreview", {
          funder_id: this.funderreviewform.funder_id,
        })
        .then((response) => {
          this.temp_funderreviewtable = response.data;
        });
    },
    getfirmdata: function () {
      // console.log(this.funder_selected);
      if (this.funder_selected == "") {
        this.showfirm = 0;
        // console.log("为空");
        return;
      }
      let funder_name = this.funder_option_list[this.funder_selected];
      if (funder_name.indexOf("实盘") != -1) {
        this.showfirm = 1;
      } else {
        this.showfirm = 0;
      }
    },
    filtertable: function () {
      // console.log(this.funder_selected);
      // console.log(this.fund_label_selected);
      if (this.funder_selected == "" && this.fund_label_selected == "") {
        this.getreviewtabledata();
        return;
      }
      // console.log("开始判断");
      let temp_list = this.orgreviewtabledata;
      this.reviewtabledata = [];
      for (var i in temp_list) {
        if (temp_list[i].funder_id == 1) {
          // console.log("我的");
          this.reviewtabledata.push(temp_list[i]);
          continue;
        }
        if (this.funder_selected != "" && this.fund_label_selected == "") {
          // console.log("开始判断作者");
          if (temp_list[i].funder_id == this.funder_selected) {
            this.reviewtabledata.push(temp_list[i]);
            continue;
          }
        }
        if (this.fund_label_selected != "" && this.funder_selected == "") {
          // console.log("开始行业");
          if (temp_list[i].fund_label == this.fund_label_selected) {
            this.reviewtabledata.push(temp_list[i]);
            continue;
          }
        }
        if (this.fund_label_selected != "" && this.funder_selected != "") {
          // console.log("开始判断作者和行业");
          if (
            temp_list[i].fund_label == this.fund_label_selected &&
            temp_list[i].funder_id == this.funder_selected
          ) {
            this.reviewtabledata.push(temp_list[i]);
            continue;
          }
        }
      }
    },
    getfunderreviewondday: function () {
      if (
        this.funderreviewform.fund_review_time in this.temp_funderreviewtable
      ) {
        this.funderreviewform.funder_table =
          this.temp_funderreviewtable[this.funderreviewform.fund_review_time];
      }
    },
    isformat: function (row, index) {
      if (row.isfirm == 1) {
        return "是";
      } else {
        return "否";
      }
    },
  },
};
</script>
  
  <style>
.el-row {
  margin-bottom: 5px;
}
.el-col {
  border-radius: 4px;
}
.formlabelwidth {
  width: 120px;
}
</style>
  
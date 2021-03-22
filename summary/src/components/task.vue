<template>
  <!-- TODO 重构界面 增加  4象限，然后展示4象限-->
  <div id="app">
    <el-row :gutter="5">
      <!-- 左侧面板 -->
      <el-col :span="11">
        <!-- 任务管理条 -->
        <el-col :span="21">
          <el-collapse v-model="activeName" accordion>
            <el-collapse-item name="1">
              <template slot="title">
                {{ title_now }}<i class="header-icon el-icon-info"></i>
              </template>
              <el-row :gutter="5">
                <el-select
                  @change="updatesuboption"
                  clearable
                  filterable
                  allow-create
                  default-first-option
                  v-model="task_select"
                  style="width: 95px"
                  placeholder="请选择"
                >
                  <el-option
                    v-for="item in task_select_option"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  ></el-option>
                </el-select>
                <el-select
                  v-model="task_sub_select"
                  filterable
                  clearable
                  allow-create
                  default-first-option
                  style="width: 95px"
                  placeholder="请选择"
                >
                  <el-option
                    v-for="item in task_sub_select_option"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  ></el-option>
                </el-select>
                <el-date-picker
                  :picker-options="{ firstDayOfWeek: 1 }"
                  v-model="new_edate"
                  value-format="yyyy-MM-dd"
                  type="date"
                  style="width: 150px"
                  placeholder="ddl"
                  @change="setdate"
                ></el-date-picker>
                <el-input
                  v-model="task_title"
                  style="width: 280px"
                  placeholder="请输入内容"
                ></el-input>
                <el-button
                  @click="addtask"
                  icon="el-icon-check"
                  circle
                  type="success"
                ></el-button>
              </el-row>
              <el-row :gutter="5">
                <el-select
                  v-model="person"
                  filterable
                  :filter-method="personFilter"
                  clearable
                  multiple
                  default-first-option
                  style="width: 200px"
                  placeholder="请选择相关人员"
                >
                  <el-option
                    v-for="item in person_option"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  ></el-option>
                </el-select>
                <el-date-picker
                  v-model="query_duration"
                  style="width: 275px"
                  type="daterange"
                  unlink-panels
                  value-format="yyyy-MM-dd"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  :picker-options="pickerOptions"
                  @change="setdate"
                >
                </el-date-picker>
                <el-checkbox v-model="isstime" @change="setdate"
                  >查添加日期
                </el-checkbox>
                <el-checkbox v-model="isqueryall">全查</el-checkbox>
                <el-button
                  @click="querytask('table')"
                  icon="el-icon-search"
                  type="success"
                  circle
                  style="margin: 0 5px 0 5px"
                ></el-button>
              </el-row>
            </el-collapse-item>
          </el-collapse>
        </el-col>
        <el-col
          :span="3"
          style="text-align: center; vertical-align: middle; line-height: 3"
        >
          <el-button
            @click="querytask_week"
            icon="el-icon-date"
            circle
            type="warning"
          ></el-button>
          <el-button
            @click="resetall"
            icon="el-icon-refresh"
            circle
            type="warning"
          ></el-button>
        </el-col>
        <div class="grid-content">
          <el-table
            :data="tableData"
            border
            height="750"
            :cell-style="isoverdate"
            style="width: 100%"
            :default-sort="{ prop: 'tetime', order: 'ascending' }"
            @cell-click="showprocess"
          >
            <el-table-column
              fixed
              prop="etime"
              sortable
              label="DDL"
              width="95"
            ></el-table-column>
            <el-table-column
              prop="type"
              label="分类"
              width="60"
            ></el-table-column>
            <el-table-column
              prop="sub_type"
              label="二级分类"
              width="80"
            ></el-table-column>
            <el-table-column prop="task_name" label="标题"></el-table-column>
            <el-table-column
              prop="num_person"
              label="人员"
              width="60"
            ></el-table-column>
            <el-table-column
              prop="num_process"
              label="进展"
              width="60"
            ></el-table-column>
            <el-table-column label="操作" width="170">
              <template slot-scope="scope">
                <el-button
                  @click="diashowprocess(scope.row)"
                  type="text"
                  size="small"
                  >更新</el-button
                >
                <el-button
                  @click="finishtask(scope.row)"
                  type="text"
                  size="small"
                  >完成</el-button
                >
                <el-button
                  @click="updatetask(scope.row)"
                  type="text"
                  size="small"
                  >修改</el-button
                >
                <el-button
                  @click="deletetask(scope.row)"
                  type="text"
                  size="small"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
      <!-- 右侧面板 -->
      <el-col :span="13">
        <el-row :gutter="5">
          <el-button
            @click="querytask_week"
            icon="el-icon-date"
            circle
            type="warning"
          ></el-button>
        </el-row>
        <el-row :gutter="5">
          <el-col :span="8">
            <div id="b_task" style="height: 220px"></div>
          </el-col>
          <el-col :span="8">
            <div id="task_pie_subject" style="height: 220px"></div>
          </el-col>
          <el-col :span="8">
            <div id="task_pie_summary" style="height: 220px"></div>
          </el-col>
        </el-row>
        <el-row :gutter="5">
          <el-tabs v-model="tabs_select" :lazy="true" type="border-card">
            <el-tab-pane name="summary" label="统计">
              <div id="task_summary" style="height: 455px"></div>
            </el-tab-pane>
            <el-tab-pane name="process" label="进展">
              <el-table
                :data="tableprocess"
                border
                height="455"
                style="width: 100%"
              >
                <el-table-column
                  prop="stime"
                  label="日期"
                  width="100"
                ></el-table-column>
                <el-table-column
                  prop="process_name"
                  label="内容"
                  width="400"
                ></el-table-column>
                <el-table-column
                  prop="isfinish"
                  label="状态"
                  width="100"
                ></el-table-column>
                <el-table-column label="操作" width="170">
                  <template slot-scope="scope">
                    <el-button
                      @click="showupdateprocess(scope.row)"
                      type="text"
                      size="small"
                      >修改</el-button
                    >
                    <el-button
                      v-if="scope.row.isfinish == '完成'"
                      @click="resetprocess(scope.row)"
                      type="text"
                      size="small"
                      >待做</el-button
                    >
                    <el-button
                      v-if="scope.row.isfinish == '待做'"
                      @click="finishprocess(scope.row)"
                      type="text"
                      size="small"
                      >完成</el-button
                    >
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane name="person" label="人员">
              <el-row :gutter="5">
                <el-select
                  v-model="person"
                  filterable
                  clearable
                  multiple
                  default-first-option
                  style="width: 400px"
                  placeholder="请选择相关人员"
                >
                  <el-option
                    v-for="item in person_option"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  ></el-option>
                </el-select>
                <el-button @click="appendtaskperson" type="success"
                  >追加人员</el-button
                >
              </el-row>
              <el-row :gutter="5">
                <el-table :data="persondata" style="width: 100%">
                  <el-table-column prop="company" label="单位" width="180">
                  </el-table-column>
                  <el-table-column prop="person_name" label="名称" width="180">
                  </el-table-column>
                  <el-table-column label="操作" width="170">
                    <template slot-scope="scope">
                      <el-button
                        @click="deletetaskperson(scope.row)"
                        type="text"
                        size="small"
                        >删除</el-button
                      >
                    </template>
                  </el-table-column>
                </el-table>
              </el-row>
            </el-tab-pane>
          </el-tabs>
        </el-row>
      </el-col>
    </el-row>
    <!-- 各种弹出框 -->
    <!-- 更新 -->
    <el-dialog
      @close="closedialog"
      title="提示"
      :visible.sync="dialogpVisible"
      width="30%"
    >
      <div>{{ v_task_content }}</div>
      <el-input
        v-model="input_process"
        type="textarea"
        style="width: 500px"
        :autosize="{ minRows: 5 }"
        placeholder="请输入进展"
      ></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogpVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogaddprocess">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 完成 -->
    <el-dialog
      @close="closedialog"
      title="提示"
      :visible.sync="dialogsVisible"
      width="30%"
    >
      <div>{{ v_task_content }}</div>
      <el-input
        v-model="input_finish"
        type="textarea"
        placeholder="请输入完成情况"
        style="width: 500px"
        :autosize="{ minRows: 5 }"
      ></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogsVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogcommit">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改 -->
    <el-dialog
      @close="closedialog"
      title="确认修改任务？？"
      :visible.sync="dialoguVisible"
      width="40%"
    >
      <el-date-picker
        :picker-options="{ firstDayOfWeek: 1 }"
        v-model="duetime"
        value-format="yyyy-MM-dd"
        type="date"
        style="width: 150px"
      ></el-date-picker>
      <!-- 修改任务面板里面的一级分类 -->
      <el-select
        @change="updatesuboption"
        clearable
        default-first-option
        v-model="task_select"
        style="width: 120px"
        placeholder="请选择"
      >
        <el-option
          v-for="item in task_select_option"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
      <!-- 修改任务面板里面的二级分类 -->
      <el-select
        v-model="task_sub_select"
        filterable
        clearable
        allow-create
        default-first-option
        style="width: 120px"
        placeholder="请选择"
      >
        <el-option
          v-for="item in task_sub_select_option"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
      <el-input v-model="dutitle" style="width: 300px"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialoguVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogupdate">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 删除 -->
    <el-dialog
      @close="closedialog"
      title="确认删除任务？？"
      :visible.sync="dialogcVisible"
      width="30%"
    >
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogcVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogdelete">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改process -->
    <el-dialog
      @close="closedialog"
      title="提示"
      :visible.sync="dialogprocessVisible"
      width="30%"
    >
      <div>{{ process_content }}</div>
      <el-input
        v-model="process_content"
        type="textarea"
        placeholder="请输入完成情况"
        style="width: 500px"
        :autosize="{ minRows: 5 }"
      ></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogprocessVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateprocess">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import PinyinMatch from "pinyin-match";
var echarts = require("echarts");
export default {
  data: function () {
    return {
      activeName: "",
      tabs_select: "summary",
      // v_step_date: "",
      // v_step_avg: "",
      //
      title_now: "任务管理（添加&查询）",
      // 日历表
      task_option: {
        grid: {
          left: "0",
          right: "0",
        },
        visualMap: {
          show: false,
          min: 0,
          max: 20,
          // orient: "vertical",
          inRange: {
            color: ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"],
          },
        },
        tooltip: {
          formatter: function (params) {
            return "完成任务数量: " + params.value[1];
          },
        },
        calendar: {
          range: ["2020-06", "2020-08"],
          orient: "vertical",
          left: 50,
          right: 10,
          top: 50,
          bottom: 10,
          yearLabel: {
            show: false,
          },
          dayLabel: {
            firstDay: 1, // 从周一开始
            nameMap: "cn",
          },
          monthLabel: {
            nameMap: "cn",
          },
        },
        series: {
          type: "heatmap",
          coordinateSystem: "calendar",
          label: {
            show: true,
            formatter: function (params) {
              var d = echarts.number.parseDate(params.value[0]);
              return d.getDate() + "\n" + params.value[1] + "个";
            },
            color: "#000",
          },
          data: [],
        },
      },
      // 统计柱形图
      task_summary_option: {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            // 坐标轴指示器，坐标轴触发有效
            type: "shadow", // 默认为直线，可选为：'line' | 'shadow'
          },
        },
        color: ["black", "red", "Orange", "green", "#939393"],
        legend: {
          data: ["逾期完成", "待做逾期", "待做", "正常完成", "作废"],
        },
        grid: {
          left: 110,
        },
        xAxis: {
          type: "value",
        },
        yAxis: {
          type: "category",
          data: [],
        },
        series: [
          {
            name: "逾期完成",
            type: "bar",
            stack: "总量",
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: function (num) {
                  if (num.value == 0) {
                    return "";
                  }
                },
              },
            },
            data: [],
          },
          {
            name: "待做逾期",
            type: "bar",
            stack: "总量",
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: function (num) {
                  if (num.value == 0) {
                    return "";
                  }
                },
              },
            },
            data: [],
          },
          {
            name: "待做",
            type: "bar",
            stack: "总量",
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: function (num) {
                  if (num.value == 0) {
                    return "";
                  }
                },
              },
            },
            data: [],
          },
          {
            name: "正常完成",
            type: "bar",
            stack: "总量",
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: function (num) {
                  if (num.value == 0) {
                    return "";
                  }
                },
              },
            },
            data: [],
          },
          {
            name: "作废",
            type: "bar",
            stack: "总量",
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: function (num) {
                  if (num.value == 0) {
                    return "";
                  }
                },
              },
            },
            data: [],
          },
        ],
      },
      // pie subject图
      tab_type_pie_option: {
        title: {
          text: "类型统计",
          x: "center",
        },
        color: [
          "#5470c6",
          "#91cc75",
          "#fac858",
          "#ee6666",
          "#73c0de",
          "#3ba272",
          "#fc8452",
          "#9a60b4",
          "#ea7ccc",
        ],
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        series: [
          {
            name: "任务情况",
            type: "pie",
            radius: ["45%", "60%"],
            center: ["50%", "60%"],
            data: [],
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: "{b}：{c}",
              },
            },
          },
          {
            name: "分类",
            type: "pie",
            label: {
              position: "inner",
            },
            radius: ["0%", "30%"],
            center: ["50%", "60%"],
            data: [],
          },
        ],
      },
      // pie summary图
      tab_summary_pie_option: {
        title: {
          text: "任务统计",
          x: "center",
        },
        color: ["black", "red", "Orange", "green", "#939393"],
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        series: [
          {
            name: "任务情况",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: [],
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: "{b}：{c}",
              },
            },
          },
        ],
      },
      // left input
      select_option: [
        {
          value: "step",
          label: "步数",
        },
        {
          value: "weight",
          label: "体重",
        },
      ],
      // right input
      task_select: "",
      new_edate: "",
      task_title: "",
      task_select_option: [],
      // 二级分类
      task_sub_select: "",
      task_sub_select_option: [],
      task_sub_all_option: [],

      // table
      tableData: [],
      tableprocess: [],

      //
      // new_edate: "",
      isstime: false,
      isqueryall: true,
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
      query_duration: null,

      //
      person: "",
      person_option: "",
      copyperson_option: "",

      // dialog process
      dialogpVisible: false,
      v_task_content: "",
      input_process: "",

      // dialog commit
      dialogsVisible: false,
      s_task_id: "",
      input_finish: "",

      // dialog update
      dialoguVisible: false,
      dutitle: "",
      duetime: "",
      dustatus: "",

      // dialog delete
      dialogcVisible: false,

      dialogprocessVisible: false,
      process_content: "",
      process_id: "",

      now_time: new Date().getTime(),
      task_chart: "",
      tasksummary_chart: "",
      tasktype_pie_chart: "",
      tasksummary_pie_chart: "",
      persondata: [],
    };
  },
  mounted: function () {
    // console.log(this);
    let now = new Date();
    let year = now.getFullYear(); //得到年份
    let month = now.getMonth() + 1; //得到月份
    let date = now.getDate(); //得到日期
    let day = now.getDay(); //得到周几
    let week;
    let arr_week = new Array(
      "星期日",
      "星期一",
      "星期二",
      "星期三",
      "星期四",
      "星期五",
      "星期六"
    );
    week = arr_week[day];
    let time_ts = "";
    time_ts =
      "当前时间：" + year + "年" + month + "月" + date + "日" + " " + week;
    // ****
    this.title_now = this.title_now + "  ||  " + time_ts;
    let that = this;
    // console.log('asdasdasda');
    // console.log(this.tableData);
    this.task_chart = echarts.init(document.getElementById("b_task"), "white", {
      renderer: "canvas",
    });
    this.task_chart.on("click", function (params) {
      // console.log(params["data"][0]);
      that.new_edate = params["data"][0];
      that.task_title = "";
      that.task_select = "";
      that.task_sub_select = "";
      that.isqueryall = true;
      that.querytask("table");
    });
    this.tasksummary_chart = echarts.init(
      document.getElementById("task_summary"),
      "white",
      {
        renderer: "canvas",
      }
    );
    this.tasksummary_chart.on("click", function (params) {
      // console.log(params["name"]);
      let temp = params["name"];
      // subject: this.task_select,
      // subsub: this.task_sub_select,
      that.task_select = temp.split("-")[0];
      that.task_sub_select = temp.split("-")[1];
      that.task_title = "";
      that.new_edate = "";
      // that.new_edate = params["data"][0];
      that.isqueryall = true;
      that.querytask("graph");
    });
    this.tasktype_pie_chart = echarts.init(
      document.getElementById("task_pie_subject"),
      "white",
      {
        renderer: "canvas",
      }
    );
    this.tasksummary_pie_chart = echarts.init(
      document.getElementById("task_pie_summary"),
      "white",
      {
        renderer: "canvas",
      }
    );
    this.freshright();
  },
  methods: {
    freshright: function (event) {
      this.initoption();
      this.setbar();
      this.task_title = "";
      this.task_select = "";
      this.task_sub_select = "";
      this.new_edate = "";
      this.isstime = false;
      this.query_duration = [];
      this.settasksummary_bar();
      this.isqueryall = false;
      this.querytask("table");
      this.getperson_option();
    },
    resetall: function () {
      this.task_title = "";
      this.freshright();
    },
    // 初始化分类的下拉列表
    initoption: function (event) {
      axios.get("/initoption").then((response) => {
        if (response.status == 200) {
          // console.log(response);
          this.task_sub_all_option = [];
          this.task_sub_all_option = response.data.task_sub_all_option;
          this.task_select_option = [];
          this.task_select_option = response.data.task_select_option;
          // console.log(this.task_sub_all_option);
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
    deletetaskperson: function (event) {
      axios
        .post("/deletetaskperson", {
          task_id: this.s_task_id,
          person_id: event.person_id,
        })
        .then((response) => {
          this.persondata = response.data;
        });
    },
    appendtaskperson: function () {
      axios
        .post("/appendtaskperson", {
          task_id: this.s_task_id,
          person_id: this.person,
        })
        .then((response) => {
          this.persondata = response.data;
          this.person = "";
        });
    },
    getperson_data: function (task_id) {
      axios
        .post("/getperson_data", {
          task_id: task_id,
        })
        .then((response) => {
          this.persondata = response.data;
        });
    },
    setdate: function (event) {
      if (
        this.isstime == false &&
        !(this.query_duration == null || this.query_duration == "")
      ) {
        this.new_edate = "";
      }
      if (
        this.isstime == false &&
        !(this.new_edate == null || this.new_edate == "")
      ) {
        this.query_duration = "";
      }
    },
    // 更新二级下拉列表
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
    setbar: function (event) {
      // console.log('setbar');
      axios.get("/gettimedata").then((response) => {
        // console.log(response.data.result);
        if (response.status == 200) {
          // console.log(response.data.result);
          this.task_option.series.data = response.data.result;
          this.task_option.calendar.range = response.data.range;

          // console.log(this.task_option);
          this.task_chart.setOption(this.task_option);
        }
      });
    },
    settasksummary_bar: function (event) {
      axios.get("/gettasksummary_bar").then((response) => {
        if (response.status == 200) {
          // 柱形图
          // console.log(response.data);
          this.task_summary_option.yAxis.data = response.data.yAxisdata;
          this.task_summary_option.series[0].data =
            response.data.yAxisoverdue_list;
          this.task_summary_option.series[1].data =
            response.data.yAxistodooverdue_list;
          this.task_summary_option.series[2].data =
            response.data.yAxistodo_list;
          this.task_summary_option.series[3].data =
            response.data.yAxisnormal_list;
          this.task_summary_option.series[4].data =
            response.data.yAxisabandon_list;
          this.tasksummary_chart.setOption(this.task_summary_option);
          // pie type图
          this.tab_type_pie_option.series[0].data = response.data.pie_type_data;
          this.tab_type_pie_option.series[1].data =
            response.data.pie_type_data_c;
          this.tasktype_pie_chart.setOption(this.tab_type_pie_option);

          // pie summary图
          this.tab_summary_pie_option.series[0].data =
            response.data.pie_summary_data;
          this.tab_summary_pie_option.title.text =
            "完成率:" +
            response.data.percent[0] +
            "%，逾期率:" +
            response.data.percent[1] +
            "%";
          this.tab_summary_pie_option.title.subtext =
            "总统计数:" + response.data.sum_task + "个";
          this.tasksummary_pie_chart.setOption(this.tab_summary_pie_option);
        }
      });
    },
    // 展示进展面板
    diashowprocess: function (event) {
      this.dialogpVisible = true;
      this.v_task_content = event.title;
      this.s_task_id = event.task_id;
    },

    // 调用进展接口
    dialogaddprocess: function (event) {
      // console.log(this.s_task_id);
      axios
        .post("/addprocess", {
          task_id: this.s_task_id,
          process_name: this.input_process,
        })
        .then((response) => {
          this.$message({
            message: "更新成功",
            type: "success",
          });
          this.input_process = "";
          this.dialogpVisible = false;
          this.showprocess();
          // TODO 是否可以做成局部刷新，只更新该任务的数据即可
          this.isqueryall = false;
          this.querytask("table");
        });
    },
    // 添加任务
    addtask: function (event) {
      if (this.new_edate != "" && this.task_title) {
        // console.log(this.person);
        axios
          .post("/addtask", {
            type: this.task_select,
            sub_type: this.task_sub_select,
            task_name: this.task_title,
            edate: this.new_edate,
            person: this.person,
          })
          .then((response) => {
            // console.log(response);
            this.task_title = "";
            this.new_edate = "";
            this.task_select = "";
            this.task_select = "";
            this.task_sub_select = "";
            this.person = "";
            this.freshright();
          });
      }
    },
    finishtask: function (event) {
      // console.log(event.task_id);
      this.dialogsVisible = true;
      this.s_task_id = event.task_id;
      this.v_task_content = event.title;
    },
    // 查询任务
    // TODO 是否查询已完成直接放到this的参数里面，query改成只有一个参数
    querytask: function (mode) {
      // console.log(this.query_duration);
      if (mode == "graph") {
        this.isqueryall = true;
      }
      axios
        .post("/querytask", {
          query: this.task_title,
          type: this.task_select,
          sub_type: this.task_sub_select,
          ftime: this.new_edate,
          query_duration: this.query_duration,
          isstime: this.isstime,
          isqueryall: this.isqueryall,
          mode: mode,
        })
        .then((response) => {
          // console.log(response.data);
          this.tableData = response.data.arrays;
        });
    },
    querytask_week: function () {
      axios.get("/querytask_week").then((response) => {
        if (response.status == 200) {
          this.tableData = response.data.arrays;
        }
      });
    },
    dialogcommit: function (event) {
      // console.log(this.s_task_id);
      this.dialogsVisible = false;
      axios
        .post("/finishtask", {
          task_id: this.s_task_id,
          input_finish: this.input_finish,
        })
        .then((response) => {
          // console.log(response);
          this.input_finish = "";
          this.freshright();
        });
    },

    // 展示修改任务面板
    updatetask: function (event) {
      this.dialoguVisible = true;
      // console.log(event);
      this.task_select = event.type;
      this.task_sub_select = event.sub_type;
      this.dutitle = event.task_name;
      this.s_task_id = event.task_id;
      this.duetime = event.tetime;
      this.dustatus = event.status;
    },

    // 调用修改任务接口
    dialogupdate: function (event) {
      // console.log(this.s_task_id);
      axios
        .post("/updatetask", {
          task_id: this.s_task_id,
          type: this.task_select,
          sub_type: this.task_sub_select,
          task_name: this.dutitle,
          etime: this.duetime,
          dustatus: this.dustatus,
        })
        .then((response) => {
          this.dialoguVisible = false;
          this.task_title = "";
          this.new_edate = "";
          this.task_select = "";
          this.task_select = "";
          this.task_sub_select = "";
          this.dustatus = "";
          this.freshright();
        });
    },
    removetask: function (event) {
      axios.get("/removetask").then((response) => {
        // console.log(response);
      });
    },
    deletetask: function (event) {
      // console.log(event.task_id);
      this.dialogcVisible = true;
      this.s_task_id = event.task_id;
    },

    dialogdelete: function (event) {
      // console.log(this.s_task_id);
      this.dialogcVisible = false;
      axios
        .post("/deletetask", {
          task_id: this.s_task_id,
        })
        .then((response) => {
          // console.log(response);
          this.freshright();
        });
    },
    // TODO 增加逾期的黑色显示
    isoverdate: function ({ row, column, rowIndex, columnIndex }) {
      if (columnIndex == 0) {
        // console.log(row);
        if (row.status == 1) {
          return "";
        }
        if (row.status == 3) {
          return "background-color:red;color:white";
        }
        if (row.status == 2) {
          return "background-color:green;color:white";
        }
        if (row.status == 4) {
          return "background-color:black;color:white";
        }
        if (row.status == 5) {
          return "background-color:'#939393'";
        }
      }
    },
    closedialog: function (event) {
      this.task_select = "";
      this.task_sub_select = "";
      this.process_content = "";
    },
    showprocess: function (row, column, cell, event) {
      // console.log(column, row.task_id);
      if (
        column !== undefined &&
        column.label != "进展" &&
        column.label != "人员"
      ) {
        this.tabs_select = "summary";
        return;
      }
      if (
        (column !== undefined && column.label == "进展") ||
        (column == undefined && this.s_task_id != "" && !this.dialogpVisible)
      ) {
        if (row !== undefined) {
          this.s_task_id = row.task_id;
        }
        this.tabs_select = "process";
        this.getprocess(this.s_task_id);
        return;
      }
      if (
        (column !== undefined && column.label == "人员") ||
        this.s_task_id != ""
      ) {
        if (row !== undefined) {
          this.s_task_id = row.task_id;
        }
        this.tabs_select = "person";
        this.getperson_data(this.s_task_id);
        return;
      }
    },
    getprocess: function (task_id) {
      axios
        .post("/getprocess", {
          task_id: task_id,
        })
        .then((response) => {
          this.tableprocess = response.data.arrays;
          for (let i in this.tableprocess) {
            if (this.tableprocess[i].isfinish == 1) {
              this.tableprocess[i].isfinish = "完成";
            } else {
              this.tableprocess[i].isfinish = "待做";
            }
          }
          for (var i in this.tableData) {
            // console.log(i);
            if (this.tableData[i].task_id == response.data.status.k) {
              this.tableData[i].num_process = response.data.status.num_process;
            }
          }
          this.s_task_id = "";
        });
    },
    resetprocess: function (event) {
      axios
        .post("/resetprocess", {
          process_id: event.process_id,
        })
        .then((response) => {
          if (response.status == 200) {
            this.$message({
              message: "禁用成功",
              type: "success",
            });
            // console.log(event);
            this.getprocess(event.task_id);
          }
        });
    },
    finishprocess: function (event) {
      axios
        .post("/finishprocess", {
          process_id: event.process_id,
        })
        .then((response) => {
          if (response.status == 200) {
            this.$message({
              message: "启用成功",
              type: "success",
            });
            this.getprocess(event.task_id);
          }
        });
    },
    showupdateprocess: function (event) {
      this.dialogprocessVisible = true;
      this.process_content = event.process_name;
      console.log(event);
      this.process_id = event.process_id;
      this.s_task_id = event.task_id;
    },
    updateprocess: function (event) {
      axios
        .post("/updateprocess", {
          process_id: this.process_id,
          process_name: this.process_content,
        })
        .then((response) => {
          if (response.status == 200) {
            this.$message({
              message: "启用成功",
              type: "success",
            });
            this.getprocess(this.s_task_id);
            this.s_task_id = "";
            this.dialogprocessVisible = false;
          }
        });
    },
  },
};
</script>

<style>
.el-row {
  margin-top: 5px;
  margin-bottom: 5px;

  /* &:last-child {
    margin-bottom: 0;
  } */
}

.el-col {
  border-radius: 4px;
}

.el-input {
  margin: 0 5px 0 5px;
}

.el-select {
  margin: 0 5px 0 5px;
}

.el-date-picker {
  margin: 0 5px 0 5px;
}

.el-date-editor {
  margin: 0 5px 0 5px;
}

.el-checkbox {
  margin: 0 5px 0 5px;
}

.el-switch {
  margin: 0 5px 0 5px;
}

.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #d3dce6;
}

.bg-purple-light {
  background: #e5e9f2;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

.item {
  margin-right: 40px;
}

#step_avg {
  font-size: 60px;
  text-align: center;
  line-height: 100px;
}
</style>

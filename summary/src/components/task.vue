<template>
  <!-- TODO 重构界面 增加  4象限，然后展示4象限-->
  <div id="app">
    <el-row :gutter="5">
      <!-- 左侧面板 -->
      <el-col :span="14">
        <!-- 任务管理条 -->
        <el-collapse v-model="activeName" accordion>
          <el-collapse-item title="任务管理（添加&查询）" name="1">
            <el-row :gutter="5">
              <el-select
                @change="updatesuboption"
                clearable
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
              <!-- <el-input v-model="task_sub_select" style="width: 100px" placeholder="二级分类"></el-input> -->
              <el-select
                v-model="task_sub_select"
                filterable
                clearable
                allow-create
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
              <el-date-picker
                :picker-options="{'firstDayOfWeek': 1}"
                v-model="new_edate"
                value-format="yyyy-MM-dd"
                type="date"
                style="width:150px"
                placeholder="ddl"
              ></el-date-picker>
              <el-input v-model="task_title" style="width: 300px" placeholder="请输入内容"></el-input>
              <el-button @click="addtask">提交</el-button>
              <el-button @click="resetall">重置</el-button>
            </el-row>
            <el-row :gutter="5">
              <el-date-picker
                :picker-options="{'firstDayOfWeek': 1}"
                v-model="querytimerange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                align="right"
              ></el-date-picker>
              <el-switch
                v-model="isqueryall"
                active-color="#13ce66"
                inactive-color="#ff4949"
                active-text="全部"
                inactive-text="待做"
              ></el-switch>
              <el-button @click="querytask">查询</el-button>
            </el-row>
          </el-collapse-item>
        </el-collapse>
        <div class="grid-content bg-purple">
          <el-table
            :data="tableData"
            border
            height="750"
            :cell-style="isoverdate"
            style="width: 100%"
            :default-sort="{prop: 'tetime'  ,order: 'ascending'}"
            @cell-click="showprocess"
          >
            <el-table-column fixed prop="etime" sortable label="DDL" width="95"></el-table-column>
            <el-table-column prop="subject" label="分类" width="60"></el-table-column>
            <el-table-column prop="subsub" label="二级分类" width="80"></el-table-column>
            <el-table-column prop="title" label="标题"></el-table-column>
            <el-table-column prop="num_process" label="进展" width="60"></el-table-column>
            <el-table-column label="操作" width="170">
              <template slot-scope="scope">
                <el-button @click="diashowprocess(scope.row)" type="text" size="small">更新</el-button>
                <el-button @click="finishtask(scope.row)" type="text" size="small">完成</el-button>
                <el-button @click="updatetask(scope.row)" type="text" size="small">修改</el-button>
                <el-button @click="deletetask(scope.row)" type="text" size="small">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
      <!-- 右侧面板 -->
      <el-col :span="10">
        <el-row :gutter="5">
          <el-col :span="12">
            <div id="b_task" style="height:220px"></div>
          </el-col>
          <el-col :span="12">
            <div id="task_pie_summary" style="height:220px"></div>
          </el-col>
        </el-row>
        <el-tabs v-model="tabs_select" :lazy="true" type="border-card">
          <el-tab-pane name="summary" label="统计">
            <div id="task_summary" style="height:500px"></div>
          </el-tab-pane>
          <el-tab-pane name="process" label="进展">
            <el-table :data="tableprocess" border height="500" style="width: 100%">
              <el-table-column prop="stime" label="日期" width="100"></el-table-column>
              <el-table-column prop="content" label="内容" width="400"></el-table-column>
              <el-table-column prop="isfinish" label="状态" width="100"></el-table-column>
              <el-table-column label="操作" width="170">
                <template slot-scope="scope">
                  <el-button @click="showupdateprocess(scope.row)" type="text" size="small">修改</el-button>
                  <el-button
                    v-if="scope.row.isfinish=='完成'"
                    @click="resetprocess(scope.row)"
                    type="text"
                    size="small"
                  >待做</el-button>
                  <el-button
                    v-if="scope.row.isfinish=='待做'"
                    @click="finishprocess(scope.row)"
                    type="text"
                    size="small"
                  >完成</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
    <!-- 各种弹出框 -->
    <!-- 更新 -->
    <el-dialog @close="closedialog" title="提示" :visible.sync="dialogpVisible" width="30%">
      <div>{{v_task_content}}</div>
      <el-input
        v-model="input_process"
        type="textarea"
        style="width: 500px"
        :autosize="{ minRows: 5}"
        placeholder="请输入进展"
      ></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogpVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogaddprocess">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 完成 -->
    <el-dialog @close="closedialog" title="提示" :visible.sync="dialogsVisible" width="30%">
      <div>{{v_task_content}}</div>
      <el-input
        v-model="input_finish"
        type="textarea"
        placeholder="请输入完成情况"
        style="width: 500px"
        :autosize="{ minRows: 5}"
      ></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogsVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogcommit">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改 -->
    <el-dialog @close="closedialog" title="确认修改任务？？" :visible.sync="dialoguVisible" width="40%">
      <el-date-picker
        :picker-options="{'firstDayOfWeek': 1}"
        v-model="duetime"
        value-format="yyyy-MM-dd"
        type="date"
        style="width:150px"
      ></el-date-picker>
      <!-- 修改任务面板里面的一级分类 -->
      <el-select
        @change="updatesuboption"
        clearable
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
    <el-dialog @close="closedialog" title="确认删除任务？？" :visible.sync="dialogcVisible" width="30%">
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogcVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogdelete">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改process -->
    <el-dialog @close="closedialog" title="提示" :visible.sync="dialogprocessVisible" width="30%">
      <div>{{process_content}}</div>
      <el-input
        v-model="process_content"
        type="textarea"
        placeholder="请输入完成情况"
        style="width: 500px"
        :autosize="{ minRows: 5}"
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
var echarts = require("echarts");
export default {
  data: function() {
    return {
      activeName: "",
      tabs_select: "summary",
      // v_step_date: "",
      // v_step_avg: "",
      // 日历表
      task_option: {
        tooltip: {},
        visualMap: {
          show: false,
          min: 0,
          max: 10,
          inRange: {
            color: ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"]
          }
        },
        calendar: {
          range: ["2020-06", "2020-08"],
          dayLabel: {
            firstDay: 1 // 从周一开始
          }
        },
        series: {
          type: "heatmap",
          coordinateSystem: "calendar",
          data: []
        }
      },
      // 统计柱形图
      task_summary_option: {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            // 坐标轴指示器，坐标轴触发有效
            type: "shadow" // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        color: ["black", "red", "Orange", "green"],
        legend: {
          data: ["逾期", "待做逾期", "待做", "正常完成"]
        },
        grid: {
          left: 80
        },
        xAxis: {
          type: "value"
        },
        yAxis: {
          type: "category",
          data: []
        },
        series: [
          {
            name: "逾期",
            type: "bar",
            stack: "总量",
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: function(num) {
                  if (num.value == 0) {
                    return "";
                  }
                }
              }
            },
            data: []
          },
          {
            name: "待做逾期",
            type: "bar",
            stack: "总量",
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: function(num) {
                  if (num.value == 0) {
                    return "";
                  }
                }
              }
            },
            data: []
          },
          {
            name: "待做",
            type: "bar",
            stack: "总量",
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: function(num) {
                  if (num.value == 0) {
                    return "";
                  }
                }
              }
            },
            data: []
          },
          {
            name: "正常完成",
            type: "bar",
            stack: "总量",
            label: {
              normal: {
                show: true,
                position: "insideRight",
                formatter: function(num) {
                  if (num.value == 0) {
                    return "";
                  }
                }
              }
            },
            data: []
          }
        ]
      },
      // pie图
      tab_pie_option: {
        title: {
          text: "任务统计",
          x: "center"
        },
        color: ["black", "red", "Orange", "green"],
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        // legend: {
        //     data: ['逾期', '待做', '正常完成']
        // },
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
                formatter: "{b}：{c}"
              }
            }
          }
        ]
      },
      // left input
      select_option: [
        {
          value: "step",
          label: "步数"
        },
        {
          value: "weight",
          label: "体重"
        }
      ],
      // right input
      task_select: "",
      new_edate: "",
      task_title: "",
      // TODO 从数据库获得
      task_select_option: [],
      // 二级分类
      task_sub_select: "",
      task_sub_select_option: [],
      task_sub_all_option: [],

      // table
      tableData: [],
      tableprocess: [],

      // 查询
      pickerOptions: {
        shortcuts: [
          {
            text: "本月",
            onClick(picker) {
              let now = new Date();
              let start = new Date(now.getFullYear(), now.getMonth());
              let end = "";
              // console.log(now.getMonth());
              if (now.getMonth() == "12") {
                end = new Date(now.getFullYear() + 1, 1);
                // console.log("ii", end);
              } else {
                end = new Date(now.getFullYear(), now.getMonth() + 1);
                // console.log("ee", end);
              }
              end.setTime(end.getTime() - 3600 * 1000 * 24 * 1);
              picker.$emit("pick", [start, end]);
            }
          }
        ]
      },
      querytimerange: "",
      isqueryall: true,

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

      // dialog delete
      dialogcVisible: false,

      dialogprocessVisible: false,
      process_content: "",
      process_id: "",

      now_time: new Date().getTime(),
      task_chart: "",
      tasksummary_chart: "",
      tasksummary_pie_chart: ""
    };
  },
  mounted: function() {
    console.log(this);
    // console.log('asdasdasda');
    // console.log(this.tableData);
    this.task_chart = echarts.init(document.getElementById("b_task"), "white", {
      renderer: "canvas"
    });
    this.tasksummary_chart = echarts.init(
      document.getElementById("task_summary"),
      "white",
      {
        renderer: "canvas"
      }
    );
    this.tasksummary_pie_chart = echarts.init(
      document.getElementById("task_pie_summary"),
      "white",
      {
        renderer: "canvas"
      }
    );
    this.freshright();
  },
  methods: {
    freshright: function(event) {
      this.initoption();
      this.setbar();
      this.settasksummary_bar();
      this.querytask(false);
    },
    resetall: function() {
      this.task_title = "";
      this.freshright();
    },
    // 初始化分类的下拉列表
    initoption: function(event) {
      axios.get("http://127.0.0.1:5000/initoption").then(response => {
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
    // 更新二级下拉列表
    updatesuboption: function(event) {
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
              label: temp[i]
            });
          }
        }
      }
    },
    setbar: function(event) {
      // console.log('setbar');
      axios.get("http://127.0.0.1:5000/gettimedata").then(response => {
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
    settasksummary_bar: function(event) {
      axios.get("http://127.0.0.1:5000/gettasksummary_bar").then(response => {
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
          this.tasksummary_chart.setOption(this.task_summary_option);

          // 饼图
          this.tab_pie_option.series[0].data = response.data.piedata;
          this.tab_pie_option.title.text =
            "完成率:" +
            response.data.percent[0] +
            "%，逾期率:" +
            response.data.percent[1] +
            "%";
          this.tab_pie_option.title.subtext =
            "总统计数:" + response.data.sum_task + "个";
          this.tasksummary_pie_chart.setOption(this.tab_pie_option);
        }
      });
    },
    // 展示进展面板
    diashowprocess: function(event) {
      this.dialogpVisible = true;
      this.v_task_content = event.title;
      this.s_task_id = event.task_id;
    },

    // 调用进展接口
    dialogaddprocess: function(event) {
      // console.log(this.s_task_id);
      axios
        .post("http://127.0.0.1:5000/addprocess", {
          task_id: this.s_task_id,
          content: this.input_process
        })
        .then(response => {
          this.$message({
            message: "更新成功",
            type: "success"
          });
          this.input_process = "";
          this.dialogpVisible = false;
          this.showprocess();
          // TODO 是否可以做成局部刷新，只更新该任务的数据即可
          this.querytask(false);
        });
    },
    // 添加任务
    addtask: function(event) {
      if (this.new_edate != "" && this.task_title) {
        axios
          .post("http://127.0.0.1:5000/addtask", {
            subject: this.task_select,
            subsub: this.task_sub_select,
            title: this.task_title,
            edate: this.new_edate
          })
          .then(response => {
            // console.log(response);
            this.task_title = "";
            this.new_edate = "";
            this.task_select = "";
            this.task_select = "";
            this.task_sub_select = "";
            this.freshright();
          });
      }
    },
    finishtask: function(event) {
      // console.log(event.task_id);
      this.dialogsVisible = true;
      this.s_task_id = event.task_id;
      this.v_task_content = event.title;
    },
    // 查询任务
    querytask: function(isquery) {
      let isqueryall;
      if (isquery == false) {
        isqueryall = false;
      } else {
        isqueryall = this.isqueryall;
      }

      axios
        .post("http://127.0.0.1:5000/querytask", {
          query: this.task_title,
          subject: this.task_select,
          subsub: this.task_sub_select,
          isqueryall: isqueryall
        })
        .then(response => {
          this.tableData = response.data.arrays;
        });
    },
    dialogcommit: function(event) {
      // console.log(this.s_task_id);
      this.dialogsVisible = false;
      axios
        .post("http://127.0.0.1:5000/finishtask", {
          task_id: this.s_task_id,
          input_finish: this.input_finish
        })
        .then(response => {
          // console.log(response);
          this.input_finish = "";
          this.freshright();
        });
    },

    // 展示修改任务面板
    updatetask: function(event) {
      this.dialoguVisible = true;
      // console.log(event);
      this.task_select = event.subject;
      this.task_sub_select = event.subsub;
      this.dutitle = event.title;
      this.s_task_id = event.task_id;
      this.duetime = event.tetime;
    },

    // 调用修改任务接口
    dialogupdate: function(event) {
      // console.log(this.s_task_id);
      axios
        .post("http://127.0.0.1:5000/updatetask", {
          task_id: this.s_task_id,
          subject: this.task_select,
          subsub: this.task_sub_select,
          title: this.dutitle,
          etime: this.duetime
        })
        .then(response => {
          this.dialoguVisible = false;
          this.task_title = "";
          this.new_edate = "";
          this.task_select = "";
          this.task_select = "";
          this.task_sub_select = "";
          this.freshright();
        });
    },
    removetask: function(event) {
      axios.get("http://127.0.0.1:5000/removetask").then(response => {
        // console.log(response);
      });
    },
    deletetask: function(event) {
      // console.log(event.task_id);
      this.dialogcVisible = true;
      this.s_task_id = event.task_id;
    },

    dialogdelete: function(event) {
      // console.log(this.s_task_id);
      this.dialogcVisible = false;
      axios
        .post("http://127.0.0.1:5000/deletetask", {
          task_id: this.s_task_id
        })
        .then(response => {
          // console.log(response);
          this.freshright();
        });
    },
    isoverdate: function({ row, column, rowIndex, columnIndex }) {
      if (columnIndex == 0) {
        let temp = new Date(row.tetime + " 23:59:59").getTime();
        // console.log(row);
        if (temp < this.now_time && row.isfinish == 0) {
          return "background-color:red;color:white";
        }
        if (row.isfinish == 1) {
          return "background-color:green;color:white";
        }
      }
    },
    closedialog: function(event) {
      this.task_select = "";
      this.task_sub_select = "";
      this.process_content = "";
    },
    showprocess: function(row, column, cell, event) {
      if (column !== undefined && column.label != "进展") {
        this.tabs_select = "summary";
        return;
      }
      if (
        (column !== undefined && column.label == "进展") ||
        (this.s_task_id != "" && !this.dialogpVisible)
      ) {
        if (row !== undefined) {
          this.s_task_id = row.task_id;
        }
        this.tabs_select = "process";
        this.getprocess(this.s_task_id);
      }
    },
    getprocess: function(task_id) {
      axios
        .post("http://127.0.0.1:5000/getprocess", {
          task_id: task_id
        })
        .then(response => {
          this.tableprocess = response.data.arrays;
          for (let i in this.tableprocess) {
            if (this.tableprocess[i].isfinish == 1) {
              this.tableprocess[i].isfinish = "完成";
            } else {
              this.tableprocess[i].isfinish = "待做";
            }
          }
          this.s_task_id = "";
        });
    },
    resetprocess: function(event) {
      axios
        .post("http://127.0.0.1:5000/resetprocess", {
          process_id: event.process_id
        })
        .then(response => {
          if (response.status == 200) {
            this.$message({
              message: "禁用成功",
              type: "success"
            });
            console.log(event);
            this.getprocess(event.task_id);
          }
        });
    },
    finishprocess: function(event) {
      axios
        .post("http://127.0.0.1:5000/finishprocess", {
          process_id: event.process_id
        })
        .then(response => {
          if (response.status == 200) {
            this.$message({
              message: "启用成功",
              type: "success"
            });
            this.getprocess(event.task_id);
          }
        });
    },
    showupdateprocess: function(event) {
      this.dialogprocessVisible = true;
      this.process_content = event.content;
      this.process_id = event.process_id;
      this.s_task_id = event.task_id;
    },
    updateprocess: function(event) {
      axios
        .post("http://127.0.0.1:5000/updateprocess", {
          process_id: this.process_id,
          content: this.process_content
        })
        .then(response => {
          if (response.status == 200) {
            this.$message({
              message: "启用成功",
              type: "success"
            });
            this.getprocess(this.s_task_id);
            this.s_task_id = "";
            this.dialogprocessVisible = false;
          }
        });
    }
  }
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

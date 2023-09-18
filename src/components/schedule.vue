<template>
  <div id="app">
    <el-col :span="14" class="grid-content bg-purple-light">
      <el-row>
        <el-collapse v-model="activeName" accordion>
          <el-collapse-item :title="lastchecktime" name="1">
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
              <el-select
                v-model="schedule_type"
                filterable
                clearable
                allow-create
                style="width: 120px"
                placeholder="请选择"
              >
                <el-option
                  v-for="item in schedule_type_option"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
              <el-input
                v-model="schedule_frequence"
                style="width: 300px"
                placeholder="请输入频率"
              ></el-input>
            </el-row>
            <el-row :gutter="5">
              <el-col :span="20">
                <el-input
                  v-model="schedule_content"
                  placeholder="请输入内容"
                ></el-input>
              </el-col>
              <el-col :span="2" :offset="1">
                <el-button @click="addschedule">提交</el-button>
              </el-col>
            </el-row>
          </el-collapse-item>
        </el-collapse>
      </el-row>
      <el-row>
        <!-- scheduledata -->
        <el-table
          :data="scheduledata"
          border
          height="750"
          style="width: 100%"
          @cell-click="showscheduleprocess"
        >
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
          <el-table-column prop="task_name" label="内容"></el-table-column>
          <el-table-column
            prop="schedule_type"
            label="类型"
            width="80"
          ></el-table-column>
          <el-table-column
            prop="schedule_frequence"
            label="频率"
            width="150"
          ></el-table-column>
          <el-table-column
            prop="lasttime"
            label="上次更新"
            width="100"
          ></el-table-column>
          <el-table-column
            prop="nexttime"
            label="下次执行"
            width="100"
          ></el-table-column>
          <el-table-column
            prop="isabandon"
            label="状态"
            width="60"
          ></el-table-column>
          <el-table-column label="操作" width="120">
            <template slot-scope="scope">
              <el-button
                @click="showupdateschedule(scope.row)"
                type="text"
                size="small"
                >修改</el-button
              >
              <el-button
                v-if="scope.row.isabandon == '启用'"
                @click="forbidschedule(scope.row)"
                type="text"
                size="small"
                >禁用</el-button
              >
              <el-button
                v-if="scope.row.isabandon == '禁用'"
                @click="startschedule(scope.row)"
                type="text"
                size="small"
                >启用</el-button
              >
              <el-button
                @click="deleteschedule(scope.row)"
                type="text"
                size="small"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="9" :offset="1" class="grid-content bg-purple-light">
      <el-table :data="scheduletaskdata" height="800" style="width: 100%">
        <el-table-column
          prop="task_name"
          label="内容"
          width="180"
        ></el-table-column>
        <el-table-column
          prop="task_id"
          label="任务号"
          width="70"
        ></el-table-column>
        <el-table-column
          prop="etime"
          label="执行时间"
          width="180"
        ></el-table-column>
        <el-table-column prop="addtime" label="添加时间"></el-table-column>
      </el-table>
    </el-col>
    <!-- 各种弹出框 -->
    <el-dialog title="修改计划任务" :visible.sync="modifysVisible" width="25%">
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
        <el-select
          v-model="schedule_type"
          filterable
          clearable
          allow-create
          style="width: 120px"
          placeholder="请选择"
        >
          <el-option
            v-for="item in schedule_type_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
        <el-input
          v-model="schedule_frequence"
          placeholder="请输入频率"
        ></el-input>
      </el-row>
      <el-input
        v-model="schedule_content"
        type="textarea"
        :autosize="{ minRows: 5 }"
        placeholder="请输入内容"
      ></el-input>
      <el-button @click="modifysVisible = false">取 消</el-button>
      <el-button type="primary" @click="modifyschedule">确 定</el-button>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      // 控制
      activeName: "",
      task_select: "",
      task_select_option: "",
      task_sub_select: "",
      task_sub_select_option: "",
      new_edate: "",
      schedule_frequence: "",
      schedule_content: "",
      lastchecktime: "",
      scheduleselect_id: "",

      // 弹出框
      modifysVisible: false,

      schedule_type: "",
      schedule_type_option: [
        {
          value: "week",
          label: "周任务",
        },
        {
          value: "month",
          label: "月任务",
        },
      ],

      // 左侧表格-计划任务
      scheduledata: [],
      // 右侧表格-计划任务添加记录
      scheduletaskdata: [],
    };
  },
  mounted: function () {
    // console.log('asdasdasda');
    // console.log(this.tableData);

    this.initall();
  },
  methods: {
    initall: function (event) {
      this.initoption();
      this.getscheduledata();
      this.getscheduletaskdata("");
    },
    initoption: function (event) {
      axios.get("/initoption").then((response) => {
        if (response.status == 200) {
          // console.log(response);
          this.task_sub_all_option = [];
          this.task_sub_all_option = response.data.task_sub_all_option;
          this.task_select_option = [];
          this.task_select_option = response.data.task_select_option;
          this.lastchecktime =
            "计划任务添加，上次自动检查时间为：" + response.data.lastchecktime;
          // console.log(this.task_sub_all_option);
          this.updatesuboption();
        }
      });
    },
    getscheduledata: function () {
      axios.get("/getscheduledata").then((response) => {
        if (response.status == 200) {
          // console.log(response.data);
          this.scheduledata = response.data.data;
          for (let i in this.scheduledata) {
            if (this.scheduledata[i].isabandon == 1) {
              this.scheduledata[i].isabandon = "禁用";
            } else {
              this.scheduledata[i].isabandon = "启用";
            }
          }
        }
      });
    },
    getscheduletaskdata: function (isquery) {
      axios
        .post("/getscheduletaskdata", {
          schedule_id: isquery,
        })
        .then((response) => {
          if (response.status == 200) {
            this.scheduletaskdata = response.data.data;
          }
        });
    },
    // TODO 应该有更优雅的方法，比如说计算函数
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
    addschedule: function (event) {
      axios
        .post("/addschedule", {
          type: this.task_select,
          sub_type: this.task_sub_select,
          schedule_type: this.schedule_type,
          schedule_frequence: this.schedule_frequence,
          task_name: this.schedule_content,
        })
        .then((response) => {
          if (response.status == 200) {
            this.initall();
          }
        });
    },
    showupdateschedule: function (event) {
      this.modifysVisible = true;
      this.task_select = event.type;
      this.task_sub_select = event.sub_type;
      this.schedule_type = event.schedule_type;
      this.schedule_frequence = event.schedule_frequence;
      this.schedule_content = event.task_name;
      this.scheduleselect_id = event.schedule_id;
    },
    modifyschedule: function (event) {
      axios
        .post("/modifyschedule", {
          schedule_id: this.scheduleselect_id,
          type: this.task_select,
          sub_type: this.task_sub_select,
          schedule_type: this.schedule_type,
          schedule_frequence: this.schedule_frequence,
          schedule_content: this.schedule_content,
        })
        .then((response) => {
          if (response.status == 200) {
            this.modifysVisible = false;
            this.$message({
              message: "修改成功",
              type: "success",
            });
            this.initall();
          }
        });
    },
    deleteschedule: function (event) {
      axios
        .post("/deleteschedule", {
          schedule_id: event.schedule_id,
        })
        .then((response) => {
          if (response.status == 200) {
            this.$message({
              message: "删除成功",
              type: "success",
            });
            this.initall();
          }
        });
    },
    forbidschedule: function (event) {
      axios
        .post("/forbidschedule", {
          schedule_id: event.schedule_id,
        })
        .then((response) => {
          if (response.status == 200) {
            this.$message({
              message: "禁用成功",
              type: "success",
            });
            this.initall();
          }
        });
    },
    startschedule: function (event) {
      axios
        .post("/startschedule", {
          schedule_id: event.schedule_id,
        })
        .then((response) => {
          if (response.status == 200) {
            this.$message({
              message: "启用成功",
              type: "success",
            });
            this.initall();
          }
        });
    },
    showscheduleprocess: function (row, column, cell, event) {},
  },
};
</script>

<style>
</style>
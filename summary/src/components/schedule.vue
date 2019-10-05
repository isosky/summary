<template>
  <div id="app">
    <el-col :span="11" class="grid-content bg-purple-light">
      <el-row>
        <el-collapse v-model="activeName" accordion>
          <el-collapse-item title="定期计划任务添加" name="1">
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
              <el-input v-model="schedule_frequence" style="width: 300px" placeholder="请输入频率"></el-input>
            </el-row>
            <el-row :gutter="5">
              <el-col :span="20">
                <el-input v-model="schedule_content" placeholder="请输入内容"></el-input>
              </el-col>
              <el-col :span="2" :offset="1">
                <el-button @click="addschedule">提交</el-button>
              </el-col>
            </el-row>
          </el-collapse-item>
        </el-collapse>
      </el-row>
      <el-row>
        <el-table :data="scheduledata" style="width: 100%">
          <el-table-column prop="date" label="日期" width="180"></el-table-column>
          <el-table-column prop="name" label="姓名" width="180"></el-table-column>
          <el-table-column prop="address" label="地址"></el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="11" :offset="1" class="grid-content bg-purple-light">
      <el-table :data="schedulehistorydata" style="width: 100%">
        <el-table-column prop="date" label="日期" width="180"></el-table-column>
        <el-table-column prop="name" label="姓名" width="180"></el-table-column>
        <el-table-column prop="address" label="地址"></el-table-column>
      </el-table>
    </el-col>
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

      schedule_type: "",
      schedule_type_option: [
        {
          value: "week",
          label: "周任务"
        },
        {
          value: "month",
          label: "月任务"
        }
      ],

      // 左侧表格-计划任务
      scheduledata: [],
      // 右侧表格-计划任务添加记录
      schedulehistorydata: []
    };
  },
  mounted: function() {
    // console.log('asdasdasda');
    // console.log(this.tableData);

    this.initall();
  },
  methods: {
    initall: function(event) {
      this.initoption();
    },
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
    // TODO 应该有更优雅的方法，比如说计算函数
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
    addschedule: function(event) {
      axios
        .post("http://127.0.0.1:5000/addschedule", {
          task_select: this.task_select,
          task_sub_select: this.task_sub_select,
          schedule_type: this.schedule_type,
          schedule_frequence: this.schedule_frequence,
          schedule_content: this.schedule_content
        })
        .then(response => {
          if (response.status == 200) {
            this.updatesuboption();
          }
        });
    }
  }
};
</script>

<style>
</style>
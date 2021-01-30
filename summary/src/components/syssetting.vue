<template>
  <div id="app">
    <el-row :span="6">
      <el-switch
        inactive-text="工作模式"
        v-model="iswork"
        active-color="#13ce66"
        inactive-color="#ff4949"
      ></el-switch>
      <el-button @click="setiswork">提交</el-button>
    </el-row>
    <el-row :span="6">
      <el-select v-model="firstpage" placeholder="请选择">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>
      <el-button @click="setfristpage">提交</el-button>
    </el-row>
    <el-row :span="6">
      <el-input
        v-model="subjectname"
        style="width: 200px"
        placeholder="请输入分类名称"
      ></el-input>
      <el-input
        v-model="subjectvalue"
        style="width: 200px"
        placeholder="请输入分类类型"
      ></el-input
      ><el-button @click="addsubject">添加分类</el-button></el-row
    >
    <el-row :span="6"
      ><el-table :data="subjectdata" style="width: 100%">
        <el-table-column prop="name" label="类型" width="180">
        </el-table-column>
        <el-table-column prop="value" label="数值" width="180">
        </el-table-column>
        <el-table-column label="操作" width="170">
          <template slot-scope="scope">
            <el-button
              @click="deletesubject(scope.row)"
              type="text"
              size="small"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      iswork: true,
      firstpage: "",
      // TODO 可以将这部分也放到数据库中
      options: [
        { value: "task", label: "task" },
        { value: "schedule", label: "schedule" },
        { value: "syssetting", label: "syssetting" },
      ],
      subjectdata: [],
      subjectname: "",
      subjectvalue: "",
    };
  },
  mounted: function () {
    this.getfirstpage();
    this.getiswork();
    this.getsubject();
  },
  methods: {
    getsubject: function () {
      axios.get("/getsubject").then((response) => {
        console.log(response);
        this.subjectdata = response.data;
      });
    },
    addsubject: function (event) {
      if (this.subjectname != "" && this.subjectvalue != "") {
        axios
          .post("/addsubject", {
            subjectname: this.subjectname,
            subjectvalue: this.subjectvalue,
          })
          .then((response) => {
            // console.log(response);
            this.subjectname = "";
            this.subjectvalue = "";
            this.getsubject();
          });
      }
    },
    deletesubject: function (event) {
      let temp = event.subjectid;
      // console.log(temp);
      axios
        .post("/deletesubject", {
          subjectid: temp,
        })
        .then((response) => {
          this.getsubject();
        });
    },
    getiswork: function () {
      axios.get("/getiswork").then((response) => {
        if (response.status == 200) {
          if (response.data.iswork == 1) {
            this.iswork = true;
          } else {
            this.iswork = false;
          }
        }
      });
    },
    setiswork: function () {
      console.log(this.iswork);
      axios
        .post("/setiswork", {
          iswork: this.iswork,
        })
        .then((response) => {
          this.getiswork();
        });
    },
    getfirstpage: function () {
      axios.get("/getfirstpage").then((response) => {
        if (response.status == 200) {
          this.firstpage = response.data.firstpage;
        }
      });
    },
    setfristpage: function () {
      axios
        .post("/setfirstpage", {
          firstpage: this.firstpage,
        })
        .then((response) => {
          this.getfirstpage();
        });
    },
  },
};
</script>

<style>
</style>
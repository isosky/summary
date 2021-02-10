<template>
  <div id="app">
    <el-col :span="12">
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
        ><el-button @click="addtype">添加分类</el-button></el-row
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
                @click="deletetype(scope.row)"
                type="text"
                size="small"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="12">
      <el-row :span="6">
        <el-select
          v-model="company"
          filterable
          allow-create
          default-first-option
          placeholder="请选择单位"
        >
          <el-option
            v-for="item in company_selector"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-input
          v-model="person_name"
          style="width: 200px"
          placeholder="请输入名称"
        ></el-input>
        <el-button @click="addperson">添加人员</el-button></el-row
      >
      </el-row>
      <el-row :span="6">
        <el-table :data="persondata"  height="800" style="width: 100%">
          <el-table-column prop="company" label="单位" width="180">
          </el-table-column>
          <el-table-column prop="person_name" label="名称" width="180">
          </el-table-column>
          <el-table-column label="操作" width="170">
            <template slot-scope="scope">
              <el-button
                @click="deleteperson(scope.row)"
                type="text"
                size="small"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-row></el-col
    >
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
      persondata: [],
      company_selector: [],
      company: "",
      person_name: "",
    };
  },
  mounted: function () {
    this.getfirstpage();
    this.getiswork();
    this.gettype();
    this.getcompany();
    this.getperson();
  },
  methods: {
    gettype: function () {
      axios.get("/gettype").then((response) => {
        // console.log(response);
        this.subjectdata = response.data;
      });
    },
    addtype: function (event) {
      if (this.subjectname != "" && this.subjectvalue != "") {
        axios
          .post("/addtype", {
            typename: this.subjectname,
            typevalue: this.subjectvalue,
          })
          .then((response) => {
            // console.log(response);
            this.subjectname = "";
            this.subjectvalue = "";
            this.gettype();
          });
      }
    },
    deletetype: function (event) {
      let temp = event.type_id;
      // console.log(temp);
      axios
        .post("/deletetype", {
          typeid: temp,
        })
        .then((response) => {
          this.gettype();
        });
    },
    // person
    getcompany: function () {
      axios.get("/getcompany").then((response) => {
        // console.log(response);
        this.company_selector = response.data;
      });
    },
    getperson: function () {
      axios.get("/getperson").then((response) => {
        // console.log(response);
        this.persondata = response.data;
      });
    },
    addperson: function (event) {
      if (this.company != "" && this.person_name != "") {
        axios
          .post("/addperson", {
            company: this.company,
            person_name: this.person_name,
          })
          .then((response) => {
            // console.log(response);
            this.company = "";
            this.person_name = "";
            this.getperson();
            this.getcompany();
          });
      }
    },
    deleteperson: function (event) {
      let temp = event.person_id;
      // console.log(temp);
      axios
        .post("/deleteperson", {
          personid: temp,
        })
        .then((response) => {
          this.getperson();
          this.getcompany();
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
      // console.log(this.iswork);
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
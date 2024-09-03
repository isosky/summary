<template>
  <div id="app">
    <el-col :span="5">
      <el-row :span="6">
        <el-select
          v-model="company"
          filterable
          allow-create
          default-first-option
          placeholder="请选择单位"
          style="width: 140px"
        >
          <el-option
            v-for="item in company_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-select
          v-model="department"
          filterable
          allow-create
          default-first-option
          placeholder="请选择部门"
          style="width: 140px"
        >
          <el-option
            v-for="item in department_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-select
          v-model="post"
          filterable
          allow-create
          default-first-option
          placeholder="请选择岗位"
          style="width: 140px"
        >
          <el-option
            v-for="item in post_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>

      </el-row>
      <el-row :span="6">
        <el-input
          v-model="person_name"
          style="width: 120px"
          placeholder="请输入姓名"
        ></el-input>
        <el-checkbox v-model="person_forceadd">强制添加 </el-checkbox>
        <el-button
          @click="addperson"
          icon="el-icon-check"
          type="success"
        ></el-button>
        <el-button
          @click="addperson"
          icon="el-icon-search"
          type="success"
        ></el-button>
      </el-row>
      <el-row :span="6">
        <!-- TODO 表格排序 -->
        <el-table :data="persondata" height="800" style="width: 100%">
          <el-table-column prop="company" label="单位" width="80">
          </el-table-column>
          <el-table-column prop="department" label="部门" width="80">
          </el-table-column>
          <el-table-column prop="post" label="职位" width="80">
          </el-table-column>
          <el-table-column prop="person_name" label="名称" width="120">
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template slot-scope="scope">
              <el-button
                @click="deleteperson(scope.row)"
                type="text"
                size="small"
                >编辑
              </el-button>
              <el-button
                @click="deleteperson(scope.row)"
                type="text"
                size="small"
                >删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="19"></el-col>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      persondata: [],
      person_name: "",
      company: "",
      company_option: [],
      department:"",
      department_option:"",
      post: "",
      post_option: [],
      person_forceadd: false,
    };
  },
  mounted: function () {
    this.getoptions();
    this.getperson();
  },
  methods: {
    // person
    getoptions: function () {
      axios.get("/getpersonoptions").then((response) => {
        // console.log(response);
        this.company_option = response.data.company_options;
        this.department_option = response.data.department_options;
        this.post_option = response.data.post_options;
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
            department: this.department,
            person_name: this.person_name,
            post: this.post,
            force: this.person_forceadd,
          })
          .then((response) => {
            if (response.data.msg == true) {
              this.company = "";
              this.department = "";
              this.person_name = "";
              this.post = "";
              this.getperson();
              this.getoptions();
            } else {
              this.$message.error("有重名的，请确认是否强制添加");
            }
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
          this.getoptions();
        });
    },
  },
};
</script>


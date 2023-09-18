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
            v-for="item in company_selector"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-input
          v-model="person_name"
          style="width: 120px"
          placeholder="请输入姓名"
        ></el-input>
        <el-button
          @click="addperson"
          icon="el-icon-check"
          circle
          type="success"
        ></el-button>
        <el-button
          @click="addperson"
          icon="el-icon-search"
          circle
          type="success"
        ></el-button>
      </el-row>
      <el-row :span="6">
        <el-select
          v-model="person_post"
          filterable
          allow-create
          default-first-option
          placeholder="请选择岗位"
          style="width: 140px"
        >
          <el-option
            v-for="item in person_post_selector"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-checkbox v-model="person_forceadd">强制添加 </el-checkbox>
      </el-row>
      <el-row :span="6">
        <el-table :data="persondata" height="800" style="width: 100%">
          <el-table-column prop="company" label="单位" width="80">
          </el-table-column>
          <el-table-column prop="person_name" label="名称" width="120">
          </el-table-column>
          <el-table-column prop="person_post" label="职位" width="80">
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
      company_selector: [],
      company: "",
      person_name: "",
      person_post: "",
      person_post_selector: [],
      person_forceadd: false,
    };
  },
  mounted: function () {
    this.getcompany();
    this.getperson();
  },
  methods: {
    // person
    getcompany: function () {
      axios.get("/getcompany").then((response) => {
        // console.log(response);
        this.company_selector = response.data.company_selector;
        this.person_post_selector = response.data.person_post_selector;
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
            person_post: this.person_post,
            force: this.person_forceadd,
          })
          .then((response) => {
            if (response.data.msg == true) {
              this.company = "";
              this.person_name = "";
              this.person_post = "";
              this.getperson();
              this.getcompany();
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
          this.getcompany();
        });
    },
  },
};
</script>


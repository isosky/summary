<template>
  <div id="app">
    <el-col :span="6">
      <el-row :span="6">
        <el-select @change="updatelevel2option" v-model="company" filterable allow-create default-first-option
          placeholder="请选择单位" style="width: 140px">
          <el-option v-for="item in company_option" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
        <el-select @change="updatelevel3option" v-model="department" filterable allow-create default-first-option
          placeholder="请选择部门" style="width: 140px">
          <el-option v-for="item in department_option" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
        <el-select v-model="post" filterable allow-create default-first-option placeholder="请选择岗位" style="width: 140px">
          <el-option v-for="item in post_option" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-row>
      <el-row :span="6">
        <el-input v-model="person_name" style="width: 120px" placeholder="请输入姓名"></el-input>
        <el-checkbox v-model="person_forceadd">强制添加 </el-checkbox>
        <el-button @click="addperson" icon="el-icon-check" type="success"></el-button>
        <el-button @click="addperson" icon="el-icon-search" type="success"></el-button>
        <el-button @click="closedialog" icon="el-icon-refresh" type="success"></el-button>
      </el-row>
      <el-row :span="6">
        <!-- TODO 表格排序 -->
        <el-table :data="persondata" border height="800" style="width: 100%" @cell-click="showpersondetail">
          <el-table-column prop="company" label="单位" width="100">
          </el-table-column>
          <el-table-column prop="department" label="部门" width="100">
          </el-table-column>
          <el-table-column prop="post" label="职位" width="100">
          </el-table-column>
          <el-table-column prop="person_name" label="名称" width="120">
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template slot-scope="scope">
              <el-button @click="showdialogperson(scope.row)" type="text" size="small">编辑
              </el-button>
              <el-button @click="deleteperson(scope.row)" type="text" size="small">删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="18">
      <el-row :span="6"></el-row>
      <el-row :span="6">
        <el-col :span="8">
          <el-row :span="6">
            <el-date-picker :picker-options="{ firstDayOfWeek: 1 }" v-model="person_profile_start"
              value-format="yyyy-MM-dd" type="date" placeholder="开始时间" @change="setdate"
              style="width: 140px"></el-date-picker>
            <el-date-picker :picker-options="{ firstDayOfWeek: 1 }" v-model="person_profile_end"
              value-format="yyyy-MM-dd" type="date" placeholder="结束时间" @change="setdate"
              style="width: 140px"></el-date-picker>
            <el-button @click="addpersonprofile" icon="el-icon-check" type="success"></el-button>
            <el-button @click="clearpersonprofile" icon="el-icon-refresh" type="success"></el-button>
          </el-row>
          <el-row :span="6">
            <el-select v-model="person_profile_company" filterable allow-create default-first-option placeholder="请选择单位"
              style="width: 140px">
              <el-option v-for="item in company_option" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-select v-model="person_profile_department" filterable allow-create default-first-option
              placeholder="请选择部门" style="width: 140px">
              <el-option v-for="item in department_option" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-select v-model="person_profile_post" filterable allow-create default-first-option placeholder="请选择岗位"
              style="width: 140px">
              <el-option v-for="item in post_option" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-row>
          <el-table :data="person_profile_data" border height="800" style="width: 100%">
            <el-table-column prop="start_date" label="开始时间" width="100">
            </el-table-column>
            <el-table-column prop="end_date" label="结束时间" width="100">
            </el-table-column>
            <el-table-column prop="company" label="公司" width="80">
            </el-table-column>
            <el-table-column prop="department" label="部门" width="80">
            </el-table-column>
            <el-table-column prop="post" label="职位" width="80">
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template slot-scope="scope">
                <el-button @click="updatepersonprofile(scope.row)" type="text" size="small">编辑
                </el-button>
                <el-button @click="deletepersonprofile(scope.row)" type="text" size="small">删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

        </el-col>
        <el-col :span="10">
          <!-- TODO 单元格颜色弄一下，然后醒目点 -->
          <el-table :data="person_task_data" border height="800" style="width: 100%" @cell-click="showpersonleveltask"
            :cell-style="persontaskdatastyle">
            <el-table-column prop="level2" label="level2" width="120">
            </el-table-column>
            <el-table-column prop="level3" label="level3" width="120">
            </el-table-column>
            <el-table-column prop="start_time" sortable label="开始时间" width="120">
            </el-table-column>
            <el-table-column prop="end_time" sortable label="结束时间" width="120">
            </el-table-column>
            <el-table-column prop="score_activity" sortable label="积极" width="80">
            </el-table-column>
            <el-table-column prop="score_critical" sortable label="批判" width="80">
            </el-table-column>
            <el-table-column prop="task_number" sortable label="数量" width="80">
            </el-table-column>
          </el-table>
        </el-col>
        <el-col :span="5">
          <el-table :data="person_record_data" border height="800" style="width: 100%">
            <el-table-column prop="company" label="单位" width="80">
            </el-table-column>
            <el-table-column prop="department" label="部门" width="80">
            </el-table-column>
            <el-table-column prop="post" label="职位" width="80">
            </el-table-column>
            <el-table-column prop="person_name" label="名称" width="120">
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </el-col>
    <el-dialog @close="dialogpersonVisible = false" title="添加人员" :visible="dialogpersonVisible" width="40%">
      <div>
        <el-row :span="6">
          <el-select v-model="company" filterable allow-create default-first-option placeholder="请选择单位"
            style="width: 140px">
            <el-option v-for="item in company_option" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
          <el-select v-model="department" filterable allow-create default-first-option placeholder="请选择部门"
            style="width: 140px">
            <el-option v-for="item in department_option" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
          <el-select v-model="post" filterable allow-create default-first-option placeholder="请选择岗位"
            style="width: 140px">
            <el-option v-for="item in post_option" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
          <el-input v-model="person_name" style="width: 120px" placeholder="请输入姓名"></el-input>
        </el-row>
      </div>

      <span slot="footer" class="dialog-footer">
        <el-button @click="updateperson">提交</el-button>
        <el-button @click="closedialog">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      persondata: [],
      person_id: "",
      person_name: "",
      company: "",
      company_option: [],
      company_department_options: [],
      department_post_options: [],
      department: "",
      department_option: [],
      post: "",
      post_option: [],
      person_forceadd: false,
      dialogpersonVisible: false,
      person_profile_id: '',
      person_profile_name: '',
      person_profile_start: '',
      person_profile_end: '',
      person_profile_company: '',
      person_profile_department: '',
      person_profile_post: '',
      person_profile_data: [],
      person_task_data: [],
      person_task_detail_data: [],
      person_record_data: [],
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
        this.company_department_options = response.data.company_department_options;
        this.department_post_options = response.data.department_post_options;
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
    // 展示修改任务面板
    showdialogperson: function (event) {
      this.dialogpersonVisible = true;
      // console.log(event);
      this.company = event.company;
      this.department = event.department;
      this.person_id = event.person_id;
      this.person_name = event.person_name;
      this.post = event.post;
    },
    closedialog: function () {
      this.company = '';
      this.department = '';
      this.person_id = '';
      this.person_name = '';
      this.post = '';
      this.dialogpersonVisible = false;
    },
    updateperson: function () {
      axios
        .post("/updateperson", {
          company: this.company,
          department: this.department,
          person_name: this.person_name,
          post: this.post,
          person_id: this.person_id
        })
        .then((response) => {
          if (response.data.msg == true) {
            this.company = '';
            this.department = '';
            this.person_id = '';
            this.person_name = '';
            this.post = '';
            this.dialogpersonVisible = false;
            this.getperson();
            this.getoptions();
          }
        });
    },
    showpersondetail: function (row, column, cell, event) {
      this.person_profile_id = row.person_id;
      this.person_profile_name = row.person_name;
      this.showpersonprofile();
      this.showpersontask();
    },
    showpersonprofile: function () {
      axios
        .post("/getpersonprofile", {
          person_profile_id: this.person_profile_id,
        })
        .then((response) => {
          this.person_profile_data = response.data
        });
    },
    showpersontask: function () {
      axios
        .post("/getpersontask", {
          person_profile_id: this.person_profile_id,
        })
        .then((response) => {
          this.person_task_data = response.data
        });
    },
    addpersonprofile: function () {
      axios
        .post("/addpersonprofile", {
          person_profile_start: this.person_profile_start,
          person_profile_end: this.person_profile_end,
          person_profile_company: this.person_profile_company,
          person_profile_department: this.person_profile_department,
          person_profile_post: this.person_profile_post,
          person_profile_id: this.person_profile_id,
          person_profile_name: this.person_profile_name
        })
        .then((response) => {
          if (response.data.msg == true) {
            this.clearpersonprofile()
          }
        });
    },
    clearpersonprofile: function () {
      this.person_profile_start = '';
      this.person_profile_end = '';
      this.person_profile_company = '';
      this.person_profile_department = '';
      this.person_profile_post = '';
    },
    updatepersonprofile: function (row, column, cell, event) { },
    deletepersonprofile: function (row, column, cell, event) { },
    showpersonleveltask: function (row, column, cell, event) {
      axios
        .post("/getpersonleveltask", {
          person_profile_id: this.person_profile_id,
          level2: row.level2,
          level3: row.level3
        })
        .then((response) => {
          // this.person_task_data = response.data
          // TODO 待实现
        });
    },
    persontaskdatastyle: function ({
      row,
      column,
      rowIndex,
      columnIndex
    }) {
      if (columnIndex == 4) {
        console.log(row, column, rowIndex, columnIndex);
        if (row.score_activity < 5) {
          return "background-color:red;color:white";
        }
        if (row.score_activity > 5) {
          return "background-color:green;color:white";
        }
        if (row.score_activity == 5) {
          return "";
        }
        return "";
      }
      if (columnIndex == 5) {
        console.log(row, column, rowIndex, columnIndex);
        if (row.score_critical < 5) {
          return "background-color:red;color:white";
        }
        if (row.score_critical > 5) {
          return "background-color:green;color:white";
        }
        if (row.score_critical == 5) {
          return "";
        }
        return "";
      }
    },
    updatelevel2option: function (event) {
      // console.log('update option');
      this.department = "";
      if (this.company != "" && this.department_option != []) {
        this.department_option = [];
        let temp = this.company_department_options[this.company];
        if (temp) {
          this.department_option = [];
          for (let i in temp) {
            this.department_option.push({
              value: temp[i],
              label: temp[i],
            });
          }
        }
      }
    },
    updatelevel3option: function (event) {
      // console.log('update option');
      this.post = "";
      if (this.department != "" && this.post_option != []) {
        this.post_option = [];
        let temp = this.department_post_options[this.department];
        if (temp) {
          this.post_option = [];
          for (let i in temp) {
            this.post_option.push({
              value: temp[i],
              label: temp[i],
            });
          }
        }
      }
    },
  },
};
</script>

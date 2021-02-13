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
          placeholder="请输入名称"
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
        <el-table :data="persondata" height="800" style="width: 100%">
          <el-table-column prop="company" label="单位" width="80">
          </el-table-column>
          <el-table-column prop="person_name" label="名称" width="80">
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

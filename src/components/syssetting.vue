<template>
  <div id="app">
    <el-col :span="6">
      <el-row :span="5">
        <el-col :span="12">
          <el-switch
            inactive-text="工作模式"
            v-model="iswork"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </el-col>
        <el-col :span="12">
          <el-button @click="setiswork">提交</el-button>
        </el-col>
      </el-row>
      <el-row :span="5">
        <el-col :span="12">
          <el-select v-model="firstpage" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
        <el-col :span="12">
          <el-button @click="setfristpage">提交</el-button>
        </el-col>
      </el-row>
      <el-row :span="6">
        <el-col :span="8">
          <el-input
            v-model="subjectname"
            style="width: 150px"
            placeholder="请输入分类名称"
          ></el-input>
        </el-col>
        <el-col :span="8">
          <el-input
            v-model="subjectvalue"
            style="width: 150px"
            placeholder="请输入分类类型"
          ></el-input
        ></el-col>
        <el-col :span="8">
          <el-button @click="addtype">添加分类</el-button></el-col
        ></el-row
      >

      <el-row :span="6"
        ><el-table :data="subjectdata" style="width: 100%">
          <el-table-column prop="name" label="类型" width="130">
          </el-table-column>
          <el-table-column prop="value" label="数值" width="130">
          </el-table-column>
          <el-table-column label="操作" width="170">
            <template slot-scope="scope">
              <el-button @click="deletetype(scope.row)" type="text" size="small"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-row>
      <el-row :span="6"
        ><el-table :data="nodirdata" style="width: 100%">
          <el-table-column prop="dir" label="类型" width="130">
          </el-table-column>
          <el-table-column prop="sub_dir" label="数值" width="130">
          </el-table-column>
          <el-table-column label="操作" width="170">
            <template slot-scope="scope">
              <el-button
                @click="showdirupdatepanel(scope.row)"
                type="text"
                size="small"
                >修改</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="6">
      <el-table :data="typedata" style="width: 100%" height="700">
        <el-table-column prop="type" label="大类" width="130">
        </el-table-column>
        <el-table-column prop="subtype" label="小类" width="130">
        </el-table-column>
        <el-table-column label="操作" width="170">
          <template slot-scope="scope">
            <el-button
              @click="showupdatepanel(scope.row)"
              type="text"
              size="small"
              >修改</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-col>
    <el-col :span="12">
      <el-row :span="5">
        <el-col :span="4">
          <el-input
            clearable
            v-model="city_name"
            style="width: 150px"
            placeholder="城市名称"
          ></el-input>
        </el-col>
        <el-col :span="4">
          <el-input
            clearable
            v-model="city_lon"
            style="width: 150px"
            placeholder="经度"
          ></el-input
        ></el-col>
        <el-col :span="4">
          <el-input
            clearable
            v-model="city_lat"
            style="width: 150px"
            placeholder="纬度"
          ></el-input>
        </el-col>
        <el-col :span="3">
          <el-button @click="addcity">添加城市</el-button></el-col
        >
        <el-col :span="3">
          <el-button @click="querycity">查询城市</el-button></el-col
        >
        <el-col :span="3"> <el-button @click="getcity">重置</el-button></el-col>
      </el-row>
      <el-row :span="5">
        <el-table :data="citydata" style="width: 100%" height="700">
          <el-table-column prop="city" label="城市名称" width="130">
          </el-table-column>
          <el-table-column prop="lon" label="经度" width="130">
          </el-table-column>
          <el-table-column prop="lat" label="纬度" width="130">
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-dialog
      @close="dialogpVisible = false"
      title="提示"
      :visible.sync="dialogpVisible"
      width="30%"
    >
      <el-input
        v-model="new_sub_type"
        style="width: 200px"
        placeholder="请输入新类型"
      ></el-input>

      <el-button type="primary" @click="commitnewsubtype">确 定</el-button>
    </el-dialog>
    <el-dialog
      @close="dialogdirVisible = false"
      title="提示"
      :visible.sync="dialogdirVisible"
      width="30%"
    >
      <!-- <el-input
        v-model="new_dir_type"
        style="width: 200px"
        placeholder="请输入新方向"
      ></el-input> -->
      <el-select v-model="new_dir_type" placeholder="请选择">
        <el-option
          v-for="item in diroptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
      <el-button type="primary" @click="commitnewdirtype">确 定</el-button>
    </el-dialog>
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
        { value: "fund", label: "fund" },
        { value: "schedule", label: "schedule" },
        { value: "person", label: "person" },
        { value: "count", label: "count" },
        { value: "syssetting", label: "syssetting" },
      ],
      diroptions: [
        {
          value: "领域",
          label: "领域",
        },
        {
          value: "技术",
          label: "技术",
        },
        {
          value: "技能",
          label: "技能",
        },
        {
          value: "行业",
          label: "行业",
        },
      ],
      subjectdata: [],
      nodirdata: [],
      typedata: [],
      subjectname: "",
      subjectvalue: "",
      dialogpVisible: false,
      dialogdirVisible: false,
      sub_dir: "",
      new_dir_type: "",
      old_sub_type: "",
      new_sub_type: "",
      typenow: "",
      city_name: "",
      city_lon: "",
      city_lat: "",
      citydata: [],
    };
  },
  mounted: function () {
    this.getfirstpage();
    this.getiswork();
    this.gettype();
    this.getsubtype();
    this.getcity();
    this.getnodirdata();
  },
  methods: {
    getnodirdata: function () {
      axios.get("/getnodirdata").then((response) => {
        this.nodirdata = response.data;
      });
    },
    gettype: function () {
      axios.get("/gettype").then((response) => {
        // console.log(response);
        this.subjectdata = response.data;
      });
    },
    getsubtype: function () {
      axios.get("/getsubtype").then((response) => {
        // console.log(response);
        this.typedata = response.data;
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
    showdirupdatepanel: function (event) {
      this.sub_dir = event.sub_dir;
      this.dialogdirVisible = true;
    },
    showupdatepanel: function (event) {
      this.typenow = event.type;
      this.old_sub_type = event.subtype;
      this.dialogpVisible = true;
    },
    commitnewdirtype: function (event) {
      if (this.new_dir_type == "") {
        this.$message.error("新方向不能为空");
      } else {
        axios
          .post("/updatedir", {
            sub_dir: this.sub_dir,
            new_dir_type: this.new_dir_type,
          })
          .then((response) => {
            this.dialogdirVisible = false;
            this.new_dir_type = "";
            this.sub_dir = "";
            this.getnodirdata();
          });
      }
    },
    commitnewsubtype: function (event) {
      if (this.new_sub_type == "") {
        this.$message.error("新类型不能为空");
      } else {
        // TODO tupe改为type
        axios
          .post("/updatesubtupe", {
            typenow: this.typenow,
            old_sub_type: this.old_sub_type,
            new_sub_type: this.new_sub_type,
          })
          .then((response) => {
            this.dialogpVisible = false;
            this.typenow = "";
            this.old_sub_type = "";
            this.new_sub_type = "";
            this.getsubtype();
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
    getcity: function () {
      axios.get("/getcitydata").then((response) => {
        // console.log(response);
        this.citydata = response.data;
      });
    },
    addcity: function () {
      axios
        .post("/addcity", {
          city_name: this.city_name,
          city_lon: this.city_lon,
          city_lat: this.city_lat,
        })
        .then((response) => {
          // console.log(response);
          if (response.data != true) {
            this.$message.error(response.data);
          } else {
            this.city_name = "";
            this.city_lon = "";
            this.city_lat = "";
            this.getcity();
          }
        });
    },
    querycity: function () {
      axios
        .post("/querycity", {
          city_name: this.city_name,
          city_lon: this.city_lon,
          city_lat: this.city_lat,
        })
        .then((response) => {
          this.citydata = response.data;
        });
    },
  },
};
</script>

<style>
.el-row {
  margin-bottom: 5px;
}
.el-col {
  border-radius: 4px;
}
</style>
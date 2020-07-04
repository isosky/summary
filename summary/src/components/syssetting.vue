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
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      iswork: true,
      firstpage: "",
      options: [
        { value: "task", label: "task" },
        { value: "yysyh", label: "yysyh" },
        { value: "schedule", label: "schedule" },
        { value: "syssetting", label: "syssetting" }
      ]
    };
  },
  mounted: function() {
    this.getfirstpage();
    this.getiswork();
  },
  methods: {
    getiswork: function() {
      axios.get("http://127.0.0.1:5000/getiswork").then(response => {
        if (response.status == 200) {
          if (response.data.iswork == 1) {
            this.iswork = true;
          } else {
            this.iswork = false;
          }
        }
      });
    },
    setiswork: function() {
      console.log(this.iswork);
      axios
        .post("http://127.0.0.1:5000/setiswork", {
          iswork: this.iswork
        })
        .then(response => {
          this.getiswork();
        });
    },
    getfirstpage: function() {
      axios.get("http://127.0.0.1:5000/getfirstpage").then(response => {
        if (response.status == 200) {
          this.firstpage = response.data.firstpage;
        }
      });
    },
    setfristpage: function() {
      axios
        .post("http://127.0.0.1:5000/setfirstpage", {
          firstpage: this.firstpage
        })
        .then(response => {
          this.getfirstpage();
        });
    }
  }
};
</script>

<style>
</style>
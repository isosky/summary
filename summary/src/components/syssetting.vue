<template>
  <div id="app">
    <el-switch v-model="iswork" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
    <el-button @click="setiswork">提交</el-button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      iswork: true
    };
  },
  mounted: function() {
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
    }
  }
};
</script>

<style>
</style>
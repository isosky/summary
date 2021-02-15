<template>
  <div id="app">
    <el-col :span="6">
      <el-col :span="8" v-for="t in mdata" :key="t.k">
        <el-card class="box-card">
          <div class="text item" @click="ttt(t)">
            {{ t.v }}
          </div>
        </el-card>
      </el-col>
    </el-col>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      mdata: "",
    };
  },
  mounted: function () {
    this.init();
  },
  methods: {
    init: function () {
      axios.get("/gettotalmonth").then((response) => {
        if (response.status == 200) {
          console.log(response);
          this.mdata = response.data;
        }
      });
    },

    ttt: function (event) {
      console.log(event.v);
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

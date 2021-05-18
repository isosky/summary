<template>
  <div id="app">
    <el-col :span="10">
      <el-table :data="funddata" height="800" style="width: 100%">
        <el-table-column prop="fund_name" label="基金名称" width="180">
        </el-table-column>
        <el-table-column prop="fund_shares" label="份额" width="70">
        </el-table-column>
        <el-table-column prop="fund_sum" label="成本净值" width="80">
        </el-table-column>
        <el-table-column prop="cost" label="成本" width="70"> </el-table-column>
        <el-table-column prop="earn_sum" label="持有盈利" width="80">
        </el-table-column>
        <el-table-column prop="earn_today" label="今日收益" width="80">
        </el-table-column>
        <el-table-column prop="earn_history" label="落袋收益" width="80">
        </el-table-column>
      </el-table>
    </el-col>
    <el-col :span="14"> </el-col>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      funddata: [],
    };
  },
  mounted: function () {
    this.getfundtable();
  },
  methods: {
    getfundtable: function () {
      axios.get("/getfundtable").then((response) => {
        // console.log(response);
        this.funddata = response.data;
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

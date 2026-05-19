<template>
  <div id="app">
    <el-col :span="24">
      <div id="cycling_strava_summary_charts" style="height: 960px"></div>
    </el-col>
  </div>
</template>

<script>
var echarts = require('echarts');

export default {
  data() {
    return {
      cycling_summary_chart: ''
    };
  },
  mounted: function() {
    this.cycling_summary_chart = echarts.init(
      document.getElementById('cycling_strava_summary_charts'),
      'white',
      {
        renderer: 'canvas'
      }
    );
  },
  methods: {
    init: function() { }
  }
};
</script>

<style>
.el-table {
  overflow: visible !important;
}
</style>

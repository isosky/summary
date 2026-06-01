<template>
  <div id="activity-ride-segment-analysis">
    <el-card>
      <div slot="header">
        <span>骑行路段分析</span>
        <el-button style="float: right;" size="mini" @click="$router.push('/activity')">返回运动总览</el-button>
      </div>

      <el-card shadow="never">
        <div slot="header">
          <span>骑行路段字典维护</span>
        </div>
        <el-form inline size="mini">
          <el-form-item label="路段ID">
            <el-input v-model="rideSegmentDictForm.segment_id" placeholder="请输入需要保留的骑行路段ID"
              style="width: 220px;"></el-input>
          </el-form-item>
          <el-form-item label="路段名称">
            <el-input v-model="rideSegmentDictForm.segment_name" placeholder="可选：手工填写名称，后续同步会自动刷新"
              style="width: 320px;"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="rideSegmentDictSaving" @click="saveRideSegmentDict">新增或启用</el-button>
          </el-form-item>
        </el-form>
        <el-table :data="rideSegmentDictRows" stripe size="mini" style="width: 100%; margin-top: 12px;">
          <el-table-column prop="segment_id" label="路段ID" min-width="120"></el-table-column>
          <el-table-column prop="segment_name" label="路段名称" min-width="260"></el-table-column>
          <el-table-column label="启用" width="100">
            <template slot-scope="scope">
              <el-switch :value="Boolean(scope.row.is_enabled)"
                @change="toggleRideSegmentDict(scope.row, $event)"></el-switch>
            </template>
          </el-table-column>
          <el-table-column prop="updated_at" label="更新时间" width="170"></el-table-column>
          <el-table-column label="操作" width="100">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="deleteRideSegmentDict(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <el-card shadow="never" style="margin-top: 12px;">
        <div slot="header">
          <span>骑行路段趋势</span>
        </div>
        <el-form inline size="mini">
          <el-form-item label="日期">
            <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd" start-placeholder="开始日期"
              end-placeholder="结束日期"></el-date-picker>
          </el-form-item>
          <el-form-item label="路段关键字">
            <el-input v-model="segmentNameKeyword" placeholder="请输入路段名称关键字"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="queryAnalysis">查询</el-button>
          </el-form-item>
        </el-form>

        <el-row :gutter="12">
          <el-col :span="12">
            <el-table :data="segmentSummaryList" stripe size="mini" height="520" @row-click="selectSegment">
              <el-table-column prop="segment_name" label="路段名称" min-width="180"></el-table-column>
              <el-table-column prop="effort_count" label="完成次数" width="90"></el-table-column>
              <el-table-column prop="latest_start_time" label="最近一次" width="160"></el-table-column>
              <el-table-column prop="average_heartrate" label="平均心率" width="100"></el-table-column>
              <el-table-column prop="average_power_watt" label="平均功率" width="100"></el-table-column>
            </el-table>
          </el-col>
          <el-col :span="12">
            <div ref="segmentTrendChart" style="height: 280px;"></div>
            <el-table :data="segmentTrendList" stripe size="mini" height="220" style="margin-top: 12px;">
              <el-table-column prop="start_time" label="开始时间" width="160"></el-table-column>
              <el-table-column prop="distance_meter" label="距离(m)" width="100"></el-table-column>
              <el-table-column prop="duration_second" label="时长(s)" width="90"></el-table-column>
              <el-table-column prop="average_heartrate" label="平均心率" width="100"></el-table-column>
              <el-table-column prop="average_power_watt" label="平均功率" width="100"></el-table-column>
            </el-table>
          </el-col>
        </el-row>
      </el-card>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
var echarts = require('echarts');

export default {
  data() {
    return {
      rideSegmentDictSaving: false,
      rideSegmentDictForm: {
        segment_id: '',
        segment_name: ''
      },
      rideSegmentDictRows: [],
      dateRange: [],
      segmentNameKeyword: '',
      segmentSummaryList: [],
      segmentTrendList: [],
      trendChart: null
    };
  },
  mounted: function () {
    this.getRideSegmentDict();
    this.queryAnalysis();
  },
  beforeDestroy: function () {
    if (this.trendChart) {
      this.trendChart.dispose();
    }
  },
  methods: {
    buildValueAxis: function (axisName, valueList, minimumPadding) {
      const validValues = (valueList || []).filter(item => Number.isFinite(item));
      if (!validValues.length) {
        return {
          type: 'value',
          name: axisName,
          scale: true
        };
      }

      const minValue = Math.min.apply(null, validValues);
      const maxValue = Math.max.apply(null, validValues);
      const basePadding = minimumPadding || 1;
      const dynamicPadding = maxValue === minValue
        ? Math.max(basePadding, Math.abs(minValue) * 0.05)
        : Math.max(basePadding, (maxValue - minValue) * 0.15);

      return {
        type: 'value',
        name: axisName,
        scale: true,
        min: Math.max(0, Math.floor(minValue - dynamicPadding)),
        max: Math.ceil(maxValue + dynamicPadding)
      };
    },
    getRideSegmentDict: function () {
      axios.get('/get_ride_segment_dict').then((response) => {
        this.rideSegmentDictRows = response.data.data || [];
      });
    },
    saveRideSegmentDict: function () {
      if (!this.rideSegmentDictForm.segment_id) {
        this.$message.error('请先输入路段ID');
        return;
      }
      this.rideSegmentDictSaving = true;
      axios.post('/save_ride_segment_dict', {
        segment_id: this.rideSegmentDictForm.segment_id,
        segment_name: this.rideSegmentDictForm.segment_name,
        is_enabled: 1
      }).then(() => {
        this.rideSegmentDictSaving = false;
        this.rideSegmentDictForm.segment_id = '';
        this.rideSegmentDictForm.segment_name = '';
        this.getRideSegmentDict();
        this.queryAnalysis();
      }).catch(() => {
        this.rideSegmentDictSaving = false;
      });
    },
    toggleRideSegmentDict: function (row, value) {
      axios.post('/save_ride_segment_dict', {
        segment_id: row.segment_id,
        segment_name: row.segment_name,
        is_enabled: value ? 1 : 0
      }).then(() => {
        this.getRideSegmentDict();
        this.queryAnalysis();
      });
    },
    deleteRideSegmentDict: function (row) {
      axios.post('/delete_ride_segment_dict', {
        id: row.id
      }).then(() => {
        this.getRideSegmentDict();
        this.queryAnalysis();
      });
    },
    queryAnalysis: function () {
      axios.post('/query_ride_segment_analysis', {
        start_date: this.dateRange && this.dateRange.length ? this.dateRange[0] : null,
        end_date: this.dateRange && this.dateRange.length ? this.dateRange[1] : null,
        segment_name_keyword: this.segmentNameKeyword
      }).then((response) => {
        const data = response.data.data || {};
        this.segmentSummaryList = data.segment_summary_list || [];
        this.segmentTrendList = data.segment_trend_list || [];
        this.$nextTick(() => {
          this.renderTrendChart();
        });
      });
    },
    selectSegment: function (row) {
      this.segmentNameKeyword = row.segment_name;
      this.queryAnalysis();
    },
    renderTrendChart: function () {
      if (!this.$refs.segmentTrendChart) {
        return;
      }
      if (!this.trendChart) {
        this.trendChart = echarts.init(this.$refs.segmentTrendChart);
      }
      const powerList = this.segmentTrendList
        .map(item => Number(item.average_power_watt))
        .filter(item => Number.isFinite(item));
      const heartrateList = this.segmentTrendList
        .map(item => Number(item.average_heartrate))
        .filter(item => Number.isFinite(item));
      this.trendChart.setOption({
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['平均功率', '平均心率']
        },
        xAxis: {
          type: 'category',
          data: this.segmentTrendList.map(item => item.start_time)
        },
        yAxis: [
          this.buildValueAxis('功率', powerList, 5),
          this.buildValueAxis('心率', heartrateList, 3)
        ],
        series: [
          {
            name: '平均功率',
            type: 'line',
            smooth: true,
            data: this.segmentTrendList.map(item => item.average_power_watt)
          },
          {
            name: '平均心率',
            type: 'line',
            smooth: true,
            yAxisIndex: 1,
            data: this.segmentTrendList.map(item => item.average_heartrate)
          }
        ]
      });
    }
  }
};
</script>
<template>
  <div id="activity-run-segment-analysis">
    <el-card>
      <div slot="header">
        <span>跑步路段分析</span>
        <el-button style="float: right;" size="mini" @click="$router.push('/activity')">返回运动总览</el-button>
      </div>
      <div class="analysis-toolbar">
        <el-form inline size="mini" class="analysis-toolbar-form">
          <el-form-item label="日期">
            <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd" start-placeholder="开始日期"
              end-placeholder="结束日期"></el-date-picker>
          </el-form-item>
          <el-form-item label="路段关键字">
            <el-input v-model="segmentNameKeyword" placeholder="请输入路段名称关键字" clearable></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="queryAnalysis">查询</el-button>
          </el-form-item>
        </el-form>
        <div class="analysis-toolbar-tip">
          <el-tag size="mini" type="info">路段数 {{ segmentSummaryList.length }}</el-tag>
          <el-tag size="mini" type="success">明细条数 {{ segmentTrendList.length }}</el-tag>
        </div>
      </div>

      <el-row :gutter="12" class="analysis-main-row">
        <el-col :span="6">
          <el-card shadow="never" class="analysis-panel-card">
            <div slot="header" class="panel-header">
              <span>路段列表</span>
              <span class="panel-header-desc">点击左侧路段刷新右侧趋势和明细</span>
            </div>
            <el-table :data="segmentSummaryList" stripe size="mini" height="560" highlight-current-row
              @row-click="selectSegment">
              <el-table-column prop="segment_name" label="路段名称" min-width="180"></el-table-column>
              <el-table-column prop="effort_count" label="完成次数" width="90"></el-table-column>
              <el-table-column prop="average_heartrate" label="平均心率" width="90"></el-table-column>
              <el-table-column prop="average_pace_second_per_km" label="平均配速" width="100"></el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card shadow="never" class="analysis-panel-card">
            <div slot="header" class="panel-header">
              <span>趋势图</span>
              <span class="panel-header-desc">{{ selectedSegmentName || '请选择左侧路段' }}</span>
            </div>
            <div ref="segmentTrendChart" style="height: 360px;"></div>
          </el-card>
        </el-col>

        <el-col :span="6">
          <el-card shadow="never" class="analysis-panel-card">
            <div slot="header" class="panel-header">
              <span>跑步路段明细</span>
              <span class="panel-header-desc">按开始时间降序展示最近记录</span>
            </div>
            <el-table :data="segmentTrendList" stripe size="mini" height="560">
              <el-table-column prop="start_time" label="开始时间" width="160"></el-table-column>
              <el-table-column prop="duration_second" label="时长(s)" width="100"></el-table-column>
              <el-table-column prop="average_heartrate" label="平均心率" width="100"></el-table-column>
              <el-table-column prop="average_pace_second_per_km" label="平均配速" width="110"></el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
var echarts = require('echarts');

export default {
  data() {
    return {
      dateRange: [],
      segmentNameKeyword: '',
      selectedSegmentName: '',
      segmentSummaryList: [],
      segmentTrendList: [],
      trendChart: null
    };
  },
  mounted: function () {
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
    queryAnalysis: function () {
      axios.post('/query_run_segment_analysis', {
        start_date: this.dateRange && this.dateRange.length ? this.dateRange[0] : null,
        end_date: this.dateRange && this.dateRange.length ? this.dateRange[1] : null,
        segment_name_keyword: this.segmentNameKeyword,
        selected_segment_name: this.selectedSegmentName
      }).then((response) => {
        const data = response.data.data || {};
        this.segmentSummaryList = data.segment_summary_list || [];
        this.segmentTrendList = data.segment_trend_list || [];
        if (!this.selectedSegmentName && this.segmentSummaryList.length > 0) {
          this.selectedSegmentName = this.segmentSummaryList[0].segment_name;
        }
        this.$nextTick(() => {
          this.renderTrendChart();
        });
      });
    },
    selectSegment: function (row) {
      this.selectedSegmentName = row.segment_name;
      axios.post('/query_run_segment_analysis', {
        start_date: this.dateRange && this.dateRange.length ? this.dateRange[0] : null,
        end_date: this.dateRange && this.dateRange.length ? this.dateRange[1] : null,
        segment_name_keyword: this.segmentNameKeyword,
        selected_segment_name: row.segment_name
      }).then((response) => {
        const data = response.data.data || {};
        this.segmentTrendList = data.segment_trend_list || [];
        this.$nextTick(() => {
          this.renderTrendChart();
        });
      });
    },
    renderTrendChart: function () {
      if (!this.$refs.segmentTrendChart) {
        return;
      }
      if (!this.trendChart) {
        this.trendChart = echarts.init(this.$refs.segmentTrendChart);
      }
      const chartTrendList = (this.segmentTrendList || []).slice().sort((leftItem, rightItem) => {
        return new Date(leftItem.start_time).getTime() - new Date(rightItem.start_time).getTime();
      });
      const paceList = chartTrendList
        .map(item => Number(item.average_pace_second_per_km))
        .filter(item => Number.isFinite(item));
      const heartrateList = chartTrendList
        .map(item => Number(item.average_heartrate))
        .filter(item => Number.isFinite(item));
      this.trendChart.setOption({
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['平均配速', '平均心率']
        },
        xAxis: {
          type: 'category',
          data: chartTrendList.map(item => item.start_time)
        },
        yAxis: [
          this.buildValueAxis('配速', paceList, 5),
          this.buildValueAxis('心率', heartrateList, 3)
        ],
        series: [
          {
            name: '平均配速',
            type: 'line',
            smooth: true,
            data: chartTrendList.map(item => item.average_pace_second_per_km)
          },
          {
            name: '平均心率',
            type: 'line',
            smooth: true,
            yAxisIndex: 1,
            data: chartTrendList.map(item => item.average_heartrate)
          }
        ]
      });
    }
  }
};
</script>

<style scoped>
.analysis-toolbar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.analysis-toolbar-form {
  flex: 1;
}

.analysis-toolbar-tip {
  display: flex;
  gap: 8px;
  margin-left: 12px;
  padding-top: 2px;
}

.analysis-main-row {
  margin-top: 4px;
}

.analysis-panel-card {
  border: 1px solid #ebeef5;
}

.detail-card {
  margin-top: 12px;
}

.detail-row {
  margin-top: 12px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
}

.panel-header-desc {
  color: #909399;
  font-size: 12px;
}
</style>
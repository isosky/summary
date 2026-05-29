<template>
    <div id="activity-page">
        <el-row :gutter="12" type="flex" align="stretch">
            <el-col :span="16" style="display: flex;">
                <el-card class="compact-overview-card" style="width: 100%;">
                    <div slot="header">
                        <span>Strava 同步状态</span>
                    </div>
                    <el-row :gutter="12">
                        <el-col :span="16">
                            <el-descriptions :column="4" border size="mini">
                                <el-descriptions-item label="最近同步时间">{{ syncStatus.created_at || '-'
                                    }}</el-descriptions-item>
                                <el-descriptions-item label="同步模式">{{ syncStatus.sync_mode || '-'
                                    }}</el-descriptions-item>
                                <el-descriptions-item label="同步状态">{{ syncStatus.status || '-' }}</el-descriptions-item>
                                <el-descriptions-item label="活动负荷填充">{{ loadFilledText }}</el-descriptions-item>
                                <el-descriptions-item label="抓取活动数">{{ syncSummary.fetched_activity_count || 0
                                    }}</el-descriptions-item>
                                <el-descriptions-item label="写入活动数">{{ syncSummary.saved_activity_count || 0
                                    }}</el-descriptions-item>
                                <el-descriptions-item label="跑步路段数">{{ syncSummary.saved_run_segment_count || 0
                                    }}</el-descriptions-item>
                                <el-descriptions-item label="骑行路段数">{{ syncSummary.saved_ride_segment_count || 0
                                    }}</el-descriptions-item>
                            </el-descriptions>
                        </el-col>
                        <el-col :span="8">
                            <el-form inline size="mini">
                                <el-form-item>
                                    <el-date-picker v-model="syncDateRange" size="mini" type="daterange"
                                        value-format="yyyy-MM-dd" start-placeholder="开始日期"
                                        end-placeholder="结束日期"></el-date-picker>
                                </el-form-item>
                                <el-form-item>
                                    <el-input v-model="resyncActivityId" size="mini" placeholder="Activity ID"
                                        style="width:140px"></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-button type="info" size="mini"
                                        @click="resyncSingleActivity">抓取单个活动路段</el-button>
                                </el-form-item>
                                <el-form-item>
                                    <el-button type="primary" size="mini" :loading="syncLoading"
                                        @click="syncStrava('incremental')">增量同步</el-button>
                                    <el-button type="warning" size="mini" :loading="syncLoading"
                                        @click="syncStrava('full')">全量同步</el-button>
                                    <el-button type="success" size="mini" :loading="syncLoading"
                                        @click="syncStrava('range')">区间同步</el-button>
                                </el-form-item>
                            </el-form>
                        </el-col>
                    </el-row>
                </el-card>
            </el-col>
            <el-col :span="8" style="display: flex;">
                <el-card class="compact-overview-card" style="width: 100%;">
                    <div slot="header">
                        <span>{{ currentYear }} 年目标进度</span>
                    </div>
                    <el-descriptions :column="2" border size="mini">
                        <el-descriptions-item label="骑行已完成(km)">{{ yearGoal.ride_distance_done_km || 0
                            }}</el-descriptions-item>
                        <el-descriptions-item label="骑行完成率">{{ yearGoal.ride_completion_rate || 0
                            }}%</el-descriptions-item>
                        <el-descriptions-item label="骑行每日还需(km)">{{ yearGoal.ride_daily_required_km || 0
                            }}</el-descriptions-item>
                        <el-descriptions-item label="跑步已完成(km)">{{ yearGoal.run_distance_done_km || 0
                            }}</el-descriptions-item>
                        <el-descriptions-item label="跑步完成率">{{ yearGoal.run_completion_rate || 0
                            }}%</el-descriptions-item>
                        <el-descriptions-item label="跑步每日还需(km)">{{ yearGoal.run_daily_required_km || 0
                            }}</el-descriptions-item>
                    </el-descriptions>
                </el-card>
            </el-col>
        </el-row>

        <el-row :gutter="12" type="flex" align="stretch" style="margin-top: 6px;">
            <el-col :span="12" style="display: flex;">
                <el-card class="compact-overview-card" style="width: 100%;">
                    <div slot="header">
                        <span>健康度趋势</span>
                        <el-button style="float: right;" type="primary" size="mini" :loading="computingHealth"
                            @click="computeHealthMetrics">计算健康度</el-button>
                    </div>
                    <el-row :gutter="8" style="margin-bottom: 6px;">
                        <el-col :span="2">
                            <div style="display:flex;flex-direction:column;align-items:flex-start;">
                                <el-tag size="mini" type="info" style="margin-bottom:8px;display:block;">今日负荷 {{
                                    healthMetrics.today_load || 0 }}</el-tag>
                                <el-tag size="mini" type="success" style="margin-bottom:8px;display:block;">健康度 {{
                                    healthMetrics.ctl_value || 0 }}</el-tag>
                                <el-tag size="mini" type="warning" style="display:block;">状态值 {{ healthMetrics.tsb_value
                                    || 0 }}</el-tag>
                            </div>
                        </el-col>
                        <el-col :span="22">
                            <div ref="healthChart" style="height: 280px;"></div>
                        </el-col>
                    </el-row>
                </el-card>
            </el-col>
            <el-col :span="12" style="display: flex;">
                <el-card class="compact-overview-card" style="width: 100%;">
                    <div slot="header">
                        <span>统计汇总</span>
                        <el-radio-group v-model="summaryGranularity" size="mini" style="margin-left: 16px;"
                            @change="queryActivitySummary">
                            <el-radio-button label="year">年</el-radio-button>
                            <el-radio-button label="quarter">季度</el-radio-button>
                            <el-radio-button label="month">月</el-radio-button>
                            <el-radio-button label="week">周</el-radio-button>
                        </el-radio-group>
                    </div>
                    <el-row :gutter="8" style="margin-bottom: 6px;">
                        <el-col :span="4">
                            <div style="display:flex;flex-direction:column;align-items:flex-start;">
                                <el-tag size="mini" style="margin-bottom:8px;display:block;">活动 {{
                                    overview.activity_count || 0 }}</el-tag>
                                <el-tag size="mini" type="success" style="margin-bottom:8px;display:block;">跑步 {{
                                    overview.run_count || 0 }}</el-tag>
                                <el-tag size="mini" type="primary" style="margin-bottom:8px;display:block;">骑行 {{
                                    overview.ride_count || 0 }}</el-tag>
                                <el-tag size="mini" type="warning" style="margin-bottom:8px;display:block;">跑步里程 {{
                                    overview.run_distance_km || 0 }}km</el-tag>
                                <el-tag size="mini" type="warning" style="margin-bottom:8px;display:block;">骑行里程 {{
                                    overview.ride_distance_km || 0 }}km</el-tag>
                                <el-tag size="mini" type="danger" style="display:block;">总负荷 {{
                                    overview.total_exercise_load || 0 }}</el-tag>
                            </div>
                        </el-col>
                        <el-col :span="20">
                            <el-table :data="summaryRows" stripe size="mini" max-height="320" style="width: 100%">
                                <el-table-column prop="period_label" label="周期" width="120"></el-table-column>
                                <el-table-column prop="activity_count" label="活动数" width="90"></el-table-column>
                                <el-table-column prop="run_count" label="跑步数" width="90"></el-table-column>
                                <el-table-column prop="ride_count" label="骑行数" width="90"></el-table-column>
                                <el-table-column prop="run_distance_km" label="跑步距离(km)" width="120"></el-table-column>
                                <el-table-column prop="ride_distance_km" label="骑行距离(km)" width="120"></el-table-column>
                                <el-table-column prop="total_duration_second" label="总时长(s)"
                                    width="120"></el-table-column>
                                <el-table-column prop="total_elevation_gain" label="总爬升" width="100"></el-table-column>
                                <el-table-column prop="total_exercise_load" label="总负荷" width="100"></el-table-column>
                            </el-table>
                        </el-col>
                    </el-row>
                </el-card>
            </el-col>
        </el-row>

        <el-row :gutter="12" style="margin-top: 8px;">
            <el-col :span="14">
                <el-card>
                    <div slot="header">
                        <span>运动列表</span>
                    </div>
                    <el-form inline size="mini">
                        <el-form-item label="类型">
                            <el-select v-model="filters.activity_type" clearable placeholder="全部">
                                <el-option label="Run" value="Run"></el-option>
                                <el-option label="Ride" value="Ride"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="日期">
                            <el-date-picker v-model="filters.date_range" type="daterange" value-format="yyyy-MM-dd"
                                start-placeholder="开始日期" end-placeholder="结束日期"></el-date-picker>
                        </el-form-item>
                        <el-form-item>
                            <el-switch v-model="filters.require_exercise_load" inactive-text="只看有负荷"></el-switch>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="reloadActivityList">查询</el-button>
                        </el-form-item>
                    </el-form>

                    <el-table :data="activityRows" stripe size="mini" style="width: 100%" max-height="520">
                        <el-table-column prop="start_time" label="开始时间" width="170"></el-table-column>
                        <el-table-column prop="activity_type" label="类型" width="80"></el-table-column>
                        <el-table-column prop="activity_name" label="名称" width="220"></el-table-column>
                        <el-table-column prop="duration_second" label="时长(s)" width="100"></el-table-column>
                        <el-table-column prop="distance_meter" label="距离(m)" width="100"></el-table-column>
                        <el-table-column prop="elevation_gain" label="爬升" width="90"></el-table-column>
                        <el-table-column prop="average_heartrate" label="平均心率" width="100"></el-table-column>
                        <el-table-column prop="average_power_watt" label="平均功率" width="100"></el-table-column>
                        <el-table-column prop="average_pace_second_per_km" label="平均配速" width="100"></el-table-column>
                        <el-table-column prop="exercise_load_score" label="运动负荷" width="100"></el-table-column>
                        <el-table-column label="操作" width="120">
                            <template slot-scope="scope">
                                <el-button v-if="scope.row.activity_type === 'Run'" type="text" size="small"
                                    @click="openRunDrawer(scope.row)">路段</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <el-pagination style="margin-top: 12px;" @size-change="handleSizeChange"
                        @current-change="handleCurrentChange" :current-page="pageNum" :page-sizes="[10, 20, 30, 40]"
                        :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper"
                        :total="activityTotal"></el-pagination>
                </el-card>
            </el-col>
            <el-col :span="10">
                <el-card>
                    <div slot="header">
                        <span>跑步路段详情</span>
                        <el-button v-if="selectedActivityId" style="float: right;" type="primary" size="mini"
                            @click="gotoRunSegmentAnalysis">进入路段分析页</el-button>
                    </div>
                    <div v-if="selectedActivityId">
                        <div style="margin-bottom: 12px; color: #909399; font-size: 12px;">
                            当前活动ID：{{ selectedActivityId }}
                        </div>
                        <el-table :data="runSegmentRows" stripe size="mini" style="width: 100%;" max-height="360">
                            <el-table-column prop="segment_name" label="路段名称" min-width="180"></el-table-column>
                            <el-table-column prop="start_time" label="开始时间" width="160"></el-table-column>
                            <el-table-column prop="duration_second" label="时长(s)" width="90"></el-table-column>
                            <el-table-column prop="average_heartrate" label="平均心率" width="100"></el-table-column>
                            <el-table-column prop="average_pace_second_per_km" label="平均配速"
                                width="100"></el-table-column>
                        </el-table>
                    </div>
                    <el-empty v-else description="点击左侧跑步活动查看路段详情"></el-empty>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import axios from 'axios';
var echarts = require('echarts');

export default {
    data() {
        return {
            currentYear: new Date().getFullYear(),
            computingHealth: false,
            syncLoading: false,
            healthChart: null,
            syncStatus: {},
            syncSummary: {},
            loadFilledText: '0 / 0',
            yearGoal: {},
            healthMetrics: {
                trend_list: []
            },
            overview: {},
            summaryGranularity: 'month',
            summaryRows: [],
            filters: {
                activity_type: '',
                date_range: [],
                require_exercise_load: false
            },
            syncDateRange: [],
            activityRows: [],
            activityTotal: 0,
            pageNum: 1,
            pageSize: 10,
            selectedActivityId: null,
            runSegmentRows: []
            ,
            resyncActivityId: ''
        };
    },
    mounted: function () {
        this.init();
    },
    beforeDestroy: function () {
        if (this.healthChart) {
            this.healthChart.dispose();
        }
    },
    methods: {
        init: function () {
            this.getActivityInitData();
            this.queryActivitySummary();
            this.queryActivityList();
        },
        getActivityInitData: function () {
            axios.get('/get_activity_init_data', {
                params: {
                    year: this.currentYear
                }
            }).then((response) => {
                const data = response.data.data || {};
                this.syncStatus = data.sync_status || {};
                this.syncSummary = this.syncStatus.summary || {};
                this.yearGoal = data.year_goal || {};
                this.healthMetrics = data.health_metrics || { trend_list: [] };
                this.overview = data.overview || {};
                this.loadFilledText = ((this.syncSummary.saved_activity_count || this.overview.activity_count || 0) ? '' : '');
                this.loadExerciseLoadFilled();
                this.$nextTick(() => {
                    this.renderHealthChart();
                });
            });
        },
        computeHealthMetrics: function () {
            this.computingHealth = true;
            axios.post('/compute_health_metrics', {}).then((response) => {
                const data = response.data.data || {};
                this.healthMetrics = data || { trend_list: [] };
                this.$nextTick(() => {
                    this.renderHealthChart();
                });
                this.$message.success('健康度计算已完成');
            }).catch(() => {
                this.$message.error('计算健康度失败');
            }).finally(() => {
                this.computingHealth = false;
            });
        },
        resyncSingleActivity: function () {
            if (!this.resyncActivityId) {
                this.$message.error('请先输入 activity_id');
                return;
            }
            axios.post('/resync_activity_segments', {
                activity_id: this.resyncActivityId
            }).then(() => {
                this.$message.success('已开始重抓，可在稍后查看结果');
            }).catch(() => {
                this.$message.error('启动重抓失败');
            });
        },
        loadExerciseLoadFilled: function () {
            axios.post('/query_activity_list', {
                page_num: 1,
                page_size: 1,
                require_exercise_load: true
            }).then((response) => {
                const filled = response.data.data.total || 0;
                const total = this.overview.activity_count || 0;
                this.loadFilledText = filled + ' / ' + total;
            });
        },
        renderHealthChart: function () {
            if (!this.$refs.healthChart) {
                return;
            }
            if (!this.healthChart) {
                this.healthChart = echarts.init(this.$refs.healthChart);
            }
            const trend = this.healthMetrics.trend_list || [];
            this.healthChart.setOption({
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['健康度', '疲劳度', '状态值']
                },
                xAxis: {
                    type: 'category',
                    data: trend.map(item => item.metric_date)
                },
                yAxis: {
                    type: 'value'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%'
                },
                series: [
                    {
                        name: '健康度',
                        type: 'line',
                        smooth: true,
                        data: trend.map(item => item.ctl_value)
                    },
                    {
                        name: '疲劳度',
                        type: 'line',
                        smooth: true,
                        data: trend.map(item => item.atl_value)
                    },
                    {
                        name: '状态值',
                        type: 'line',
                        smooth: true,
                        data: trend.map(item => item.tsb_value)
                    }
                ]
            });
        },
        queryActivitySummary: function () {
            axios.post('/query_activity_summary', {
                granularity: this.summaryGranularity,
                year: this.currentYear
            }).then((response) => {
                this.summaryRows = response.data.data || [];
            });
        },
        queryActivityList: function () {
            axios.post('/query_activity_list', {
                activity_type: this.filters.activity_type,
                start_date: this.filters.date_range && this.filters.date_range.length ? this.filters.date_range[0] : null,
                end_date: this.filters.date_range && this.filters.date_range.length ? this.filters.date_range[1] : null,
                require_exercise_load: this.filters.require_exercise_load,
                page_num: this.pageNum,
                page_size: this.pageSize
            }).then((response) => {
                const data = response.data.data || {};
                this.activityRows = data.list || [];
                this.activityTotal = data.total || 0;
            });
        },
        reloadActivityList: function () {
            this.pageNum = 1;
            this.queryActivityList();
        },
        handleSizeChange: function (val) {
            this.pageSize = val;
            this.queryActivityList();
        },
        handleCurrentChange: function (val) {
            this.pageNum = val;
            this.queryActivityList();
        },
        syncStrava: function (mode) {
            if (mode === 'range' && (!this.syncDateRange || this.syncDateRange.length !== 2)) {
                this.$message.error('请先选择区间日期');
                return;
            }
            if (mode === 'full') {
                this.$confirm('确认执行全量同步吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.doSyncStrava(mode);
                }).catch(() => { });
                return;
            }
            this.doSyncStrava(mode);
        },
        doSyncStrava: function (mode) {
            this.syncLoading = true;
            axios.post('/sync_strava_activities', {
                mode: mode,
                start_date: this.syncDateRange && this.syncDateRange.length ? this.syncDateRange[0] : null,
                end_date: this.syncDateRange && this.syncDateRange.length ? this.syncDateRange[1] : null
            }).then(() => {
                this.syncLoading = false;
                this.getActivityInitData();
                this.queryActivitySummary();
                this.queryActivityList();
            }).catch(() => {
                this.syncLoading = false;
            });
        },
        openRunDrawer: function (row) {
            this.selectedActivityId = row.activity_id;
            axios.post('/query_run_segment_detail', {
                activity_id: row.activity_id
            }).then((response) => {
                this.runSegmentRows = response.data.data || [];
            });
        },
        gotoRunSegmentAnalysis: function () {
            this.$router.push('/activity_run_segment_analysis');
        }
    }
};
</script>

<style scoped>
#activity-page .compact-overview-card /deep/ .el-card__header {
    padding: 8px 10px;
}

#activity-page .compact-overview-card /deep/ .el-card__body {
    padding: 8px 10px;
}

#activity-page .compact-overview-card /deep/ .el-form-item {
    margin-bottom: 6px;
}
</style>

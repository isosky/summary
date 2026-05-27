<template>
    <div id="activity-settings">
        <el-row :gutter="12">
            <el-col :span="6">
                <el-card>
                    <div slot="header">
                        <span>{{ currentYear }} 年骑行目标维护</span>
                    </div>
                    <el-form label-width="120px" size="mini">
                        <el-form-item label="骑行目标(km)">
                            <el-input-number v-model="goalForm.ride_distance_goal_km" :min="0"
                                :precision="2"></el-input-number>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" size="mini" :loading="goalSaving"
                                @click="saveGoal">保存目标</el-button>
                        </el-form-item>
                    </el-form>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card>
                    <div slot="header">
                        <span>{{ currentYear }} 年跑步目标维护</span>
                    </div>
                    <el-form label-width="120px" size="mini">
                        <el-form-item label="跑步目标(km)">
                            <el-input-number v-model="goalForm.run_distance_goal_km" :min="0"
                                :precision="2"></el-input-number>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" size="mini" :loading="goalSaving"
                                @click="saveGoal">保存目标</el-button>
                        </el-form-item>
                    </el-form>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card>
                    <div slot="header">
                        <span>骑行路段维护</span>
                    </div>
                    <el-form inline size="mini">
                        <el-form-item label="路段名称">
                            <el-input v-model="rideSegmentDictForm.segment_name" placeholder="请输入需要保留的骑行路段名称"
                                style="width: 320px;"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" :loading="rideSegmentDictSaving"
                                @click="saveRideSegmentDict">新增或启用</el-button>
                        </el-form-item>
                    </el-form>
                    <el-table :data="rideSegmentDictRows" stripe size="mini" style="width: 100%; margin-top: 12px;">
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
                                <el-button type="text" size="small"
                                    @click="deleteRideSegmentDict(scope.row)">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            currentYear: new Date().getFullYear(),
            goalSaving: false,
            rideSegmentDictSaving: false,
            goalForm: {
                ride_distance_goal_km: 0,
                run_distance_goal_km: 0
            },
            yearGoal: {},
            rideSegmentDictForm: {
                segment_name: ''
            },
            rideSegmentDictRows: []
        };
    },
    mounted: function () {
        this.getGoal();
        this.getRideSegmentDict();
    },
    methods: {
        getGoal: function () {
            axios.get('/get_activity_goal', {
                params: {
                    year: this.currentYear
                }
            }).then((response) => {
                this.yearGoal = response.data.data || {};
                this.goalForm.ride_distance_goal_km = this.yearGoal.ride_distance_goal_km || 0;
                this.goalForm.run_distance_goal_km = this.yearGoal.run_distance_goal_km || 0;
            });
        },
        saveGoal: function () {
            this.goalSaving = true;
            axios.post('/save_activity_goal', {
                year: this.currentYear,
                ride_distance_goal_km: this.goalForm.ride_distance_goal_km,
                run_distance_goal_km: this.goalForm.run_distance_goal_km
            }).then((response) => {
                this.yearGoal = response.data.data || {};
                this.goalForm.ride_distance_goal_km = this.yearGoal.ride_distance_goal_km || 0;
                this.goalForm.run_distance_goal_km = this.yearGoal.run_distance_goal_km || 0;
                this.goalSaving = false;
            }).catch(() => {
                this.goalSaving = false;
            });
        },
        getRideSegmentDict: function () {
            axios.get('/get_ride_segment_dict').then((response) => {
                this.rideSegmentDictRows = response.data.data || [];
            });
        },
        saveRideSegmentDict: function () {
            if (!this.rideSegmentDictForm.segment_name) {
                this.$message.error('请先输入路段名称');
                return;
            }
            this.rideSegmentDictSaving = true;
            axios.post('/save_ride_segment_dict', {
                segment_name: this.rideSegmentDictForm.segment_name,
                is_enabled: 1
            }).then(() => {
                this.rideSegmentDictSaving = false;
                this.rideSegmentDictForm.segment_name = '';
                this.getRideSegmentDict();
            }).catch(() => {
                this.rideSegmentDictSaving = false;
            });
        },
        toggleRideSegmentDict: function (row, value) {
            axios.post('/save_ride_segment_dict', {
                segment_name: row.segment_name,
                is_enabled: value ? 1 : 0
            }).then(() => {
                this.getRideSegmentDict();
            });
        },
        deleteRideSegmentDict: function (row) {
            axios.post('/delete_ride_segment_dict', {
                id: row.id
            }).then(() => {
                this.getRideSegmentDict();
            });
        }
    }
};
</script>
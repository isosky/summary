<template>
    <div class="market-sync-ops-page">
        <el-row :gutter="12">
            <el-col :span="24">
                <el-card>
                    <div slot="header" class="page-header">
                        <div>
                            <span>市场同步运维</span>
                            <p>手动触发行情同步，并查看最近任务执行日志。</p>
                        </div>
                        <div class="header-actions">
                            <el-button size="mini" @click="loadLogs">刷新日志</el-button>
                            <el-button size="mini" type="primary" :loading="syncing"
                                @click="triggerSync">触发同步</el-button>
                        </div>
                    </div>

                    <el-form :inline="true" size="mini" class="filter-form">
                        <el-form-item label="mode">
                            <el-select v-model="triggerForm.mode" style="width: 120px;">
                                <el-option label="all" value="all"></el-option>
                                <el-option label="plan" value="plan"></el-option>
                                <el-option label="watchlist" value="watchlist"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="run_mode">
                            <el-select v-model="triggerForm.run_mode" style="width: 150px;">
                                <el-option label="manual" value="manual"></el-option>
                                <el-option label="intraday_30m" value="intraday_30m"></el-option>
                                <el-option label="close_confirm" value="close_confirm"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="起始日期">
                            <el-date-picker v-model="triggerForm.start_date" type="date" value-format="yyyy-MM-dd"
                                placeholder="可选"></el-date-picker>
                        </el-form-item>
                        <el-form-item label="结束日期">
                            <el-date-picker v-model="triggerForm.end_date" type="date" value-format="yyyy-MM-dd"
                                placeholder="可选"></el-date-picker>
                        </el-form-item>
                        <el-form-item label="limit">
                            <el-input-number v-model="triggerForm.limit" :min="1" :max="500"
                                :step="1"></el-input-number>
                        </el-form-item>
                        <el-form-item label="dry_run">
                            <el-switch v-model="triggerForm.dry_run"></el-switch>
                        </el-form-item>
                    </el-form>

                    <div class="last-result" v-if="lastResultText">
                        <div class="last-result-title">最近一次触发结果</div>
                        <el-input type="textarea" :rows="8" :value="lastResultText" readonly></el-input>
                    </div>
                </el-card>
            </el-col>
        </el-row>

        <el-row :gutter="12" style="margin-top: 12px;">
            <el-col :span="24">
                <el-card>
                    <div slot="header" class="page-header">
                        <div>
                            <span>同步任务日志</span>
                        </div>
                        <div class="header-actions">
                            <el-select v-model="filters.run_mode" clearable size="mini" placeholder="run_mode"
                                style="width: 150px;">
                                <el-option label="manual" value="manual"></el-option>
                                <el-option label="intraday_30m" value="intraday_30m"></el-option>
                                <el-option label="close_confirm" value="close_confirm"></el-option>
                            </el-select>
                            <el-select v-model="filters.status" clearable size="mini" placeholder="status"
                                style="width: 140px;">
                                <el-option label="running" value="running"></el-option>
                                <el-option label="success" value="success"></el-option>
                                <el-option label="partial_success" value="partial_success"></el-option>
                                <el-option label="failed" value="failed"></el-option>
                                <el-option label="skipped" value="skipped"></el-option>
                            </el-select>
                            <el-input-number v-model="filters.limit" size="mini" :min="1" :max="100"
                                :step="1"></el-input-number>
                            <el-button size="mini" type="primary" @click="loadLogs">查询</el-button>
                        </div>
                    </div>

                    <el-table :data="logs" stripe size="mini" v-loading="loading" style="width: 100%;">
                        <el-table-column prop="id" label="ID" width="80"></el-table-column>
                        <el-table-column prop="run_mode" label="run_mode" width="130"></el-table-column>
                        <el-table-column prop="status" label="状态" width="130">
                            <template slot-scope="scope">
                                <el-tag size="mini" :type="getStatusTag(scope.row.status)">{{ scope.row.status
                                }}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column prop="started_at" label="开始时间" width="170"></el-table-column>
                        <el-table-column prop="finished_at" label="结束时间" width="170"></el-table-column>
                        <el-table-column prop="total_symbols" label="总数" width="80"></el-table-column>
                        <el-table-column prop="success_symbols" label="成功" width="80"></el-table-column>
                        <el-table-column prop="failed_symbols" label="失败" width="80"></el-table-column>
                        <el-table-column prop="upsert_rows" label="Upsert" width="90"></el-table-column>
                        <el-table-column prop="error_summary" label="错误摘要" min-width="220"></el-table-column>
                        <el-table-column label="详情" width="90">
                            <template slot-scope="scope">
                                <el-button size="mini" type="text" @click="openDetail(scope.row)">查看</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
        </el-row>

        <el-dialog title="任务详情" :visible.sync="detailVisible" width="720px">
            <el-input type="textarea" :rows="18" :value="detailText" readonly></el-input>
            <span slot="footer">
                <el-button size="mini" @click="detailVisible = false">关闭</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import marketApi from '@/api/market_data';

export default {
    data() {
        return {
            loading: false,
            syncing: false,
            detailVisible: false,
            detailText: '',
            lastResultText: '',
            logs: [],
            triggerForm: {
                mode: 'all',
                run_mode: 'manual',
                start_date: '',
                end_date: '',
                limit: 30,
                dry_run: true
            },
            filters: {
                run_mode: '',
                status: '',
                limit: 20
            }
        };
    },
    mounted() {
        this.loadLogs();
    },
    methods: {
        isUnauthorizedError(err) {
            return Boolean(err && err.response && err.response.status === 401);
        },
        getStatusTag(status) {
            if (status === 'success') return 'success';
            if (status === 'failed') return 'danger';
            if (status === 'partial_success') return 'warning';
            if (status === 'running') return 'info';
            return '';
        },
        async triggerSync() {
            if ((this.triggerForm.start_date && !this.triggerForm.end_date) || (!this.triggerForm.start_date && this.triggerForm.end_date)) {
                this.$message({ message: 'start_date 和 end_date 需要同时填写', type: 'warning' });
                return;
            }
            this.syncing = true;
            try {
                const payload = {
                    mode: this.triggerForm.mode,
                    run_mode: this.triggerForm.run_mode,
                    start_date: this.triggerForm.start_date || undefined,
                    end_date: this.triggerForm.end_date || undefined,
                    limit: this.triggerForm.limit,
                    dry_run: this.triggerForm.dry_run
                };
                const resp = await marketApi.triggerSync(payload);
                if (!resp || !resp.data || resp.data.code !== 200) {
                    throw new Error((resp && resp.data && resp.data.message) || '触发同步失败');
                }
                const data = resp.data.data || {};
                this.lastResultText = JSON.stringify(data, null, 2);
                this.$message({ message: '同步已触发。', type: 'success' });
                this.loadLogs();
            } catch (err) {
                console.error(err);
                if (this.isUnauthorizedError(err)) {
                    return;
                }
                this.$message({ message: err.message || '触发同步失败', type: 'error' });
            } finally {
                this.syncing = false;
            }
        },
        async loadLogs() {
            this.loading = true;
            try {
                const payload = {
                    run_mode: this.filters.run_mode || undefined,
                    status: this.filters.status || undefined,
                    limit: this.filters.limit
                };
                const resp = await marketApi.listSyncJobs(payload);
                if (!resp || !resp.data || resp.data.code !== 200) {
                    throw new Error((resp && resp.data && resp.data.message) || '加载日志失败');
                }
                this.logs = resp.data.data || [];
            } catch (err) {
                console.error(err);
                if (this.isUnauthorizedError(err)) {
                    return;
                }
                this.$message({ message: err.message || '加载日志失败', type: 'error' });
            } finally {
                this.loading = false;
            }
        },
        openDetail(row) {
            const detail = row && row.detail ? row.detail : row;
            this.detailText = JSON.stringify(detail || {}, null, 2);
            this.detailVisible = true;
        }
    }
};
</script>

<style scoped>
.market-sync-ops-page {
    box-sizing: border-box;
    padding: 12px;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.page-header p {
    margin: 6px 0 0;
    color: #64748b;
    font-size: 12px;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.filter-form {
    margin-bottom: 6px;
}

.last-result {
    margin-top: 10px;
}

.last-result-title {
    margin-bottom: 8px;
    font-size: 12px;
    color: #64748b;
}
</style>

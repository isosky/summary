<template>
    <div class="market-watchlist-page">
        <el-row :gutter="12">
            <el-col :span="24">
                <el-card>
                    <div slot="header" class="page-header">
                        <div>
                            <span>观察池管理</span>
                            <p>维护 ETF 和指数观察池，供每日自动同步使用。</p>
                        </div>
                        <div class="header-actions">
                            <el-button size="mini" @click="loadRows">刷新</el-button>
                            <el-button size="mini" type="primary" @click="openCreateDialog">新增标的</el-button>
                        </div>
                    </div>

                    <el-form inline size="mini" class="filter-form">
                        <el-form-item label="标的类型">
                            <el-select v-model="filters.symbol_type" clearable placeholder="全部类型" style="width: 140px;">
                                <el-option label="股票" value="stock"></el-option>
                                <el-option label="ETF" value="etf"></el-option>
                                <el-option label="指数" value="index"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="启用状态">
                            <el-select v-model="filters.enabled" clearable placeholder="全部状态" style="width: 140px;">
                                <el-option label="启用" :value="1"></el-option>
                                <el-option label="停用" :value="0"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="loadRows">查询</el-button>
                        </el-form-item>
                    </el-form>

                    <el-table :data="rows" stripe size="mini" v-loading="loading" style="width: 100%;">
                        <el-table-column prop="symbol_code" label="标的代码" width="150">
                            <template slot-scope="scope">
                                {{ stripMarketSuffix(scope.row.symbol_code) }}
                            </template>
                        </el-table-column>
                        <el-table-column prop="symbol_name" label="标的名称" min-width="150"></el-table-column>
                        <el-table-column prop="symbol_type" label="类型" width="100">
                            <template slot-scope="scope">
                                <el-tag size="mini" :type="getTypeTag(scope.row.symbol_type)">{{ getTypeLabel(scope.row.symbol_type) }}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column label="启用" width="100">
                            <template slot-scope="scope">
                                <el-switch :value="Boolean(scope.row.enabled)" @change="toggleRow(scope.row, $event)"></el-switch>
                            </template>
                        </el-table-column>
                        <el-table-column prop="remark" label="备注" min-width="180"></el-table-column>
                        <el-table-column prop="updated_at" label="更新时间" width="170"></el-table-column>
                        <el-table-column label="操作" width="100">
                            <template slot-scope="scope">
                                <el-button type="text" size="small" class="danger-text" @click="removeRow(scope.row)">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
        </el-row>

        <el-dialog title="新增观察标的" :visible.sync="dialogVisible" width="420px">
            <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-width="90px" size="mini">
                <el-form-item label="标的代码" prop="symbol_code">
                    <el-input v-model="createForm.symbol_code" placeholder="如 510300 / 000300 / 300750"></el-input>
                </el-form-item>
                <el-form-item label="标的名称">
                    <el-input v-model="createForm.symbol_name"></el-input>
                </el-form-item>
                <el-form-item label="标的类型" prop="symbol_type">
                    <el-select v-model="createForm.symbol_type" placeholder="请选择" style="width: 100%;">
                        <el-option label="股票" value="stock"></el-option>
                        <el-option label="ETF" value="etf"></el-option>
                        <el-option label="指数" value="index"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input v-model="createForm.remark" type="textarea" :rows="3"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer">
                <el-button size="mini" @click="dialogVisible = false">取消</el-button>
                <el-button size="mini" type="primary" :loading="saving" @click="submitCreate">保存</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import marketApi from '@/api/market_data';

function createEmptyForm() {
    return {
        symbol_code: '',
        symbol_name: '',
        symbol_type: 'etf',
        remark: ''
    };
}

export default {
    data() {
        return {
            loading: false,
            saving: false,
            dialogVisible: false,
            rows: [],
            filters: {
                symbol_type: '',
                enabled: ''
            },
            createForm: createEmptyForm(),
            createRules: {
                symbol_code: [{ required: true, message: '请填写标的代码', trigger: 'blur' }],
                symbol_type: [{ required: true, message: '请选择标的类型', trigger: 'change' }]
            }
        };
    },
    mounted() {
        this.loadRows();
    },
    methods: {
        stripMarketSuffix(code) {
            const text = String(code || '').trim();
            if (!text) {
                return '';
            }
            return text.replace(/\.(SH|SZ)$/i, '');
        },
        normalizeSymbolType(symbolDigits, symbolType) {
            const normalizedType = String(symbolType || '').trim().toLowerCase();
            if (normalizedType === 'stock' || normalizedType === 'etf' || normalizedType === 'index') {
                return normalizedType;
            }
            if (symbolDigits.startsWith('5') || symbolDigits.startsWith('1')) {
                return 'etf';
            }
            if (symbolDigits.startsWith('0') || symbolDigits.startsWith('3') || symbolDigits.startsWith('6') || symbolDigits.startsWith('8') || symbolDigits.startsWith('4')) {
                return 'stock';
            }
            return 'index';
        },
        normalizeSymbolCodeForSubmit(symbolCode, symbolType) {
            const raw = String(symbolCode || '').trim().toUpperCase();
            if (!raw) {
                throw new Error('请填写标的代码');
            }

            let exchange = '';
            let digits = '';

            if (/^(SH|SZ)\d{6}$/.test(raw)) {
                exchange = raw.slice(0, 2);
                digits = raw.slice(2);
            } else if (/^\d{6}\.(SH|SZ)$/.test(raw)) {
                digits = raw.slice(0, 6);
                exchange = raw.slice(7, 9);
            } else if (/^\d{6}$/.test(raw)) {
                digits = raw;
            } else {
                throw new Error('代码格式不正确，请输入 6 位数字（如 510300）');
            }

            const normalizedType = this.normalizeSymbolType(digits, symbolType);
            if (!exchange) {
                if (normalizedType === 'index') {
                    exchange = 'SH';
                } else if (digits.startsWith('6') || digits.startsWith('5') || digits.startsWith('9')) {
                    exchange = 'SH';
                } else {
                    exchange = 'SZ';
                }
            }
            return `${digits}.${exchange}`;
        },
        getTypeLabel(symbolType) {
            if (symbolType === 'stock') return '股票';
            if (symbolType === 'etf') return 'ETF';
            if (symbolType === 'index') return '指数';
            return symbolType || '--';
        },
        getTypeTag(symbolType) {
            if (symbolType === 'stock') return '';
            if (symbolType === 'etf') return 'success';
            if (symbolType === 'index') return 'warning';
            return 'info';
        },
        async loadRows() {
            this.loading = true;
            try {
                const payload = {};
                if (this.filters.symbol_type) {
                    payload.symbol_type = this.filters.symbol_type;
                }
                if (this.filters.enabled === 0 || this.filters.enabled === 1) {
                    payload.enabled = this.filters.enabled;
                }
                const resp = await marketApi.listWatchlist(payload);
                if (!resp || !resp.data || resp.data.code !== 200) {
                    throw new Error((resp && resp.data && resp.data.message) || '加载观察池失败');
                }
                this.rows = resp.data.data || [];
            } catch (err) {
                console.error(err);
                this.$message({ message: err.message || '加载观察池失败', type: 'error' });
            } finally {
                this.loading = false;
            }
        },
        openCreateDialog() {
            this.createForm = createEmptyForm();
            this.dialogVisible = true;
            this.$nextTick(() => {
                if (this.$refs.createFormRef) {
                    this.$refs.createFormRef.clearValidate();
                }
            });
        },
        submitCreate() {
            this.$refs.createFormRef.validate(async (valid) => {
                if (!valid) {
                    return;
                }
                this.saving = true;
                try {
                    const normalizedCode = this.normalizeSymbolCodeForSubmit(this.createForm.symbol_code, this.createForm.symbol_type);
                    const payload = {
                        ...this.createForm,
                        symbol_code: normalizedCode
                    };
                    const resp = await marketApi.addWatchlist(payload);
                    if (!resp || !resp.data || resp.data.code !== 200) {
                        throw new Error((resp && resp.data && resp.data.message) || '保存观察标的失败');
                    }
                    this.createForm.symbol_code = normalizedCode;
                    this.dialogVisible = false;
                    this.$message({ message: '观察标的已保存。', type: 'success' });
                    this.loadRows();
                } catch (err) {
                    console.error(err);
                    this.$message({ message: err.message || '保存观察标的失败', type: 'error' });
                } finally {
                    this.saving = false;
                }
            });
        },
        async toggleRow(row, enabled) {
            try {
                const resp = await marketApi.toggleWatchlist({
                    symbol_code: row.symbol_code,
                    enabled: enabled ? 1 : 0
                });
                if (!resp || !resp.data || resp.data.code !== 200) {
                    throw new Error((resp && resp.data && resp.data.message) || '更新启用状态失败');
                }
                this.$message({ message: '状态已更新。', type: 'success' });
                this.loadRows();
            } catch (err) {
                console.error(err);
                this.$message({ message: err.message || '更新启用状态失败', type: 'error' });
                this.loadRows();
            }
        },
        async removeRow(row) {
            try {
                await this.$confirm(`确认删除 ${this.stripMarketSuffix(row.symbol_code)} 吗？`, '提示', { type: 'warning' });
                const resp = await marketApi.removeWatchlist({ symbol_code: row.symbol_code });
                if (!resp || !resp.data || resp.data.code !== 200) {
                    throw new Error((resp && resp.data && resp.data.message) || '删除观察标的失败');
                }
                this.$message({ message: '观察标的已删除。', type: 'success' });
                this.loadRows();
            } catch (err) {
                if (err === 'cancel') {
                    return;
                }
                console.error(err);
                this.$message({ message: err.message || '删除观察标的失败', type: 'error' });
            }
        }
    }
};
</script>

<style scoped>
.market-watchlist-page {
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
    gap: 8px;
}

.filter-form {
    margin-bottom: 12px;
}

.danger-text {
    color: #ef4444;
}
</style>

<template>
    <div class="investment-review-page">
        <section class="hero-panel">
            <div class="hero-main">
                <div>
                    <p class="eyebrow">Investment Review Workspace</p>
                    <h1>投资复盘工作台</h1>
                </div>
                <div class="plan-switch-block">
                    <span class="switch-label">当前计划</span>
                    <el-select v-model="currentPlanId" size="mini" class="plan-switcher" @change="handlePlanChange">
                        <el-option v-for="item in planOptions" :key="item.id" :label="item.label"
                            :value="item.id"></el-option>
                    </el-select>
                    <el-button size="mini" plain @click="createNewPlan">新建计划</el-button>
                </div>
            </div>
            <div class="hero-metrics">
                <div class="metric-card">
                    <span class="metric-label">本轮状态</span>
                    <strong>{{ reviewSummary.status }}</strong>
                </div>
                <div class="metric-card accent">
                    <span class="metric-label">计划执行评分</span>
                    <strong>{{ reviewSummary.score }}</strong>
                </div>
                <div class="metric-card">
                    <span class="metric-label">累计收益</span>
                    <strong :class="getPnlDisplayClass()">{{ getPnlRatioText() }}</strong>
                </div>
            </div>
        </section>

        <el-tabs v-model="activeTab" class="workspace-tabs" :before-leave="handleBeforeTabLeave">
            <el-tab-pane label="录入页面" name="entry">
                <div class="workspace-grid">
                    <section class="panel panel-main">
                        <div class="panel-header">
                            <div>
                                <h2>计划与执行录入</h2>
                                <p>一页完成计划建立、追加修改、执行记录与结束确认。</p>
                                <p v-if="getDisplayStockCode()">当前标的：{{ getDisplayStockCode() }}</p>
                            </div>
                            <div class="header-actions">
                                <el-button size="mini" type="primary" @click="saveCurrentPlan">保存计划</el-button>
                            </div>
                        </div>

                        <el-form label-position="top" size="small" class="plan-form">
                            <div class="form-grid four-columns">
                                <el-form-item label="股票代码">
                                    <el-input v-model="entryForm.stockCode"></el-input>
                                </el-form-item>
                                <el-form-item label="股票名称">
                                    <el-input v-model="entryForm.stockName"></el-input>
                                </el-form-item>
                                <el-form-item label="所属行业">
                                    <el-input v-model="entryForm.industry"></el-input>
                                </el-form-item>
                                <el-form-item label="计划类型">
                                    <div class="option-button-group">
                                        <el-button v-for="item in planTypeOptions" :key="item" size="mini"
                                            :type="entryForm.planType === item ? 'primary' : 'default'"
                                            @click="entryForm.planType = item">{{ item }}</el-button>
                                    </div>
                                </el-form-item>
                            </div>

                            <div class="form-grid two-columns">
                                <el-form-item label="计划周期">
                                    <el-date-picker v-model="entryForm.period" type="daterange" unlink-panels
                                        range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期"
                                        value-format="yyyy-MM-dd" style="width: 100%"></el-date-picker>
                                </el-form-item>
                                <el-form-item label="交易分类标签">
                                    <el-input v-model="entryForm.tags"></el-input>
                                </el-form-item>
                            </div>

                            <div class="form-grid two-columns">
                                <el-form-item label="开仓策略">
                                    <div class="option-button-group">
                                        <el-button v-for="item in openStrategyOptions" :key="item" size="mini"
                                            :type="entryForm.openStrategy === item ? 'primary' : 'default'"
                                            @click="entryForm.openStrategy = item">{{ item }}</el-button>
                                    </div>
                                </el-form-item>
                                <el-form-item label="平仓策略">
                                    <div class="option-button-group">
                                        <el-button v-for="item in closeStrategyOptions" :key="item" size="mini"
                                            :type="entryForm.closeStrategy === item ? 'primary' : 'default'"
                                            @click="entryForm.closeStrategy = item">{{ item }}</el-button>
                                    </div>
                                </el-form-item>
                            </div>

                            <el-form-item label="买入/卖出理由">
                                <el-input v-model="entryForm.reason" type="textarea" :rows="4"></el-input>
                            </el-form-item>

                            <div class="form-grid three-columns">
                                <el-form-item label="计划买入区间">
                                    <el-input v-model="entryForm.entryZone"></el-input>
                                </el-form-item>
                                <el-form-item label="止损位">
                                    <el-input v-model="entryForm.stopLoss"></el-input>
                                </el-form-item>
                                <el-form-item label="目标位">
                                    <el-input v-model="entryForm.targetPrice"></el-input>
                                </el-form-item>
                            </div>

                            <div class="form-grid two-columns">
                                <el-form-item label="大盘情况">
                                    <el-input v-model="entryForm.marketStatus" type="textarea" :rows="3"></el-input>
                                </el-form-item>
                                <el-form-item label="板块情况">
                                    <el-input v-model="entryForm.sectorStatus" type="textarea" :rows="3"></el-input>
                                </el-form-item>
                            </div>
                        </el-form>
                    </section>

                    <section class="panel panel-side">
                        <div class="panel-header compact">
                            <div>
                                <h2>计划修改记录</h2>
                                <p>修改采用追加，不覆盖原计划。</p>
                            </div>
                            <el-button size="mini" plain @click="openModificationDialog">追加修改</el-button>
                        </div>

                        <div class="timeline-stack">
                            <article v-for="item in modifications" :key="item.id" class="timeline-card">
                                <div class="timeline-head">
                                    <span class="timeline-time">{{ item.time }}</span>
                                    <div class="timeline-actions">
                                        <el-tag :type="item.tagType" size="mini">{{ item.label }}</el-tag>
                                        <el-button size="mini" type="text"
                                            @click="openModificationDialog(item)">修改</el-button>
                                        <el-button size="mini" type="text" class="danger-text-button"
                                            @click="deleteModification(item)">删除</el-button>
                                    </div>
                                </div>
                                <h3>{{ item.title }}</h3>
                                <p>{{ item.reason }}</p>
                                <div class="timeline-foot">
                                    <span>调整后计划：{{ item.plan }}</span>
                                </div>
                            </article>
                        </div>
                    </section>

                    <section class="panel panel-main">
                        <div class="panel-header compact">
                            <div>
                                <h2>执行明细</h2>
                                <p>按时间追加真实成交或模拟执行。</p>
                                <p class="field-help">“新增执行”用于追加一笔买入、卖出、加仓或减仓；“确认平仓”表示本轮剩余仓位已清零，准备进入复盘。</p>
                            </div>
                            <div class="header-actions">
                                <el-button size="mini" plain @click="openExecutionDialog">新增执行</el-button>
                                <el-button size="mini" type="success" @click="finishExecution">执行完毕</el-button>
                            </div>
                        </div>

                        <el-table :data="executionRecords" stripe size="mini" class="execution-table">
                            <el-table-column prop="time" label="时间" width="150"></el-table-column>
                            <el-table-column prop="action" label="动作" width="110"></el-table-column>
                            <el-table-column prop="price" label="价格" width="100"></el-table-column>
                            <el-table-column prop="volume" label="数量" width="100"></el-table-column>
                            <el-table-column prop="position" label="仓位变化" width="120"></el-table-column>
                            <el-table-column prop="note" label="阶段性偏差"></el-table-column>
                            <el-table-column label="操作" width="90">
                                <template slot-scope="scope">
                                    <el-button size="mini" type="text" class="danger-text-button"
                                        @click="deleteExecution(scope.row)">删除</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </section>

                    <section class="panel panel-side summary-panel">
                        <div class="panel-header compact">
                            <div>
                                <h2>结束摘要</h2>
                                <p>录入页底部直接看到本轮收口结果。</p>
                            </div>
                        </div>

                        <div class="summary-metrics">
                            <div>
                                <span>当前状态</span>
                                <strong>{{ reviewSummary.status }}</strong>
                            </div>
                            <div>
                                <span>执行次数</span>
                                <strong>{{ executionRecords.length }} 次</strong>
                            </div>
                            <div>
                                <span>修改次数</span>
                                <strong>{{ modifications.length }} 次</strong>
                            </div>
                            <div>
                                <span>平均成本</span>
                                <strong>{{ reviewSummary.avgPrice }}</strong>
                            </div>
                            <div>
                                <span>最新动作</span>
                                <strong>{{ getLatestExecutionText() }}</strong>
                            </div>
                            <div>
                                <span>计划风险收益比</span>
                                <strong>{{ getRiskRewardText() }}</strong>
                            </div>
                            <div>
                                <span>盈亏比例</span>
                                <strong :class="getPnlDisplayClass()">{{ getPnlRatioText() }}</strong>
                            </div>
                            <div>
                                <span>执行偏差</span>
                                <strong>{{ getExecutionDeviationText() }}</strong>
                            </div>
                        </div>
                    </section>
                </div>
            </el-tab-pane>

            <el-tab-pane label="复盘页面" name="review">
                <div class="review-grid">
                    <section class="panel review-main">
                        <div class="panel-header">
                            <div>
                                <h2>图表复盘区</h2>
                                <p>按 K 线、成交量、RSI、MACD 四个独立图表自上而下展示，时间范围保持一致。</p>
                                <p v-if="getDisplayStockCode()">当前标的：{{ getDisplayStockCode() }}</p>
                            </div>
                            <div class="header-actions">
                                <el-select v-model="selectedWatchSymbol" size="mini" class="watchlist-switcher"
                                    filterable clearable default-first-option placeholder="输入代码/名称快速选择"
                                    :loading="watchlistLoading" :filter-method="handleWatchlistQuery"
                                    @keyup.enter.native="selectFirstFilteredWatchSymbol"
                                    @change="handleWatchSymbolChange">
                                    <el-option v-for="item in displayWatchlistOptions" :key="item.value"
                                        :label="item.label" :value="item.value"></el-option>
                                </el-select>
                                <el-date-picker v-model="chartDateRange" size="mini" type="daterange" unlink-panels
                                    range-separator="至" start-placeholder="图表开始" end-placeholder="图表结束"
                                    value-format="yyyy-MM-dd" class="chart-range-picker"></el-date-picker>
                                <el-button size="mini" @click="applyLastHalfYearRange">近半年</el-button>
                                <el-button size="mini" type="primary" @click="reloadChartsByRange">刷新图表</el-button>
                            </div>
                        </div>
                        <div class="review-chart-stack">
                            <div class="chart-panel">
                                <div class="chart-panel-title">K 线</div>
                                <div ref="candlestickChart" class="review-chart review-chart-k"></div>
                            </div>
                            <div class="chart-panel">
                                <div class="chart-panel-title">成交量</div>
                                <div ref="volumeChart" class="review-chart review-chart-volume"></div>
                            </div>
                            <div class="chart-panel">
                                <div class="chart-panel-title">RSI</div>
                                <div ref="rsiChart" class="review-chart review-chart-rsi"></div>
                            </div>
                            <div class="chart-panel">
                                <div class="chart-panel-title">MACD</div>
                                <div ref="macdChart" class="review-chart review-chart-macd"></div>
                            </div>
                        </div>
                        <div class="chart-legend-grid">
                            <div class="legend-item">
                                <span class="legend-dot plan"></span>
                                <span>计划买入区间 / 止损 / 目标位</span>
                            </div>
                            <div class="legend-item">
                                <span class="legend-dot modify"></span>
                                <span>计划修改节点</span>
                            </div>
                            <div class="legend-item">
                                <span class="legend-dot trade"></span>
                                <span>实际买卖点</span>
                            </div>
                        </div>
                    </section>

                    <section class="panel review-side">
                        <div class="panel-header compact">
                            <div>
                                <h2>复盘摘要</h2>
                                <p>右侧展示结果摘要、主观反思、情绪记录和后续改进动作。</p>
                            </div>
                            <div class="header-actions">
                                <el-button size="mini" type="primary" @click="submitReview">保存复盘</el-button>
                            </div>
                        </div>

                        <div class="review-score-card">
                            <span>计划执行评分</span>
                            <strong>{{ reviewSummary.score }} / 5</strong>
                            <div class="score-button-group">
                                <el-button v-for="item in scoreOptions" :key="item" size="mini"
                                    :type="reviewSummary.score === item ? 'primary' : 'default'"
                                    @click="setPlanScore(item)">{{ item
                                    }}分</el-button>
                            </div>
                            <p>在复盘阶段直接给本轮计划打分，评价计划与执行的一致性。</p>
                        </div>

                        <div class="summary-metrics review-summary-metrics">
                            <div>
                                <span>平均成本</span>
                                <strong>{{ getAverageEntryPriceText() }}</strong>
                            </div>
                            <div>
                                <span>卖出价格</span>
                                <strong>{{ getExitPriceText() }}</strong>
                            </div>
                            <div>
                                <span>盈亏金额</span>
                                <strong :class="getPnlDisplayClass()">{{ getPnlAmountText() }}</strong>
                            </div>
                            <div>
                                <span>盈亏比例</span>
                                <strong :class="getPnlDisplayClass()">{{ getPnlRatioText() }}</strong>
                            </div>
                        </div>

                        <div class="insight-block">
                            <h3>做对的地方</h3>
                            <el-input v-model="reviewForm.didWell" type="textarea" :rows="4"
                                placeholder="记录本轮执行中做对的地方"></el-input>
                        </div>
                        <div class="insight-block">
                            <h3>做错的地方</h3>
                            <el-input v-model="reviewForm.didWrong" type="textarea" :rows="4"
                                placeholder="记录本轮执行中做错的地方"></el-input>
                        </div>

                        <div class="emotion-panel">
                            <h3>情绪记录</h3>
                            <div class="emotion-group">
                                <span>买入时</span>
                                <div class="option-button-group compact-group">
                                    <el-button v-for="item in emotionOptions" :key="`buy-${item}`" size="mini"
                                        :type="reviewForm.buyEmotion === item ? 'primary' : 'default'"
                                        @click="reviewForm.buyEmotion = item">{{ item }}</el-button>
                                </div>
                            </div>
                            <div class="emotion-group">
                                <span>持仓中</span>
                                <div class="option-button-group compact-group">
                                    <el-button v-for="item in emotionOptions" :key="`hold-${item}`" size="mini"
                                        :type="reviewForm.holdEmotion === item ? 'primary' : 'default'"
                                        @click="reviewForm.holdEmotion = item">{{ item }}</el-button>
                                </div>
                            </div>
                            <div class="emotion-group">
                                <span>卖出时</span>
                                <div class="option-button-group compact-group">
                                    <el-button v-for="item in emotionOptions" :key="`sell-${item}`" size="mini"
                                        :type="reviewForm.sellEmotion === item ? 'primary' : 'default'"
                                        @click="reviewForm.sellEmotion = item">{{ item }}</el-button>
                                </div>
                            </div>
                        </div>

                        <div class="improvement-card">
                            <h3>后续改进动作</h3>
                            <el-input v-model="reviewForm.improvementAction" type="textarea" :rows="4"
                                placeholder="填写下一次交易前必须执行的改进行动"></el-input>
                        </div>
                    </section>
                </div>
            </el-tab-pane>
        </el-tabs>

        <el-dialog :title="modificationEditingId ? '修改记录' : '追加修改'" :visible.sync="modificationDialogVisible"
            width="560px" destroy-on-close :before-close="handleModificationDialogClose">
            <el-form ref="modificationFormRef" :model="modificationForm" :rules="modificationRules" label-position="top"
                size="small" class="dialog-form">
                <el-form-item label="修改时间" prop="time">
                    <el-date-picker v-model="modificationForm.time" type="datetime" placeholder="选择修改时间"
                        value-format="yyyy-MM-dd HH:mm" style="width: 100%"></el-date-picker>
                </el-form-item>
                <el-form-item label="修改标题" prop="title">
                    <el-input v-model="modificationForm.title"></el-input>
                </el-form-item>
                <el-form-item label="修改依据" prop="reason">
                    <el-input v-model="modificationForm.reason" type="textarea" :rows="4"></el-input>
                </el-form-item>
                <el-form-item label="调整后的新计划" prop="plan">
                    <el-input v-model="modificationForm.plan" type="textarea" :rows="3"></el-input>
                </el-form-item>
                <el-form-item label="标签颜色">
                    <div class="option-button-group compact-group">
                        <el-button size="mini" :type="modificationForm.tagType === 'info' ? 'primary' : 'default'"
                            @click="modificationForm.tagType = 'info'">原计划</el-button>
                        <el-button size="mini" :type="modificationForm.tagType === 'warning' ? 'primary' : 'default'"
                            @click="modificationForm.tagType = 'warning'">一般调整</el-button>
                        <el-button size="mini" :type="modificationForm.tagType === 'danger' ? 'primary' : 'default'"
                            @click="modificationForm.tagType = 'danger'">重点调整</el-button>
                    </div>
                </el-form-item>
            </el-form>
            <span slot="footer">
                <el-button size="mini" @click="modificationDialogVisible = false">取消</el-button>
                <el-button size="mini" type="primary" @click="submitModification">保存修改</el-button>
            </span>
        </el-dialog>

        <el-dialog title="新增执行" :visible.sync="executionDialogVisible" width="560px" destroy-on-close
            :before-close="handleExecutionDialogClose">
            <el-form ref="executionFormRef" :model="executionForm" :rules="executionRules" label-position="top"
                size="small" class="dialog-form">
                <div class="form-grid two-columns">
                    <el-form-item label="执行时间" prop="time">
                        <el-date-picker v-model="executionForm.time" type="datetime" placeholder="选择执行时间"
                            value-format="yyyy-MM-dd HH:mm" style="width: 100%"></el-date-picker>
                    </el-form-item>
                    <el-form-item label="执行动作" prop="action">
                        <div class="option-button-group compact-group">
                            <el-button size="mini" :type="executionForm.action === '买入' ? 'primary' : 'default'"
                                @click="executionForm.action = '买入'">买入</el-button>
                            <el-button size="mini" :type="executionForm.action === '加仓' ? 'primary' : 'default'"
                                @click="executionForm.action = '加仓'">加仓</el-button>
                            <el-button size="mini" :type="executionForm.action === '减仓' ? 'primary' : 'default'"
                                @click="executionForm.action = '减仓'">减仓</el-button>
                            <el-button size="mini" :type="executionForm.action === '卖出' ? 'primary' : 'default'"
                                @click="executionForm.action = '卖出'">卖出</el-button>
                        </div>
                    </el-form-item>
                </div>
                <div class="form-grid three-columns">
                    <el-form-item label="价格" prop="price">
                        <el-input v-model="executionForm.price"></el-input>
                    </el-form-item>
                    <el-form-item label="数量" prop="volume">
                        <el-input v-model="executionForm.volume"></el-input>
                    </el-form-item>
                    <el-form-item label="仓位变化" prop="position">
                        <el-input v-model="executionForm.position"></el-input>
                    </el-form-item>
                </div>
                <el-form-item label="阶段性备注">
                    <el-input v-model="executionForm.note" type="textarea" :rows="3"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer">
                <el-button size="mini" @click="executionDialogVisible = false">取消</el-button>
                <el-button size="mini" type="primary" @click="submitExecution">保存执行</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import * as echarts from 'echarts';
import api from '@/api/investment_review';
import marketApi from '@/api/market_data';

const LOCAL_PLAN_ID = 'plan-local';

function createEmptyEntryForm() {
    return {
        stockCode: '',
        stockName: '',
        industry: '',
        planType: '',
        period: [],
        openStrategy: '',
        closeStrategy: '',
        reason: '',
        entryZone: '',
        stopLoss: '',
        targetPrice: '',
        marketStatus: '',
        sectorStatus: '',
        tags: ''
    };
}

function createEmptyReviewFormState() {
    return {
        didWell: '',
        didWrong: '',
        buyEmotion: '',
        holdEmotion: '',
        sellEmotion: '',
        improvementAction: ''
    };
}

function createEmptyReviewSummary() {
    return {
        status: '未开始执行',
        score: 0,
        pnl: '--',
        pnlClass: '',
        avgPrice: '--',
        exitPrice: '--',
        deviation: '暂无'
    };
}

export default {
    data() {
        return {
            activeTab: 'entry',
            charts: {},
            modificationDialogVisible: false,
            executionDialogVisible: false,
            modificationEditingId: null,
            currentPlanId: LOCAL_PLAN_ID,
            previousPlanId: LOCAL_PLAN_ID,
            planRecords: {},
            reviewDraftBaseline: '',
            reviewSummary: createEmptyReviewSummary(),
            scoreOptions: [1, 2, 3, 4, 5],
            planTypeOptions: ['执行计划', '观察计划'],
            openStrategyOptions: ['趋势回调', '突破买入', '指标共振', '分批建仓'],
            closeStrategyOptions: ['目标止盈', '移动止盈', '止损卖出', '趋势终结卖出'],
            planOptions: [],
            watchlistLoading: false,
            watchlistOptions: [],
            selectedWatchSymbol: '',
            watchlistKeyword: '',
            chartDateRange: [],
            entryForm: createEmptyEntryForm(),
            reviewForm: createEmptyReviewFormState(),
            emotionOptions: ['平静', '谨慎', '焦虑', '犹豫', '贪婪', '恐惧', '克制'],
            modificationForm: {
                time: '',
                title: '',
                reason: '',
                plan: '',
                tagType: 'warning'
            },
            executionForm: {
                time: '',
                action: '买入',
                price: '',
                volume: '',
                position: '',
                note: ''
            },
            modificationRules: {
                time: [{ required: true, message: '请填写修改时间', trigger: 'blur' }],
                title: [{ required: true, message: '请填写修改标题', trigger: 'blur' }],
                reason: [{ required: true, message: '请填写修改依据', trigger: 'blur' }],
                plan: [{ required: true, message: '请填写调整后的新计划', trigger: 'blur' }]
            },
            executionRules: {
                time: [{ required: true, message: '请填写执行时间', trigger: 'blur' }],
                action: [{ required: true, message: '请选择执行动作', trigger: 'change' }],
                price: [{ required: true, message: '请填写价格', trigger: 'blur' }],
                volume: [{ required: true, message: '请填写数量', trigger: 'blur' }],
                position: [{ required: true, message: '请填写仓位变化', trigger: 'blur' }]
            },
            modifications: [],
            executionRecords: []
        };
    },
    computed: {
        displayWatchlistOptions() {
            const keyword = String(this.watchlistKeyword || '').trim().toUpperCase();
            if (!keyword) {
                return this.watchlistOptions;
            }
            return this.watchlistOptions.filter((item) => {
                const code = String(item.displayCode || '').toUpperCase();
                const name = String(item.symbolName || '').toUpperCase();
                const type = String(item.symbolType || '').toUpperCase();
                return code.includes(keyword) || name.includes(keyword) || type.includes(keyword);
            });
        }
    },
    mounted() {
        this.initCharts();
        window.addEventListener('resize', this.handleResize);
        window.addEventListener('beforeunload', this.handleBeforeUnload);
        this.loadWatchlistOptions();
        // try to load remote plans; fallback to local store on failure
        this.loadRemotePlans().catch(() => {
            this.initializePlanStore();
        });
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.handleResize);
        window.removeEventListener('beforeunload', this.handleBeforeUnload);
        this.disposeCharts();
    },
    methods: {
        handleResize() {
            Object.values(this.charts).forEach((chart) => {
                if (chart) {
                    chart.resize();
                }
            });
        },
        disposeCharts() {
            Object.keys(this.charts).forEach((key) => {
                if (this.charts[key]) {
                    this.charts[key].dispose();
                }
            });
            this.charts = {};
        },
        initializePlanStore() {
            if (!this.currentPlanId) {
                this.currentPlanId = LOCAL_PLAN_ID;
            }
            this.planRecords = {
                [this.currentPlanId]: this.createEmptyPlanState()
            };
            this.planOptions = [{
                id: this.currentPlanId,
                label: this.buildPlanLabel(this.planRecords[this.currentPlanId].entryForm)
            }];
            this.applyPlanSnapshot(this.planRecords[this.currentPlanId]);
            this.previousPlanId = this.currentPlanId;
            this.updatePlanOptionLabel(this.currentPlanId);
        },

        async loadRemotePlans() {
            const resp = await api.queryList({});
            if (!resp || !resp.data || resp.data.code !== 200) {
                throw new Error('无法获取计划列表');
            }
            const rows = resp.data.data || [];
            if (!rows || rows.length === 0) {
                this.initializePlanStore();
                return;
            }
            this.planOptions = rows.map((row) => ({ id: row.plan_code || String(row.id), label: `${row.stock_name || '未命名'} | ${this.stripMarketSuffix(row.stock_code) || ''}` }));
            // choose first plan by default
            this.currentPlanId = this.planOptions[0].id;
            this.previousPlanId = this.currentPlanId;
            await this.loadPlanDetail(this.currentPlanId);
        },
        async loadWatchlistOptions() {
            this.watchlistLoading = true;
            try {
                const resp = await marketApi.listWatchlist({ enabled: 1 });
                if (!resp || !resp.data || resp.data.code !== 200) {
                    throw new Error((resp && resp.data && resp.data.message) || '加载观察池失败');
                }
                const rows = resp.data.data || [];
                this.watchlistOptions = rows.map((row) => ({
                    value: row.symbol_code,
                    displayCode: this.stripMarketSuffix(row.symbol_code),
                    label: `${this.stripMarketSuffix(row.symbol_code)} | ${row.symbol_name || '未命名'} | ${row.symbol_type || ''}`,
                    symbolName: row.symbol_name || '',
                    symbolType: row.symbol_type || ''
                }));
            } catch (err) {
                console.error(err);
            } finally {
                this.watchlistLoading = false;
            }
        },
        handleWatchlistQuery(query) {
            this.watchlistKeyword = query;
        },
        selectFirstFilteredWatchSymbol() {
            if (!this.displayWatchlistOptions.length) {
                return;
            }
            const first = this.displayWatchlistOptions[0];
            this.selectedWatchSymbol = first.value;
            this.handleWatchSymbolChange(first.value);
        },
        handleWatchSymbolChange(symbolCode) {
            if (!symbolCode) {
                return;
            }
            const selected = this.watchlistOptions.find((item) => item.value === symbolCode);
            this.entryForm.stockCode = this.stripMarketSuffix(symbolCode);
            if (selected && selected.symbolName) {
                this.entryForm.stockName = selected.symbolName;
            }
            if (!this.entryForm.planType) {
                this.entryForm.planType = '观察计划';
            }
            this.$nextTick(() => this.initCharts());
        },
        formatDate(dateObj) {
            const year = dateObj.getFullYear();
            const month = String(dateObj.getMonth() + 1).padStart(2, '0');
            const day = String(dateObj.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        applyLastHalfYearRange() {
            const end = new Date();
            const start = new Date(end.getTime());
            start.setDate(start.getDate() - 180);
            this.chartDateRange = [this.formatDate(start), this.formatDate(end)];
            this.reloadChartsByRange();
        },
        reloadChartsByRange() {
            this.$nextTick(() => this.initCharts());
        },
        getChartQueryDateRange() {
            if (Array.isArray(this.chartDateRange) && this.chartDateRange.length >= 2) {
                return {
                    startDate: this.chartDateRange[0] || null,
                    endDate: this.chartDateRange[1] || null
                };
            }
            if (Array.isArray(this.entryForm.period) && this.entryForm.period.length >= 2) {
                return {
                    startDate: this.entryForm.period[0] || null,
                    endDate: this.entryForm.period[1] || null
                };
            }
            return {
                startDate: null,
                endDate: null
            };
        },

        async loadPlanDetail(planCodeOrId) {
            const resp = await api.getDetail({ plan_code: planCodeOrId, currentPlanId: planCodeOrId });
            if (!resp || !resp.data || resp.data.code !== 200) {
                throw new Error('无法获取计划详情');
            }
            const data = resp.data.data || {};
            const snapshot = this.buildRemoteSnapshot(data);
            this.planRecords[planCodeOrId] = snapshot;
            if (this.currentPlanId === planCodeOrId) {
                this.applyPlanSnapshot(snapshot);
                this.updatePlanOptionLabel(this.currentPlanId);
            }
        },
        async handlePlanChange(newPlanId) {
            if (newPlanId === this.previousPlanId) {
                return;
            }
            const canLeave = await this.confirmDiscardReviewChanges();
            if (!canLeave) {
                this.currentPlanId = this.previousPlanId;
                return;
            }
            if (this.previousPlanId && this.planRecords[this.previousPlanId] && !this.hasPendingReviewChanges()) {
                this.planRecords[this.previousPlanId] = this.buildPlanSnapshot();
                this.updatePlanOptionLabel(this.previousPlanId);
            }
            if (!this.planRecords[newPlanId]) {
                try {
                    await this.loadPlanDetail(newPlanId);
                } catch (err) {
                    console.error(err);
                    this.$message({ message: '加载计划详情失败', type: 'error' });
                    return;
                }
            }
            this.applyPlanSnapshot(this.planRecords[newPlanId]);
            this.previousPlanId = newPlanId;
        },
        async createNewPlan() {
            const canLeave = await this.confirmDiscardReviewChanges();
            if (!canLeave) {
                return;
            }
            if (this.currentPlanId && this.planRecords[this.currentPlanId]) {
                this.planRecords[this.currentPlanId] = this.buildPlanSnapshot();
                this.updatePlanOptionLabel(this.currentPlanId);
            }
            const newPlanId = `plan-${Date.now()}`;
            const newPlan = this.createEmptyPlanState();
            this.planRecords[newPlanId] = newPlan;
            this.planOptions.unshift({
                id: newPlanId,
                label: this.buildPlanLabel(newPlan.entryForm)
            });
            this.currentPlanId = newPlanId;
            this.previousPlanId = newPlanId;
            this.applyPlanSnapshot(newPlan);
            this.$message({
                message: '已创建新计划。',
                type: 'success'
            });
        },
        async saveCurrentPlan(showMessage = true) {
            try {
                this.entryForm.stockCode = this.normalizeSymbolCodeForSubmit(this.entryForm.stockCode);
            } catch (err) {
                this.$message({ message: err.message || '股票代码格式错误', type: 'error' });
                return null;
            }
            this.planRecords[this.currentPlanId] = this.buildPlanSnapshot();
            this.updatePlanOptionLabel(this.currentPlanId);
            const payload = this.buildPersistPayload(this.planRecords[this.currentPlanId], this.currentPlanId);
            try {
                const resp = await api.saveBundle(payload);
                if (resp && resp.data && resp.data.code === 200) {
                    const data = resp.data.data || {};
                    if (data.plan && data.plan.plan_code) {
                        const newCode = data.plan.plan_code;
                        if (newCode !== this.currentPlanId) {
                            this.planRecords[newCode] = this.planRecords[this.currentPlanId];
                            delete this.planRecords[this.currentPlanId];
                            const opt = this.planOptions.find((o) => o.id === this.currentPlanId);
                            if (opt) opt.id = newCode;
                            this.currentPlanId = newCode;
                        }
                    }
                    const snapshot = this.buildRemoteSnapshot(data);
                    this.planRecords[this.currentPlanId] = snapshot;
                    this.applyPlanSnapshot(snapshot);
                    this.previousPlanId = this.currentPlanId;
                    this.updatePlanOptionLabel(this.currentPlanId);
                    if (showMessage) {
                        this.$message({ message: '计划已保存。', type: 'success' });
                    }
                    return data;
                } else {
                    this.$message({ message: (resp && resp.data && resp.data.message) || '保存失败', type: 'error' });
                }
            } catch (err) {
                console.error(err);
                this.$message({ message: '保存时发生错误', type: 'error' });
            }
            return null;
        },
        openModificationDialog(item = null) {
            if (item) {
                this.modificationEditingId = item.id || null;
                this.modificationForm = {
                    time: item.time || this.getDefaultTime(),
                    title: item.title || '',
                    reason: item.reason || '',
                    plan: item.plan || '',
                    tagType: item.tagType || 'warning'
                };
                if (this.$refs.modificationFormRef) {
                    this.$refs.modificationFormRef.clearValidate();
                }
            } else {
                this.resetModificationForm();
            }
            this.modificationDialogVisible = true;
        },
        setPlanScore(score) {
            this.reviewSummary.score = score;
        },
        openExecutionDialog() {
            this.resetExecutionForm();
            this.executionDialogVisible = true;
        },
        async submitReview(showMessage = true) {
            const currentReviewForm = JSON.parse(JSON.stringify(this.reviewForm));
            const currentReviewSummary = JSON.parse(JSON.stringify(this.reviewSummary));
            const savedPlan = await this.saveCurrentPlan(false);
            if (!savedPlan) {
                return;
            }
            this.reviewForm = currentReviewForm;
            this.reviewSummary = currentReviewSummary;
            try {
                const resp = await api.saveReview({
                    currentPlanId: this.currentPlanId,
                    plan_code: this.currentPlanId,
                    entryForm: this.entryForm,
                    reviewForm: this.reviewForm,
                    reviewSummary: this.reviewSummary,
                    modifications: this.modifications,
                    executionRecords: this.executionRecords
                });
                if (!resp || !resp.data || resp.data.code !== 200) {
                    throw new Error((resp && resp.data && resp.data.message) || '保存复盘失败');
                }
                const snapshot = this.buildRemoteSnapshot(resp.data.data || {});
                this.planRecords[this.currentPlanId] = snapshot;
                this.applyPlanSnapshot(snapshot);
                this.updatePlanOptionLabel(this.currentPlanId);
                if (showMessage) {
                    this.$message({ message: '复盘已保存并完成回读。', type: 'success' });
                }
            } catch (err) {
                console.error(err);
                this.$message({ message: err.message || '保存复盘失败', type: 'error' });
            }
        },
        async deleteModification(item) {
            if (!item || !item.id) {
                return;
            }
            try {
                await this.$confirm('确认删除这条计划修改记录吗？删除后不再参与统计。', '提示', {
                    type: 'warning'
                });
                const resp = await api.deleteModification({
                    plan_code: this.currentPlanId,
                    currentPlanId: this.currentPlanId,
                    modification_id: item.id
                });
                if (!resp || !resp.data || resp.data.code !== 200) {
                    throw new Error((resp && resp.data && resp.data.message) || '删除修改记录失败');
                }
                const snapshot = this.buildRemoteSnapshot(resp.data.data || {});
                this.planRecords[this.currentPlanId] = snapshot;
                this.applyPlanSnapshot(snapshot);
                this.$message({ message: '修改记录已删除。', type: 'success' });
            } catch (err) {
                if (err === 'cancel') {
                    return;
                }
                console.error(err);
                this.$message({ message: err.message || '删除修改记录失败', type: 'error' });
            }
        },
        submitModification() {
            this.$refs.modificationFormRef.validate(async (valid) => {
                if (!valid) {
                    return;
                }
                const modification = {
                    id: this.modificationEditingId,
                    time: this.modificationForm.time,
                    label: this.modificationEditingId ? '修改' : '新增修改',
                    tagType: this.modificationForm.tagType,
                    title: this.modificationForm.title,
                    reason: this.modificationForm.reason,
                    plan: this.modificationForm.plan
                };
                try {
                    const resp = await api.saveModification({
                        plan_code: this.currentPlanId,
                        currentPlanId: this.currentPlanId,
                        modification
                    });
                    if (!resp || !resp.data || resp.data.code !== 200) {
                        throw new Error((resp && resp.data && resp.data.message) || '保存修改失败');
                    }
                    const snapshot = this.buildRemoteSnapshot(resp.data.data || {});
                    this.planRecords[this.currentPlanId] = snapshot;
                    this.applyPlanSnapshot(snapshot);
                    this.modificationDialogVisible = false;
                    const wasEditing = Boolean(this.modificationEditingId);
                    this.resetModificationForm();
                    this.$message({ message: wasEditing ? '修改记录已更新。' : '修改已保存。', type: 'success' });
                } catch (err) {
                    console.error(err);
                    this.$message({ message: err.message || '保存修改失败', type: 'error' });
                }
            });
        },
        async deleteExecution(item) {
            if (!item || !item.id) {
                return;
            }
            try {
                await this.$confirm('确认删除这条执行记录吗？删除后不会参与统计。', '提示', {
                    type: 'warning'
                });
                const resp = await api.deleteExecution({
                    plan_code: this.currentPlanId,
                    currentPlanId: this.currentPlanId,
                    execution_id: item.id
                });
                if (!resp || !resp.data || resp.data.code !== 200) {
                    throw new Error((resp && resp.data && resp.data.message) || '删除执行记录失败');
                }
                const snapshot = this.buildRemoteSnapshot(resp.data.data || {});
                this.planRecords[this.currentPlanId] = snapshot;
                this.applyPlanSnapshot(snapshot);
                this.$message({ message: '执行记录已删除。', type: 'success' });
            } catch (err) {
                if (err === 'cancel') {
                    return;
                }
                console.error(err);
                this.$message({ message: err.message || '删除执行记录失败', type: 'error' });
            }
        },
        submitExecution() {
            this.$refs.executionFormRef.validate(async (valid) => {
                if (!valid) {
                    return;
                }
                const execution = {
                    time: this.executionForm.time,
                    action: this.executionForm.action,
                    price: this.executionForm.price,
                    volume: this.executionForm.volume,
                    position: this.executionForm.position,
                    note: this.executionForm.note || '待补充执行说明'
                };
                try {
                    const resp = await api.saveExecution({
                        plan_code: this.currentPlanId,
                        currentPlanId: this.currentPlanId,
                        execution
                    });
                    if (!resp || !resp.data || resp.data.code !== 200) {
                        throw new Error((resp && resp.data && resp.data.message) || '保存执行失败');
                    }
                    const snapshot = this.buildRemoteSnapshot(resp.data.data || {});
                    this.planRecords[this.currentPlanId] = snapshot;
                    this.applyPlanSnapshot(snapshot);
                    this.executionDialogVisible = false;
                    this.resetExecutionForm();
                    this.$message({ message: '执行已保存。', type: 'success' });
                } catch (err) {
                    console.error(err);
                    this.$message({ message: err.message || '保存执行失败', type: 'error' });
                }
            });
        },
        finishExecution() {
            const latestExecution = this.executionRecords[0] || {};
            this.reviewSummary.status = '已平仓待复盘';
            this.reviewSummary.exitPrice = latestExecution.price || this.reviewSummary.exitPrice;
            if (this.executionRecords.length > 0) {
                this.reviewSummary.avgPrice = this.calculateAveragePrice();
            }
            this.saveCurrentPlan(false);
            this.activeTab = 'review';
            this.$message({
                message: '已标记为执行完毕，并切换到复盘页面。',
                type: 'success'
            });
        },
        handleModificationDialogClose(done) {
            if (!this.isModificationDirty()) {
                done();
                return;
            }
            this.$confirm('修改内容尚未保存，确认关闭吗？', '提示', {
                type: 'warning'
            }).then(() => {
                done();
                this.resetModificationForm();
            }).catch(() => { });
        },
        handleExecutionDialogClose(done) {
            if (!this.isExecutionDirty()) {
                done();
                return;
            }
            this.$confirm('执行内容尚未保存，确认关闭吗？', '提示', {
                type: 'warning'
            }).then(() => {
                done();
                this.resetExecutionForm();
            }).catch(() => { });
        },
        handleBeforeUnload(event) {
            if (!this.hasPendingReviewChanges()) {
                return undefined;
            }
            const message = '复盘内容尚未保存，确认离开吗？';
            event.preventDefault();
            event.returnValue = message;
            return message;
        },
        handleBeforeTabLeave(activeName, oldName) {
            if (activeName === 'review') {
                this.$nextTick(() => this.initCharts());
            }
            if (oldName !== 'review' || !this.hasPendingReviewChanges()) {
                return true;
            }
            return this.$confirm('复盘内容尚未保存，确认离开当前页签吗？', '提示', {
                type: 'warning'
            }).then(() => true).catch(() => false);
        },
        async confirmDiscardReviewChanges() {
            if (!this.hasPendingReviewChanges()) {
                return true;
            }
            try {
                await this.$confirm('复盘内容尚未保存，切换计划后将丢失当前改动，是否继续？', '提示', {
                    type: 'warning'
                });
                return true;
            } catch (err) {
                return false;
            }
        },
        buildReviewDraftSignature() {
            return JSON.stringify({
                score: this.reviewSummary.score,
                reviewForm: this.reviewForm,
            });
        },
        syncReviewDraftBaseline() {
            this.reviewDraftBaseline = this.buildReviewDraftSignature();
        },
        hasPendingReviewChanges() {
            return this.buildReviewDraftSignature() !== this.reviewDraftBaseline;
        },
        isModificationDirty() {
            return Boolean(
                this.modificationForm.time ||
                this.modificationForm.title ||
                this.modificationForm.reason ||
                this.modificationForm.plan
            );
        },
        isExecutionDirty() {
            return Boolean(
                this.executionForm.time ||
                this.executionForm.price ||
                this.executionForm.volume ||
                this.executionForm.position ||
                this.executionForm.note ||
                this.executionForm.action !== '买入'
            );
        },
        resetModificationForm() {
            this.modificationEditingId = null;
            this.modificationForm = {
                time: this.getDefaultTime(),
                title: '',
                reason: '',
                plan: '',
                tagType: 'warning'
            };
            if (this.$refs.modificationFormRef) {
                this.$refs.modificationFormRef.clearValidate();
            }
        },
        resetExecutionForm() {
            this.executionForm = {
                time: this.getDefaultTime(),
                action: '买入',
                price: '',
                volume: '',
                position: '',
                note: ''
            };
            if (this.$refs.executionFormRef) {
                this.$refs.executionFormRef.clearValidate();
            }
        },
        getDefaultTime() {
            const now = new Date();
            const pad = (value) => String(value).padStart(2, '0');
            return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}`;
        },
        buildPlanSnapshot() {
            return JSON.parse(JSON.stringify({
                entryForm: this.entryForm,
                reviewForm: this.reviewForm,
                modifications: this.modifications,
                executionRecords: this.executionRecords,
                reviewSummary: this.reviewSummary
            }));
        },
        buildPersistPayload(snapshot, currentPlanId) {
            const currentYear = String(new Date().getFullYear());
            const normalizeDateTime = (value) => {
                const text = String(value || '').trim();
                if (!text) {
                    return '';
                }
                if (/^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}(?::\d{2})?)?$/.test(text)) {
                    return text.length === 16 ? `${text}:00` : text;
                }
                if (/^\d{2}-\d{2} \d{2}:\d{2}$/.test(text)) {
                    return `${currentYear}-${text}:00`;
                }
                if (/^\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(text)) {
                    return `${currentYear}-${text}`;
                }
                return text;
            };

            return {
                currentPlanId,
                entryForm: snapshot.entryForm,
                reviewSummary: {
                    status: (snapshot.reviewSummary && snapshot.reviewSummary.status) || '未开始执行'
                },
                modifications: (snapshot.modifications || []).map((item) => Object.assign({}, item, {
                    time: normalizeDateTime(item.time)
                })),
                executionRecords: (snapshot.executionRecords || []).map((item) => Object.assign({}, item, {
                    time: normalizeDateTime(item.time)
                }))
            };
        },
        buildRemoteSnapshot(data) {
            const plan = data.plan || {};
            const review = data.review || {};
            let snapshot = null;
            let reviewSnapshot = null;
            if (plan.current_plan_snapshot_json) {
                try {
                    snapshot = JSON.parse(plan.current_plan_snapshot_json);
                } catch (err) {
                    console.error(err);
                }
            }
            if (review.review_snapshot_json) {
                try {
                    reviewSnapshot = JSON.parse(review.review_snapshot_json);
                } catch (err) {
                    console.error(err);
                }
            }

            const fallbackEntryForm = {
                stockCode: plan.stock_code || '',
                stockName: plan.stock_name || '',
                industry: plan.industry || '',
                planType: plan.plan_type || '',
                period: [plan.period_start || '', plan.period_end || ''].filter(Boolean),
                openStrategy: plan.open_strategy || '',
                closeStrategy: plan.close_strategy || '',
                reason: plan.reason || '',
                entryZone: plan.entry_zone || '',
                stopLoss: plan.stop_loss || '',
                targetPrice: plan.target_price || '',
                marketStatus: plan.market_status || '',
                sectorStatus: plan.sector_status || '',
                tags: plan.tags_text || ''
            };

            const modifications = (data.modifications || []).map((m) => ({
                id: m.id,
                time: m.modification_time,
                label: m.modification_label || '修改',
                tagType: m.tag_type,
                title: m.title,
                reason: m.reason,
                plan: m.updated_plan
            }));

            const executionRecords = (data.executions || []).map((e) => ({
                id: e.id,
                time: e.execution_time,
                action: e.action,
                price: e.price,
                volume: e.volume,
                position: e.position_text || '',
                note: e.note
            }));

            const reviewSummary = {
                status: review.review_status || plan.plan_status || '未开始执行',
                score: plan.plan_score || 0,
                pnl: review.realized_pnl_ratio ? `${review.realized_pnl_ratio}%` : '--',
                pnlClass: review.realized_pnl_amount > 0 ? 'positive' : (review.realized_pnl_amount < 0 ? 'negative' : ''),
                avgPrice: review.avg_entry_price || '--',
                exitPrice: review.exit_price || '--',
                deviation: review.execution_deviation || '暂无'
            };

            const fallbackReviewForm = {
                didWell: review.did_well || '',
                didWrong: review.did_wrong || '',
                buyEmotion: review.buy_emotion || '',
                holdEmotion: review.hold_emotion || '',
                sellEmotion: review.sell_emotion || '',
                improvementAction: review.improvement_action || ''
            };

            return {
                entryForm: (snapshot && snapshot.entryForm) || fallbackEntryForm,
                reviewForm: (reviewSnapshot && reviewSnapshot.reviewForm) || (snapshot && snapshot.reviewForm) || fallbackReviewForm || this.createEmptyReviewForm(),
                modifications: modifications.length ? modifications : ((snapshot && snapshot.modifications) || []),
                executionRecords: executionRecords.length ? executionRecords : ((snapshot && snapshot.executionRecords) || []),
                reviewSummary: Object.assign({}, createEmptyReviewSummary(), (snapshot && snapshot.reviewSummary) || {}, (reviewSnapshot && reviewSnapshot.reviewSummary) || {}, reviewSummary)
            };
        },
        applyPlanSnapshot(snapshot) {
            if (!snapshot) {
                return;
            }
            this.entryForm = JSON.parse(JSON.stringify(snapshot.entryForm));
            this.chartDateRange = Array.isArray(this.entryForm.period) && this.entryForm.period.length >= 2
                ? [this.entryForm.period[0], this.entryForm.period[1]]
                : [];
            this.reviewForm = JSON.parse(JSON.stringify(snapshot.reviewForm || this.createEmptyReviewForm()));
            this.modifications = JSON.parse(JSON.stringify(snapshot.modifications));
            this.executionRecords = JSON.parse(JSON.stringify(snapshot.executionRecords));
            this.reviewSummary = JSON.parse(JSON.stringify(snapshot.reviewSummary));
            this.syncReviewDraftBaseline();
            this.$nextTick(() => this.initCharts());
        },
        createEmptyReviewForm() {
            return createEmptyReviewFormState();
        },
        createEmptyPlanState() {
            return {
                entryForm: createEmptyEntryForm(),
                reviewForm: this.createEmptyReviewForm(),
                modifications: [],
                executionRecords: [],
                reviewSummary: createEmptyReviewSummary()
            };
        },
        stripMarketSuffix(code) {
            const text = String(code || '').trim();
            if (!text) {
                return '';
            }
            return text.replace(/\.(SH|SZ)$/i, '');
        },
        normalizeSymbolCodeForSubmit(symbolCode) {
            const raw = String(symbolCode || '').trim().toUpperCase();
            if (!raw) {
                return '';
            }
            if (/^(SH|SZ)\d{6}$/.test(raw)) {
                return `${raw.slice(2)}.${raw.slice(0, 2)}`;
            }
            if (/^\d{6}\.(SH|SZ)$/.test(raw)) {
                return raw;
            }
            if (!/^\d{6}$/.test(raw)) {
                throw new Error('股票代码格式不正确，请输入 6 位数字，例如 300750');
            }
            if (raw.startsWith('6') || raw.startsWith('5') || raw.startsWith('9')) {
                return `${raw}.SH`;
            }
            return `${raw}.SZ`;
        },
        getDisplayStockCode() {
            return this.stripMarketSuffix(this.entryForm.stockCode);
        },
        buildPlanLabel(form) {
            const stockName = form.stockName || '未命名计划';
            const stockCode = this.stripMarketSuffix(form.stockCode) || '未填代码';
            const planType = form.planType || '未设置类型';
            return `${stockName} | ${stockCode} | ${planType}`;
        },
        updatePlanOptionLabel(planId) {
            const option = this.planOptions.find((item) => item.id === planId);
            const snapshot = this.planRecords[planId];
            if (option && snapshot) {
                option.label = this.buildPlanLabel(snapshot.entryForm);
            }
        },
        calculateAveragePrice() {
            let totalAmount = 0;
            let totalVolume = 0;
            this.executionRecords.forEach((item) => {
                if (item.action !== '买入' && item.action !== '加仓') {
                    return;
                }
                const numericPrice = Number(item.price);
                const numericVolume = this.getNumericVolume(item.volume);
                if (!Number.isNaN(numericPrice) && !Number.isNaN(numericVolume) && numericVolume > 0) {
                    totalAmount += numericPrice * numericVolume;
                    totalVolume += numericVolume;
                }
            });
            if (!totalVolume) {
                return this.reviewSummary.avgPrice;
            }
            return (totalAmount / totalVolume).toFixed(2);
        },
        getNumericVolume(value) {
            const numericVolume = Number(String(value || '').replace(/[^\d.]/g, ''));
            return Number.isNaN(numericVolume) ? Number.NaN : numericVolume;
        },
        getAverageEntryPriceValue() {
            const averagePrice = Number(this.calculateAveragePrice());
            return Number.isNaN(averagePrice) ? Number.NaN : averagePrice;
        },
        getAverageEntryPriceText() {
            const averagePrice = this.getAverageEntryPriceValue();
            if (!Number.isFinite(averagePrice) || averagePrice <= 0) {
                return '--';
            }
            return averagePrice.toFixed(2);
        },
        getExitPriceValue() {
            const exitExecutions = this.executionRecords
                .filter((item) => item.action === '卖出' || item.action === '减仓')
                .map((item) => ({
                    ...item,
                    price: Number(item.price)
                }))
                .filter((item) => !Number.isNaN(item.price))
                .sort((first, second) => String(second.time).localeCompare(String(first.time)));

            if (exitExecutions.length > 0) {
                return exitExecutions[0].price;
            }

            const fallbackExitPrice = Number(this.reviewSummary.exitPrice);
            return Number.isNaN(fallbackExitPrice) ? Number.NaN : fallbackExitPrice;
        },
        getExitPriceText() {
            const exitPrice = this.getExitPriceValue();
            if (!Number.isFinite(exitPrice) || exitPrice <= 0) {
                return '--';
            }
            return exitPrice.toFixed(2);
        },
        getExitedVolume() {
            return this.executionRecords
                .filter((item) => item.action === '卖出' || item.action === '减仓')
                .reduce((totalVolume, item) => {
                    const numericVolume = this.getNumericVolume(item.volume);
                    if (!Number.isFinite(numericVolume) || numericVolume <= 0) {
                        return totalVolume;
                    }
                    return totalVolume + numericVolume;
                }, 0);
        },
        getPnlAmountValue() {
            const averagePrice = this.getAverageEntryPriceValue();
            const exitPrice = this.getExitPriceValue();
            const exitedVolume = this.getExitedVolume();
            if (!Number.isFinite(averagePrice) || !Number.isFinite(exitPrice) || !Number.isFinite(exitedVolume) || exitedVolume <= 0) {
                return Number.NaN;
            }
            return (exitPrice - averagePrice) * exitedVolume;
        },
        getPnlAmountText() {
            const pnlAmount = this.getPnlAmountValue();
            if (!Number.isFinite(pnlAmount)) {
                return '--';
            }
            const prefix = pnlAmount > 0 ? '+' : '';
            return `${prefix}${pnlAmount.toFixed(2)}`;
        },
        getPnlRatioValue() {
            const averagePrice = this.getAverageEntryPriceValue();
            const exitPrice = this.getExitPriceValue();
            if (!Number.isFinite(averagePrice) || !Number.isFinite(exitPrice) || averagePrice <= 0) {
                return Number.NaN;
            }
            return ((exitPrice - averagePrice) / averagePrice) * 100;
        },
        getPnlRatioText() {
            const pnlRatio = this.getPnlRatioValue();
            if (!Number.isFinite(pnlRatio)) {
                return '--';
            }
            const prefix = pnlRatio > 0 ? '+' : '';
            return `${prefix}${pnlRatio.toFixed(2)}%`;
        },
        getPnlDisplayClass() {
            const pnlAmount = this.getPnlAmountValue();
            if (!Number.isFinite(pnlAmount) || pnlAmount === 0) {
                return '';
            }
            return pnlAmount > 0 ? 'positive' : 'negative';
        },
        getLatestExecutionText() {
            const latestExecution = this.executionRecords[0];
            if (!latestExecution) {
                return '暂无';
            }
            return `${latestExecution.action} @ ${latestExecution.price}`;
        },
        getExecutionDeviationText() {
            const entryExecutions = this.getChronologicalEntryExecutions();
            if (entryExecutions.length === 0) {
                return '未执行';
            }
            const firstEntry = entryExecutions[0];
            const entryRange = this.getEntryRange();
            const deviations = [];

            if (entryRange) {
                if (firstEntry.price > entryRange.max) {
                    deviations.push('高于计划区间买入');
                } else if (firstEntry.price < entryRange.min) {
                    deviations.push('低于计划区间提前买入');
                }
            }

            if (this.modifications.length > 1) {
                deviations.push(`有${this.modifications.length - 1}次计划调整`);
            }

            const hasReduceBeforeExit = this.executionRecords.some((item) => item.action === '减仓');
            if (hasReduceBeforeExit) {
                deviations.push('过程中存在主动减仓');
            }

            if (deviations.length === 0) {
                return '基本按计划执行';
            }
            return deviations.join('，');
        },
        getRiskRewardText() {
            const entryPrice = this.getEntryReferencePrice();
            const stopLoss = Number(this.entryForm.stopLoss);
            const targetPrice = Number(this.entryForm.targetPrice);
            if (!entryPrice || Number.isNaN(stopLoss) || Number.isNaN(targetPrice) || entryPrice <= stopLoss) {
                return '--';
            }
            const ratio = (targetPrice - entryPrice) / (entryPrice - stopLoss);
            if (!Number.isFinite(ratio)) {
                return '--';
            }
            return `1 : ${ratio.toFixed(2)}`;
        },
        getChronologicalEntryExecutions() {
            return [...this.executionRecords]
                .filter((item) => item.action === '买入' || item.action === '加仓')
                .map((item) => ({
                    ...item,
                    price: Number(item.price)
                }))
                .filter((item) => !Number.isNaN(item.price))
                .sort((first, second) => String(first.time).localeCompare(String(second.time)));
        },
        getEntryRange() {
            const zone = String(this.entryForm.entryZone || '');
            const parts = zone.match(/\d+(?:\.\d+)?/g);
            if (!parts || parts.length === 0) {
                return null;
            }
            if (parts.length === 1) {
                const value = Number(parts[0]);
                return { min: value, max: value };
            }
            const first = Number(parts[0]);
            const second = Number(parts[1]);
            return {
                min: Math.min(first, second),
                max: Math.max(first, second)
            };
        },
        getEntryReferencePrice() {
            const range = this.getEntryRange();
            if (!range) {
                return Number.NaN;
            }
            return (range.min + range.max) / 2;
        },
        getClosePricesFromCandles(candles) {
            return (candles || []).map((item) => {
                if (!Array.isArray(item) || item.length < 2) {
                    return Number.NaN;
                }
                return Number(item[1]);
            });
        },
        buildMovingAverage(closePrices, period) {
            return closePrices.map((_, index) => {
                if (index < period - 1) {
                    return null;
                }
                const slice = closePrices.slice(index - period + 1, index + 1);
                if (slice.some((value) => !Number.isFinite(value))) {
                    return null;
                }
                const sum = slice.reduce((acc, value) => acc + value, 0);
                return Number((sum / period).toFixed(4));
            });
        },
        getDemoReviewChartData() {
            const categories = [
                '05-08', '05-09', '05-12', '05-13', '05-14', '05-15', '05-16', '05-19',
                '05-20', '05-21', '05-22', '05-23', '05-26', '05-27', '05-28', '05-29'
            ];

            const candles = [
                [17.55, 17.92, 17.40, 18.02],
                [17.90, 17.80, 17.58, 18.05],
                [17.78, 17.66, 17.41, 17.88],
                [17.68, 17.96, 17.60, 18.08],
                [18.00, 18.14, 17.92, 18.22],
                [18.16, 18.05, 17.95, 18.20],
                [18.08, 18.72, 18.05, 18.88],
                [18.70, 18.94, 18.56, 19.05],
                [18.95, 19.16, 18.82, 19.22],
                [19.18, 19.05, 18.90, 19.30],
                [19.04, 19.22, 18.94, 19.40],
                [19.20, 19.58, 19.10, 19.70],
                [19.60, 19.42, 19.22, 19.68],
                [19.40, 19.88, 19.32, 20.02],
                [19.92, 20.12, 19.80, 20.22],
                [20.10, 20.02, 19.92, 20.18]
            ];
            const volumes = [120, 98, 88, 132, 145, 116, 220, 180, 172, 148, 160, 210, 166, 196, 238, 184];
            const rsi = [42, 45, 40, 47, 52, 49, 62, 66, 69, 64, 67, 72, 68, 74, 78, 73];
            const diff = [-0.22, -0.18, -0.2, -0.12, -0.05, -0.02, 0.08, 0.16, 0.22, 0.18, 0.21, 0.30, 0.28, 0.36, 0.41, 0.38];
            const dea = [-0.18, -0.17, -0.18, -0.16, -0.12, -0.08, -0.01, 0.06, 0.12, 0.14, 0.17, 0.22, 0.25, 0.30, 0.35, 0.36];
            const macd = diff.map(function (item, index) {
                return Number(((item - dea[index]) * 2).toFixed(2));
            });
            const closePrices = this.getClosePricesFromCandles(candles);

            return {
                categories,
                candles,
                volumes,
                rsi,
                diff,
                dea,
                macd,
                ma5: this.buildMovingAverage(closePrices, 5),
                ma10: this.buildMovingAverage(closePrices, 10),
                ma20: this.buildMovingAverage(closePrices, 20),
                ma60: this.buildMovingAverage(closePrices, 60)
            };
        },
        buildChartDataFromRemote(remoteData) {
            const chart = (remoteData && remoteData.chart) || {};
            const categories = chart.dates || [];
            const candles = chart.kline || [];
            const volumes = (chart.volume || []).map((item) => Number(item || 0));
            const rsi14 = chart.rsi14 || [];
            const rsi6 = chart.rsi6 || [];
            const diff = chart.dif || [];
            const dea = chart.dea || [];
            const macd = chart.macd_hist || [];
            const ma5 = chart.ma5 || [];
            const ma10 = chart.ma10 || [];
            const ma20 = chart.ma20 || [];
            const ma60 = chart.ma60 || [];

            if (!categories.length || !candles.length) {
                return null;
            }

            return {
                categories,
                candles,
                volumes,
                rsi: rsi14.length ? rsi14 : rsi6,
                diff,
                dea,
                macd,
                ma5,
                ma10,
                ma20,
                ma60
            };
        },
        async getReviewChartData() {
            const stockCode = this.entryForm.stockCode;
            if (!stockCode) {
                return this.getDemoReviewChartData();
            }
            const { startDate, endDate } = this.getChartQueryDateRange();

            try {
                const resp = await marketApi.getKlineIndicators({
                    symbol_code: stockCode,
                    start_date: startDate,
                    end_date: endDate,
                    limit: 1200
                });
                if (!resp || !resp.data || resp.data.code !== 200) {
                    return this.getDemoReviewChartData();
                }
                const parsed = this.buildChartDataFromRemote(resp.data.data || {});
                return parsed || this.getDemoReviewChartData();
            } catch (err) {
                console.error(err);
                return this.getDemoReviewChartData();
            }
        },
        async initCharts() {
            const chartData = await this.getReviewChartData();
            this.disposeCharts();

            if (this.$refs.candlestickChart) {
                this.charts.candlestick = echarts.init(this.$refs.candlestickChart);
                this.charts.candlestick.setOption(this.getCandlestickOption(chartData));
            }

            if (this.$refs.volumeChart) {
                this.charts.volume = echarts.init(this.$refs.volumeChart);
                this.charts.volume.setOption(this.getVolumeOption(chartData));
            }

            if (this.$refs.rsiChart) {
                this.charts.rsi = echarts.init(this.$refs.rsiChart);
                this.charts.rsi.setOption(this.getRsiOption(chartData));
            }

            if (this.$refs.macdChart) {
                this.charts.macd = echarts.init(this.$refs.macdChart);
                this.charts.macd.setOption(this.getMacdOption(chartData));
            }
        },
        getBaseChartOption(categories) {
            const totalCount = (categories || []).length;
            let startPercent = 0;
            if (totalCount > 0) {
                const keepCount = Math.min(120, totalCount);
                startPercent = Math.max(0, Number((((totalCount - keepCount) / totalCount) * 100).toFixed(2)));
            }
            return {
                backgroundColor: '#0b1020',
                animation: false,
                tooltip: {
                    trigger: 'axis'
                },
                grid: {
                    left: 48,
                    right: 18,
                    top: 16,
                    bottom: 52
                },
                xAxis: {
                    type: 'category',
                    data: categories,
                    scale: true,
                    boundaryGap: false,
                    axisLine: { lineStyle: { color: '#42506d' } },
                    axisLabel: { color: '#8b9bbd' },
                    splitLine: { show: false },
                    axisTick: { show: false }
                },
                yAxis: {
                    scale: true,
                    axisLine: { lineStyle: { color: '#42506d' } },
                    axisLabel: { color: '#8b9bbd' },
                    splitLine: { lineStyle: { color: 'rgba(66, 80, 109, 0.25)' } }
                },
                dataZoom: [
                    {
                        type: 'inside',
                        xAxisIndex: 0,
                        start: startPercent,
                        end: 100
                    },
                    {
                        type: 'slider',
                        xAxisIndex: 0,
                        start: startPercent,
                        end: 100,
                        bottom: 10,
                        height: 16,
                        borderColor: '#42506d',
                        backgroundColor: 'rgba(66, 80, 109, 0.2)',
                        fillerColor: 'rgba(91, 140, 255, 0.28)',
                        handleStyle: { color: '#94a3b8', borderColor: '#cbd5e1' },
                        textStyle: { color: '#8b9bbd' }
                    }
                ]
            };
        },
        getCandlestickOption(chartData) {
            const option = this.getBaseChartOption(chartData.categories);
            option.series = [
                {
                    name: 'K线',
                    type: 'candlestick',
                    data: chartData.candles,
                    itemStyle: {
                        color: '#ff6b6b',
                        color0: '#2ad3b6',
                        borderColor: '#ff8f8f',
                        borderColor0: '#7cf0dd'
                    },
                    markLine: {
                        symbol: 'none',
                        label: { color: '#e6ecff' },
                        lineStyle: { type: 'dashed', width: 1.2 },
                        data: [
                            { yAxis: 18.0, name: '计划买入区间', lineStyle: { color: '#5b8cff' } },
                            { yAxis: 17.2, name: '原止损', lineStyle: { color: '#ff9f43' } },
                            { yAxis: 20.2, name: '目标位', lineStyle: { color: '#34d399' } },
                            { yAxis: 18.9, name: '移动止损', lineStyle: { color: '#f97316' } }
                        ]
                    },
                    markPoint: {
                        symbolSize: 38,
                        label: { color: '#ffffff', fontWeight: 'bold' },
                        data: [
                            { coord: ['05-14', 18.02], value: '买', itemStyle: { color: '#22c55e' } },
                            { coord: ['05-16', 18.68], value: '加', itemStyle: { color: '#0ea5e9' } },
                            { coord: ['05-28', 20.12], value: '卖', itemStyle: { color: '#ef4444' } },
                            { coord: ['05-16', 18.88], value: '改1', itemStyle: { color: '#f59e0b' } },
                            { coord: ['05-23', 19.70], value: '改2', itemStyle: { color: '#fb7185' } }
                        ]
                    }
                },
                {
                    name: 'MA5',
                    type: 'line',
                    data: chartData.ma5 || [],
                    smooth: true,
                    symbol: 'none',
                    connectNulls: true,
                    lineStyle: { color: '#22d3ee', width: 1.3 }
                },
                {
                    name: 'MA10',
                    type: 'line',
                    data: chartData.ma10 || [],
                    smooth: true,
                    symbol: 'none',
                    connectNulls: true,
                    lineStyle: { color: '#a78bfa', width: 1.3 }
                },
                {
                    name: 'MA20',
                    type: 'line',
                    data: chartData.ma20 || [],
                    smooth: true,
                    symbol: 'none',
                    connectNulls: true,
                    lineStyle: { color: '#f59e0b', width: 1.3 }
                },
                {
                    name: 'MA60',
                    type: 'line',
                    data: chartData.ma60 || [],
                    smooth: true,
                    symbol: 'none',
                    connectNulls: true,
                    lineStyle: { color: '#34d399', width: 1.3 }
                }
            ];
            return option;
        },
        getVolumeOption(chartData) {
            const option = this.getBaseChartOption(chartData.categories);
            option.series = [
                {
                    name: '成交量',
                    type: 'bar',
                    data: chartData.volumes,
                    itemStyle: {
                        color: '#4c78ff'
                    }
                }
            ];
            return option;
        },
        getRsiOption(chartData) {
            const option = this.getBaseChartOption(chartData.categories);
            option.yAxis.min = 0;
            option.yAxis.max = 100;
            option.series = [
                {
                    name: 'RSI',
                    type: 'line',
                    data: chartData.rsi,
                    smooth: true,
                    lineStyle: { color: '#ffd166', width: 2 },
                    symbol: 'none'
                }
            ];
            return option;
        },
        getMacdOption(chartData) {
            const option = this.getBaseChartOption(chartData.categories);
            option.series = [
                {
                    name: 'DIFF',
                    type: 'line',
                    data: chartData.diff,
                    smooth: true,
                    lineStyle: { color: '#60a5fa', width: 2 },
                    symbol: 'none'
                },
                {
                    name: 'DEA',
                    type: 'line',
                    data: chartData.dea,
                    smooth: true,
                    lineStyle: { color: '#f8fafc', width: 2 },
                    symbol: 'none'
                },
                {
                    name: 'MACD',
                    type: 'bar',
                    data: chartData.macd,
                    itemStyle: {
                        color: function (params) {
                            return params.value >= 0 ? '#ef4444' : '#22c55e';
                        }
                    }
                }
            ];
            return option;
        }
    }
};
</script>

<style scoped>
.investment-review-page {
    box-sizing: border-box;
    padding: 16px 18px;
    background: #f5f7fb;
}

.hero-panel,
.panel {
    border: 1px solid rgba(116, 139, 178, 0.16);
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.88);
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
}

.hero-panel {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 12px;
    padding: 10px 14px;
}

.hero-main {
    display: flex;
    align-items: center;
    gap: 18px;
    min-width: 0;
}

.plan-switch-block {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
}

.switch-label {
    color: #64748b;
    font-size: 12px;
    white-space: nowrap;
}

.plan-switcher {
    width: 260px;
}

.watchlist-switcher {
    width: 220px;
}

.chart-range-picker {
    width: 250px;
}

.eyebrow {
    margin: 0 0 2px;
    color: #4f46e5;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.hero-panel h1,
.panel-header h2,
.timeline-card h3,
.insight-block h3,
.improvement-card h3 {
    margin: 0;
    color: #0f172a;
    font-family: Georgia, 'Times New Roman', serif;
}

.hero-panel h1 {
    font-size: 24px;
    line-height: 1.1;
}

.hero-copy,
.panel-header p,
.timeline-card p,
.review-score-card p,
.insight-block p,
.improvement-card p {
    margin: 6px 0 0;
    color: #475569;
    line-height: 1.55;
}

.hero-metrics {
    display: grid;
    grid-template-columns: repeat(3, minmax(110px, 1fr));
    gap: 10px;
}

.metric-card {
    padding: 8px 10px;
    border-radius: 12px;
    background: #f8fbff;
    border: 1px solid rgba(91, 140, 255, 0.14);
}

.metric-card.accent {
    background: linear-gradient(135deg, #123c76, #1d4ed8);
}

.metric-card.accent .metric-label,
.metric-card.accent strong {
    color: #f8fbff;
}

.metric-label {
    display: block;
    margin-bottom: 6px;
    color: #64748b;
    font-size: 11px;
}

.metric-card strong {
    font-size: 16px;
    color: #0f172a;
}

.workspace-tabs :deep(.el-tabs__header) {
    margin-bottom: 10px;
}

.workspace-tabs :deep(.el-tabs__nav-wrap::after) {
    background-color: rgba(148, 163, 184, 0.22);
}

.workspace-tabs :deep(.el-tabs__item) {
    height: 36px;
    line-height: 36px;
    color: #475569;
    font-weight: 600;
}

.workspace-tabs :deep(.el-tabs__item.is-active) {
    color: #1d4ed8;
}

.workspace-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
}

.review-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.5fr) minmax(320px, 1fr);
    gap: 14px;
    align-items: start;
}

.panel {
    padding: 16px;
}

.panel-main,
.review-main {
    min-width: 0;
}

.panel-side,
.review-side {
    min-width: 0;
}

.summary-panel {
    align-self: start;
}

.panel-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 12px;
}

.panel-header.compact {
    margin-bottom: 10px;
}

.header-actions {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}

.plan-form {
    margin-top: 2px;
}

.plan-form :deep(.el-form-item) {
    margin-bottom: 10px;
}

.plan-form :deep(.el-form-item__label) {
    padding-bottom: 4px;
    line-height: 1.3;
    font-size: 12px;
}

.plan-form :deep(.el-input__inner),
.plan-form :deep(.el-textarea__inner) {
    border-radius: 10px;
}

.plan-form :deep(.el-input__inner) {
    height: 34px;
    line-height: 34px;
}

.plan-form :deep(.el-radio-button__inner) {
    padding: 9px 14px;
}

.option-button-group {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.option-button-group :deep(.el-button) {
    margin-left: 0;
    border-radius: 10px;
    padding: 8px 14px;
}

.compact-group :deep(.el-button) {
    padding: 7px 12px;
}

.dialog-form {
    margin-top: 6px;
}

.field-help {
    margin: 6px 0 0;
    color: #64748b;
    font-size: 12px;
    line-height: 1.45;
}

.form-grid {
    display: grid;
    gap: 10px;
}

.four-columns {
    grid-template-columns: repeat(4, minmax(0, 1fr));
}

.two-columns {
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.three-columns {
    grid-template-columns: repeat(3, minmax(0, 1fr));
}

.timeline-stack {
    display: grid;
    gap: 10px;
}

.timeline-card {
    padding: 12px;
    border-radius: 14px;
    background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
    border: 1px solid rgba(148, 163, 184, 0.2);
}

.timeline-head,
.timeline-foot,
.summary-metrics div {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.timeline-time {
    color: #64748b;
    font-size: 12px;
}

.timeline-actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.timeline-foot {
    margin-top: 8px;
    color: #1e3a8a;
    font-size: 12px;
    line-height: 1.45;
}

.danger-text-button {
    color: #dc2626;
}

.danger-text-button:hover,
.danger-text-button:focus {
    color: #b91c1c;
}

.execution-table :deep(.el-table__header-wrapper th) {
    background: #f8fbff;
    color: #334155;
}

.execution-table :deep(.el-table td),
.execution-table :deep(.el-table th) {
    padding: 6px 0;
}

.execution-table :deep(.el-table__row td) {
    padding: 6px 0;
}

.summary-metrics {
    display: grid;
    gap: 10px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.review-summary-metrics {
    margin-bottom: 10px;
}

.summary-metrics div {
    padding: 11px 13px;
    border-radius: 14px;
    background: #f8fafc;
    border: 1px solid rgba(148, 163, 184, 0.18);
}

.summary-metrics span {
    color: #64748b;
}

.summary-metrics strong {
    color: #0f172a;
    line-height: 1.35;
}

.positive {
    color: #16a34a !important;
}

.negative {
    color: #dc2626 !important;
}

.review-chart-stack {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.chart-panel {
    border-radius: 16px;
    overflow: hidden;
    background: #0b1020;
    border: 1px solid rgba(91, 140, 255, 0.14);
}

.chart-panel-title {
    padding: 10px 14px 0;
    color: #dbe7ff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.06em;
}

.review-chart {
    border-radius: 16px;
    overflow: hidden;
    background: #0b1020;
}

.review-chart-k {
    height: 240px;
}

.review-chart-volume,
.review-chart-rsi,
.review-chart-macd {
    height: 140px;
}

.chart-legend-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
    margin-top: 10px;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 10px;
    border-radius: 12px;
    background: #f8fbff;
    color: #334155;
    font-size: 12px;
}

.legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 999px;
}

.legend-dot.plan {
    background: #5b8cff;
}

.legend-dot.modify {
    background: #f59e0b;
}

.legend-dot.trade {
    background: #22c55e;
}

.review-score-card,
.improvement-card,
.insight-block {
    padding: 14px;
    border-radius: 16px;
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid rgba(148, 163, 184, 0.2);
}

.review-score-card {
    margin-bottom: 10px;
    padding: 12px 14px;
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.review-score-card strong {
    display: block;
    margin-top: 4px;
    font-size: 20px;
    color: #0f172a;
}

.review-score-card span,
.review-score-card p {
    color: #475569;
}

.insight-block :deep(.el-textarea__inner),
.improvement-card :deep(.el-textarea__inner) {
    border-radius: 10px;
    min-height: 96px !important;
}

.emotion-panel {
    margin-bottom: 12px;
    padding: 14px;
    border-radius: 16px;
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid rgba(148, 163, 184, 0.2);
}

.emotion-panel h3 {
    margin: 0 0 10px;
    color: #0f172a;
    font-family: Georgia, 'Times New Roman', serif;
}

.emotion-group {
    margin-bottom: 10px;
}

.emotion-group:last-child {
    margin-bottom: 0;
}

.emotion-group span {
    display: block;
    margin-bottom: 6px;
    color: #64748b;
    font-size: 12px;
}

.score-button-group {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 10px;
}

.score-button-group :deep(.el-button) {
    margin-left: 0;
    border-radius: 10px;
}

.insight-block {
    margin-bottom: 10px;
}

.emotion-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 10px 0;
}

.emotion-strip :deep(.el-tag) {
    height: 26px;
    line-height: 24px;
}

@media (min-width: 1800px) {
    .investment-review-page {
        padding: 14px 16px;
    }

    .review-grid {
        grid-template-columns: minmax(0, 1.5fr) minmax(360px, 1fr);
    }

    .review-chart-k {
        height: 250px;
    }

    .review-chart-volume,
    .review-chart-rsi,
    .review-chart-macd {
        height: 150px;
    }
}

@media (max-width: 1280px) {

    .hero-panel {
        flex-direction: column;
        align-items: stretch;
    }

    .hero-main,
    .plan-switch-block {
        flex-wrap: wrap;
    }

    .plan-switcher,
    .watchlist-switcher {
        width: 100%;
    }

    .workspace-grid,
    .review-grid,
    .hero-panel,
    .four-columns {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 900px) {
    .investment-review-page {
        padding: 14px;
    }

    .two-columns,
    .three-columns,
    .chart-legend-grid,
    .summary-metrics {
        grid-template-columns: 1fr;
    }

    .panel,
    .hero-panel {
        padding: 16px;
        border-radius: 18px;
    }

    .review-chart-k {
        height: 220px;
    }

    .review-chart-volume,
    .review-chart-rsi,
    .review-chart-macd {
        height: 132px;
    }
}
</style>
<template>
    <!-- TODO 重构界面 增加  4象限，然后展示4象限-->
    <div id="app">
        <el-row> <el-switch v-model="query_all" inactive-text="只展示未归档" :span="10" @change="get_transaction">
            </el-switch></el-row>
        <el-row>
            <el-col :span="15">
                <!-- 分页 -->
                <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                    :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                    layout="total, sizes, prev, pager, next, jumper" :total="total">
                </el-pagination>
                <el-table :data="pagedData" height="1080" style="width: 100%">
                    <el-table-column prop="file_type" label="类型" width="80"></el-table-column>
                    <el-table-column prop="transaction_time" label="交易时间" width="160"></el-table-column>
                    <el-table-column prop="level1" label="一级" width="80"></el-table-column>
                    <el-table-column prop="level2" label="二级" width="80"></el-table-column>
                    <el-table-column prop="level3" label="三级" width="80"></el-table-column>
                    <el-table-column prop="transaction_type" label="原始类型" width="130"></el-table-column>
                    <el-table-column prop="counterparty" label="交易方" width="200">
                    </el-table-column>
                    <el-table-column prop="product" label="商品" width="300">
                    </el-table-column>
                    <el-table-column prop="transaction_direction" label="收/支" width="80"></el-table-column>
                    <el-table-column prop="amount" label="金额" width="80"></el-table-column>
                    <el-table-column prop="data_status" label="状态" width="80"></el-table-column>
                    <el-table-column label="操作" width="50">
                        <template slot-scope="scope">
                            <el-button @click="show_transaction(scope.row)" type="text" size="small">编辑
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <el-dialog @close="dialogtransactionVisible = false" title="修改" :visible="dialogtransactionVisible" width="40%">
            <div>
                <el-row :span="6">
                    <el-select @change="updatelevel2option" v-model="level1" filterable allow-create
                        default-first-option placeholder="请选择一级" style="width: 140px">
                        <el-option v-for="item in level1_option" :key="item.value" :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                    <el-select @change="updatelevel3option" v-model="level2" filterable allow-create
                        default-first-option placeholder="请选择二级" style="width: 140px">
                        <el-option v-for="item in level2_option" :key="item.value" :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                    <el-select v-model="level3" filterable allow-create default-first-option placeholder="请选择三级"
                        style="width: 140px">
                        <el-option v-for="item in level3_option" :key="item.value" :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                    <el-select v-model="d_data_status" clearable default-first-option style="width: 120px"
                        placeholder="请选择状态">
                        <el-option v-for="item in data_status_option" :key="item.value" :label="item.label"
                            :value="item.value"></el-option>
                    </el-select>
                    <el-switch v-model="merge_data" inactive-text="合并同类" :span="10">
                    </el-switch>
                </el-row>
                <el-row :span="6"><el-input v-model="d_counterparty" style="width: 300px" :disabled="true"></el-input>
                    <el-input v-model="d_transaction_id" style="width: 300px" :disabled="true"></el-input></el-row>
                <el-row :span="6"><el-input v-model="d_product" style="width: 300px"
                        :disabled="true"></el-input></el-row>
            </div>

            <span slot="footer" class="dialog-footer">
                <el-button @click="closedialog">取 消</el-button>
                <el-button type="primary" @click="update_transaction">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>



<script>
import axios from "axios";
var echarts = require("echarts");
export default {
    data() {
        return {
            query_all: false,
            transaction_data: [],
            dialogtransactionVisible: false,
            // 分页数据
            pagedData: [],
            // 当前页
            currentPage: 1,
            // 每页显示条目个数
            pageSize: 15,
            // 总条目数
            total: 0,
            // 选项沟通
            level1: '',
            level1_option: [],
            level2: '',
            level2_option: [],
            level3: '',
            level3_option: [],
            pay_level1_option: [],
            pay_level1_level2_option: [],
            pay_level2_level3_option: [],
            income_level1_option: [],
            income_level1_level2_option: [],
            income_level2_level3_option: [],
            data_status_option: [{
                value: 0,
                label: '初始'
            }, {
                value: 1,
                label: '已确认'
            }, {
                value: 3,
                label: '有退款'
            }, {
                value: 4,
                label: '已mapping'
            }],
            d_data_status: '',
            d_transaction_id: '',
            d_counterparty: '',
            d_product: '',
            d_transaction_direction: '',
            merge_data: false,
        };
    },
    mounted: function () {
        this.init();
    },
    methods: {
        init: function () {
            this.get_transaction();
            this.get_transaction_option()
        },
        get_transaction: function () {
            axios.post("/get_transaction", {
                query_all: this.query_all
            }).then((response) => {
                // console.log(response);
                this.transaction_data = response.data;
                this.total = this.transaction_data.length;
                this.fetchPagedData()
            });
        },
        get_transaction_option: function () {
            axios.get("/get_transaction_option").then((response) => {
                // console.log(response);
                this.pay_level1_option = response.data.pay_level1_option;
                this.pay_level1_level2_option = response.data.pay_level1_level2_option
                this.pay_level2_level3_option = response.data.pay_level2_level3_option
                this.income_level1_option = response.data.income_level1_option;
                this.income_level1_level2_option = response.data.income_level1_level2_option
                this.income_level2_level3_option = response.data.income_level2_level3_option

            });
        },
        show_transaction: function (event) {
            // console.log(event);
            this.dialogtransactionVisible = true;
            this.d_data_status = event.data_status;
            this.level1 = event.level1;
            this.level2 = event.level2;
            this.level3 = event.level3;
            this.d_counterparty = event.counterparty;
            this.d_product = event.product;
            this.d_transaction_id = event.transaction_id;
            this.d_transaction_direction = event.transaction_direction
            if (event.transaction_direction == '支出') {
                this.level1_option = this.pay_level1_option;
                this.pay_level1_level2_option = this.pay_level1_level2_option;
                this.pay_level2_level3_option = this.pay_level2_level3_option;
            } else {
                this.level1_option = this.income_level1_option;
                this.level1_level2_option = this.income_level1_level2_option;
                this.level2_level3_option = this.income_level2_level3_option;
            }
        },
        // 分页大小改变时触发
        handleSizeChange(newSize) {
            this.pageSize = newSize;
            this.fetchPagedData();
        },
        // 当前页码改变时触发
        handleCurrentChange(newPage) {
            this.currentPage = newPage;
            this.fetchPagedData();
        },
        // 获取分页数据
        fetchPagedData() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = this.currentPage * this.pageSize;
            this.pagedData = this.transaction_data.slice(start, end);
        },
        updatelevel2option: function (event) {
            // console.log('update option');
            this.level2 = "";
            if (this.level1 != "" && this.level2_option != []) {
                this.level2_option = [];
                let temp = this.level1_level2_option[this.level1];
                if (temp) {
                    this.level2_option = [];
                    for (let i in temp) {
                        this.level2_option.push({
                            value: temp[i],
                            label: temp[i],
                        });
                    }
                }
            }
        },
        updatelevel3option: function (event) {
            // console.log('update option');
            this.post = "";
            if (this.level2 != "" && this.level3_option != []) {
                this.level3_option = [];
                let temp = this.level2_level3_option[this.level2];
                if (temp) {
                    this.level3_option = [];
                    for (let i in temp) {
                        this.level3_option.push({
                            value: temp[i],
                            label: temp[i],
                        });
                    }
                }
            }
        },
        update_transaction: function () {
            axios.post("/update_transaction", {
                level1: this.level1,
                level2: this.level2,
                level3: this.level3,
                d_data_status: this.d_data_status,
                merge_data: this.merge_data,
                d_product: this.d_product,
                d_counterparty: this.d_counterparty,
                d_transaction_id: this.d_transaction_id
            }).then((response) => {
                this.closedialog()
                this.get_transaction();
                this.get_transaction_option();
            });
        },
        closedialog: function () {
            this.level1 = '';
            this.level2 = '';
            this.level3 = '';
            this.d_data_status = '';
            this.d_counterparty = '';
            this.d_product = '';
            this.d_transaction_id = '';
            this.merge_data = false;
            this.dialogtransactionVisible = false;
        },
    },
};
</script>

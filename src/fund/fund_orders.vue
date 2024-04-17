<template>
  <div id="app">
    <el-row>
      <el-col :span="14"><el-button type="primary" @click="showdialog('1')" icon="el-icon-sell">买</el-button>
        <el-button type="primary" @click="showdialog('0')" icon="el-icon-sold-out">卖</el-button>
        <el-button type="primary" @click="showdialog_cost">更新成本</el-button>
        <el-button type="primary" @click="caltoday">caltoay</el-button>
        <!-- <el-button type="primary" @click="generatejsons">生成json</el-button> -->
        <el-input v-model="fundnamesearch" placeholder="基金名称" style="width: 300px"><el-button slot="append"
            icon="el-icon-refresh" @click="fundnamesearch = ''"></el-button>
        </el-input>
      </el-col>
      <!-- TODO 加个筛选 -->
    </el-row>
    <el-row>
      <el-col :span="13">
        <!-- tableData.filter((v) => v.action != 'delete') -->
        <el-table :data="fund_order_data.filter((v) => v.fund_name.includes(fundnamesearch))
          " style="width: 100%" height="850">
          <el-table-column prop="fund_name" label="基金名称" width="260">
          </el-table-column>
          <el-table-column prop="trade_time" label="交易时间" width="120">
          </el-table-column>
          <el-table-column prop="order_amount" label="交易金额" width="80">
          </el-table-column>
          <el-table-column prop="unit_net_value" label="确认净值" width="80">
          </el-table-column>
          <el-table-column prop="transaction_amount" label="份额" width="80">
          </el-table-column>
          <el-table-column prop="order_date" label="确认时间" width="120">
          </el-table-column>
          <el-table-column prop="operation" label="买卖" width="80" :formatter="isformat">
          </el-table-column>
          <el-table-column prop="methods" label="操作类型" width="80" :formatter="isformat">
          </el-table-column>
          <el-table-column label="操作" width="170">
            <template slot-scope="scope">
              <el-button v-if="scope.row.methods != 'w'" @click="diashowrelate(scope.row)" type="text"
                size="small">联</el-button>
              <!-- 展示转换对比图 -->
              <el-button v-if="scope.row.relate_id != null" @click="diashowprocess(scope.row)" type="text"
                size="small">图</el-button>
              <!-- <el-button @click="diashowprocess(scope.row)" type="text" size="small">删</el-button> -->
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col :span="11">
        <el-table :data="funds_for_cost_update" style="width: 100%" height="300">
          <el-table-column prop="fund_name" label="基金名称" width="260">
          </el-table-column>
          <el-table-column prop="cost_update_time" label="成本更新时间" width="160">
          </el-table-column>
          <el-table-column prop="order_date" label="订单确认时间" width="120">
          </el-table-column>
          <el-table-column prop="cost" label="成本" width="80">
          </el-table-column>
          <el-table-column prop="unit_net_value" label="订单" width="80">
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>

    <!-- 成本更新框 -->
    <el-dialog :visible.sync="dialogcostFormVisible" width="30%">
      <el-form :model="costform">
        <el-row :span="5">
          <el-form-item label="产品" :label-width="formLabelWidth">
            <el-select v-model="costform.fund_code" @change="updatecost" filterable placeholder="请选择">
              <el-option v-for="item in funds_list_for_cost_update" :key="item.value" :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="更新时间" :label-width="formLabelWidth">
            <el-date-picker readonly v-model="costform.update_time" type="datetime" placeholder="选择日期时间">
            </el-date-picker></el-form-item></el-row>
        <el-row :span="5">
          <el-form-item label="成本" :label-width="formLabelWidth">
            <el-input v-model="costform.cost" style="width: 220px"></el-input>
          </el-form-item>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogcostFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="commitcost">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 交易关联框 -->
    <el-dialog :visible.sync="dialogrelateFormVisible" width="30%">
      <el-input v-model="relate_todo_order_fund_name" disabled style="width: 520px"></el-input>
      <el-input v-model="relate_todo_order_fund_sum" disabled style="width: 520px"></el-input>
      <el-select v-model="relate_select_order" filterable placeholder="请选择" style="width: 520px">
        <el-option v-for="item in relate_fund_orders" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>
      <div slot="footer" class="dialog-footer">
        <el-button @click="
          dialogrelateFormVisible = false;
        relate_fund_orders = [];
        relate_select_order = '';
        ">取 消</el-button>
        <el-button type="primary" @click="commitrelate">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 转换对比框 -->
    <el-dialog :visible.sync="dialogcompareFormVisible" width="35%">
      <el-table :data="comparetabledata" style="width: 100%" height="300">
        <el-table-column prop="fund_name" label="基金名称" width="260">
        </el-table-column>
        <el-table-column prop="operation" label="操作" width="120">
        </el-table-column>
        <el-table-column prop="3天" label="3天" width="120"> </el-table-column>
        <el-table-column prop="7天" label="7天" width="120"> </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogcompareFormVisible = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 基金交易框 -->
    <el-dialog :visible.sync="dialogorderFormVisible" width="30%">
      <el-form :model="orderform">
        <el-row :span="5">
          <el-form-item label="产品" :label-width="formLabelWidth">
            <el-select v-model="orderform.fund_code" filterable placeholder="请选择" @change="alter_order_fund_prices">
              <el-option v-for="item in fund_list" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="净值时间" :label-width="formLabelWidth">
            <el-date-picker v-model="orderform.trade_time" @change="alter_order_fund_prices" type="date"
              placeholder="选择日期时间" value-format="yyyy-MM-dd">
            </el-date-picker>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="确认净值" :label-width="formLabelWidth">
            <el-input v-model="orderform.fund_prices" style="width: 220px"></el-input>
          </el-form-item>
        </el-row>
        <el-row :span="5" v-if="ordertype">
          <el-form-item label="买入金额" :label-width="formLabelWidth">
            <el-input v-model="orderform.order_sum" style="width: 220px" @change="totalAmount"></el-input>
          </el-form-item>
        </el-row>
        <el-row :span="5" v-if="!ordertype">
          <el-form-item label="卖出份额" :label-width="formLabelWidth">
            <el-input v-model="orderform.fund_shares" style="width: 220px" @change="calselltotal"></el-input>
          </el-form-item>
        </el-row>
        <el-row :span="5" v-if="!ordertype">
          <el-form-item label="卖出金额" :label-width="formLabelWidth">
            <el-input v-model="orderform.order_sum" style="width: 220px"></el-input>
          </el-form-item>
        </el-row>
        <el-row :span="5" v-if="ordertype">
          <el-form-item label="买入份额" :label-width="formLabelWidth">
            <el-input v-model="orderform.fund_shares" style="width: 220px"></el-input>
          </el-form-item>
        </el-row>

        <el-row :span="5">
          <el-form-item label="核算结果" :label-width="formLabelWidth">
            <el-input v-model="fund_sum_check" disabled style="width: 220px"></el-input>
          </el-form-item>
        </el-row>

        <el-row :span="5" v-if="ordertype">
          <el-form-item label="投资模式" :label-width="formLabelWidth">
            <el-switch v-model="orderform.buytype" active-text="定投" inactive-text="人工">
            </el-switch>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="标签信息" :label-width="formLabelWidth">
            <el-switch v-model="orderform.isfry" active-text="正常" inactive-text="鱼苗">
            </el-switch>
          </el-form-item>
        </el-row>
        <!-- <el-divider></el-divider> -->
        <el-row :span="5" v-if="ordertype">
          <el-form-item label="确认时间" :label-width="formLabelWidth">
            <el-date-picker v-model="orderform.check_time" type="date" placeholder="选择日期时间" value-format="yyyy-MM-dd">
            </el-date-picker>
          </el-form-item>
        </el-row>
        <el-row :span="5" v-if="!ordertype">
          <el-form-item label="到账时间" :label-width="formLabelWidth">
            <el-date-picker v-model="orderform.check_time" type="date" placeholder="选择日期时间" value-format="yyyy-MM-dd">
            </el-date-picker>
          </el-form-item>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogorderFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="commitorders">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import axios from "axios";
export default {
  data() {
    return {
      fund_list: [],
      fundnamesearch: "",
      fund_order_data: [],
      comparetabledata: [],
      fund_closed_net_vaule_data: [],
      orderform: {
        fund_code: "",
        name: "",
        order_sum: "",
        trade_time: "",
        buytype: true,
        isfry: true,
        fund_sum: "",
        fund_shares: "",
        fund_prices: "",
        fund_fee: "",
        check_time: "",
      },
      funds_for_cost_update: [],
      funds_list_for_cost_update: [],
      costform: {
        fundcoe: "",
        update_time: "",
        cost: "",
      },
      ordertype: "",
      dialogorderFormVisible: false,
      dialogcostFormVisible: false,
      dialogrelateFormVisible: false,
      dialogcompareFormVisible: false,
      relate_todo_order_fund_name: "",
      relate_todo_order_fund_sum: "",
      relate_select_order: "",
      relate_fund_orders: "",
      formLabelWidth: "100px", // 不知道能不能干掉
    };
  },
  computed: {
    fund_sum_check: function () {
      return (
        this.orderform.order_sum -
        this.orderform.fund_shares * this.orderform.fund_prices
      ).toFixed(2);
    },
  },
  mounted: function () {
    this.init();
  },
  methods: {
    init() {
      this.get_order_data();
      this.get_cost_info(); //获取基金的成本和成本的更新时间
      this.get_fund_closed_net_value();
      this.get_fund_info();
      this.get_funds_for_cost_update();
      //   this.getestimatedata();  //预计的数据
      //   this.getfundtable();  //统计的数据
      //   this.getcostdata(); -> get_cost_info //获取基金的成本和成本的更新时间
      //   this.getfundpricedata(); ->get_fund_closed_net_value
      //   this.getcosttable(); // 获取待更新成本的基金列表
      //   this.getfundorders();  //get_order_data
      //   this.getfundbasetable();  //获取fundbasedata
      //   this.getcostfundlist(); //获取cost的option
    },
    // 获取基金所有的闭市的净值，提供买入卖出计算使用
    // TODO 改成近30天的就可以了，避免数据太多。
    // 获取待更新成本的基金列表
    get_funds_for_cost_update() {
      axios.get("/get_funds_for_cost_update").then((response) => {
        this.funds_for_cost_update = response.data.data;
        this.funds_list_for_cost_update = response.data.data_list;
      });
    },
    get_fund_info() {
      axios.get("/get_fund_info").then((response) => {
        this.fund_list = response.data.data;
        // this.fundbasedata = response.data.listdata; // fund_order好像没用到这个东西
      });
    },
    get_fund_closed_net_value() {
      axios.get("/get_fund_closed_net_value").then((response) => {
        this.fund_closed_net_vaule_data = response.data.data;
      });
    },
    // 在基金交易框里面，根据所选基金的时间和日期，自带带入当日净值
    alter_order_fund_prices() {
      if (this.orderform.fund_code != "" && this.orderform.trade_time != "") {
        if (
          this.fund_closed_net_vaule_data.hasOwnProperty(
            this.orderform.fund_code
          )
        ) {
          let fc = this.orderform.fund_code;
          let temp_fc_data = this.fund_closed_net_vaule_data[fc];
          if (temp_fc_data.hasOwnProperty(this.orderform.trade_time)) {
            this.orderform.fund_prices =
              temp_fc_data[this.orderform.trade_time];
          }
        }
      }
    },
    get_cost_info() {
      axios.get("/get_cost_info").then((response) => {
        this.cost_data = response.data.data;
      });
    },
    get_order_data() {
      axios.get("/get_order_data").then((response) => {
        this.fund_order_data = response.data.data;
      });
    },
    showdialog(type) {
      if (type == "1") {
        this.ordertype = true;
      } else {
        this.ordertype = false;
      }
      this.dialogorderFormVisible = true;
    },
    showdialog_cost() {
      this.dialogcostFormVisible = true;
    },
    isformat: function (row, index) {
      // console.log(row, index);
      if (index.label == "买卖") {
        if (row.transaction_type == 1) {
          return "买";
        } else {
          return "卖";
        }
      }
      if (index.label == "操作类型") {
        if (row.transaction_methods == "w") {
          return "定投";
        } else {
          return "人工";
        }
      }
    },
    diashowrelate: function (data) {
      axios.post("/getorderbyrow", { orders: data }).then((response) => {
        if (response.data.data.length > 0) {
          this.relate_todo_order = data["order_id"];
          this.relate_todo_order_fund_name = data["fund_name"];
          this.relate_todo_order_fund_sum = data["order_sum"];
          this.relate_fund_orders = response.data.data;
          this.dialogrelateFormVisible = true;
        } else {
          this.$message.warning("无可关联订单");
        }
      });
    },
    diashowprocess: function (data) {
      axios
        .post("/getcompare", { order: data["order_id"] })
        .then((response) => {
          console.log(response);
          console.log(response.data.data);
          this.comparetabledata = response.data.data;
          this.dialogcompareFormVisible = true;
        });
    },
    updatecost: function (event) {
      // console.log(this.costform.fund_code);
      this.costform.cost = this.cost_data[this.costform.fund_code].cost;
      this.costform.update_time =
        this.cost_data[this.costform.fund_code].cost_update_time;
    },
    commitcost: function () {
      axios
        .post("/update_fund_cost", {
          fund_code: this.costform.fund_code,
          cost: this.costform.cost,
        })
        .then((response) => {
          this.costform = this.$options.data().costform;
          this.dialogcostFormVisible = false;
          this.init();
        });
    },
    commitorders: function () {
      axios
        .post("/commitorders", {
          ordertype: this.ordertype,
          orderform: this.orderform,
        })
        .then((response) => {
          this.orderform = this.$options.data().orderform;
          this.dialogorderFormVisible = false;
          this.init();
        });
    },
    caltoday() {
      axios.get("/fund_update_once").then().then((response) => {
        console.log(response)
      });
    },
    commitrelate() {
      axios
        .post("/commitrelate", {
          src_order: this.relate_todo_order,
          relate_order: this.relate_select_order,
        })
        .then((response) => {
          this.relate_fund_orders = [];
          this.relate_select_order = "";
          this.relate_todo_order_fund_name = "";
          this.relate_todo_order_fund_sum = "";
          this.dialogrelateFormVisible = false;
          this.get_order_data();
        });
    },
    calselltotal: function () {
      if (
        this.orderform.fund_shares != "" &&
        this.orderform.fund_prices != ""
      ) {
        this.orderform.order_sum = (
          this.orderform.fund_shares * this.orderform.fund_prices
        ).toFixed(2);
      }
    },
    totalAmount: function () {
      if (
        this.orderform.order_sum != "" &&
        this.orderform.fund_prices != "" &&
        this.orderform.fund_prices != 0
      ) {
        this.orderform.fund_shares = (
          this.orderform.order_sum / this.orderform.fund_prices
        ).toFixed(2);
      }
    },
  },
};
</script>

<style>
.formlabelwidth {
  width: 120px;
}
</style>
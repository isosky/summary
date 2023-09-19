<template>
  <div id="app">
    <el-col :span="2">
      <el-row :span="5">
        <el-input v-model="new_fund_label" style="width: 100px"></el-input>
        <el-button
          type="primary"
          @click="add_new_label"
          icon="el-icon-check"
        ></el-button>
      </el-row>
      <el-row :span="5">
        <el-table :data="fund_base_label" height="800">
          <el-table-column
            prop="fund_label"
            label="行业"
            width="120"
          ></el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="6">
      <el-row :span="5">
        <el-select
          v-model="fund_base_label_selected"
          clearable
          filterable
          allow-create
          default-first-option
          placeholder="请选择行业"
          style="width: 200px"
        >
          <el-option
            v-for="item in fund_base_label_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-select
          v-model="fund_had_code_selected"
          clearable
          filterable
          default-first-option
          placeholder="请选择基金"
        >
          <el-option
            v-for="item in fund_had_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-button
          type="primary"
          @click="add_fund_label"
          icon="el-icon-check"
        ></el-button>
      </el-row>
      <el-row :span="5">
        <el-table
          :data="
            fund_base_label_data.filter(
              (v) =>
                v.fund_code == fund_had_code_selected || !fund_had_code_selected
            )
          "
          height="800"
        >
          <el-table-column
            prop="fund_label"
            label="行业"
            width="120"
          ></el-table-column>
          <el-table-column
            prop="fund_code"
            label="基金代码"
            width="120"
          ></el-table-column>
          <el-table-column
            prop="fund_name"
            label="基金名称"
            width="240"
          ></el-table-column>
          <!-- TODO 加个删除 -->
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="5">
      <el-row :span="5">
        <el-input
          v-model="new_author"
          placeholder="author"
          style="width: 140px"
        ></el-input>
        <el-select
          v-model="apps_selected"
          clearable
          filterable
          allow-create
          default-first-option
          placeholder="请选择apps"
          style="width: 140px"
        >
          <el-option
            v-for="item in author_app_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-switch
          v-model="isfirm"
          active-color="#13ce66"
          inactive-color="#ff4949"
        >
        </el-switch>
        <el-button
          type="primary"
          @click="add_fund_author"
          icon="el-icon-check"
        ></el-button>
      </el-row>
      <el-row :span="5">
        <el-table :data="fund_author_data" height="800">
          <el-table-column
            prop="funder_name"
            label="作者"
            width="160"
          ></el-table-column>
          <el-table-column
            prop="apps"
            label="行业"
            width="120"
          ></el-table-column>
          <el-table-column
            prop="is_firm"
            label="实盘"
            width="80"
            :formatter="isformat"
          ></el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="6">
      <el-row :span="5">
        <el-select
          v-model="fund_customer_fund_selected"
          clearable
          filterable
          default-first-option
          placeholder="请选择基金"
          style="width: 240px"
        >
          <el-option
            v-for="item in fund_customer_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-select
          v-model="fund_customer_label_selected"
          clearable
          filterable
          allow-create
          default-first-option
          placeholder="请选择行业"
          style="width: 120px"
        >
          <el-option
            v-for="item in fund_customer_label_option"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-button
          type="primary"
          @click="add_fund_customer_label"
          icon="el-icon-check"
        ></el-button>
      </el-row>
      <el-row :span="5">
        <el-table :data="fund_customer_label_data" height="800">
          <el-table-column
            prop="hist_label"
            label="分类"
            width="100"
          ></el-table-column>
          <el-table-column
            prop="fund_name"
            label="基金名称"
            width="300"
          ></el-table-column>
          <el-table-column label="操作" width="80">
            <template slot-scope="scope">
              <el-button
                @click="delete_fund_customer_label(scope.row)"
                type="text"
                size="small"
                >删</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
  </div>
</template>
  
<script>
import axios from "axios";
export default {
  data() {
    return {
      new_fund_label: "",
      fund_base_label: [],
      fund_base_label_selected: "",
      fund_base_label_option: [],
      fund_had_code_selected: "",
      fund_customer_option: [],
      fund_customer_fund_selected: "",
      fund_customer_label_option: [
        { label: "债券", value: "债券" },
        { label: "榜一", value: "榜一" },
        { label: "关注", value: "关注" },
        { label: "定投", value: "定投" },
      ],
      fund_customer_label_selected: "",
      fund_customer_label_data: [],
      fund_had_option: [],
      new_author: "",
      apps_selected: "",
      author_app_option: [],
      fund_base_label_data: [],
      fund_author_data: [],
      isfirm: null,
    };
  },
  mounted: function () {
    this.freshall();
  },
  methods: {
    freshall: function () {
      this.get_fund_base_label();
      this.get_fund_option();
      this.get_fund_base_label_data();
      this.get_author_app_option();
      this.get_fund_author_data();
      this.get_fund_customer_label_option();
    },
    // 添加行业标签
    add_new_label: function () {
      axios
        .post("/add_new_label", {
          new_fund_label: this.new_fund_label,
        })
        .then((response) => {
          this.new_fund_label = "";
          this.freshall();
        });
    },
    // 获取行业标签table和标签option
    get_fund_base_label: function () {
      axios.get("/get_fund_base_label").then((response) => {
        this.fund_base_label = response.data.data;
        this.fund_base_label_option = response.data.data_option;
      });
    },
    // 获取基金列表
    get_fund_option: function () {
      axios.get("/get_fund_info").then((response) => {
        this.fund_had_option = response.data.data;
      });
    },
    // 添加基金对应的行业标签
    add_fund_label: function () {
      axios
        .post("/add_fund_label", {
          fund_base_label_selected: this.fund_base_label_selected,
          fund_had_code_selected: this.fund_had_code_selected,
        })
        .then((response) => {
          this.fund_base_label_selected = "";
          this.fund_had_code_selected = "";
          this.freshall();
        });
    },
    // 获取基金-行业标签表格的数据
    get_fund_base_label_data: function () {
      axios.get("/get_fund_base_label_data").then((response) => {
        this.fund_base_label_data = response.data;
      });
    },
    // 添加基金评论作者
    add_fund_author: function () {
      axios
        .post("/add_fund_author", {
          new_author: this.new_author,
          apps_selected: this.apps_selected,
          isfirm: this.isfirm,
        })
        .then((response) => {
          this.new_author = "";
          this.apps_selected = "";
          this.isfirm = null;
          this.freshall();
        });
    },
    // 获得作者表格的数据
    get_fund_author_data: function () {
      axios.get("/get_fund_author_data").then((response) => {
        this.fund_author_data = response.data;
      });
    },
    // 获得作者所属的app的option
    get_author_app_option: function () {
      axios.get("/get_author_app_option").then((response) => {
        this.author_app_option = response.data;
      });
    },
    // 获得自定义标签的表格的数据和待分类的基金列表
    get_fund_customer_label_option: function () {
      axios.get("/get_fund_customer_label_option").then((response) => {
        // console.log(response);
        this.fund_customer_option = response.data.option_data;
        this.fund_customer_label_data = response.data.table_data;
      });
    },
    // 删除自定义标签
    delete_fund_customer_label: function (event) {
      axios
        .post("/delete_fund_customer_label", {
          fund_operation_lable_id: event.id,
        })
        .then((response) => {
          this.fund_customer_label_selected = "";
          this.fund_customer_fund_selected = "";
          this.freshall();
        });
    },
    // 添加基金的自定义标签
    add_fund_customer_label: function () {
      axios
        .post("/add_fund_customer_label", {
          fund_customer_label_selected: this.fund_customer_label_selected,
          fund_customer_fund_selected: this.fund_customer_fund_selected,
        })
        .then((response) => {
          this.fund_customer_label_selected = "";
          this.fund_customer_fund_selected = "";
          this.freshall();
        });
    },
    // 表格格式化
    isformat: function (row, index) {
      if (row.isfirm == 1) {
        return "是";
      } else {
        return "否";
      }
    },
  },
};
</script>
  
<style>
.el-row {
  margin-bottom: 5px;
}

.el-col {
  border-radius: 4px;
}
</style>
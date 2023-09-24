<template>
  <div id="app">
    <el-tabs v-model="ngatabname" @tab-click="ngatabClick">
      <el-tab-pane label="实时" name="nga_post_list">
        <el-row>
          <el-button
            type="primary"
            @click="getposttabledata"
            icon="el-icon-refresh"
            >刷新</el-button
          >
          <el-button
            type="primary"
            @click="
              is_gloabl = true;
              nga_reply_table = [];
              select_title = '';
            "
            icon="el-icon-refresh"
            >返回</el-button
          >
          <el-input
            placeholder="title"
            v-model="select_title"
            :disabled="true"
            style="width: 720px"
          >
          </el-input>
        </el-row>
        <el-row>
          <el-col :span="17" v-if="is_gloabl">
            <el-table
              :data="nga_post_table"
              style="width: 100%"
              height="820"
              @row-click="getonepost"
              ref="nga_post_table"
              :row-class-name="tablepostRowClassName"
            >
              <el-table-column
                prop="post_name"
                label="帖子名称"
                width="420"
              ></el-table-column>
              <el-table-column
                prop="user_name"
                label="发帖人"
                width="220"
              ></el-table-column>
              <el-table-column
                prop="create_time"
                label="发帖时间"
                sortable
                width="180"
              ></el-table-column>
              <el-table-column
                prop="reply_count"
                label="回复"
                sortable
                width="80"
              ></el-table-column>
              <el-table-column
                prop="reply_get"
                label="已爬"
                sortable
                width="80"
              ></el-table-column>
              <el-table-column
                prop="mrt"
                label="回复时间"
                sortable
                width="180"
              ></el-table-column>
              <el-table-column
                prop="fund_relation"
                label="相关股票"
                width="240"
              ></el-table-column>
              <el-table-column label="操作" width="60">
                <template slot-scope="scope">
                  <!-- TODO 手动更新一下某个帖子，然后局部刷新 -->
                  <el-button
                    @click="freshonepost(scope.row)"
                    type="text"
                    size="small"
                    >更</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
          </el-col>
          <el-col :span="16" v-if="!is_gloabl">
            <el-table
              :data="
                nga_reply_table.slice(
                  (currentPage - 1) * pageSize,
                  currentPage * pageSize
                )
              "
              style="width: 100%"
              height="820"
              ref="nga_reply_table"
              :row-class-name="tablepostRowClassName"
            >
              <el-table-column
                prop="nga_user_name"
                label="发帖人"
                width="180"
              ></el-table-column>
              <el-table-column
                prop="reply_sequence"
                label="楼"
                width="60"
              ></el-table-column>
              <el-table-column
                prop="reply_time"
                label="回帖时间"
                sortable
                width="180"
              ></el-table-column>
              <el-table-column
                prop="content"
                label="回复"
                width="480"
              ></el-table-column>
              <el-table-column
                prop="fund_relation"
                label="相关股票"
                width="240"
              ></el-table-column>
              <el-table-column
                prop="reply_attitude"
                label="nlp"
                width="120"
              ></el-table-column>
              <el-table-column label="操作" width="60">
                <template slot-scope="scope">
                  <!-- TODO 图片的展示方式 -->
                  <el-button
                    v-if="scope.row.has_image > 0"
                    type="text"
                    size="small"
                    >图</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
            <div class="tabListPage">
              <el-pagination
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                layout="total, prev, pager, next, jumper"
                :total="totalCount"
                :page-size="pageSize"
              >
              </el-pagination>
            </div>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="热力图" name="post_heatmap"> </el-tab-pane>
      <el-tab-pane label="特别关注" name="special_post">
        <!-- TODO 加特别关注  -->
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import axios from "axios";
var echarts = require("echarts");
export default {
  data() {
    return {
      ngatabname: "nga_post_list",
      is_gloabl: true,
      nga_post_table: [],
      nga_reply_table: [],
      post_click: "36271735",
      select_title: "",
      currentPage: 1,
      totalCount: 50,
      pageSize: 25,
    };
  },
  mounted: function () {
    this.init();
  },
  methods: {
    ngatabClick(tab, event) {
      // console.log(tab, event);
    },
    init: function () {
      this.getposttabledata();
      this.getreplytabledata();
    },
    getposttabledata: function () {
      axios.get("/getposttabledata").then((response) => {
        // console.log(response);
        this.nga_post_table = response.data;
        this.is_gloabl = true;
      });
    },
    getreplytabledata: function () {
      axios
        .post("/getreplytabledata", { tid: this.post_click })
        .then((response) => {
          // console.log(response);
          this.nga_reply_table = response.data;
          this.totalCount = response.data.length;
          return true;
        });
    },
    getonepost: function (row, event, column) {
      this.post_click = row.tid;
      this.getreplytabledata();
      this.select_title = row.post_name;
      this.is_gloabl = false;
    },
    handleCurrentChange: function (val) {
      this.currentPage = val;
    },
    freshonepost: function (event) {
      // TODO 还没实现，哈哈。
      console.log(event);
    },
    tablepostRowClassName({ row, rowIndex }) {
      // console.log(row);
      if (row["st"] === "special") {
        return "warning-row";
      } else {
        return "";
      }
    },
  },
  created: function () {
    this.getreplytabledata();
  },
};
</script>


<style>
.formlabelwidth {
  width: 120px;
}
.el-table .warning-row {
  background: rgba(145, 241, 132, 0.712);
}
</style>
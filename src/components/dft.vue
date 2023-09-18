<template>
  <div id="app">
    <el-row :span="5">
      <el-button
        type="primary"
        @click="showdialog"
        icon="el-icon-sell"
      ></el-button>
      <el-input
        v-model="dftnamesearch"
        placeholder="请输入文章名称"
        style="width: 300px"
      >
        <el-button
          slot="append"
          icon="el-icon-refresh"
          @click="dftnamesearch = ''"
        ></el-button
      ></el-input>
      <el-input
        v-model="dfttagssearch"
        placeholder="请输入标签名称"
        style="width: 300px"
      >
        <el-button
          slot="append"
          icon="el-icon-refresh"
          @click="dfttagssearch = ''"
        ></el-button
      ></el-input>
      <el-badge v-model="unread_count" class="item">
        <el-button size="small">未读</el-button>
      </el-badge>
    </el-row>
    <el-row :span="5">
      <el-col :span="24">
        <el-table
          :data="
            dfttabledata.filter(
              (data) =>
                (!dftnamesearch || data.title.includes(dftnamesearch)) &&
                (!dfttagssearch || data.tags.includes(dfttagssearch))
            )
          "
          style="width: 100%"
          height="900"
          @cell-click="showdocappendix"
        >
          <!-- <el-table-column
            property="isClose"
            label="已读"
            width="100"
            :formatter="isreadFormatter"
          ></el-table-column> -->
          <el-table-column
            property="isClose"
            :formatter="isreadFormatter"
            label="已读"
            width="100"
            :filters="[
              { text: '是', value: true },
              { text: '否', value: false },
            ]"
            :filter-method="filterTag"
            filter-placement="bottom-end"
          >
            <!-- <template slot-scope="scope">
              <el-tag
                :type="scope.row.isread === '是' ? 'primary' : 'success'"
                disable-transitions
                >{{ scope.row.isread }}</el-tag
              >
            </template> -->
          </el-table-column>
          <el-table-column prop="title" label="标题" width="400">
          </el-table-column>
          <el-table-column prop="author" label="作者名称" width="120">
          </el-table-column>
          <el-table-column prop="author_com" label="单位" width="120">
          </el-table-column>
          <el-table-column prop="url_org" label="知乎链接" width="500">
            <template scope="scope">
              <a
                :href="scope.row.url_org"
                target="_blank"
                style="text-decoration: none"
                >{{ scope.row.url_org }}</a
              >
            </template>
          </el-table-column>
          <!-- <el-table-column prop="url_csdn" label="csdn链接" width="300">
            <template scope="scope">
              <a
                :href="scope.row.url_csdn"
                target="_blank"
                style="text-decoration: none"
                >{{ scope.row.url_csdn }}</a
              >
            </template>
          </el-table-column> -->
          <el-table-column prop="tagslabel" label="标签" width="220">
          </el-table-column>
          <el-table-column prop="publish_time" label="发布时间" width="120">
          </el-table-column>
          <el-table-column prop="reading_time" label="阅读时间" width="120">
          </el-table-column>
          <el-table-column prop="doc_appendix_num" label="附件" width="120">
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template slot-scope="scope">
              <el-button @click="updatedft(scope.row)" type="text" size="small"
                >修改</el-button
              >
              <el-button @click="deletedft(scope.row)" type="text" size="small"
                >删除</el-button
              ></template
            >
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <el-dialog :visible.sync="dialogdftVisible" width="35%">
      <el-form :model="dftform" :rules="formrule">
        <el-row :span="5">
          <el-col :span="12">
            <el-form-item label="已读" :label-width="formLabelWidth">
              <el-switch v-model="dftform.isread"></el-switch>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :span="5">
          <el-col :span="7">
            <el-form-item label="作者" :label-width="formLabelWidth">
              <el-input
                v-model="dftform.author"
                style="width: 120px"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="7">
            <el-form-item label="公司" :label-width="formLabelWidth">
              <el-input
                v-model="dftform.author_com"
                style="width: 120px"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="7">
            <el-form-item
              label="耗时"
              :label-width="formLabelWidth"
              v-if="dftform.isread"
              prop="hours"
            >
              <el-input
                v-model.number="dftform.hours"
                style="width: 120px"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :span="5">
          <!-- <el-col :span="20">
            <el-form-item
              label="tags"
              :label-width="formLabelWidth"
              v-if="dftform.isread"
            >
              <el-input v-model="dftform.tags" style="width: 220px"></el-input>
            </el-form-item>
          </el-col> -->
          <el-col :span="4"></el-col>
          <el-col :span="20">
            <el-select
              label="标题"
              :label-width="formLabelWidth"
              v-model="dftform.tags"
              multiple
              clearable
              filterable
              allow-create
              default-first-option
              placeholder="请选择"
              style="width: 620px"
              v-if="dftform.isread"
            >
              <el-option
                v-for="item in dftdiroption"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </el-col>
        </el-row>
        <el-row :span="5">
          <el-form-item label="标题" :label-width="formLabelWidth">
            <el-input v-model="dftform.title" style="width: 575px"></el-input>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="base链接" :label-width="formLabelWidth">
            <el-input v-model="dftform.url_org" style="width: 575px"></el-input>
          </el-form-item>
        </el-row>

        <el-row :span="5">
          <el-col :span="12">
            <el-form-item label="发布时间" :label-width="formLabelWidth">
              <el-date-picker
                v-model="dftform.publish_time"
                type="date"
                placeholder="选择日期时间"
                value-format="yyyy-MM-dd"
              >
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="阅读时间"
              :label-width="formLabelWidth"
              v-if="dftform.isread"
            >
              <el-date-picker
                v-model="dftform.reading_time"
                type="datetime"
                placeholder="选择日期时间"
                value-format="yyyy-MM-dd HH:mm:ss"
              >
              </el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :span="5">
          <el-col :span="12">
            <el-form-item label="作者背景" :label-width="formLabelWidth">
              <el-input
                v-model="dftform.author_base"
                type="textarea"
                style="width: 575px"
                :autosize="{ minRows: 5 }"
                placeholder="作者背景"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="6">
            <el-input
              v-model="ixtags"
              style="width: 100px"
              placeholder="请输入标签"
            ></el-input>
          </el-col>
          <el-col :span="6">
            <el-input
              v-model="ixtitle"
              style="width: 100px"
              placeholder="请输入标题"
            ></el-input>
          </el-col>
          <el-col :span="6">
            <el-input
              v-model="ixurl"
              style="width: 300px"
              placeholder="请输入url"
            ></el-input>
          </el-col>
          <el-col :span="6">
            <el-button
              @click="addappendix"
              icon="el-icon-check"
              circle
              type="success"
              style="float: right; margin: 0 5px 0 5px"
            ></el-button>
          </el-col>
        </el-row>
        <el-row>
          <el-table :data="dftform.appendixtable" style="width: 100%">
            <el-table-column prop="tags" label="标签"> </el-table-column>
            <el-table-column prop="title" label="标题"> </el-table-column>
            <el-table-column prop="url" label="url"> </el-table-column>
            <el-table-column label="操作" width="170">
              <template slot-scope="dirscope">
                <el-button
                  @click="ixdelete(dirscope.$index, dftform.appendixtable)"
                  type="text"
                  size="small"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogdftVisible = false">取 消</el-button>
        <el-button type="primary" @click="commitdft">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog :visible.sync="dialogdftappendixVisible" width="45%">
      <el-table :data="dfttableappendixdata" style="width: 100%" height="500">
        <el-table-column prop="tags" label="标签" width="180"></el-table-column>
        <el-table-column
          prop="title"
          label="标题"
          width="300"
        ></el-table-column>
        <el-table-column prop="url" label="链接">
          <template scope="scope">
            <a
              :href="scope.row.url"
              target="_blank"
              style="text-decoration: none"
              >{{ scope.row.url }}</a
            >
          </template>
        </el-table-column></el-table
      >
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      dialogdftVisible: false,
      dialogdftappendixVisible: false,
      dfttabledata: [],
      unread_count: "",
      // dftreadsearch: "",
      dftnamesearch: "",
      dfttagssearch: "",
      dfttableappendixdata: [],
      dftform: {
        isread: false,
        doc_id: "",
        author: "",
        title: "",
        author_com: "",
        author_base: "",
        url_org: "",
        tags: [],
        hours: "",
        publish_time: "",
        reading_time: "",
        appendixtable: [],
      },
      formrule: {
        hours: [
          { required: true, message: "耗时不能为空" },
          { type: "number", message: "耗时必须为数字值" },
        ],
      },
      ixtags: "",
      ixtitle: "",
      ixurl: "",
      formLabelWidth: "100px",
      mode: "",
      dftdiroption: "",
    };
  },
  mounted: function () {
    this.init();
  },
  methods: {
    init: function () {
      this.getdftdata();
      this.getdftdir();
    },
    showdialog(type) {
      this.dialogdftVisible = true;
      this.mode = "add";
    },
    getdftdata: function () {
      axios.get("/getdftdata").then((response) => {
        this.dfttabledata = response.data.data;
        this.unread_count = response.data.unread_count;
      });
    },
    commitdft: function () {
      // console.log(this.orderform);
      axios
        .post("/commitdft", {
          dftform: this.dftform,
          mode: this.mode,
        })
        .then((response) => {
          // console.log(response);
          this.dftform = this.$options.data().dftform;
          this.dialogdftVisible = false;
          if (!response.data.res) {
            this.$message({
              message: "有的少分类，请人工修正数据",
              type: "warning",
            });
          }
          this.getdftdata();
        });
    },
    isreadFormatter: function (row, index) {
      // console.log(row);
      if (row.isread) {
        return "是";
      } else {
        return "否";
      }
    },
    filterTag(value, row) {
      // console.log(row.isread, value);
      return row.isread === value;
    },
    updatedft: function (event) {
      // console.log(event);
      this.dftform = event;
      this.dialogdftVisible = true;
      this.mode = "update";
    },
    deletedft: function (event) {
      // console.log(event);
      axios
        .post("/deletedft", {
          doc_id: event.doc_id,
        })
        .then((response) => {
          // console.log(response);
          this.getdftdata();
        });
    },
    addappendix: function () {
      this.dftform.appendixtable.push({
        tags: this.ixtags,
        title: this.ixtitle,
        url: this.ixurl,
      });
      this.ixtags = "";
      this.ixtitle = "";
      this.ixurl = "";
    },
    getdftdir: function () {
      axios.get("/getdftdir").then((response) => {
        this.dftdiroption = response.data.res;
      });
    },
    ixdelete: function (index, rows) {
      // console.log(rows);
      rows.splice(index, 1);
    },
    showdocappendix: function (row, column, cell, event) {
      // console.log(column, row.doc_id);
      if (column.label == "附件") {
        // console.log(row.doc_id);
        axios
          .post("/getappendixdata", {
            doc_id: row.doc_id,
          })
          .then((response) => {
            // console.log(response);
            this.dfttableappendixdata = response.data.data;
            this.dialogdftappendixVisible = true;
          });
        return;
      }
    },
  },
};
</script>


<style>
</style>
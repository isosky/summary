<template>
  <div id="app">
    <el-row type="flex">
      <el-button
        type="primary"
        icon="el-icon-sell"
        @click="dialogorderFormVisible = true"
        >新增书籍</el-button
      >
      <el-input
        v-model="booktypesearch"
        placeholder="请输入类型"
        style="width: 300px"
      >
        <el-button
          slot="append"
          icon="el-icon-refresh"
          @click="booktypesearch = ''"
        ></el-button
      ></el-input>
      <el-input
        v-model="booknamesearch"
        placeholder="请输入书名"
        style="width: 300px"
      >
        <el-button
          slot="append"
          icon="el-icon-refresh"
          @click="booknamesearch = ''"
        ></el-button
      ></el-input>
    </el-row>
    <el-row>
      <el-table
        :data="
          bookdata.filter(
            (data) =>
              (!booknamesearch || data.bookname.includes(booknamesearch)) &&
              (!booktypesearch || data.booktype.includes(booktypesearch))
          )
        "
        height="855"
      >
        <el-table-column
          label="类型"
          prop="booktype"
          width="120"
        ></el-table-column>
        <el-table-column
          label="子类型"
          prop="booksubtype"
          width="150"
        ></el-table-column>
        <el-table-column
          label="中图法"
          prop="ztf"
          width="150"
        ></el-table-column>
        <el-table-column
          label="书名"
          prop="bookname"
          width="500"
        ></el-table-column>
        <el-table-column
          label="购买日期"
          prop="buytime"
          width="120"
        ></el-table-column>
        <el-table-column
          label="地点"
          prop="location"
          width="120"
        ></el-table-column>
        <el-table-column label="ISBN" prop="isbn" width="150"></el-table-column>
        <el-table-column label="操作" width="170">
          <template slot-scope="scope">
            <el-button size="mini" @click="updatebook(scope.$index, scope.row)"
              >编辑</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-row>
    <el-dialog :visible.sync="dialogorderFormVisible" width="30%">
      <el-form :model="bookorderform">
        <el-row :span="5">
          <el-form-item label="类型" :label-width="formLabelWidth">
            <el-select
              v-model="bookorderform.booktype"
              @change="updatesuboption"
              clearable
              filterable
              allow-create
              default-first-option
              placeholder="请选择"
            >
              <el-option
                v-for="item in booktypeoption"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="子类型" :label-width="formLabelWidth">
            <el-select
              v-model="bookorderform.booksubtype"
              clearable
              filterable
              allow-create
              default-first-option
              placeholder="请选择"
            >
              <el-option
                v-for="item in booksubtypeoption"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="中图法分类" :label-width="formLabelWidth">
            <el-input
              v-model="bookorderform.ztf"
              style="width: 220px"
              @change="suggesttype"
              clearable
            ></el-input>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="ISBN" :label-width="formLabelWidth">
            <el-input
              v-model="bookorderform.ISBN"
              style="width: 220px"
              clearable
            ></el-input>
          </el-form-item>
        </el-row>
        <el-divider></el-divider>
        <el-row :span="5">
          <el-form-item label="书名" :label-width="formLabelWidth">
            <el-input
              v-model="bookorderform.bookname"
              style="width: 220px"
              clearable
            ></el-input>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="购买时间" :label-width="formLabelWidth">
            <el-date-picker
              v-model="bookorderform.buytime"
              type="date"
              placeholder="选择日期时间"
              value-format="yyyy-MM-dd"
            >
            </el-date-picker>
          </el-form-item>
        </el-row>
        <el-row :span="5">
          <el-form-item label="地点" :label-width="formLabelWidth">
            <el-select
              v-model="bookorderform.location"
              clearable
              filterable
              allow-create
              default-first-option
              placeholder="请选择"
            >
              <el-option
                v-for="item in locationoption"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="resetform">取 消</el-button>
        <el-button type="primary" @click="commitbookorders">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import axios from "axios";
export default {
  data() {
    return {
      bookdata: [],
      booknamesearch: "",
      booktypesearch: "",
      typesuggest: {},
      booktypeoption: [],
      bookalltypeoption: [],
      booksubtypeoption: [],
      locationoption: [],
      dialogorderFormVisible: false,
      formLabelWidth: "100px",
      bookorderform: {
        bookid: "",
        booktype: "",
        booksubtype: "",
        ztf: "",
        bookname: "",
        buytime: "",
        location: "",
        ISBN: "",
      },
    };
  },
  mounted: function () {
    this.init();
  },
  methods: {
    updatebook(index, row) {
      this.bookorderform.bookid = row.bookid;
      this.bookorderform.bookname = row.bookname;
      this.bookorderform.booktype = row.booktype;
      this.bookorderform.booksubtype = row.booksubtype;
      this.bookorderform.buytime = row.buytime;
      this.bookorderform.ztf = row.ztf;
      this.bookorderform.location = row.location;
      this.bookorderform.ISBN = row.isbn;
      this.dialogorderFormVisible = true;
    },
    init: function () {
      this.getbookoption();
      this.getbook();
    },
    getbook: function () {
      axios.get("/getbook").then((response) => {
        this.bookdata = response.data.data;
      });
    },
    getbookoption: function () {
      axios.get("/getbookoption").then((response) => {
        this.booktypeoption = response.data.booktypeoption;
        this.bookalltypeoption = response.data.bookalltypeoption;
        this.locationoption = response.data.locationoption;
        this.typesuggest = response.data.typesuggest;
      });
    },
    updatesuboption: function (event) {
      if (event != "" && this.bookalltypeoption != []) {
        this.bookorderform.booksubtype = "";
        this.booksubtypeoption = this.bookalltypeoption[event];
      }
      if (event == "") {
        this.booksubtypeoption = [];
        this.bookorderform.booksubtype = "";
      }
    },
    resetform: function () {
      this.bookorderform = this.$options.data().bookorderform;
      this.dialogorderFormVisible = false;
    },
    commitbookorders: function () {
      axios
        .post("/commitbookorders", {
          bookorderform: this.bookorderform,
        })
        .then((response) => {
          this.init();
          this.resetform();
        });
    },
    suggesttype: function (event) {
      this.bookorderform.ztf = event.toUpperCase();
      let temp = this.bookorderform.ztf;
      if (temp == "") {
        this.bookorderform.booktype = "";
        this.bookorderform.booksubtype = "";
        return;
      }
      if (this.typesuggest.hasOwnProperty(temp)) {
        this.bookorderform.booktype = this.typesuggest[temp].type;
        this.bookorderform.booksubtype = this.typesuggest[temp].subtype;
      }
    },
  },
};
</script>

<style>
</style>
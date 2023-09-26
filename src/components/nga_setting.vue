<template>
  <div id="app">
    <el-col :span="10">
      <el-row :span="5">
        <el-input
          v-model="new_nga_special_post_id"
          style="width: 200px"
        ></el-input>
        <el-button
          type="primary"
          @click="add_nga_special_post"
          icon="el-icon-check"
        ></el-button>
      </el-row>
      <el-row :span="5">
        <el-table :data="nga_special_post_data" height="800">
          <el-table-column prop="tid" label="tid" width="120"></el-table-column>
          <el-table-column
            prop="post_name"
            label="帖子名称"
            width="240"
          ></el-table-column>
          <el-table-column label="操作" width="80">
            <template slot-scope="scope">
              <el-button
                @click="delete_nga_special_post(scope.row)"
                type="text"
                size="small"
                >删</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-col>
    <el-col :span="10">
      <el-row :span="5">
        <el-input
          v-model="new_nga_special_user_id"
          style="width: 200px"
        ></el-input>
        <el-button
          type="primary"
          @click="add_nga_special_user"
          icon="el-icon-check"
        ></el-button>
      </el-row>
      <el-row :span="5">
        <el-table :data="nga_special_user_data" height="800">
          <el-table-column
            prop="nga_user_id"
            label="nga_user_id"
            width="120"
          ></el-table-column>
          <el-table-column
            prop="nga_user_name"
            label="用户名称"
            width="240"
          ></el-table-column>
          <el-table-column label="操作" width="80">
            <template slot-scope="scope">
              <el-button
                @click="delete_nga_special_user(scope.row)"
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
      new_nga_special_post_id: "",
      nga_special_post_data: [],
      new_nga_special_user_id: "",
      nga_special_user_data: [],
    };
  },
  mounted: function () {
    this.freshall();
  },
  methods: {
    freshall: function () {
      this.get_nga_specia_post();
      this.get_nga_specia_user();
    },
    delete_nga_special_post: function (event) {
      //   console.log(event);
      axios
        .post("/delete_nga_special_post", {
          delete_nga_special_post_id: event.tid,
        })
        .then((response) => {
          this.get_nga_specia_post();
        });
    },
    get_nga_specia_post: function () {
      axios.get("/get_nga_specia_post").then((response) => {
        this.nga_special_post_data = response.data.data;
      });
    },
    add_nga_special_post: function () {
      axios
        .post("/add_nga_special_post", {
          new_nga_special_post_id: this.new_nga_special_post_id,
        })
        .then((response) => {
          this.new_nga_special_post_id = "";
          this.get_nga_specia_post();
        });
    },
    delete_nga_special_user: function (event) {
      //   console.log(event);
      axios
        .post("/delete_nga_special_user", {
          delete_nga_special_user_id: event.nga_user_id,
        })
        .then((response) => {
          this.freshall();
        });
    },
    get_nga_specia_user: function () {
      axios.get("/get_nga_specia_user").then((response) => {
        this.nga_special_user_data = response.data.data;
      });
    },
    add_nga_special_user: function () {
      axios
        .post("/add_nga_special_user", {
          new_nga_special_user_id: this.new_nga_special_user_id,
        })
        .then((response) => {
          this.new_nga_special_user_id = "";
          this.freshall();
        });
    },
  },
};
</script>
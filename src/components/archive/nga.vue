<template>
    <div id="app">
        <el-tabs v-model="ngatabname">
            <el-tab-pane label="实时" name="nga_post_list">
                <el-row>
                    <el-button type="primary" icon="el-icon-refresh">刷新</el-button>
                </el-row>
                <el-row>
                    <el-col :span="22">
                        <el-table :data="nga_post_table" style="width:100%" height="820">
                            <el-table-column prop="post_name" label="帖子名称" width="520"></el-table-column>
                        </el-table>
                    </el-col>
                </el-row>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            ngatabname: "nga_post_list",
            nga_post_table: [],
        };
    },
    mounted: function () { },
};
</script>

<style>
.el-table .warning-row {
    background: rgba(145, 241, 132, 0.712);
}
</style>

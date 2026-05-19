<template>
    <div id="app">
        <el-col :span="10">
            <el-row :span="5">
                <el-input v-model="new_nga_special_post_id" style="width:200px"></el-input>
                <el-button type="primary" icon="el-icon-check">添加</el-button>
            </el-row>
            <el-row :span="5">
                <el-table :data="nga_special_post_data" height="800">
                    <el-table-column prop="tid" label="tid" width="120"></el-table-column>
                </el-table>
            </el-row>
        </el-col>
    </div>
</template>

<script>
export default {
    data() {
        return {
            new_nga_special_post_id: "",
            nga_special_post_data: [],
        };
    },
    mounted: function () { },
};
</script>

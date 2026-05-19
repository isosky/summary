<template>
    <div id="app">
        <el-row :span="5">
            <el-button type="primary" @click="showdialog" icon="el-icon-sell"></el-button>
            <el-input v-model="dftnamesearch" placeholder="请输入文章名称" style="width: 300px">
                <el-button slot="append" icon="el-icon-refresh" @click="dftnamesearch = ''"></el-button></el-input>
            <el-input v-model="dfttagssearch" placeholder="请输入标签名称" style="width: 300px">
                <el-button slot="append" icon="el-icon-refresh" @click="dfttagssearch = ''"></el-button></el-input>
            <el-badge v-model="unread_count" class="item">
                <el-button size="small">未读</el-button>
            </el-badge>
        </el-row>
        <el-row :span="5">
            <el-col :span="24">
                <el-table :data="dfttabledata.filter(
                    (data) =>
                        (!dftnamesearch || data.title.includes(dftnamesearch)) &&
                        (!dfttagssearch || data.tags.includes(dfttagssearch))
                )
                    " style="width: 100%" height="900" @cell-click="showdocappendix">
                    <el-table-column property="isClose" :formatter="isreadFormatter" label="已读" width="100" :filters="[
                        { text: '是', value: true },
                        { text: '否', value: false },
                    ]" :filter-method="filterTag" filter-placement="bottom-end">
                    </el-table-column>
                    <el-table-column prop="title" label="标题" width="400">
                    </el-table-column>
                    <el-table-column prop="author" label="作者名称" width="120">
                    </el-table-column>
                    <el-table-column prop="author_com" label="单位" width="120">
                    </el-table-column>
                    <el-table-column prop="url_org" label="知乎链接" width="500">
                        <template scope="scope">
                            <a :href="scope.row.url_org" target="_blank" style="text-decoration: none">{{
                                scope.row.url_org }}</a>
                        </template>
                    </el-table-column>
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
                            <el-button @click="updatedft(scope.row)" type="text" size="small">修改</el-button>
                            <el-button @click="deletedft(scope.row)" type="text" size="small">删除</el-button></template>
                    </el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <!-- Archived component: original logic preserved here for reference -->
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
            dftnamesearch: "",
            dfttagssearch: "",
        };
    },
    mounted: function () {
        this.init();
    },
    methods: {
        init: function () {
            // archived: original methods retained in archive copy
        },
    },
};
</script>

<style></style>

<template>
    <div id="app">
        <el-col :span="12">
            <el-row :gutter="5">
                <el-button type="primary" @click="showdialog" icon="el-icon-sell"></el-button>
                <el-select v-model="cycling_type_selected" clearable filterable default-first-option placeholder="请选择"
                    style="width: 220px">
                </el-select>
            </el-row>
            <div class="grid-content">
                <el-table :data="cyclingdata" border height="855" style="width: 100%"
                    :default-sort="{ prop: 'date', order: 'descending' }">
                    <el-table-column prop="date" sortable label="日期" width="180"></el-table-column>
                    <el-table-column prop="strava_id" label="strava_id" width="120"></el-table-column>
                    <el-table-column prop="name" label="名称" width="110"></el-table-column>
                </el-table>
            </div>
        </el-col>
        <el-col :span="12">
            <div id="cycling_charts" style="height: 240px">图零</div>
        </el-col>
    </div>
</template>

<script>
export default {
  data() {
    return {
      cyclingdata: [],
      cycling_type_selected: ''
    };
  },
  mounted: function() { },
  methods: {
    init: function() { }
  }
};
</script>

<style>
.el-table {
    overflow: visible !important;
}
</style>

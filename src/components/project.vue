<template>
    <!-- TODO 重构界面 增加  4象限，然后展示4象限-->
    <div id="app">
        <el-col :span="5">
            <el-table :data="projectdata" height="1080" style="width: 100%" @cell-click="showprojectdetail">
                <el-table-column prop="level2" sortable label="二级" width="100"></el-table-column>
                <el-table-column prop="level3" sortable label="三级" width="130"></el-table-column>
                <el-table-column prop="task_count" sortable label="任务" width="80">
                </el-table-column>
                <el-table-column prop="person_count" sortable label="人员" width="80">
                </el-table-column>
                <el-table-column label="操作" width="50">
                    <template slot-scope="scope">
                        <el-button @click="update_project(scope.row)" type="text" size="small">编辑
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
        <el-col :span="19">
            <el-row :span="18">
                <div
                    style="display: flex;  align-items: center;  padding: 0;  border-bottom: 1px solid #c2c4ca; margin: 0 auto;">
                    <div style="line-height: 30px; padding: 0;">
                        <ul>
                            <li>
                                项目名称：{{ this.project_name }}
                            </li>
                            <li>
                                开始时间：{{ this.project_start_time }}
                            </li>
                            <li>
                                最后时间：{{ this.project_last_time }}
                            </li>
                        </ul>
                    </div>
                    <div style="line-height: 30px; left: 100px; width: 800px;"> 项目简介
                        <el-input type="textarea" v-model="project_desc"></el-input>
                    </div>
                    <div>
                        <el-button icon="el-icon-check" type="success" circle @click="updateprojectdesc"></el-button>
                    </div>
                </div>

            </el-row>
            <el-row :gutter="5">
                <el-tabs v-model="tabs_select" :lazy="true" type="border-card" @tab-click="tabclick">
                    <el-tab-pane name="project_task" label="项目对应任务">
                        <el-col :span="12">
                            <el-table :data="project_task_data" border height="1000" style="width: 100%"
                                :cell-style="isoverdate">
                                <el-table-column prop="stime" label="添加日期" width="120"></el-table-column>
                                <el-table-column prop="etime" label="应完成" width="120"></el-table-column>
                                <el-table-column prop="ftime" label="实际完成" width="120"></el-table-column>
                                <el-table-column prop="task_name" label="内容" width="400"></el-table-column>
                                <el-table-column prop="status" label="状态" width="100"></el-table-column>
                            </el-table>
                        </el-col>
                        <el-col :span="12">
                            <div id="project_task_summary" style="height: 450px"></div>
                            <div id="project_taskstatus_summary" style="height: 250px"></div>
                        </el-col>
                    </el-tab-pane>
                    <el-tab-pane name="project_person" label="项目对应人员">
                        <el-col :span="9">
                            <el-table :data="project_person_data" border height="1000" style="width: 100%">
                                <el-table-column prop="company" label="公司" width="75"></el-table-column>
                                <el-table-column prop="department" label="部门" width="75"></el-table-column>
                                <el-table-column prop="post" label="职位" width="75"></el-table-column>
                                <el-table-column prop="person_name" label="姓名" width="80">
                                </el-table-column>
                                <el-table-column prop="project_activity" sortable label="积极" width="80">
                                </el-table-column>
                                <el-table-column prop="project_critical" sortable label="批评" width="80">
                                </el-table-column>
                                <el-table-column prop="all_activity" label="积极a" width="70">
                                </el-table-column>
                                <el-table-column prop="all_critical" label="批评a" width="70">
                                </el-table-column>
                                <el-table-column prop="task_count" sortable label="任务数" width="95">
                                </el-table-column>
                            </el-table>
                        </el-col>
                        <el-col :span='15'>
                            <div id="project_person_graph" style="height: 800px"></div>
                        </el-col>
                    </el-tab-pane>
                </el-tabs>
            </el-row>
        </el-col>
    </div>
</template>



<script>
import axios from "axios";
var echarts = require("echarts");
export default {
    data() {
        return {
            projectdata: [],
            select_project_id: '',
            tabs_select: "project_task",
            project_name: '',
            project_start_time: '',
            project_last_time: '',
            project_desc: '',
            project_task_data: [],
            project_task_summary_chart: '',
            project_taskstatus_summary_chart: "",
            project_task_summary_chart_option: {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                color: ["green", "black", "#939393"],
                legend: {
                    data: ['完成', '超时', '删除']
                },

                xAxis:
                {
                    type: 'category',
                    axisTick: { show: false },
                    data: []
                }
                ,
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: '完成',
                        type: 'bar',
                        stack: 'total',
                        barGap: 0,
                        label: {
                            show: true
                        },
                        emphasis: {
                            focus: 'series'
                        },
                        data: []
                    },
                    {
                        name: '超时',
                        stack: 'total',
                        type: 'bar',
                        label: {
                            show: true
                        },
                        emphasis: {
                            focus: 'series'
                        },
                        data: []
                    },
                    {
                        name: '删除',
                        stack: 'total',
                        type: 'bar',
                        label: {
                            show: true
                        },
                        emphasis: {
                            focus: 'series'
                        },
                        data: []
                    }
                ]
            },
            project_taskstatus_summary_chart_option: {
                title: {
                    text: "任务统计",
                    x: "center",
                },
                color: ["black", "red", "Orange", "green", "#939393"],
                tooltip: {
                    trigger: "item",
                    formatter: "{a} <br/>{b} : {c} ({d}%)",
                },
                series: [{
                    name: "任务情况",
                    type: "pie",
                    radius: "55%",
                    center: ["50%", "60%"],
                    data: [],
                    label: {
                        show: true,
                        position: "outer",
                        alignTo: "labelLine",
                        formatter: "{b}：{c}",
                    },
                },],
            },
            project_desc: '',
            project_person_data: [],
            project_person_graph_chart: '',
            project_person_graph_chart_option: {
                legend: [
                    { data: [] }
                ],
                series: [
                    {
                        type: 'graph',
                        layout: 'force',
                        symbolSize: 50,
                        roam: true,
                        label: {
                            show: true
                        },
                        edgeSymbol: ['circle', 'arrow'],
                        edgeSymbolSize: [4, 10],
                        edgeLabel: {
                            fontSize: 20
                        },
                        categories: [],
                        data: [],
                        links: [],
                        force: {
                            repulsion: 1000
                        }
                    }
                ]
            },
        };
    },
    mounted: function () {
        this.init();
        this.project_task_summary_chart = echarts.init(
            document.getElementById("project_task_summary"),
            "white", {
            renderer: "canvas",
        }
        );
        this.project_taskstatus_summary_chart = echarts.init(
            document.getElementById("project_taskstatus_summary"),
            "white", {
            renderer: "canvas",
        }
        );
    },
    methods: {
        init: function () {
            this.getproject();

        },
        getproject: function () {
            axios.get("/getproject").then((response) => {
                // console.log(response);
                this.projectdata = response.data;
            });
        },
        showprojectdetail: function (row, column, cell, event) {
            // console.log(row)
            this.select_project_id = row.project_id;
            if (this.tabs_select == 'project_task') {
                this.get_project_task()
            } else {
                this.get_project_person()
            }
            this.get_project_detail()

        },
        get_project_detail: function () {
            axios.post("/update_project_detail", { project_id: this.select_project_id }).then((response) => {
                this.project_desc = response.data.project_desc
                this.project_last_time = response.data.project_last_time
                this.project_start_time = response.data.project_start_time
                this.project_name = response.data.project_name

            })
        },
        updateprojectdesc: function () {
            axios.post("/update_project_desc", { project_id: this.select_project_id, project_desc: this.project_desc }).then((response) => {

            })
        },
        get_project_task: function () {
            axios
                .post("/get_task_by_project_id", {
                    project_id: this.select_project_id,
                })
                .then((response) => {
                    // console.log(response)
                    this.project_task_data = response.data.project_task_data;
                    // pie summary图
                    this.project_taskstatus_summary_chart_option.series[0].data =
                        response.data.project_pie_data.pie_summary_data;
                    this.project_taskstatus_summary_chart_option.title.text =
                        "完成率:" +
                        response.data.project_pie_data.percent[0] +
                        "%，逾期率:" +
                        response.data.project_pie_data.percent[1] +
                        "%";
                    this.project_taskstatus_summary_chart_option.title.subtext =
                        "总统计数:" + response.data.project_pie_data.sum_task + "个";
                    this.project_taskstatus_summary_chart.setOption(this.project_taskstatus_summary_chart_option);
                    // bar 图
                    this.project_task_summary_chart_option.xAxis.data = response.data.project_bar_data.ym;
                    this.project_task_summary_chart_option.series[0].data = response.data.project_bar_data.bar_data['完成'];
                    this.project_task_summary_chart_option.series[1].data = response.data.project_bar_data.bar_data['超时'];
                    this.project_task_summary_chart_option.series[2].data = response.data.project_bar_data.bar_data['删除'];
                    this.project_task_summary_chart.setOption(this.project_task_summary_chart_option);
                });
        },
        get_project_person: function () {
            // todo 判断是否有选中
            if (this.select_project_id == null) {
                return
            }
            axios.post("/get_person_by_project_id", {
                project_id: this.select_project_id,
            }).then((response) => {
                // console.log(response)
                this.project_person_data = response.data.project_person_data;
                this.project_person_graph_chart_option.legend[0].data = response.data.project_person_graph.legend;
                this.project_person_graph_chart_option.series[0].data = response.data.project_person_graph.nodes;
                this.project_person_graph_chart_option.series[0].links = response.data.project_person_graph.links;
                this.project_person_graph_chart_option.series[0].categories = response.data.project_person_graph.categories;
                console.log(this.project_person_graph_chart_option);
                this.project_person_graph_chart.setOption(this.project_person_graph_chart_option);
            })
        },
        tabclick: function () {
            if (this.tabs_select == "project_person") {
                // console.log(document.getElementById("sankey_chart_div"));
                if (this.project_person_graph_chart == "") {
                    setTimeout(() => {
                        this.project_person_graph_chart = echarts.init(
                            document.getElementById("project_person_graph"),
                            "white",
                            {
                                renderer: "canvas",
                            }
                        );
                        this.get_project_person()

                    }, 500);
                } else { this.get_project_person() }
            }
        },
        isoverdate: function ({
            row,
            column,
            rowIndex,
            columnIndex
        }) {
            // console.log(row);
            if (columnIndex == 4) {
                if (row.status == '待做逾期') {
                    return "background-color:red;color:white";
                }
                if (row.status == '及时') {
                    return "background-color:green;color:white";
                }
                if (row.status == '超时') {
                    return "background-color:black;color:white";
                }
                if (row.status == '删除') {
                    return "background-color:gray;color:white";
                }
            }
        },
    },
};
</script>

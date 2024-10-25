<template>
    <!-- TODO 重构界面 增加  4象限，然后展示4象限-->
    <div id="app">
        <el-row :gutter="5">
            <!-- 左侧面板 -->
            <el-col :span="11">
                <!-- 任务管理条 -->
                <el-row :gutter="5">
                    <el-col :span="3">
                        <el-select @change="updatelevel2option" clearable filterable allow-create default-first-option
                            v-model="task_level1_select" placeholder="请选择">
                            <el-option v-for="item in task_level1_option" :key="item.value" :label="item.label"
                                :value="item.value"></el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="4">
                        <el-select @change="updatelevel3option" v-model="task_level2_select" filterable clearable
                            allow-create default-first-option placeholder="请选择">
                            <el-option v-for="item in task_level2_option" :key="item.value" :label="item.label"
                                :value="item.value"></el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="4">
                        <el-select v-model="task_level3_select" filterable clearable allow-create default-first-option
                            placeholder="请选择">
                            <el-option v-for="item in task_level3_option" :key="item.value" :label="item.label"
                                :value="item.value"></el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="6">
                        <el-date-picker :picker-options="{ firstDayOfWeek: 1 }" v-model="new_edate"
                            value-format="yyyy-MM-dd" type="date" placeholder="ddl" @change="setdate"></el-date-picker>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="4">
                        <el-input v-model="task_title" style="width: 640px" placeholder="请输入内容"></el-input>
                    </el-col>
                </el-row>
                <el-row :gutter="5">
                    <el-col :span="10">
                        <el-date-picker v-model="query_duration" type="daterange" unlink-panels
                            value-format="yyyy-MM-dd" range-separator="至" start-placeholder="开始日期"
                            end-placeholder="结束日期" :picker-options="pickerOptions" @change="setdate">
                        </el-date-picker>
                    </el-col>
                    <el-col :span="5">
                        <el-checkbox-button v-model="isstime" @change="setdate">查添加日期</el-checkbox-button>
                        <el-checkbox-button v-model="isqueryall">全查</el-checkbox-button>
                    </el-col>
                    <el-col :span="9">
                        <el-button @click="querytask_week" icon="el-icon-date" circle type="warning"
                            style="float: right; margin: 0 5px 0 5px"></el-button>
                        <el-button @click="resetall" icon="el-icon-refresh" circle type="warning"
                            style="float: right; margin: 0 5px 0 5px"></el-button>
                        <el-button @click="querytask('table')" icon="el-icon-search" type="success" circle
                            style="float: right; margin: 0 5px 0 5px"></el-button>
                        <!-- <el-badge :value="12" class="item"> -->
                        <el-button @click="diashowperson()" icon="el-icon-user" circle type="success"
                            style="float: right; margin: 0 5px 0 5px"></el-button>
                        <!-- </el-badge> -->
                        <el-button @click="addtask" icon="el-icon-check" circle type="success"
                            style="float: right; margin: 0 5px 0 5px"></el-button>
                    </el-col>
                </el-row>
                <div class="grid-content">
                    <el-table :data="tableData" border height="855" :cell-style="isoverdate" style="width: 100%"
                        :default-sort="{ prop: 'tetime', order: 'ascending' }" @cell-click="showprocess">
                        <el-table-column fixed prop="etime" sortable label="DDL" width="95"></el-table-column>
                        <el-table-column prop="level1" label="一级" width="80"></el-table-column>
                        <el-table-column prop="level2" label="二级" width="80"></el-table-column>
                        <el-table-column prop="level3" label="三级" width="80"></el-table-column>
                        <el-table-column prop="task_name" label="标题"></el-table-column>
                        <el-table-column prop="num_person" label="人员" width="60"></el-table-column>
                        <el-table-column prop="num_process" label="进展" width="60"></el-table-column>
                        <el-table-column label="操作" width="170">
                            <template slot-scope="scope">
                                <el-button @click="diashowprocess(scope.row)" type="text" size="small">更新</el-button>
                                <el-button @click="finishtask(scope.row)" type="text" size="small">完成</el-button>
                                <el-button @click="updatetask(scope.row)" type="text" size="small">修改</el-button>
                                <el-button @click="deletetask(scope.row)" type="text" size="small">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </el-col>
            <!-- 右侧面板 -->
            <el-col :span="13">
                <el-row :gutter="5">
                    <el-col :span="8">
                        <div id="b_task" style="height: 220px"></div>
                    </el-col>
                    <el-col :span="8">
                        <div id="task_pie_subject" style="height: 220px"></div>
                    </el-col>
                    <el-col :span="8">
                        <div id="task_pie_summary" style="height: 220px"></div>
                    </el-col>
                </el-row>
                <el-row :gutter="5">
                    <el-tabs v-model="tabs_select" :lazy="true" type="border-card" @tab-click="tabclick">
                        <el-tab-pane name="summary" label="统计">
                            <div id="task_summary" style="height: 650px"></div>
                        </el-tab-pane>
                        <el-tab-pane name="process" label="进展">
                            <el-table :data="tableprocess" border height="455" style="width: 100%">
                                <el-table-column prop="stime" label="日期" width="100"></el-table-column>
                                <el-table-column prop="process_name" label="内容" width="400"></el-table-column>
                                <el-table-column prop="isfinish" label="状态" width="100"></el-table-column>
                                <el-table-column label="操作" width="170">
                                    <template slot-scope="scope">
                                        <el-button @click="deleteprocess(scope.row)" type="text"
                                            size="small">删除</el-button>
                                        <el-button @click="showupdateprocess(scope.row)" type="text"
                                            size="small">修改</el-button>
                                        <el-button v-if="scope.row.isfinish == '完成'" @click="resetprocess(scope.row)"
                                            type="text" size="small">待做</el-button>
                                        <el-button v-if="scope.row.isfinish == '待做'" @click="finishprocess(scope.row)"
                                            type="text" size="small">完成</el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-tab-pane>
                        <el-tab-pane name="person" label="人员">
                            <el-row :gutter="5">
                                <el-select v-model="person" filterable :filter-method="personFilter" clearable multiple
                                    default-first-option style="width: 400px" placeholder="请选择相关人员">
                                    <el-option v-for="item in person_option" :key="item.value" :label="item.label"
                                        :value="item.value"></el-option>
                                </el-select>
                                <el-button @click="appendtaskperson" type="success">追加人员</el-button>
                            </el-row>
                            <el-row :gutter="5">
                                <el-table :data="persondata" style="width: 100%">
                                    <el-table-column prop="company" label="单位" width="180">
                                    </el-table-column>
                                    <el-table-column prop="person_name" label="名称" width="180">
                                    </el-table-column>
                                    <el-table-column prop="sub_activity" label="本分类积极性" width="120">
                                    </el-table-column>
                                    <el-table-column prop="sub_critical" label="本分类批评性" width="120">
                                    </el-table-column>
                                    <el-table-column prop="all_activity" label="平均积极性" width="120">
                                    </el-table-column>
                                    <el-table-column prop="all_critical" label="平均批评性" width="120">
                                    </el-table-column>
                                    <el-table-column label="操作" width="170">
                                        <template slot-scope="scope">
                                            <el-button @click="deletetaskperson(scope.row)" type="text"
                                                size="small">删除</el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </el-row>
                        </el-tab-pane>
                        <el-tab-pane name="finishtask" label="任务对应分类">
                            <el-table :data="finishtaskdata" style="width: 100%">
                                <el-table-column prop="dir" label="类型" width="120">
                                </el-table-column>
                                <el-table-column prop="sub_dir" label="子类型" width="120">
                                </el-table-column>
                                <el-table-column prop="hours" label="耗时" width="120">
                                </el-table-column>
                            </el-table>
                        </el-tab-pane>
                    </el-tabs>
                </el-row>
            </el-col>
        </el-row>
        <!-- 各种弹出框 -->
        <!-- 更新 -->
        <el-dialog @close="dialogpersonVisible = false" title="添加人员" :visible="dialogpersonVisible" width="40%">
            <div>
                <el-checkbox-group v-model="personrecommendselected">
                    <el-checkbox v-for="t in personrecommend" :key="t.id" :label="t.label"
                        @change="addrecommendperson(t.id)"></el-checkbox>
                </el-checkbox-group>
            </div>
            <el-divider></el-divider>
            <el-transfer v-model="person" :data="pppdata" filterable :filter-method="personfilterMethod"
                filter-placeholder="请输入拼音首字母" :titles="['所有人', '关联人']"></el-transfer>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogpersonVisible = false">关 闭</el-button>
            </span>
        </el-dialog>

        <el-dialog @close="closedialog" title="提示" :visible.sync="dialogpVisible" width="30%">
            <div>{{ v_task_content }}</div>
            <el-input v-model="input_process" type="textarea" style="width: 500px" :autosize="{ minRows: 5 }"
                placeholder="请输入进展"></el-input>

            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogpVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogaddprocess">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 完成 -->
        <!-- TODO 修改这个面板 -->
        <el-dialog @close="closedialog" title="提示" :visible.sync="dialogsVisible" width="70%">
            <el-container>
                <el-main>
                    <el-form ref="form" :model="finishtaskform" label-width="80px">
                        <el-form-item label="耗时">
                            <el-slider :min="0" :max="8" :step="0.5" show-input show-stops
                                v-model="finishtaskform.hours"></el-slider>
                        </el-form-item>
                        <el-row>
                            <el-col :span="3">
                                <el-form-item label="是否有效">
                                    <el-switch v-model="finishtaskform.isok"></el-switch>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row>
                            <el-col :span="12">
                                <el-row>
                                    <el-col :span="6">
                                        <el-select @change="updatediroption" clearable filterable allow-create
                                            default-first-option v-model="dir_select" placeholder="请选择">
                                            <el-option v-for="item in dir_select_option" :key="item.value"
                                                :label="item.label" :value="item.value"></el-option>
                                        </el-select>
                                    </el-col>
                                    <el-col :span="6">
                                        <el-select v-model="dir_sub_select" filterable clearable allow-create
                                            default-first-option placeholder="请选择">
                                            <el-option v-for="item in dir_sub_select_option" :key="item.value"
                                                :label="item.label" :value="item.value"></el-option>
                                        </el-select>
                                    </el-col>
                                    <el-col :span="6">
                                        <el-input v-model="dir_hours" style="width: 120px"
                                            placeholder="请输时长"></el-input>
                                    </el-col>
                                    <el-button @click="adddir" icon="el-icon-check" circle type="success"
                                        style="float: right; margin: 0 5px 0 5px"></el-button>
                                </el-row>
                                <el-row>
                                    <el-table :data="finishtaskform.dirtable" style="width: 100%">
                                        <el-table-column prop="dir" label="父类"> </el-table-column>
                                        <el-table-column prop="sub_dir" label="子类">
                                        </el-table-column>
                                        <el-table-column prop="hours" label="时长">
                                        </el-table-column>
                                        <el-table-column label="操作" width="170">
                                            <template slot-scope="dirscope">
                                                <el-button @click="
                                                    dirdeletetask(
                                                        dirscope.$index,
                                                        finishtaskform.dirtable
                                                    )
                                                    " type="text" size="small">删除</el-button>
                                            </template>
                                        </el-table-column>
                                    </el-table>
                                </el-row>
                            </el-col>
                            <el-col :span="12">
                                <el-row>
                                    <el-button @click="scoresth($event)" type="success" name="1">1</el-button>
                                    <el-button @click="scoresth($event)" type="success" name="2">2</el-button>
                                    <el-button @click="scoresth($event)" type="success" name="3">3</el-button>
                                    <el-button @click="scoresth($event)" type="success" name="4">4</el-button>
                                    <el-button @click="scoresth($event)" type="success" name="5">5</el-button>
                                    <el-button @click="scoresth($event)" type="success" name="6">6</el-button>
                                    <el-button @click="scoresth($event)" type="success" name="7">7</el-button>
                                    <el-button @click="leaveclick" icon="el-icon-check" type="success"></el-button>
                                </el-row>
                                <el-row>
                                    <el-table ref="singleTable" :data="finishtaskform.peoples" style="width: 100%"
                                        class="tb-edit" highlight-current-row :row-class-name="tableRowClassName"
                                        @row-click="handleCurrentChange">
                                        <el-table-column prop="person_name" label="姓名" align="center">
                                        </el-table-column>
                                        <el-table-column prop="score_activity" label="积极性" align="center">
                                            <template scope="scope">
                                                <el-input size="small" v-model="scope.row.score_activity"
                                                    placeholder="请输入内容"
                                                    @change="handleEdit(scope.$index, scope.row)"></el-input>
                                                <span>{{ scope.row.score_activity }}</span>
                                            </template>
                                        </el-table-column>
                                        <el-table-column prop="score_critical" label="批判性" align="center">
                                            <template scope="scope">
                                                <el-input size="small" v-model="scope.row.score_critical"
                                                    placeholder="请输入内容"
                                                    @change="handleEdit(scope.$index, scope.row)"></el-input>
                                                <span>{{ scope.row.score_critical }}</span>
                                            </template>
                                        </el-table-column>
                                    </el-table>
                                </el-row>
                            </el-col>
                        </el-row>

                        <el-form-item label="描述">
                            <el-input type="textarea" v-model="finishtaskform.desc"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="committask">完成任务</el-button>
                        </el-form-item>
                    </el-form>
                </el-main>
                <el-aside width="350px" style="background-color: rgb(238, 241, 246)">
                    <el-row>
                        <span>积极性评价</span>
                    </el-row>
                    <el-row>
                        <el-table :data="scoreactivity" style="width: 100%">
                            <el-table-column prop="stype" label="项目"> </el-table-column>
                            <el-table-column prop="pic" label="负责人"> </el-table-column>
                            <el-table-column prop="pe" label="参与者"> </el-table-column>
                            <el-table-column prop="po" label="其他"> </el-table-column>
                        </el-table>
                    </el-row>
                    <el-row> <span>批判性评价</span></el-row>
                    <el-row>
                        <el-table :data="scorecritical" style="width: 100%">
                            <el-table-column prop="stype" label="项目"> </el-table-column>
                            <el-table-column prop="pic" label="负责人"> </el-table-column>
                            <el-table-column prop="pe" label="参与者"> </el-table-column>
                            <el-table-column prop="po" label="其他"> </el-table-column>
                        </el-table>
                    </el-row>
                </el-aside>
            </el-container>
        </el-dialog>

        <!-- 修改 -->
        <el-dialog @close="closedialog" title="确认修改任务？？" :visible.sync="dialoguVisible" width="40%">
            <el-date-picker :picker-options="{ firstDayOfWeek: 1 }" v-model="duetime" value-format="yyyy-MM-dd"
                type="date" style="width: 150px"></el-date-picker>
            <!-- 修改任务面板里面的一级分类 -->
            <el-select @change="updatelevel2option" clearable default-first-option v-model="task_level1_select"
                style="width: 120px" placeholder="请选择">
                <el-option v-for="item in task_level1_option" :key="item.value" :label="item.label"
                    :value="item.value"></el-option>
            </el-select>
            <!-- 修改任务面板里面的二级分类 -->
            <el-select @change="updatelevel3option" v-model="task_level2_select" filterable clearable allow-create
                default-first-option style="width: 120px" placeholder="请选择">
                <el-option v-for="item in task_level2_option" :key="item.value" :label="item.label"
                    :value="item.value"></el-option>
            </el-select>
            <!-- 修改任务面板里面的三级分类 -->
            <el-select v-model="task_level3_select" filterable clearable allow-create default-first-option
                style="width: 120px" placeholder="请选择">
                <el-option v-for="item in task_level3_option" :key="item.value" :label="item.label"
                    :value="item.value"></el-option>
            </el-select>
            <el-input v-model="dutitle" style="width: 300px"></el-input>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialoguVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogupdate">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 删除 -->
        <el-dialog @close="closedialog" title="确认删除任务？？" :visible.sync="dialogcVisible" width="30%">
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogcVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogdelete">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 修改process -->
        <el-dialog @close="closedialog" title="提示" :visible.sync="dialogprocessVisible" width="30%">
            <div>{{ process_content }}</div>
            <el-input v-model="process_content" type="textarea" placeholder="请输入完成情况" style="width: 500px"
                :autosize="{ minRows: 5 }"></el-input>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogprocessVisible = false">取 消</el-button>
                <el-button type="primary" @click="updateprocess">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import axios from "axios";
import PinyinMatch from "pinyin-match";
var echarts = require("echarts");
export default {
    data: function () {
        return {
            currentRow: null,
            scoreactivity: [{
                stype: "初始",
                pic: 1.5,
                pe: 0,
                po: -2.5
            },
            {
                stype: "延期",
                pic: 0,
                pe: -1.5,
                po: -2.5
            },
            {
                stype: "有追踪",
                pic: "+0.5",
                pe: "+0.5",
                po: "+0.5"
            },
            ],
            scorecritical: [{
                stype: "初始",
                pic: 1.5,
                pe: 0,
                po: -2.5
            },
            {
                stype: "有效质疑",
                pic: "0",
                pe: "+1.5",
                po: "+1"
            },
            {
                stype: "有效答疑",
                pic: "+0.5",
                pe: "0",
                po: "0"
            },
            {
                stype: "无效答疑",
                pic: "-0.5",
                pe: "0",
                po: "0"
            },
            {
                stype: "有效建议",
                pic: "0",
                pe: "+0.5",
                po: "+0.5"
            },
            ],
            tabs_select: "summary",
            task_option: {
                grid: {
                    left: "0",
                    right: "0",
                },
                visualMap: {
                    show: false,
                    min: 0,
                    max: 20,
                    // seriesIndex: [1],
                    // orient: "vertical",
                    inRange: {
                        color: ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"],
                    },
                },
                tooltip: {
                    formatter: function (params) {
                        return "完成任务数量: " + params.value[1];
                    },
                },
                calendar: {
                    range: ["2020-06", "2020-08"],
                    orient: "vertical",
                    left: 50,
                    right: 10,
                    top: 50,
                    bottom: 10,
                    yearLabel: {
                        show: false,
                    },
                    dayLabel: {
                        firstDay: 1, // 从周一开始
                        nameMap: "cn",
                    },
                    monthLabel: {
                        nameMap: "cn",
                    },
                },
                series: {
                    type: "heatmap",
                    coordinateSystem: "calendar",
                    label: {
                        show: true,
                        formatter: function (params) {
                            var d = echarts.number.parseDate(params.value[0]);
                            return d.getDate() + "\n" + params.value[1] + "个";
                        },
                        color: "#000",
                    },
                    data: [],
                },
            },
            // 统计柱形图
            task_summary_option: {
                tooltip: {
                    trigger: "axis",
                    axisPointer: {
                        // 坐标轴指示器，坐标轴触发有效
                        type: "shadow", // 默认为直线，可选为：'line' | 'shadow'
                    },
                },
                color: ["black", "red", "Orange", "green", "#939393"],
                legend: {
                    data: ["逾期完成", "待做逾期", "待做", "正常完成", "作废"],
                    orient: "vertical",
                    left: 800,
                    top: 200,
                },
                grid: {
                    left: 110,
                    top: 30,
                    bottom: 30,
                },
                xAxis: {
                    type: "value",
                },
                yAxis: {
                    type: "category",
                    data: [],
                },
                series: [{
                    name: "逾期完成",
                    type: "bar",
                    stack: "总量",
                    label: {
                        show: true,
                        position: "insideRight",
                        formatter: function (num) {
                            if (num.value == 0) {
                                return "";
                            }
                        },
                    },
                    data: [],
                },
                {
                    name: "待做逾期",
                    type: "bar",
                    stack: "总量",
                    label: {
                        show: true,
                        position: "insideRight",
                        formatter: function (num) {
                            if (num.value == 0) {
                                return "";
                            }
                        },
                    },
                    data: [],
                },
                {
                    name: "待做",
                    type: "bar",
                    stack: "总量",
                    label: {
                        show: true,
                        position: "insideRight",
                        formatter: function (num) {
                            if (num.value == 0) {
                                return "";
                            }
                        },
                    },
                    data: [],
                },
                {
                    name: "正常完成",
                    type: "bar",
                    stack: "总量",
                    label: {
                        show: true,
                        position: "insideRight",
                        formatter: function (num) {
                            if (num.value == 0) {
                                return "";
                            }
                        },
                    },
                    data: [],
                },
                {
                    name: "作废",
                    type: "bar",
                    stack: "总量",
                    label: {
                        show: true,
                        position: "insideRight",
                        formatter: function (num) {
                            if (num.value == 0) {
                                return "";
                            }
                        },
                    },
                    data: [],
                },
                ],
            },
            // pie subject图
            tab_type_pie_option: {
                title: {
                    text: "类型统计",
                    x: "center",
                },
                color: [
                    "#5470c6",
                    "#91cc75",
                    "#fac858",
                    "#ee6666",
                    "#73c0de",
                    "#3ba272",
                    "black",
                    "red",
                    "black",
                ],
                tooltip: {
                    trigger: "item",
                    formatter: "{a} <br/>{b} : {c} ({d}%)",
                },
                series: [{
                    name: "任务情况",
                    type: "pie",
                    radius: ["45%", "60%"],
                    center: ["50%", "60%"],
                    data: [],
                    label: {
                        show: true,
                        position: "outer",
                        alignTo: "labelLine",
                        formatter: "{b}：{c}",
                    },
                },
                {
                    name: "分类",
                    type: "pie",
                    label: {
                        position: "inner",
                    },
                    // color: ["gray"],
                    radius: ["0%", "30%"],
                    center: ["50%", "60%"],
                    data: [],
                },
                ],
            },
            // pie summary图
            tab_summary_pie_option: {
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
            // left input
            select_option: [{
                value: "step",
                label: "步数",
            },
            {
                value: "weight",
                label: "体重",
            },
            ],
            // right input      
            new_edate: "",
            task_title: "",
            task_level1_select: "",
            task_level1_option: [],
            // 二级分类
            task_level2_select: "",
            task_level2_option: [],
            task_sub_all_option: [],

            // 三级分类
            task_level3_select: "",
            task_level3_option: [],
            level2_level3: [],

            // table
            tableData: [],
            tableprocess: [],

            //
            // new_edate: "",
            isstime: false,
            isqueryall: true,
            pickerOptions: {
                shortcuts: [{
                    text: "最近一周",
                    onClick(picker) {
                        const end = new Date();
                        const start = new Date();
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                        picker.$emit("pick", [start, end]);
                    },
                },
                {
                    text: "最近一个月",
                    onClick(picker) {
                        const end = new Date();
                        const start = new Date();
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                        picker.$emit("pick", [start, end]);
                    },
                },
                {
                    text: "最近三个月",
                    onClick(picker) {
                        const end = new Date();
                        const start = new Date();
                        start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                        picker.$emit("pick", [start, end]);
                    },
                },
                ],
            },
            query_duration: null,

            // TODO 这个和下面的那个person在一块肯定有问题啊。。。
            person: "",
            person_option: "",
            copyperson_option: "",

            // dialog person
            dialogpersonVisible: false,
            pppdata: [],
            person: [],
            personrecommend: [],
            personrecommendselected: [],

            // dialog process
            dialogpVisible: false,
            v_task_content: "",
            input_process: "",

            // dialog commit
            dialogsVisible: false,
            s_task_id: "",
            tech_options: [],
            industry_options: [],
            domain_options: [],
            skill_options: [],
            finishtaskform: {
                hours: 1,
                isok: true,
                dirtable: [],
                peoples: [],
                tech: "",
                skill: "",
                industry: "",
                domain: "",
                desc: "",
            },

            // dialog update
            dialoguVisible: false,
            dutitle: "",
            duetime: "",
            dustatus: "",

            // dialog delete
            dialogcVisible: false,

            dialogprocessVisible: false,
            process_content: "",
            process_id: "",

            now_time: new Date().getTime(),
            task_chart: "",
            tasksummary_chart: "",
            tasktype_pie_chart: "",
            tasksummary_pie_chart: "",
            persondata: [],
            title_now: "",
            finishtaskdata: [],

            dir_select: "",
            dir_sub_select: "",
            dir_hours: "",
            dir_select_option: [],
            dir_sub_select_option: [],
            dir_sub_all_option: [],

            person_target: "",
        };
    },
    mounted: function () {
        // console.log(this);
        let now = new Date();
        let year = now.getFullYear(); //得到年份
        let month = now.getMonth() + 1; //得到月份
        let date = now.getDate(); //得到日期
        let day = now.getDay(); //得到周几
        let week;
        let arr_week = new Array(
            "星期日",
            "星期一",
            "星期二",
            "星期三",
            "星期四",
            "星期五",
            "星期六"
        );
        week = arr_week[day];
        let time_ts = "";
        time_ts =
            "当前时间：" + year + "年" + month + "月" + date + "日" + " " + week;
        // ****
        this.title_now = time_ts;
        let that = this;
        // console.log('asdasdasda');
        // console.log(this.tableData);
        this.task_chart = echarts.init(document.getElementById("b_task"), "white", {
            renderer: "canvas",
        });
        this.task_chart.on("click", function (params) {
            // console.log(params["data"][0]);
            that.new_edate = params["data"][0];
            that.task_title = "";
            that.task_level1_select = "";
            that.task_level2_select = "";
            that.task_level3_select = "";
            that.isqueryall = true;
            that.tabs_select = "summary";
            that.querytask("table");
        });
        this.tasksummary_chart = echarts.init(
            document.getElementById("task_summary"),
            "white", {
            renderer: "canvas",
        }
        );
        this.tasksummary_chart.on("click", function (params) {
            // console.log(params["name"]);
            let temp = params["name"];
            // subject: this.task_level1_select,
            // subsub: this.task_level2_select,
            that.task_level1_select = temp.split("-")[0];
            let temp_sub_select = temp.split("-");
            // fix 项目-b山东-数管，原传递b山东，改为传递b山东-数管
            temp_sub_select.shift();
            that.task_level2_select = temp_sub_select.join("-");
            that.task_title = "";
            that.new_edate = "";
            // that.new_edate = params["data"][0];
            that.isqueryall = true;
            that.querytask("graph");
        });
        this.tasktype_pie_chart = echarts.init(
            document.getElementById("task_pie_subject"),
            "white", {
            renderer: "canvas",
        }
        );
        this.tasksummary_pie_chart = echarts.init(
            document.getElementById("task_pie_summary"),
            "white", {
            renderer: "canvas",
        }
        );
        this.freshright();
    },
    methods: {
        freshright: function (event) {
            this.initoption();
            this.setbar();
            this.task_title = "";
            this.task_level1_select = "";
            this.task_level2_select = "";
            this.task_level3_select = "";
            this.new_edate = "";
            this.isstime = false;
            this.query_duration = [];
            this.settasksummary_bar();
            this.isqueryall = false;
            this.querytask("table");
            this.getperson_option();
        },
        resetall: function () {
            this.task_title = "";
            this.tabs_select = "summary";
            this.freshright();
        },
        // 初始化分类的下拉列表
        initoption: function (event) {
            axios.get("/initoption").then((response) => {
                if (response.status == 200) {
                    // console.log(response);
                    this.task_sub_all_option = [];
                    this.task_sub_all_option = response.data.task_sub_all_option;
                    this.task_level1_option = [];
                    this.task_level1_option = response.data.task_level1_option;

                    this.dir_sub_all_option = [];
                    this.dir_sub_all_option = response.data.dir_sub_all_option;
                    this.dir_select_option = [];
                    this.dir_select_option = response.data.dir_select_option;
                    this.level2_level3 = [];
                    this.level2_level3 = response.data.level2_level3;
                    this.updatelevel2option();
                }
            });
        },
        getperson_option: function () {
            axios.get("/getperson_option").then((response) => {
                // console.log(response);
                this.person_option = response.data;
                this.copyperson_option = Object.assign(this.person_option);
            });
        },
        personFilter: function (val) {
            if (val) {
                this.person_option = this.copyperson_option.filter((item) => {
                    // 如果直接包含输入值直接返回true
                    if (item.label) {
                        if (item.label.toUpperCase().indexOf(val.toUpperCase()) != -1) {
                            return true;
                        }
                        // 输入值拼音d
                        return PinyinMatch.match(item.label, val);
                    }
                });
            } else {
                this.person_option = this.copyperson_option;
            }
        },
        deletetaskperson: function (event) {
            axios
                .post("/deletetaskperson", {
                    task_id: this.s_task_id,
                    person_id: event.person_id,
                })
                .then((response) => {
                    this.persondata = response.data.arrays;
                });
        },
        appendtaskperson: function () {
            axios
                .post("/appendtaskperson", {
                    task_id: this.s_task_id,
                    person_id: this.person,
                })
                .then((response) => {
                    this.persondata = response.data.arrays;
                    this.person = [];
                    this.getperson_data(this.s_task_id);
                });
        },
        getperson_data: function (task_id) {
            axios
                .post("/getperson_data", {
                    task_id: task_id,
                })
                .then((response) => {
                    // console.log(this.tableData);
                    this.persondata = response.data.arrays;
                    for (var i in this.tableData) {
                        if (this.tableData[i].task_id == response.data.task_id) {
                            this.tableData[i].num_person = response.data.num_person;
                        }
                    }
                });
        },
        getfinishtask_data: function () {
            axios
                .post("/getfinishtask_data", {
                    task_id: this.s_task_id
                })
                .then((response) => {
                    this.finishtaskdata = response.data;
                });
        },
        tabclick: function (tab, event) {
            // console.log(tab);
            // console.log(this.s_task_id);
            if (tab.name == "finishtask" && this.s_task_id !== "") {
                this.getfinishtask_data();
            }
        },
        setdate: function (event) {
            if (
                this.isstime == false &&
                !(this.query_duration == null || this.query_duration == "")
            ) {
                this.new_edate = "";
            }
            if (
                this.isstime == false &&
                !(this.new_edate == null || this.new_edate == "")
            ) {
                this.query_duration = "";
            }
        },
        // 更新二级下拉列表
        updatelevel2option: function (event) {
            // console.log('update option');
            this.task_level2_select = "";
            if (this.task_level1_select != "" && this.task_sub_all_option != []) {
                this.task_level2_option = [];
                let temp = this.task_sub_all_option[this.task_level1_select];
                // console.log(temp);
                if (temp) {
                    this.task_level2_option = [];
                    for (let i in temp) {
                        // console.log(temp[i]);
                        this.task_level2_option.push({
                            value: temp[i],
                            label: temp[i],
                        });
                    }
                }
            }
        },
        updatelevel3option: function (event) {
            // console.log('update option');
            this.task_level3_select = "";
            if (this.task_level2_select != "" && this.level2_level3 != []) {
                this.task_level3_option = [];
                let temp = this.level2_level3[this.task_level2_select];
                // console.log(temp);
                if (temp) {
                    this.task_level3_option = [];
                    for (let i in temp) {
                        // console.log(temp[i]);
                        this.task_level3_option.push({
                            value: temp[i],
                            label: temp[i],
                        });
                    }
                }
            }
        },
        setbar: function (event) {
            // console.log('setbar');
            axios.get("/gettimedata").then((response) => {
                // console.log(response.data.result);
                if (response.status == 200) {
                    // console.log(response.data.result);
                    // this.task_option.series[0].data = response.data.result_desc;
                    // this.task_option.series[1].data = response.data.result;
                    // this.task_option.calendar.range = response.data.range;
                    this.task_option.series.data = response.data.result;
                    this.task_option.calendar.range = response.data.range;
                    // console.log(this.task_option);
                    this.task_chart.setOption(this.task_option);
                }
            });
        },
        settasksummary_bar: function (event) {
            axios.get("/gettasksummary_bar").then((response) => {
                if (response.status == 200) {
                    // 柱形图
                    // console.log(response.data);
                    this.task_summary_option.yAxis.data = response.data.yAxisdata;
                    this.task_summary_option.series[0].data =
                        response.data.yAxisoverdue_list;
                    this.task_summary_option.series[1].data =
                        response.data.yAxistodooverdue_list;
                    this.task_summary_option.series[2].data =
                        response.data.yAxistodo_list;
                    this.task_summary_option.series[3].data =
                        response.data.yAxisnormal_list;
                    this.task_summary_option.series[4].data =
                        response.data.yAxisabandon_list;
                    this.tasksummary_chart.setOption(this.task_summary_option);
                    // pie type图
                    this.tab_type_pie_option.series[0].data = response.data.pie_type_data;
                    this.tab_type_pie_option.series[1].data =
                        response.data.pie_type_data_c;
                    // console.log(this.tab_type_pie_option);
                    this.tasktype_pie_chart.setOption(this.tab_type_pie_option);

                    // pie summary图
                    this.tab_summary_pie_option.series[0].data =
                        response.data.pie_summary_data;
                    this.tab_summary_pie_option.title.text =
                        "完成率:" +
                        response.data.percent[0] +
                        "%，逾期率:" +
                        response.data.percent[1] +
                        "%";
                    this.tab_summary_pie_option.title.subtext =
                        "总统计数:" + response.data.sum_task + "个";
                    this.tasksummary_pie_chart.setOption(this.tab_summary_pie_option);
                }
            });
        },
        personfilterMethod(query, item) {
            return item.person_py.indexOf(query) > -1;
        },

        // 展示进展面板
        diashowperson: function (event) {
            if (this.task_level1_select != "" && this.task_level2_select != "") {
                this.dialogpersonVisible = true;
                axios
                    .post("/getrecommendperson", {
                        level1: this.task_level1_select,
                        level2: this.task_level2_select,
                    })
                    .then((response) => {
                        // console.log(response.data);
                        this.personrecommend = response.data.personrecommend;
                        this.pppdata = response.data.person_list;
                    });
            } else {
                this.$message({
                    message: "一级分类和二级分类必选",
                    type: "warning",
                });
            }
        },

        addrecommendperson: function (person_id) {
            // console.log(this.person.indexOf(person_id));
            if (this.person.indexOf(person_id) != -1) {
                this.person.splice(this.person.indexOf(person_id), 1);
            } else {
                this.person.push(person_id);
            }
        },

        // 展示进展面板
        diashowprocess: function (event) {
            this.dialogpVisible = true;
            this.v_task_content = event.title;
            this.s_task_id = event.task_id;
        },

        // 调用进展接口
        dialogaddprocess: function (event) {
            // console.log(this.s_task_id);
            axios
                .post("/addprocess", {
                    task_id: this.s_task_id,
                    process_name: this.input_process,
                })
                .then((response) => {
                    this.$message({
                        message: "更新成功",
                        type: "success",
                    });
                    this.input_process = "";
                    this.dialogpVisible = false;
                    this.showprocess();
                    // TODO 是否可以做成局部刷新，只更新该任务的数据即可
                    this.isqueryall = false;
                    this.querytask("table");
                });
        },
        adddir: function () {
            this.finishtaskform.dirtable.push({
                dir: this.dir_select,
                sub_dir: this.dir_sub_select,
                hours: this.dir_hours,
            });
            this.dir_select = "";
            this.dir_sub_select = "";
            this.dir_hours = "";
        },
        getdiroption: function () { },
        updatediroption: function (event) {
            // console.log('update option');
            this.dir_sub_select = "";
            if (this.dir_select != "" && this.dir_sub_all_option != []) {
                this.dir_sub_select_option = [];
                let temp = this.dir_sub_all_option[this.dir_select];
                // console.log(temp);
                if (temp) {
                    this.dir_sub_select_option = [];
                    for (let i in temp) {
                        // console.log(temp[i]);
                        this.dir_sub_select_option.push({
                            value: temp[i],
                            label: temp[i],
                        });
                    }
                }
            }
        },
        // 添加任务
        addtask: function (event) {
            if (this.new_edate != "" && this.task_title) {
                // console.log(this.person);
                axios
                    .post("/addtask", {
                        level1: this.task_level1_select,
                        level2: this.task_level2_select,
                        level3: this.task_level3_select,
                        task_name: this.task_title,
                        edate: this.new_edate,
                        person: this.person,
                    })
                    .then((response) => {
                        // console.log(response);
                        this.task_title = "";
                        this.new_edate = "";
                        this.task_level1_select = "";
                        this.task_level2_select = "";
                        this.task_level3_select = "";
                        this.person = [];
                        this.freshright();
                    });
            }
        },
        finishtask: function (event) {
            // console.log(event.task_id);

            axios
                .post("/getperson_data", {
                    task_id: event.task_id,
                })
                .then((response) => {
                    this.dialogsVisible = true;
                    this.s_task_id = event.task_id;
                    this.finishtaskform.peoples = response.data.arrays;
                });
            // this.v_task_content = event.title;
        },
        // 查询任务
        // TODO 是否查询已完成直接放到this的参数里面，query改成只有一个参数
        querytask: function (mode) {
            // console.log(this.query_duration);
            if (mode == "graph") {
                this.isqueryall = true;
            }
            axios
                .post("/querytask", {
                    query: this.task_title,
                    type: this.task_level1_select,
                    sub_type: this.task_level2_select,
                    ftime: this.new_edate,
                    query_duration: this.query_duration,
                    isstime: this.isstime,
                    isqueryall: this.isqueryall,
                    mode: mode,
                })
                .then((response) => {
                    // console.log(response.data);
                    this.tableData = response.data.arrays;
                });
        },
        querytask_week: function () {
            axios.get("/querytask_week").then((response) => {
                if (response.status == 200) {
                    this.tableData = response.data.arrays;
                    this.tabs_select = "summary";
                }
            });
        },

        committask: function (event) {
            // console.log(this.finishtaskform);
            this.dialogsVisible = false;
            axios
                .post("/finishtask", {
                    task_id: this.s_task_id,
                    finishtaskform: this.finishtaskform,
                })
                .then((response) => {
                    // console.log(response);
                    // this.input_finish = "";
                    this.finishtaskform = this.$options.data().finishtaskform;
                    this.freshright();
                });
        },

        tableRowClassName({
            row,
            rowIndex
        }) {
            row.index = rowIndex;
        },

        handleCurrentChange(row, event, column) {
            // console.log(row.index);
            // console.log(row);
            this.person_target = row.index;
        },
        scoresth(event) {
            // console.log(event);
            let scorelevel = 0;
            let scoremetrix = [
                [7.5, 7.5],
                [6.5, 6.5],
                [5, 5],
                [5, 3.5],
                [3.5, 5],
                [3.5, 3.5],
                [2.5, 2.5],
            ];
            if (event.target.nodeName == "SPAN") {
                // 如果标签名是 i，拿下一个标签
                scorelevel = event.target.innerText; // <span>22</span>
            } else if (event.target.nodeName == "BUTTON") {
                // 如果是 button，拿第二个子标签
                scorelevel = event.target.name; // '2'
            }
            // this.
            this.finishtaskform.peoples[this.person_target]["score_activity"] =
                scoremetrix[scorelevel - 1][0];
            this.finishtaskform.peoples[this.person_target]["score_critical"] =
                scoremetrix[scorelevel - 1][1];
            this.$refs.singleTable.setCurrentRow(this.person_target);
        },
        leaveclick(index, row) {
            // console.log(index, row);
            this.$refs.singleTable.setCurrentRow(row);
        },
        handleEdit(index, row) {
            // console.log(index, row);
        },
        handleDelete(index, row) {
            // console.log(index, row);
        },

        // 展示修改任务面板
        updatetask: function (event) {
            this.dialoguVisible = true;
            // console.log(event);
            this.task_level1_select = event.level1;
            this.task_level2_select = event.level2;
            this.task_level3_select = event.level3;
            this.dutitle = event.task_name;
            this.s_task_id = event.task_id;
            this.duetime = event.tetime;
            this.dustatus = event.status;
        },

        // 调用修改任务接口
        dialogupdate: function (event) {
            // console.log(this.s_task_id);
            axios
                .post("/updatetask", {
                    task_id: this.s_task_id,
                    level1: this.task_level1_select,
                    level2: this.task_level2_select,
                    level3: this.task_level3_select,
                    task_name: this.dutitle,
                    etime: this.duetime,
                    dustatus: this.dustatus,
                })
                .then((response) => {
                    this.dialoguVisible = false;
                    this.task_title = "";
                    this.new_edate = "";
                    this.task_level1_select = "";
                    this.task_level2_select = "";
                    this.task_level3_select = "";
                    this.dustatus = "";
                    this.freshright();
                });
        },
        removetask: function (event) {
            axios.get("/removetask").then((response) => {
                // console.log(response);
            });
        },
        deletetask: function (event) {
            // console.log(event.task_id);
            this.dialogcVisible = true;
            this.s_task_id = event.task_id;
        },

        dirdeletetask: function (index, rows) {
            // console.log(rows);
            rows.splice(index, 1);
            // this.finishtaskform.dirtable
        },

        dialogdelete: function (event) {
            // console.log(this.s_task_id);
            this.dialogcVisible = false;
            axios
                .post("/deletetask", {
                    task_id: this.s_task_id,
                })
                .then((response) => {
                    // console.log(response);
                    this.freshright();
                });
        },
        // TODO 增加逾期的黑色显示
        isoverdate: function ({
            row,
            column,
            rowIndex,
            columnIndex
        }) {
            if (columnIndex == 0) {
                // console.log(row);
                if (row.status == 1) {
                    return "";
                }
                if (row.status == 3) {
                    return "background-color:red;color:white";
                }
                if (row.status == 2) {
                    return "background-color:green;color:white";
                }
                if (row.status == 4) {
                    return "background-color:black;color:white";
                }
                if (row.status == 5) {
                    return "background-color:'#939393'";
                }
            }
        },
        closedialog: function (event) {
            this.task_level1_select = "";
            this.task_level2_select = "";
            this.task_level3_select = "";
            this.process_content = "";
        },
        // TODO 点任务的逻辑重新梳理一下
        showprocess: function (row, column, cell, event) {
            // console.log(column, column.label, row.task_id);
            if (
                column !== undefined &&
                column.label != "进展" &&
                column.label != "人员"
            ) {
                this.tabs_select = "summary";
                this.s_task_id = row.task_id;
                return;
            }
            if (
                (column !== undefined && column.label == "进展") ||
                (column == undefined && this.s_task_id != "" && !this.dialogpVisible)
            ) {
                if (row !== undefined) {
                    this.s_task_id = row.task_id;
                }
                this.tabs_select = "process";
                this.getprocess(this.s_task_id);
                return;
            }
            if (
                (column !== undefined && column.label == "人员") ||
                this.s_task_id != ""
            ) {
                if (row !== undefined) {
                    this.s_task_id = row.task_id;
                }
                this.tabs_select = "person";
                this.getperson_data(this.s_task_id);
                return;
            }
        },
        getprocess: function (task_id) {
            axios
                .post("/getprocess", {
                    task_id: task_id,
                })
                .then((response) => {
                    this.tableprocess = response.data.arrays;
                    for (let i in this.tableprocess) {
                        if (this.tableprocess[i].isfinish == 1) {
                            this.tableprocess[i].isfinish = "完成";
                        } else {
                            this.tableprocess[i].isfinish = "待做";
                        }
                    }
                    for (var i in this.tableData) {
                        // console.log(i);
                        if (this.tableData[i].task_id == response.data.status.k) {
                            this.tableData[i].num_process = response.data.status.num_process;
                        }
                    }
                    this.s_task_id = "";
                });
        },
        deleteprocess: function (event) {
            axios
                .post("/deleteprocess", {
                    process_id: event.process_id,
                })
                .then((response) => {
                    if (response.status == 200) {
                        this.getprocess(event.task_id);
                    }
                });
        },
        resetprocess: function (event) {
            axios
                .post("/resetprocess", {
                    process_id: event.process_id,
                })
                .then((response) => {
                    if (response.status == 200) {
                        this.$message({
                            message: "禁用成功",
                            type: "success",
                        });
                        // console.log(event);
                        this.getprocess(event.task_id);
                    }
                });
        },
        finishprocess: function (event) {
            axios
                .post("/finishprocess", {
                    process_id: event.process_id,
                })
                .then((response) => {
                    if (response.status == 200) {
                        this.$message({
                            message: "启用成功",
                            type: "success",
                        });
                        this.getprocess(event.task_id);
                    }
                });
        },
        showupdateprocess: function (event) {
            this.dialogprocessVisible = true;
            this.process_content = event.process_name;
            // console.log(event);
            this.process_id = event.process_id;
            this.s_task_id = event.task_id;
        },
        updateprocess: function (event) {
            axios
                .post("/updateprocess", {
                    process_id: this.process_id,
                    process_name: this.process_content,
                })
                .then((response) => {
                    if (response.status == 200) {
                        this.$message({
                            message: "启用成功",
                            type: "success",
                        });
                        this.getprocess(this.s_task_id);
                        this.s_task_id = "";
                        this.dialogprocessVisible = false;
                    }
                });
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

.tb-edit .el-input {
    display: none;
}

.tb-edit .current-row .el-input {
    display: block;
}

.tb-edit .current-row .el-input+span {
    display: none;
}
</style>

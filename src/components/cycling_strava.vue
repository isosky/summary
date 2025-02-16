<template>
    <div id="app">
        <el-col :span="24">
            <div id="cycling_strava_summary_charts" style="height: 960px"></div>
        </el-col>
    </div>
</template>

<script>
import axios from "axios";
var echarts = require("echarts");

export default {
    data() {
        return {

            cycling_summary_chart: "",
            cycling_summary_chart_option: {
                angleAxis: {
                    type: 'category',
                    data: [],
                    boundaryGap: false,
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#999',
                            type: 'dashed'
                        }
                    },
                    axisLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    }
                },
                radiusAxis: {
                    axisLine: {
                        show: false
                    },
                    axisLabel: {
                        show: false
                    },
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#999',
                            type: 'dashed'
                        }
                    }
                },
                polar: {
                    center: ['50%', '50%']
                },
                series: [{
                    type: 'bar',
                    data: [],
                    coordinateSystem: 'polar',
                    lineStyle: {
                        width: 2
                    },
                    showSymbol: false,
                    areaStyle: {}
                }]
            },
        }

    },
    mounted: function () {
        this.cycling_summary_chart = echarts.init(
            document.getElementById("cycling_strava_summary_charts"),
            "white",
            {
                renderer: "canvas",
            }
        );
        this.init();

    },
    methods: {
        init: function () {
            this.getcycdata();
        },
        getcycdata: function () {
            axios.get("/get_cycling_strava_chart_data").then((response) => {
                this.cycling_summary_chart_option.angleAxis.data = response.data.dates;
                this.cycling_summary_chart_option.series[0].data = response.data.distances;
                this.cycling_summary_chart.setOption(this.cycling_summary_chart_option);
            });
        },
    },
};
</script>


<style>
.formlabelwidth {
    width: 120px;
}

.el-table {
    overflow: visible !important;
}
</style>

<!--         // 模拟数据，这里我们使用数组来表示每天的步行里程
        var dailyMileage = [];
        for (var day = 1; day <= 365; day++) {
            // 生成随机里程数据
            dailyMileage.push(Math.floor(Math.random() * 100) + 1); // 确保至少有1的值，避免半径为0
        }

        // 指定图表的配置项和数据
        var option = {
            legend: {
                show: false
            },
            polar: {},
            angleAxis: {
                type: 'category',
                data: dailyMileage.map(function (_, idx) {
                    return idx === 0 ? '1日' : ((idx + 1) % 7 === 0 ? ((idx + 1) / 7).toFixed(0) + '月' : '');
                }),
                boundaryGap: false,
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: '#999',
                        type: 'dashed'
                    }
                },
                axisLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLabel: {
                    show: true,
                    formatter: function (value, index) {
                        return value === '' ? '' : value;
                    }
                }
            },
            radiusAxis: {
                min: 0,
                max: 100, // 根据实际数据范围调整
                interval: 10,
                axisLine: {
                    show: false
                },
                axisLabel: {
                    show: false
                },
                axisTick: {
                    show: false
                }
            },
            series: [{
                type: 'bar',
                data: dailyMileage,
                coordinateSystem: 'polar',
                name: '步数',
                showBackground: true,
                backgroundStyle: {
                    color: 'rgba(180, 180, 180, 0.2)'
                },
                roundCap: false,
                barWidth: 1,
            }]
        }; -->
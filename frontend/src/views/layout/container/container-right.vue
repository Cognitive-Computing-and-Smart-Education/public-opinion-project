<template>
    <div class="container-right-box">
        <div class="public-sentiment-box">
            <div class="current-title">
                舆情趋势
            </div>
            <div id="publicSentimentChart"></div>
        </div>
        <div class="information-sources-box">
            <div class="current-title">
                信息来源
            </div>
            <div id="informationSourcesChart"></div>
        </div>
        <div class="media-impression">
            <div class="current-title">
                媒体印象
            </div>
            <div id="mediaImpressionChart"></div>
        </div>
        <div class="hot-word-box">
            <div class="current-title">
                热门词云
            </div>
            <word-cloud-chart v-if="labelList.length" :data="labelList" width="100%" height="calc(100% - 36px)" @callback="wordCallback" />
        </div>
    </div>
</template>

<script>
    import WordCloudChart from "../../../components/word-cloud-chart";

    export default {
        name: "container-right",
        data() {
            return {
                labelList: []
            };
        },
        components: {
            WordCloudChart
        },
        mounted () {
            this.getPublicSentiment();
            this.getInformationSources();
            this.getMediaImpression();
            this.getLabelList();
        },
        methods: {
            wordCallback() {

            },
            getLabelList() {
                this.labelList = [{name: '毛泽东思想', value: 2},
                    {name: '邓小平理论', value: 3},
                    {name: '三会一课', value: 4},
                    {name: '驻村工作队', value: 2},
                    {name: '党务公开', value: 2},
                    {name: '习近平系列讲话', value: 3},
                    {name: '志愿服务', value: 5},
                    {name: '支部规范化', value: 4},
                    {name: '毛泽东思想', value: 2},
                    {name: '邓小平理论', value: 3},
                    {name: '三会一课', value: 4},
                    {name: '驻村工作队', value: 1},
                    {name: '党务公开', value: 3}];
            },
            getMediaImpression() {
                let myChart = this.$echarts.init(document.getElementById('mediaImpressionChart'))
                myChart.setOption({
                    legend: {
                        data: ['网媒', '微信', '微博'],
                        orient: 'vertical',
                        left: 'left',
                        top: 'center',
                        itemWidth: 18,
                        itemHeight: 10,
                        textStyle: {
                            color: '#fff',
                            fontSize: 14
                        },
                    },
                    grid: {
                        right: 10,
                        left: 10,
                        top: 10,
                        bottom: 10,
                        containLabel: true
                    },
                    radar: {
                        // shape: 'circle',
                        center: ['50%', '65%'],
                        radius: '85%',
                        indicator: [
                            { name: '微博平台'},
                            { name: '微信平台'},
                            { name: '微博平台'},
                        ],
                        axisLine: { // (圆内的几条直线)坐标轴轴线相关设置
                            lineStyle: {
                                opacity: 0.3
                            }
                        },
                        splitLine: {
                            lineStyle: {
                                opacity: 0.3
                            }
                        }
                    },
                    series: [{
                        name: '网媒 vs 微信 vs 微博',
                        type: 'radar',
                        symbolSize: 2,
                        data: [
                            {
                                value: [123, 322, 421],
                                name: '网媒',
                                areaStyle: {
                                    opacity: 0.2
                                }
                            },
                            {
                                value: [321, 231, 521],
                                name: '微信',
                                areaStyle: {
                                    opacity: 0.2
                                }
                            },
                            {
                                value: [254, 421, 167],
                                name: '微博',
                                areaStyle: {
                                    opacity: 0.2
                                }
                            }
                        ]
                    }]
                })
            },
            getInformationSources() {
                let myChart = this.$echarts.init(document.getElementById('informationSourcesChart'))
                myChart.setOption({
                    tooltip: {
                        trigger: 'item'
                    },
                    grid: {
                        right: 10,
                        left: 10,
                        top: 10,
                        bottom: 10,
                        containLabel: true
                    },
                    legend: {
                        type: 'scroll',
                        orient: 'vertical',
                        left: 'left',
                        top: 'center',
                        itemWidth: 18,
                        itemHeight: 10,
                        textStyle: {
                            color: '#fff',
                            fontSize: 14
                        },
                        pageIconSize: 12
                    },
                    series: [{
                        name: '信息来源',
                        type: 'pie',
                        radius: '90%',
                        data: [
                            {value: 623, name: '微信公众号'},
                            {value: 735, name: '新闻网站'},
                            {value: 580, name: '其他'},
                            {value: 484, name: '论坛'},
                            {value: 300, name: '微博'},
                            {value: 214, name: '贴吧'},
                            {value: 364, name: '博客'}
                        ],
                        emphasis: {

                        },
                        label: {
                            color: '#fff'
                        }
                    }]
                });
            },
            getPublicSentiment(){
                // 基于准备好的dom，初始化echarts实例
                let myChart = this.$echarts.init(document.getElementById('publicSentimentChart'))
                // 绘制图表
                myChart.setOption({
                    tooltip: {},
                    grid: {
                        right: 10,
                        left: 10,
                        top: 10,
                        bottom: 10,
                        containLabel: true
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: ["00.00","02.00","04.00","06.00","08.00","10.00","12.00"],
                        axisLabel: {
                            color: '#fff'
                        }
                    },
                    yAxis: {
                        type: 'value',
                        splitLine: {
                            lineStyle: {
                                color: '#142852'
                            }
                        },
                        axisLabel: {
                            color: '#fff'
                        }
                    },
                    series: [{
                        name: '趋势',
                        type: 'line',
                        smooth: true,
                        data: [5, 20, 36, 10, 10, 20, 14],
                        areaStyle: {
                            color: '#4a66a3'
                        },
                        lineStyle: {
                            color: '#4d7fbf'
                        }
                    }]
                });
            }
        }
    }
</script>

<style scoped>
    .container-right-box>div{
        height: calc((100% - 45px) / 4);
    }
    .current-title:before{
        content: '';
        display: inline-block;
        width: 8px;
        height: 18px;
        background-color: cornflowerblue;
        margin-right: 15px;
    }
    .current-title{
        height: 26px;
        display: flex;
        color: #fff;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        margin-bottom: 10px;
    }
    #publicSentimentChart,
    #informationSourcesChart,
    #mediaImpressionChart{
        width: 100%;
        height: calc(100% - 36px);
    }
</style>

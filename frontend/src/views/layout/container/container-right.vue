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
                媒体影响力
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
    import { getAreaNewsTre, getAreaNewsSource, getAreaSourceInfluence, getAreaHotWord } from '@/api/Home'
    import { mapGetters, mapMutations } from "vuex";

    export default {
        name: "container-right",
        data() {
            return {
                labelList: []
            };
        },
        computed: {
            ...mapGetters(["homeAreaName"]),
        },
        watch: {
            homeAreaName() {
                this.init(this.homeAreaName)
            }
        },
        components: {
            WordCloudChart
        },
        mounted () {
            this.init();
        },
        methods: {
            init(Area_name) {
                this.getPublicSentiment(Area_name);
                this.getInformationSources(Area_name);
                this.getMediaImpression(Area_name);
                this.getLabelList(Area_name);
            },
            wordCallback() {

            },
            getLabelList(Area_name) {
                getAreaHotWord({ Area_name: Area_name || '' }).then(res => {
                    // console.log(res)
                    for(let i in res.data.date) {
                        res.data.date[i].value = res.data.date[i].value * 10
                    }
                    this.labelList = res.data.date;

                })
                /*this.labelList = [{name: '毛泽东思想', value: 2},
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
                    {name: '党务公开', value: 3}];*/
            },
            getMediaImpression(Area_name) {
                let _that = this
                getAreaSourceInfluence({ Area_name: Area_name || '' }).then(res => {
                    let data = res.data.date
                    let indicatorList = []
                    let val = []
                    for(let i in data) {
                        let obj = {name: data[i].name, max: 8}
                        val.push(data[i].value.toFixed(2))
                        indicatorList.push(obj)
                    }
                    let myChart = this.$echarts.init(document.getElementById('mediaImpressionChart'))
                    myChart.setOption({
                        /*legend: {
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
                        },*/
                        tooltip: {
                            trigger: 'axis',
                            transitionDuration: 0
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
                            indicator: indicatorList,
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
                            tooltip: {
                                trigger: 'item'
                            },
                            symbolSize: 2,
                            data: [
                                {
                                    value: val,
                                    name: '网媒',
                                    areaStyle: {
                                        opacity: 0.2
                                    }
                                },
                                /*{
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
                                }*/
                            ]
                        }]
                    })
                })

            },
            getInformationSources(Area_name) {
                getAreaNewsSource({ Area_name: Area_name || '' }).then(res => {
                    let myChart = this.$echarts.init(document.getElementById('informationSourcesChart'))
                    myChart.setOption({
                        tooltip: {
                            trigger: 'item',
                            transitionDuration: 0
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
                            right: 40,
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
                            radius: '75%',
                            data: res.data.date,
                            label: {
                                color: '#fff'
                            }
                        }]
                    });
                })

            },
            getPublicSentiment(Area_name){
                // 基于准备好的dom，初始化echarts实例
                getAreaNewsTre({ Area_name: Area_name || '' }).then(res => {
                    let time = []
                    let data = []
                    let list = res.data.Tre_list
                    let listData = list.reverse()
                    for(let i in listData) {
                        let obj = listData[i]
                        time.push(obj.time)
                        data.push(obj.news_num)
                    }
                    let myChart = this.$echarts.init(document.getElementById('publicSentimentChart'))
                    // 绘制图表
                    myChart.setOption({
                        tooltip: {},
                        grid: {
                            right: 20,
                            left: 10,
                            top: 10,
                            bottom: 10,
                            containLabel: true
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            data: time,
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
                            data: data,
                            areaStyle: {
                                color: '#4a66a3'
                            },
                            lineStyle: {
                                color: '#4d7fbf'
                            }
                        }]
                    });
                })

            }
        }
    }
</script>

<style scoped>
    .container-right-box>div{
        height: calc((100% - 45px) / 4);
        border: 1px solid #1e2252;
        margin-bottom: 15px;
        box-sizing: border-box;
        padding: 5px 10px;
    }
    .container-right-box>div:last-child{
        margin-bottom: 0;
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

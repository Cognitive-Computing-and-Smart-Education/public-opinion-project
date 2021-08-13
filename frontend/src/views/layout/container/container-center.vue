<template>
    <div>
        <div class="statistics-box">
            <div>
                <div class="current-title">
                    累计监控总量
<!--                    <div class="current-title-time">-->
<!--                        {{ currentTime }}-->
<!--                    </div>-->
                </div>
                <div class="statistics-text statistics-cumulative">{{ cumulative }}</div>
            </div>
            <div>
                <div class="current-title">
                    今日监控总量
<!--                    <div class="current-title-time">-->
<!--                        {{ currentTime }}-->
<!--                    </div>-->
                </div>
                <div class="statistics-text statistics-todayMonitor">{{ todayMonitor }}</div>
            </div>
            <div>
                <div class="current-title">
                    敏感信息总量
                </div>
                <div class="statistics-text statistics-sensitive">{{ sensitive }}</div>
            </div>
            <div>
                <div class="current-title">
                    信息源总量
                </div>
                <div class="statistics-text statistics-informationSource">{{ informationSource }}</div>
            </div>
        </div>
        <div class="map-box">
            <div id="container" style="width:100%; height:100%"></div>
            <div class="map-box-switch">
                <el-switch
                        @change="mapSwitchChange"
                        v-model="mapSwitch"
                        :disabled="mapSwitch"
                        active-text="全国数据">
                </el-switch>
            </div>
<!--            <div style="position: absolute;z-index: 999;right: 30px;bottom: 30px;color: #fff;cursor: pointer" @click="pushBtn">跳转</div>-->
        </div>
        <div class="industry-voice-box">
            <div class="industry-voice-title">细分行业声量</div>
            <div id="industryVoiceChart"></div>
        </div>
    </div>
</template>

<script>
    import '../../../../node_modules/echarts/map/js/china.js'
    import { getNewsNum, getNewsMap, getAreaNewsIndustry } from '@/api/Home'
    import { mapGetters, mapMutations } from "vuex";

    export default {
        name: "container-center",
        data() {
            return {
                currentTime: '',
                cumulative: '',
                todayMonitor: '',
                sensitive: '',
                informationSource: '',
                mapData: [],
                mapSwitch: true
            };
        },
        computed: {
            ...mapGetters(["homeAreaName"]),
        },
        watch: {
            homeAreaName() {
                // this.getNowTime();
                this.getMonitorData(this.homeAreaName);
                this.getIndustryVoice(this.homeAreaName);
            }
        },
        mounted () {
            this.init();
            // this.getNowTime();
            this.getMonitorData();
            this.getIndustryVoice();
        },
        methods: {
            ...mapMutations(["changeHomeAreaName"]),
            mapSwitchChange() {
                let _that = this
                if(_that.mapSwitch) {
                    _that.changeHomeAreaName('全国');
                }
            },
            pushBtn() {
                this.$router.push({
                    path: '/article',
                })
            },
            // async
            async init () {
                let _that = this
                let { data } = await getNewsMap();
                this.mapData = data.date;
                let myChart = this.$echarts.init(document.getElementById('container')); //这里是为了获得容器所在位置
                // window.onresize = myChart.resize;
                myChart.setOption({ // 进行相关配置
                    backgroundColor: "#0e0f3c",
                    tooltip: {}, // 鼠标移到图里面的浮动提示框
                    dataRange: {
                        show: false,
                        min: 0,
                        max: 100,
                        text: ['High', 'Low'],
                        realtime: true,
                        calculable: true,
                        color: ['orangered', 'yellow', 'lightskyblue']
                    },
                    geo: { // 这个是重点配置区
                        map: 'china', // 表示中国地图
                        roam: true,
                        label: {
                            normal: {
                                show: true, // 是否显示对应地名
                                textStyle: {
                                    color: 'rgba(0,0,0,0.4)'
                                }
                            }
                        },
                        itemStyle: {
                            normal: {
                                borderColor: 'rgba(0, 0, 0, 0.2)'
                            },
                            emphasis: {
                                areaColor: null,
                                shadowOffsetX: 0,
                                shadowOffsetY: 0,
                                shadowBlur: 20,
                                borderWidth: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    },
                    series: [{
                        type: 'scatter',
                        coordinateSystem: 'geo' // 对应上方配置
                    },
                        {
                            name: '舆情数量', // 浮动框的标题
                            type: 'map',
                            geoIndex: 0,
                            data: this.mapData
                        }
                    ]
                })

                myChart.on('click', function (param) {
                    _that.changeHomeAreaName(param.data.name);
                    _that.mapSwitch = false
                });
            },
            getIndustryVoice(Area_name) {
                getAreaNewsIndustry({ Area_name: Area_name || '' }).then(res => {
                    let xAxisData = []
                    let data = []
                    for(let i in res.data.date) {
                        if(i < 7) {
                            let obj = res.data.date[i]
                            xAxisData.push(obj.name)
                            data.push(obj.value)
                        }
                    }
                    console.log(xAxisData)
                    let myChart = this.$echarts.init(document.getElementById('industryVoiceChart'))
                    myChart.setOption({
                        grid: {
                            right: 15,
                            left: 15,
                            top: 15,
                            bottom: 15,
                            containLabel: true
                        },
                        xAxis: {
                            type: 'category',
                            data: xAxisData,
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
                            data: data,
                            type: 'bar',
                            barWidth: 30
                        }]
                    })
                })

            },
            getMonitorData(Area_name) {
                getNewsNum({ Area_name: Area_name || '' }).then(res => {
                    this.cumulative = res.data.Total_num
                    this.todayMonitor = res.data.Today_num
                    this.sensitive = res.data.Sensitive_num
                    this.informationSource = res.data.Source_num
                })

            },
            // timestampToTime(data) {
            //     let dt = new Date()
            //     let yyyy = dt.getFullYear()
            //     let MM = (dt.getMonth() + 1).toString().padStart(2, '0')
            //     let dd = dt.getDate().toString().padStart(2, '0')
            //     let h = dt.getHours().toString().padStart(2, '0')
            //     let m = dt.getMinutes().toString().padStart(2, '0')
            //     let s = dt.getSeconds().toString().padStart(2, '0')
            //     return MM + '月' + dd + '日 ' + h + ':' + m
            // },
            // getNowTime() {
            //     let aData = new Date();
            //
            //     this.currentTime = this.timestampToTime(aData)
            // },

        }
    }
</script>

<style scoped>
    /deep/ .el-switch__label{
        color: #fff;
    }
    /deep/ .el-switch__label.is-active{
        color: #409EFF !important;
    }
    /deep/ .el-switch.is-disabled{
        opacity: 1;
    }
    .current-title{
        height: 26px;
        display: flex;
        color: #fff;
        align-items: center;
        justify-content: center;
        width: 100%;
        font-size: 14px;
        line-height: 26px;
    }
    .statistics-box{
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        height: 100px;
    }
    .statistics-box>div{
        width: 25%;
        height: 100%;
        box-sizing: border-box;
    }
    .current-title-time{
        margin-left: 15px;
        font-size: 12px;
        color: #fff;
        height: 100%;
        display: inline-block;
        line-height: 26px;
    }
    .statistics-text{
        font-size: 38px;
        font-weight: bolder;
        height: calc(100% - 36px);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .statistics-cumulative{
        color: #6dd4f2;
        text-shadow: 0 0 10px #6dd4f2;
    }
    .statistics-todayMonitor{
        color: #6dd4f2;
        text-shadow: 0 0 10px #6dd4f2;
    }
    .statistics-sensitive{
        color: #4ef740;
        text-shadow: 0 0 10px #4ef740;
    }
    .statistics-informationSource{
        color: #f47b10;
        text-shadow: 0 0 10px #f47b10;
    }
    .map-box{
        padding: 5px;
        border: 1px solid #1e2252;
        margin: 15px 0;
        height: calc(100% - 390px);
        position: relative;
    }
    .map-box-switch{
        position: absolute;
        z-index: 1000;
        left: 20px;
        bottom: 20px;
    }
    .industry-voice-box{
        width: 100%;
        height: 248px;
        background: url("../../../assets/img/current-border.png") center center no-repeat;
        background-size: 100% 100%;
    }
    .industry-voice-title{
        font-size: 15px;
        color: #fff;
        width: 100%;
        height: 26px;
        text-align: center;
    }
    #industryVoiceChart{
        width: 100%;
        height: calc(100% - 26px);
    }
</style>

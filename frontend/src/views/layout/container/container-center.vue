<template>
    <div>
        <div class="statistics-box">
            <div>
                <div class="current-title">
                    累计监控总量
                    <div class="current-title-time">
                        {{ currentTime }}
                    </div>
                </div>
                <div class="statistics-text statistics-cumulative">{{ cumulative }}</div>
            </div>
            <div>
                <div class="current-title">
                    今日监控总量
                    <div class="current-title-time">
                        {{ currentTime }}
                    </div>
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
        </div>
        <div class="industry-voice-box">
            <div class="industry-voice-title">细分行业声量</div>
            <div id="industryVoiceChart"></div>
        </div>
    </div>
</template>

<script>

    export default {
        name: "container-center",
        data() {
            return {
                currentTime: '',
                cumulative: '',
                todayMonitor: '',
                sensitive: '',
                informationSource: ''
            };
        },
        mounted () {
            this.init();
            this.getNowTime();
            this.getMonitorData();
            this.getIndustryVoice();
        },
        methods: {
            getIndustryVoice() {
                let myChart = this.$echarts.init(document.getElementById('industryVoiceChart'))
                myChart.setOption({
                    grid: {
                        right: 15,
                        left: 15,
                        top: 15,
                        bottom: 15,
                        containLabel: true
                    },
                    rader: {

                    },
                    xAxis: {
                        type: 'category',
                        data: ['婴幼儿教育', 'k12教育', '职业教育', '学科竞赛', '特殊教育', '体育经济', '国际教育','智慧教育']
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [{
                        data: [120, 200, 150, 80, 70, 110, 130,142],
                        type: 'bar',
                        barWidth: 30
                    }]
                })
            },
            getMonitorData() {
                this.cumulative = '2345'
                this.todayMonitor = '1234'
                this.sensitive = '181'
                this.informationSource = '131'
            },
            timestampToTime(data) {
                let dt = new Date()
                let yyyy = dt.getFullYear()
                let MM = (dt.getMonth() + 1).toString().padStart(2, '0')
                let dd = dt.getDate().toString().padStart(2, '0')
                let h = dt.getHours().toString().padStart(2, '0')
                let m = dt.getMinutes().toString().padStart(2, '0')
                let s = dt.getSeconds().toString().padStart(2, '0')
                return MM + '月' + dd + '日 ' + h + ':' + m
            },
            getNowTime() {
                let aData = new Date();

                this.currentTime = this.timestampToTime(aData)
            },
            init () {
                let amap = new AMap.Map('container', {
                    center: [116.05438, 38.98065],
                    resizeEnable: true,
                    zoom: 4,
                    mapStyle:'amap://styles/b9ab3c993c8dafed91c7ae9e82564c0c'
                })
            }
        }
    }
</script>

<style scoped>
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
    }
    .industry-voice-box{
        width: 100%;
        height: 260px;
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

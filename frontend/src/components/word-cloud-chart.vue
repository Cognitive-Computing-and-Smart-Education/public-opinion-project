<style scoped>
.chartsClass {
  padding-left: 1.2rem;
}
</style>
<template>
    <div :id="id" :class="className" :style="{ height:height,width:width }" />
</template>

<script>
import * as echarts from "echarts";
import "echarts-wordcloud/dist/echarts-wordcloud";
import "echarts-wordcloud/dist/echarts-wordcloud.min";
export default {
    props: {
        objecthis: {},
        className: {
            type: String,
            default: "chart"
        },
        id: {
            type: String,
            default: "chart"
        },
        width: {
            type: String,
            default: "100%"
        },
        height: {
            type: String,
            default: "400px"
        },
        data: {
            type: Array,
            default: () => []
        },
        title: {
            type: String,
            default: ""
        }
    },
    data() {
        return {
            region_code: "001.001.053",
            myChart: null,
            date_year: "2020",
            is_leader: "2",
            chart: null,
            esData: [],
            colors: ["#76FBFF", "#909DBE", "#FBFBFC"]
        };
    },
    mounted() {
        this.getSKZT_ALL();
    },
    beforeDestroy() {
        if(!this.chart) {
            return;
        }
        this.chart.dispose();
        this.chart = null;
    },
    methods: {
        getSKZT_ALL() {
            this.esData = this.data;
            console.log("this.esData", this.esData);
            this.initChart();
        },
        initChart() {
            let _this = this;
            this.chart = echarts.init(document.getElementById(this.id));
            const option = {
                title: {
                    text: this.title,
                    x: "center"
                },
                backgroundColor: "transparent",
                // tooltip: {
                //   pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>"
                // },
                series: [{
                    type: "wordCloud",

                    // 用来调整词之间的距离
                    gridSize: 30,
                    // 用来调整字的大小范围
                    // Text size range which the value in data will be mapped to.
                    // Default to have minimum 12px and maximum 60px size.
                    sizeRange: [12, 30],
                    // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
                    // 用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
                    // rotationRange: [-45, 0, 45, 90],
                    // rotationRange: [ 0,90],
                    rotationRange: [0, 0],
                    // 随机生成字体颜色
                    // maskImage: maskImage,
                    textStyle: {
                        normal: {
                            color: function() {
                                return _this.colors[Math.round(Math.random() * 2)];
                            }
                        }
                    },
                    // 位置相关设置
                    // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
                    // Default to be put in the center and has 75% x 80% size.
                    left: "center",
                    top: "center",
                    right: null,
                    bottom: null,
                    width: "200%",
                    height: "200%",
                    // 数据
                    data: this.esData
                }]
            };
            this.chart.setOption(option);
            this.chart.on("click", (params) => {
                // this.objecthis.isShow = true;
                // this.objecthis.dialogTitle = "";
                // this.objecthis.dialogQuery = {
                //     headType: 3,
                //     zhutName: params.data.name
                // };
                // this.objecthis.dialogComponentName = () => import("./ldgbsjt-detail-sjtjl-list");
            });
        }
    }
};
</script>

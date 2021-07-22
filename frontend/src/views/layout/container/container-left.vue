<template>
    <div>
        <div class="event-retrieval">
            <div class="current-title">
                事件检索
            </div>
            <el-form :inline="true" :model="retrievalForm" class="demo-form-inline">
                <el-form-item>
                    <el-input v-model="retrievalForm.search" placeholder="请输入搜索内容" size="small"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="onSubmit" style="background-color: #2f4e80;border-color: #2f4e80" size="mini">查询</el-button>
                </el-form-item>
            </el-form>
            <div class="event-retrieval-listBox">
                <div v-if="retrievalList.length == 0" class="event-retrieval-nodata">
                    暂无数据
                </div>
                <ul v-else class="event-retrieval-list">
                    <li v-for="(item,index) in retrievalList" :key="`retrievalList-${index}`">
                        <span>{{ index + 1 }}</span>
                        <p>{{ item.title }}</p>
                    </li>
                </ul>
            </div>
        </div>
        <div class="ranking-list">
            <div class="current-title">
                <div class="flex-box">
                    <el-button type="primary" plain size="small">热点信息排行榜</el-button>
                    <el-button type="primary" plain size="small">信息类型筛选</el-button>
                </div>
            </div>
            <div class="message-box">
                <ul class="scroll-content" :style="{ top }" @mouseenter="Stop()" @mouseleave="Up()">
                    <li v-for="item in prizeList" :key="item.id">
                        <div class="heat-degree">
                            <div class="heat-degree-val">{{ item.heatDegree }}</div>
                            <div class="heat-degree-txt">当前热度</div>
                        </div>
                        <div class="heat-degree-textBox">
                            <div class="heat-degree-title">{{ item.title }}</div>
                            <div class="heat-degree-time">{{ item.time }}</div>
                            <div class="heat-degree-content">{{ item.content }}</div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "container-left",
        data() {
            return {
                retrievalForm: {
                    search: ''
                },
                retrievalList: [
                    {
                        code: '12',
                        title: '1222222222222222'
                    },{
                        code: '22',
                        title: '1222222222222222'
                    },{
                        code: '33',
                        title: '1222222222222222'
                    },{
                        code: '44',
                        title: '1222222222222222'
                    }
                ],
                prizeList: [
                    {
                        id: '1',
                        heatDegree: '1675',
                        title: '11111111111111111111111',
                        time: '47分钟前',
                        content: '新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容'
                    },{
                        id: '2',
                        heatDegree: '1675',
                        title: '11111111111111111111111',
                        time: '47分钟前',
                        content: '新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容'
                    },{
                        id: '3',
                        heatDegree: '1675',
                        title: '11111111111111111111111',
                        time: '47分钟前',
                        content: '新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容'
                    },{
                        id: '4',
                        heatDegree: '1675',
                        title: '11111111111111111111111',
                        time: '47分钟前',
                        content: '新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容'
                    },{
                        id: '5',
                        heatDegree: '1675',
                        title: '11111111111111111111111',
                        time: '47分钟前',
                        content: '新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容'
                    },{
                        id: '6',
                        heatDegree: '1675',
                        title: '11111111111111111111111',
                        time: '47分钟前',
                        content: '新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容'
                    },{
                        id: '7',
                        heatDegree: '1675',
                        title: '11111111111111111111111',
                        time: '47分钟前',
                        content: '新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容'
                    },{
                        id: '8',
                        heatDegree: '1675',
                        title: '11111111111111111111111',
                        time: '47分钟前',
                        content: '新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容'
                    },{
                        id: '9',
                        heatDegree: '111',
                        title: '11111111111111111111111',
                        time: '47分钟前',
                        content: '新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容新闻内容'
                    }
                ],
                activeIndex: 0,
                intnum: undefined
            };
        },
        computed: {
            top() {
                return -this.activeIndex * 119 + 'px';
            }
        },
        mounted() {
            this.ScrollUp();
        },
        methods: {
            onSubmit() {

            },
            ScrollUp() {
                // eslint-disable-next-line no-unused-vars
                this.intnum = setInterval(_ => {
                    if (this.activeIndex < this.prizeList.length - 3) {
                        this.activeIndex += 1;
                    } else {
                        this.activeIndex = 0;
                    }
                }, 2000);
            },

            Stop() {
                clearInterval(this.intnum);
            },
            Up() {
                this.ScrollUp();
            }
        }
    }
</script>

<style scoped>
    .event-retrieval-listBox{
        width: 100%;
        margin-top: 10px;
        height: calc(100% - 108px);
    }
    .event-retrieval-list{
        width: 100%;
        height: 100%;
        overflow-y: auto;
    }
    .event-retrieval-list li{
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding-bottom: 5px;
        padding-top: 5px;
        border-bottom: 1px solid #142852;
    }
    .event-retrieval-list li:last-child{
        border-bottom: none;
    }
    .event-retrieval-list li span{
        font-size: 12px;
        color: #fff;
        height: 100%;
        display: inline-block;
        margin-right: 10px;
    }
    .event-retrieval-list li p{
        height: 100%;
        font-size: 13px;
        color: #fff;
        word-break: break-all;
        text-overflow: ellipsis;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
    }
    /deep/ .el-input__inner{
        background-color: rgba(0,0,0,0);
        border-color: #2f4e80;
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
    .event-retrieval{
        height: 340px;
        box-sizing: border-box;
        border: 1px solid #1e2252;
        padding: 10px;
    }
    .flex-box{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .ranking-list{
        width: 100%;
        box-sizing: border-box;
        margin-top: 20px;
        height: calc(100% - 360px);
        border: 1px solid #1e2252;
        padding: 10px;
    }
    .message-box{
        height: calc(100% - 36px);
        overflow: hidden;
    }
    .scroll-content {
        position: relative;
        transition: top 0.5s;
    }
    .scroll-content li{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        height: 102px;
        padding-bottom: 8px;
        border-bottom: 1px solid #142852;
        padding-top: 8px;
    }
    .scroll-content li:last-child{
        border-bottom: none;
    }
    .heat-degree{
        display: flex;
        align-items: center;
        flex-flow: wrap;
        width: 60px;
        margin-right: 10px;
    }
    .heat-degree-textBox{
        width: calc(100% - 70px);
    }
    .heat-degree-val{
        font-size: 18px;
        font-weight: bolder;
        color: #fff;
        width: 100%;
        text-align: center;
        margin-bottom: 10px;
        height: 30px;
        line-height: 30px;
        display: inline-block;
    }
    .heat-degree-txt{
        font-size: 12px;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 20px;
        background-color: orange;
    }
    .heat-degree-title{
        font-size: 14px;
        color: #fff;
        word-break: break-all;
        text-overflow: ellipsis;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
        width: 100%;
        height: 26px;
        line-height: 26px;
    }
    .heat-degree-title:before{
        content: '';
        display: inline-block;
        margin-right: 10px;
        width: 6px;
        height: 12px;
        background-color: cornflowerblue;
    }
    .heat-degree-time{
        font-size: 12px;
        color: #4a66a3;
        text-align: left;
        height: 26px;
        line-height: 26px;
    }
    .heat-degree-content{
        width: 100%;
        font-size: 14px;
        color: #6092e1;
        word-break: break-all;
        text-overflow: ellipsis;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        height: 50px;
        line-height: 26px;
    }
</style>

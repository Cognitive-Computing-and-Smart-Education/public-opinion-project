<template>
    <div>
        <div class="event-retrieval">
            <div class="current-title">
                事件检索
            </div>
            <el-form :inline="true" :model="retrievalForm" class="demo-form-inline">
                <el-form-item>
                    <el-input style="width: 400px" v-model="retrievalForm.search" placeholder="请输入搜索内容" size="small"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="onSubmit" style="background-color: #2f4e80;border-color: #2f4e80" size="mini">查询</el-button>
                </el-form-item>
            </el-form>
            <div class="event-retrieval-listBox">
                <div v-if="retrievalList.length == 0" class="event-retrieval-nodata">
                    暂无数据
                </div>
                <div style="height: 100%;width: 100%;overflow-y: auto" v-else class="infinite-list-wrapper">
                    <ul class="event-retrieval-list" v-infinite-scroll="load" @infinite-scroll-disabled="disabled" :infinite-scroll-delay="700">
                        <li v-for="(item,index) in retrievalList" :key="`retrievalList-${index}`" @click="goDetail(item)">
                            <span>{{ index + 1 }}</span>
                            <p class="audiot_style">{{ item.title }}</p>
                        </li>
                    </ul>
                    <p v-if="loading" style="color: #fff;text-align: center;">加载中...</p>
                    <p v-if="noMore" style="color: #fff;text-align: center">没有更多了</p>
                </div>
            </div>
        </div>
        <div class="ranking-list">
            <div class="current-title">
                <div class="flex-box">
                    <el-button type="primary" plain size="small" @click="geiMessage">热点信息排行榜</el-button>
                    <el-button type="primary" plain size="small">信息类型筛选</el-button>
                </div>
            </div>
            <div class="message-box">
                <ul class="scroll-content" :style="{ top }" @mouseenter="Stop()" @mouseleave="Up()">
                    <li v-for="item in prizeList" :key="`prizeList-${item.id}`">
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
    import { getNews, getNewsInfluence } from '@/api/Home'
    import { mapGetters, mapMutations } from "vuex";

    export default {
        name: "container-left",
        data() {
            return {
                retrievalForm: {
                    search: ''
                },
                retrievalList: [],
                prizeList: [],
                activeIndex: 0,
                intnum: undefined,
                loading: false,
                pageSize: 0,
                pageNum: 10,
                finished: false,
                listData: []
            };
        },
        computed: {
            ...mapGetters(["homeAreaName"]),
            top() {
                return -this.activeIndex * 131 + 'px';
            },
            noMore () {
                return this.finished
            },
            disabled () {
                return this.loading || this.noMore
            }
        },
        watch: {
            homeAreaName() {
                // console.log(this.homeAreaName)
                this.init(this.homeAreaName);
            }
        },
        mounted() {
            this.init()
        },
        methods: {
            // 排序
            sortByKey(array,key){
                return array.sort(function(a,b){
                    var x = a[key];
                    var y = b[key];
                    return ((x < y) ? -1 : (x > y) ? 1 : 0);
                })
            },
            goDetail(item) {
                window.open(item.url,'_blank')
            },
            load () {
                this.loading = true
                setTimeout(() => {
                    this.ortherSearch()
                }, 2000)
            },
            ortherSearch() {
                /*getNews({ keyword: this.retrievalForm.search || '教育', pageSize: this.pageSize + 1, pageNum: this.pageNum }).then(res => {
                    if(res.code == 200) {
                        let audiot_style = document.getElementsByClassName("audiot_style");
                        let translateText = res.data.News_list;
                        let inputValue = this.retrievalForm.search;
                        if(res.data.News_list.length > 0 || this.retrievalForm.search !== '') {
                            for (let i = 0; i < translateText.length; i++) {
                                if (translateText[i].title.indexOf(inputValue) >= 0) {
                                    var values = translateText[i].title.split(inputValue);
                                    audiot_style[i].innerHTML = values.join(
                                        '<span style="color:red;">' + inputValue + "</span>"
                                    );
                                }
                            }
                        }
                        this.retrievalList = this.retrievalList.concat(translateText)
                    }
                })*/
                let list = []
                for(let i=this.pageSize * 10; i< this.listData.length; i++) {
                    if(i > (this.pageSize + 1) * 10 - 1){
                        break;
                    }
                    this.retrievalList.push(this.listData[i])
                }
                // this.retrievalList = this.retrievalList.concat(list)
                this.pageSize = this.pageSize + 1
                this.loading = false
                if(this.listData.length <= this.pageSize * 10) {
                    this.finished = true
                }
                this.$nextTick(function () {
                    this.redList(this.retrievalList)
                })
            },
            init(Area_name) {
                this.Stop()
                this.activeIndex = 0
                this.intnum = undefined
                this.prizeList = []
                this.geiMessage(Area_name)
                this.onSubmitActive('教育')
                this.$nextTick(function () {
                    this.ScrollUp();
                })
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
            geiMessage(Area_name) {
                getNewsInfluence({ Area_name: Area_name || '' }).then(res => {
                    console.log('getNewsInfluence',res)
                    for(let i in res.data.date) {
                        if(i > 20) {
                            break;
                        }
                        let obj = res.data.date[i]
                        let objData = {
                            id: obj.id,
                            heatDegree: Math.floor(obj.value.yx) * 100,
                            title: obj.value.title,
                            time: obj.value.time,
                            content: obj.value.text
                        }
                        this.prizeList.push(objData)
                    }
                })
            },
            redList(listData) {
                let audiot_style = document.getElementsByClassName("audiot_style");
                let inputValue = this.retrievalForm.search;
                if(listData.length > 0) {
                    for (let i = (this.pageSize - 1) * 10; i < listData.length; i++) {
                        if (listData[i].title.indexOf(inputValue) >= 0) {
                            var values = listData[i].title.split(inputValue);
                            audiot_style[i].innerHTML = values.join(
                                '<span style="color:red;">' + inputValue + "</span>"
                            );
                        }
                    }
                }
            },
            onSubmit() {
                this.pageSize = 0;
                this.pageNum = 10;
                this.finished = false;
                getNews({ keyword: this.retrievalForm.search }).then(res => {
                    let translateText = res.data.News_list;
                    // listData

                    if(translateText.length > 10) {
                        this.listData = translateText
                        let list = []
                        for(let i=0; i < this.listData.length; i++) {
                            if(i > 9){
                                break;
                            }
                            list.push(this.listData[i])
                        }
                        this.retrievalList = list
                        this.pageSize = this.pageSize + 1
                        this.redList(this.retrievalList)
                        if(this.listData.length <= this.pageSize * 10) {
                            this.finished = true
                        }
                    }else {
                        this.retrievalList = res.data.News_list
                        this.redList(this.retrievalList)
                        this.finished = true
                    }
                })
            },
            onSubmitActive(data) {
                this.retrievalList = []
                getNews({ keyword: data }).then(res => {
                    let translateText = res.data.News_list;
                    if(translateText.length > 10) {
                        this.listData = translateText
                        let list = []
                        for(let i=0; i < this.listData.length; i++) {
                            if(i > 9){
                                break;
                            }
                            list.push(this.listData[i])
                        }
                        this.retrievalList = list
                        this.pageSize = this.pageSize + 1
                        if(this.listData.length <= this.pageSize * 10) {
                            this.finished = true
                        }
                    }else {
                        this.retrievalList = res.data.News_list
                        this.finished = true
                    }
                })
            },
            ScrollUp() {
                // eslint-disable-next-line no-unused-vars
                this.intnum = setInterval(_ => {
                    if (this.activeIndex <= this.prizeList.length - 3) {
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
    /deep/ .el-scrollbar__wrap{
        overflow-x: hidden;
        width: 100%;
    }
    .event-retrieval-nodata{
        font-size: 24px;
        color: #909DBE;
        width: 100%;
        font-weight: bolder;
        height: 70%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .event-retrieval-listBox{
        width: 100%;
        margin-top: 10px;
        height: calc(100% - 108px);
    }
    .event-retrieval-list{

    }
    .event-retrieval-list li{
        height: 18px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        border-bottom: 1px solid #142852;
        overflow: hidden;
        text-align: left;
        padding: 14px 0;
        width: 100%;
        cursor: pointer;
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
        width: 14px;
    }
    .event-retrieval-list li p{
        height: 100%;
        font-size: 13px;
        color: #fff;
        white-space:nowrap;
        overflow:hidden;
        text-overflow:ellipsis;
        display: inline-block;
        width: calc(100% - 34px);
    }
    /deep/ .el-input__inner{
        background-color: rgba(0,0,0,0);
        border-color: #2f4e80;
        color: #fff;
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
        padding-bottom: 14px;
        border-bottom: 1px solid #142852;
        padding-top: 14px;
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

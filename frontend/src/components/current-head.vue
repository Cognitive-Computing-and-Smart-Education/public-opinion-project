<template>
    <div class="current-head">
        {{ name }}
        <div class="head-time">
            数据更新时间：<span>{{ currentTime }}</span>
        </div>
    </div>
</template>

<script>
    export default {
        name: "current-head",
        props: {
            name: {
                type: String,
                deflate: ''
            },
            currentTime: {
                type: String,
                deflate: ''
            }
        }
    }
</script>

<style scoped>
    .current-head{
        width: 100%;
        height: 100%;
        background-color: #0e0f3c;
        color: #fff;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        line-height: 68px;
        background-image: url("../assets/img/current-title.png");
        background-repeat: no-repeat;
        background-size: 100% 100%;
        position: relative;
    }
    .head-time{
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: #79a0ff;
        position: absolute;
        right: 60px;
        top: -17px;
    }
    .head-time span{
        font-size: 13px;
        color: #d1deff;
    }
</style>

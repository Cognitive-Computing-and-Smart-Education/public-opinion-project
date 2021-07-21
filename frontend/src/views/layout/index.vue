<template>
    <el-container style="height: 100%">
        <el-header height="120px">Header</el-header>
        <el-main>
            <div id="container" style="width:500px; height:300px"></div>
<!--            <el-amap class="amap-box" :vid="'amap-vue'" style="width:500px; height:300px"></el-amap>-->
        </el-main>
    </el-container>
</template>

<script>
    export default {
        name: "index",
        mounted () {
            this.init()
        },
        methods: {
            init () {
                let map = new AMap.Map('container', {
                    center: [116.397428, 39.90923],
                    resizeEnable: true,
                    zoom: 10
                })
            }
        }
    }
</script>

<style scoped>
    /deep/ .el-header, .el-footer {
        background-color: #B3C0D1;
        color: #333;
        text-align: center;
        line-height: 120px;
    }

    /deep/ .el-main {
        background-color: #E9EEF3;
        color: #333;
        text-align: center;
        line-height: 160px;
        height: calc(100% - 120px);
    }
</style>

<template>
    <div>
        <div id="container" style="width:500px; height:300px"></div>
    </div>
</template>

<script>
    export default {
        name: "container-center",
        data() {
            return {

            };
        },
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

</style>

<template>
    <div class="current-head">
        {{ name }}
    </div>
</template>

<script>
    export default {
        name: "current-head",
        props: {
            name: {
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
        font-size: 20px;
        text-align: center;
        line-height: 120px;
        background-image: url("../assets/img/current-title.png");
        background-repeat: no-repeat;
        background-size: 100% 100%;
    }
</style>

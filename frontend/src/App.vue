<template>
  <div id="app">
<!--    <img alt="Vue logo" src="./assets/logo.png">-->
<!--    <HelloWorld msg="Welcome to Your Vue.js App"/>-->
    <router-view class="container" />
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'app',
  components: {
    // HelloWorld
  }
}
</script>

<style>
    html {
        min-height: 100%;
        height:100%;
    }
    body{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
    }
    ul,li{
        margin: 0;
        padding: 0;
        border: none;
    }
    #app {
      width: 100%;
      height: 100%;
      /*background-color: #031127;*/
    }
</style>

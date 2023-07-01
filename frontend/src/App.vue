<template>
    <h1>涂涂的贝壳标签生成器 v1.0</h1>
    <ShellLabelGenerator />
    <p style="text-align: center;margin-top: 20px;font-size: 5px;">© 2023 涂涂的角落 京ICP备2022009849号 tutu.gold <a
            href="https://github.com/KbyteTutu/shell-labels-generator">开源项目</a></p>
</template>

<script>
import ShellLabelGen from './components/ShellLabelGen.vue'

export default {
    name: 'App', mounted() {
        document.title = '涂涂的贝壳标签生成器';
    },
    components: {
        ShellLabelGenerator: ShellLabelGen,
    },
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 0px;
}
</style>

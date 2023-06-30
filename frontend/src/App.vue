<template>
    <h1>涂涂的贝壳标签生成器 v0.7</h1>
    <ShellLabelGenerator />
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
    margin-top: 60px;
}
</style>

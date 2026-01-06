<!-- src/App.vue -->
<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/store/user'

// 在应用启动时加载token
onMounted(() => {
  const userStore = useUserStore()
  userStore.loadTokens()
})
</script>

<style>
/* 全局样式保留在这里 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

body {
  background-color: #f5f7fa;
  color: #333;
  line-height: 1.6;
}
</style>
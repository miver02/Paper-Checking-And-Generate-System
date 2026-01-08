<!-- src/components/Layout/MainLayout.vue -->
<template>
  <el-container class="layout-container">
    <!-- 头部 -->
    <el-header class="layout-header">
      <!-- 添加导航栏 -->
      <Navbar/>
    </el-header>

    <!-- 主体 -->
    <el-main class="layout-main">
      <!-- 添加消息弹窗 -->
      <div v-if="messages && messages.length > 0" class="message-container">
        <MessageAlert
          v-for="(message, index) in messages"
          :key="`message-${index}`"
          :message="message"
          @close="removeMessage(index)"
        />
      </div>

      <!-- 登录 / 注册统一组件 -->
      <AuthDialog/>

      <!-- 页面内容插槽 -->
      <slot />
    </el-main>

    <!-- 尾部 -->
  </el-container>
</template>

<script setup>
import MessageAlert from '@/components/common/MessageAlert.vue'
import Navbar from './Navbar.vue'
import AuthDialog from '@/components/auth/AuthDialog.vue'

const props = defineProps({
  messages: {
    type: Array,
    default: () => [],
    validator: (value) => {
      return Array.isArray(value)
    }
  },
})

const removeMessage = index => {
  console.log(`移除消息: ${index}`)
}
</script>

<style scoped>
/* 全局盒模型兜底（scoped 不影响全局，仅作用于当前组件） */
:deep(html) {
  box-sizing: border-box;
}
*,
*::before,
*::after {
  box-sizing: inherit;
}

.layout-container {
  min-height: 100vh;
  /* 用 flex 布局替代硬编码高度计算，更健壮 */
  display: flex;
  flex-direction: column;
}

.layout-header {
  padding: 0;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  /* 给 z-index 加定位上下文，确保生效 */
  position: sticky;
  top: 0;
  z-index: 999;
  /* 明确 header 高度（若需响应式，可加媒体查询） */
  height: 60px;
}

.layout-main {
  background-color: #f5f7f9;
  padding: 20px;
  /* flex: 1 自动填充剩余高度，替代 calc(100vh - 60px) */
  flex: 1;
  /* 防止内容过少时高度不足 */
  min-height: 0;
}

.message-container {
  margin-bottom: 20px;
}
</style>
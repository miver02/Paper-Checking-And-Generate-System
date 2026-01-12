<!-- src/components/Layout/MainLayout.vue -->
<template>
  <el-container flex min-h-screen flex-col class="layout-container">
    <!-- 头部 -->
    <el-header p-0 sticky top-0 z-[999] h-[60px] shadow-[0_1px_4px_rgba(0,21,41,0.08)] class="layout-header">
      <!-- 添加导航栏 -->
      <Navbar/>
    </el-header>

    <!-- 主体 -->
    <el-main bg-[#f5f7f9] p-5 flex-1 min-h-0 class="layout-main">
      <!-- 添加消息弹窗 -->
      <div v-if="messages && messages.length > 0" mb-5 class="message-container">
        <MessageAlert
          v-for="(message, index) in messages"
          :key="`message-${index}`"
          :message="message"
          @close="removeMessage(index)"
        />
      </div>

      <!-- 登录 / 注册 / 个人资料统一组件 -->
      <AuthDialog/>
      <!-- 个人信息模态框 -->
      <template>
        <el-dialog
          v-model="profileVisible"
          title="用户信息"
          width="400px"
          :show-close="true"
        >
          <Profile @close="handleProfileClose"/>
        </el-dialog>
      </template>
    
      <!-- 页面内容插槽 -->
      <slot />
    </el-main>

    <!-- 尾部 -->
  </el-container>
</template>

<script setup>
import MessageAlert from '@/components/common/MessageAlert.vue'
import Navbar from '@/components/navbar/Navbar.vue'
import AuthDialog from '@/components/auth/AuthDialog.vue'
import Profile from '@/components/user/Profile.vue'
import { useUserStore } from '@/store/user'
import { computed } from 'vue'

const userStore = useUserStore()

// 获取消息
const props = defineProps({
  messages: {
    type: Array,
    default: () => [],
    validator: (value) => {
      return Array.isArray(value)
    }
  },
})

// 移除消息
const removeMessage = index => {
  console.log(`移除消息: ${index}`)
}

// 个人资料模态框的显示状态
const profileVisible = computed({
  get: () => userStore.isProfileModalVisible,
  set: val => userStore.toggleProfileModal(val),
})

// 处理个人资料关闭事件
const handleProfileClose = () => {
  userStore.toggleProfileModal(false)
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
</style>
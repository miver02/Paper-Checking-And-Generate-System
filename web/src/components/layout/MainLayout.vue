<!-- src/components/Layout/MainLayout.vue -->
<template>
    <el-container class="layout-container">
        <el-header class="layout-header">
            <Navbar @login-click="handleLoginClick" @register-click="handleRegisterClick" @logout-click="handleLogoutClick" />
        </el-header>

        <el-main class="layout-main">
            <!-- 添加消息弹窗 -->
            <div v-if="messages && messages.length > 0" class="message-container">
                <MessageAlert
                    v-for="(message, index) in messages"
                    :key="index"
                    :message="message"
                    @close="removeMessage(index)"
                />
            </div>

            <!-- 添加登录模态框 -->
            <el-dialog
              v-model="userStore.isLoginModalVisible"
              title="用户登录"
              width="400px"
              :show-close="true"
              @close="userStore.toggleLoginModal(false)"
            >
              <LoginForm @success="handleLoginSuccess" />
            </el-dialog>

            <!-- 添加注册模态框 -->
            <el-dialog
              v-model="userStore.isRegisterModalVisible"
              title="用户注册"
              width="400px"
              :show-close="true"
              @close="userStore.toggleRegisterModal(false)"
            >
              <RegisterForm @success="handleRegisterSuccess" />
            </el-dialog>

            <!-- 页面内容插槽 -->
             <slot />
        </el-main>
    </el-container>
</template>

<script setup>
import { useUserStore } from '@/store/user.js'
import MessageAlert from '@/components/common/MessageAlert.vue'
import RegisterForm from '@/components/auth/RegisterForm.vue' 
import LoginForm from '@/components/auth/LoginForm.vue' 
import Navbar from './Navbar.vue'

const userStore = useUserStore()

defineProps({
  messages: {
    type: Array,
    default: () => []
  }
})

// 处理登录点击事件
const handleLoginClick = () => {
  userStore.toggleLoginModal(true)
}

// 登录成功处理
const handleLoginSuccess = () => {
  userStore.toggleLoginModal(false)
  console.log('登录成功')
}

// 处理注册点击事件
const handleRegisterClick = () => {
  userStore.toggleRegisterModal(true)
}

// 注册成功处理
const handleRegisterSuccess = () => {
  userStore.toggleRegisterModal(false)
  console.log('注册成功')
}

// 退出登录成功处理
const handleLogoutClick = () => {
  userStore.logout()
  console.log('成功退出登录')
}

const removeMessage = (index) => {
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
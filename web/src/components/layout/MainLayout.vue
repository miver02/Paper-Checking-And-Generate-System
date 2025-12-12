<!-- src/components/Layout/MainLayout.vue -->
<template>
    <el-container class="layout-container">
        <el-header class="layout-header">
            <Navbar @login-click="handleLoginClick" @register-click="handleRegisterClick" @logout-click="handleLogoutClick" />
        </el-header>

        <el-main class="layout-main">
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
              v-model="showLoginModal"
              title="用户登录"
              width="400px"
              :show-close="true"
              @close="showLoginModal = false"
            >
              <LoginForm @success="handleLoginSuccess" />
            </el-dialog>

            <!-- 添加注册模态框 -->
            <el-dialog
              v-model="showRegisterModal"
              title="用户注册"
              width="400px"
              :show-close="true"
              @close="showRegisterModal = false"
            >
              <RegisterForm @success="handleRegisterSuccess" />
            </el-dialog>

            <!-- 页面内容插槽 -->
             <slot />
        </el-main>
    </el-container>
</template>

<script setup>
import { ref, watch } from 'vue'
import Navbar from './Navbar.vue'
import { useRoute } from 'vue-router'
import MessageAlert from '@/components/common/MessageAlert.vue'
import LoginForm from '@/components/auth/LoginForm.vue' 
import RegisterForm from '@/components/auth/RegisterForm.vue' 

const route = useRoute()
const showLoginModal = ref(false)
const showRegisterModal = ref(false)

// 监听路由查询参数
const createQueryWatcher = (queryKey, targetRef) => {
  return watch(
    () => route.query[queryKey],
    (value) => {
      targetRef.value = value === 'true'
    },
    { immediate: true }
  )
}

const SHOW_LOGIN_QUERY_KEY = 'showLogin'
const SHOW_REGISTER_QUERY_KEY = 'showRegister'
const TRUE_STRING = 'true'

// 监听路由查询参数
createQueryWatcher(SHOW_LOGIN_QUERY_KEY, showLoginModal)
createQueryWatcher(SHOW_REGISTER_QUERY_KEY, showRegisterModal)

// 处理登录点击事件
const handleLoginClick = () => {
  showLoginModal.value = true
}

// 登录成功处理
const handleLoginSuccess = () => {
  showLoginModal.value = false
  // 可以在这里添加登录成功后的处理逻辑
  console.log('登录成功')
}

// 处理注册点击事件
const handleRegisterClick = () => {
  showRegisterModal.value = true
}

// 注册成功处理
const handleRegisterSuccess = () => {
  showRegisterModal.value = false
  // 可以在这里添加登录成功后的处理逻辑
  console.log('注册成功')
}

const removeMessage = (index) => {
    console.log(`移除消息: ${index}`)
}

// 暴露方法给父组件使用
defineExpose('parent', {
  isLoginModalVisible: showLoginModal,
  isRegisterModalVisible: showRegisterModal
})
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
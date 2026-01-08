<template>
  <!-- 登录 -->
  <el-dialog
    v-model="loginVisible"
    title="用户登录"
    width="400px"
    :show-close="true"
  >
    <LoginForm @success="handleLoginSuccess" />
  </el-dialog>

  <!-- 注册 -->
  <el-dialog
    v-model="registerVisible"
    title="用户注册"
    width="400px"
    :show-close="true"
  >
    <RegisterForm @success="handleRegisterSuccess" />
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/store/user'

import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'

const userStore = useUserStore()

/* v-model 直接代理 store（最稳） */
const loginVisible = computed({
  get: () => userStore.isLoginModalVisible,
  set: val => userStore.toggleLoginModal(val),
})

const registerVisible = computed({
  get: () => userStore.isRegisterModalVisible,
  set: val => userStore.toggleRegisterModal(val),
})


const handleLoginSuccess = () => {
  userStore.toggleLoginModal(false)
}

const handleRegisterSuccess = () => {
  userStore.toggleRegisterModal(false)
}
</script>

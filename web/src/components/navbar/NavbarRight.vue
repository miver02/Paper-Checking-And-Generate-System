<template>
  <div flex-1 justify-center flex items-center class="navbar-right">
    <template v-if="userStore.isAuthenticated">
      <el-sub-menu index="user">
        <template #title>
          <el-icon><User /></el-icon>
          {{ userName }}
        </template>

        <el-menu-item index="profile" @click="handleProfileClick">
          个人中心
        </el-menu-item>

        <el-menu-item index="logout" divided @click="handleLogoutClick">
          退出登录
        </el-menu-item>
      </el-sub-menu>
    </template>

    <template v-else>
      <el-menu-item index="login" @click="handleLoginClick">登录</el-menu-item>
      <el-menu-item index="register" @click="handleRegisterClick"
        >注册</el-menu-item
      >
    </template>
  </div>
</template>

<script setup>
import { User } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user/index'
import { computed } from 'vue'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()

/* 用户名显示 */
const userName = computed(
  () => userStore.userInfo?.display_name || userStore.userInfo?.phone
)

// 显示登录模态框
const handleLoginClick = () => {
  userStore.toggleLoginModal(true)
}

// 显示注册模态框
const handleRegisterClick = () => {
  userStore.toggleRegisterModal(true)
}

// 显示个人信息 模态框
const handleProfileClick = () => {
  userStore.toggleProfileModal(true)
}
// 退出登录成功处理
const handleLogoutClick = async () => {
  try {
    await userStore.logoutAction()
    ElMessage.success('成功退出登录')
  } catch {
    ElMessage.error('退出登录失败')
  }
}
</script>

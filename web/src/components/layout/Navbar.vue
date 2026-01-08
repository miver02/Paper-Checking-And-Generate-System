<!-- src/components/layout/Navbar.vue -->
<template>
  <el-menu
    class="navbar-menu"
    mode="horizontal"
    :ellipsis="false"
    background-color="#409eff"
    text-color="#fff"
    active-text-color="#ffd04b"
  >
    <!-- 左侧 -->
    <div class="navbar-left">
      <el-menu-item index="/">
        <el-icon><Reading /></el-icon>
        <span>论文系统</span>
      </el-menu-item>
    </div>

    <!-- 中间 -->
    <div class="navbar-center">
      <el-menu-item
        v-for="item in menuList"
        :key="item.index"
        :index="item.index"
      >
        <el-icon>
          <component :is="item.icon" />
        </el-icon>
        <span>{{ item.label }}</span>
      </el-menu-item>
    </div>

    <!-- 右侧 -->
    <div class="navbar-right">
      <template v-if="userStore.isAuthenticated">
        <el-sub-menu index="user">
          <template #title>
            <el-icon><User /></el-icon>
            {{ userName }}
          </template>

          <el-menu-item index="/user"> 个人中心 </el-menu-item>

          <el-menu-item index="logout" divided @click="handleLogoutClick">
            退出登录
          </el-menu-item>
        </el-sub-menu>
      </template>

      <template v-else>
        <el-menu-item index="login" @click="handleLoginClick"
          >登录</el-menu-item
        >
        <el-menu-item index="register" @click="handleRegisterClick"
          >注册</el-menu-item
        >
      </template>
    </div>
  </el-menu>
</template>

<script setup>
import {
  Reading,
  Odometer,
  EditPen,
  Search,
  User,
} from '@element-plus/icons-vue'
import { computed } from 'vue'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()

/* 中间菜单配置 */
const menuList = [
  { index: '/', label: '仪表板', icon: Odometer },
  { index: '/ai/generate', label: '生成论文', icon: EditPen },
  { index: '/ai/check', label: '查重检测', icon: Search },
]

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

// 退出登录成功处理
const handleLogoutClick = () => {
  try {
    userStore.clearToken()
    ElMessage.success('成功退出登录')
  } catch (error) {
    ElMessage.error('退出登录失败:', error)
  }
}
</script>

<style scoped>
.navbar-menu {
  height: 60px;
  border: none;
}

.navbar-left,
.navbar-center,
.navbar-right {
  display: flex;
  align-items: center;
}

.navbar-left {
  flex: 1;
}

.navbar-center {
  flex: 2;
  justify-content: center;
}

.navbar-right {
  flex: 1;
  justify-content: flex-end;
}
</style>

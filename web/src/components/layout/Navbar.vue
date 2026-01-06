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
    <div class="navbar-left">
      <el-menu-item index="0">
        <el-icon><Reading /></el-icon>
        <span>论文系统</span>
      </el-menu-item>
    </div>
    
    <div class="navbar-center">
      <el-menu-item index="1">
        <router-link to="/" class="nav-link">
          <el-icon><Odometer /></el-icon>
          <span>仪表板</span>
        </router-link>
      </el-menu-item>
      <el-menu-item index="2">
        <router-link to="/ai/generate" class="nav-link">
          <el-icon><EditPen /></el-icon>
          <span>生成论文</span>
        </router-link>
      </el-menu-item>
      <el-menu-item index="3">
        <router-link to="/ai/check" class="nav-link">
          <el-icon><Search /></el-icon>
          <span>查重检测</span>
        </router-link>
      </el-menu-item>
    </div>
    
    <div class="navbar-right">
      <template v-if="userStore.isAuthenticated">
        <el-sub-menu index="user">
          <template #title>
            <el-icon><User /></el-icon>
            {{ userStore.userInfo?.username || userStore.userInfo?.phone }}
          </template>
          <el-menu-item index="user-center">
            <router-link to="/" class="dropdown-item">个人中心</router-link>
          </el-menu-item>
          <el-menu-item  index="logout" divided>
            <a href="#" @click.prevent="handleLogoutClick" class="dropdown-item">退出登录</a>
          </el-menu-item>
        </el-sub-menu>
      </template>
      
      <template v-else>
        <el-menu-item index="login" @click="handleLoginClick">
           <a href="#" class="nav-link">登录</a>
        </el-menu-item>
        <el-menu-item index="register" @click="handleRegisterClick">
           <a href="#" class="nav-link">注册</a>
        </el-menu-item>
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
import { useUserStore } from '@/store/user.js'


// 定义emits
const emit = defineEmits(['login-click', 'register-click', 'logout-click'])
const userStore = useUserStore()


// 登录
const handleLoginClick = () => {
  emit('login-click')
}

// 注册
const handleRegisterClick = () => {
  emit('register-click')
}

const handleLogoutClick = () => {
  // 实现登出逻辑
  emit('logout-click')
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

.nav-link,
.dropdown-item {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
}
</style>
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
    
    <div class="navbar-center" v-if="isAuthenticated">
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
      <template v-if="isAuthenticated">
        <el-sub-menu index="user">
          <template #title>
            <el-icon><User /></el-icon>
            {{ username }}
          </template>
          <el-menu-item>
            <router-link to="/" class="dropdown-item">个人中心</router-link>
          </el-menu-item>
          <el-menu-item divided>
            <a href="#" @click.prevent="handleLogout" class="dropdown-item">退出登录</a>
          </el-menu-item>
        </el-sub-menu>
      </template>
      
      <template v-else>
        <el-menu-item index="login">
          <router-link to="/login" class="nav-link">登录</router-link>
        </el-menu-item>
        <el-menu-item index="register">
          <router-link to="/register" class="nav-link">注册</router-link>
        </el-menu-item>
      </template>
    </div>
  </el-menu>
</template>

<script setup>
import { ref } from 'vue'
import {
  Reading,
  Odometer,
  EditPen,
  Search,
  User
} from '@element-plus/icons-vue'

// 状态管理应从Vuex或Pinia获取
const props = defineProps({
  isAuthenticated: {
    type: Boolean,
    default: false
  },
  username: {
    type: String,
    default: ''
  }
})

const handleLogout = () => {
  // 实现登出逻辑
  console.log('用户登出')
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
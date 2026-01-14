<!-- src/components/layout/Navbar.vue -->
<template>
  <el-menu
    h-[60px]
    border-none
    class="navbar-menu"
    mode="horizontal"
    :ellipsis="false"
    background-color="#409eff"
    text-color="#fff"
    active-text-color="#ffd04b"
  >
    <!-- 左侧 -->
    <div flex items-center flex-1 class="navbar-left">
      <el-menu-item index="/">
        <el-icon><Reading /></el-icon>
        <span>论文系统</span>
      </el-menu-item>
    </div>

    <!-- 中间 -->
    <div flex items-center flex-2 justify-center class="navbar-center">
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
    <NavbarRight />
  </el-menu>
</template>

<script setup>
import { Reading, Odometer, EditPen, Search } from '@element-plus/icons-vue'

import NavbarRight from './NavbarRight.vue'

/* 中间菜单配置 */
const menuList = [
  { index: '/', label: '仪表板', icon: Odometer },
  { index: '/ai/generate', label: '生成论文', icon: EditPen },
  { index: '/ai/check', label: '查重检测', icon: Search },
]
</script>

// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 路由组件导入
import Home from '@/views/home/Home.vue'

// 路由配置
const routes = [
  // 首页路由
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { hideForAuth: true },
  },
  // 用户路由
  {
    path: '/user/profile',
    name: 'profile',
    component: () => import('@/views/profile/Profile.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

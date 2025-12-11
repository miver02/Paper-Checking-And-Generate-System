// src/router/guard.js
import router from './index'
import { useUserStore } from '@/store/modules/user'

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = !!userStore.token

  // 需要认证但未登录
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  // 已登录用户访问不需要认证的页面（如登录页）
  if (to.meta.hideForAuth && isAuthenticated) {
    next('/')
    return
  }

  next()
})
// src/router/guard.js
import router from './index'
import { useUserStore } from '@/store/modules/user'

// 全局前置守卫
/**
 * 路由前置守卫函数
 * 在每次路由跳转前执行，用于处理用户认证逻辑
 * @param {Object} to - 即将要进入的目标路由对象
 * @param {Object} from - 当前导航正要离开的路由对象
 * @param {Function} next - 用来resolve这个钩子的函数，必须调用
 */
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = !!userStore.token

  // 检查需要认证但用户未登录的情况，重定向到登录页
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({
      path: '/',
      query: {
        redirect: to.fullPath,
        showLogin: 'true'
      }
    })
    return
  }

  // 检查已登录用户访问不需要认证的页面的情况，重定向到首页
  if (to.meta.hideForAuth && isAuthenticated) {
    next('/')
    return
  }

  next()
})
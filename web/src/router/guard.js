// // src/router/guard.js
// import router from './index'
// import { useUserStore } from '@/store/modules/user'

// // 全局前置守卫
// router.beforeEach((to, from, next) => {
//   const userStore = useUserStore()
//   const isAuthenticated = !!userStore.token

//   // 如果需要认证但用户未登录，重定向到登录页
//   if (to.meta.requiresAuth && !isAuthenticated) {
//     next({
//       path: '/',
//       query: {
//         redirect: to.fullPath,
//         showLogin: 'true'
//       }
//     })
//     return
//   }

//   // 如果已登录但访问的是无需认证的页面，重定向到首页
//   if (to.meta.hideForAuth && isAuthenticated) {
//     next('/')
//     return
//   }

//   // 清理查询参数中的 showLogin 和 redirect
//   if (to.query.showLogin || to.query.redirect) {
//     const cleanQuery = { ...to.query }
//     delete cleanQuery.showLogin
//     delete cleanQuery.redirect
//     next({ path: to.path, query: cleanQuery })
//     return
//   }

//   next()
// })
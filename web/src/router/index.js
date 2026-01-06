// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 路由组件导入
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import Home from '@/views/home/Home.vue'
import AIGenerate from '@/views/ai/AIGenerate.vue'
import AICheck from '@/views/ai/AICheck.vue'
import PaperList from '@/views/paper/PaperList.vue'
import PaperEdit from '@/views/paper/PaperEdit.vue'
import PaperResult from '@/views/paper/PaperResult.vue'

// 路由配置
const routes = [
  // 首页路由
  { 
    path: '/', 
    name: 'Home', 
    component: Home,
    meta: { hideForAuth: true }
  },
  
  // 登录路由
  // { 
  //   path: '/login', 
  //   name: 'Login', 
  //   component: Login,
  //   meta: { hideForAuth: true }, // 已登录用户不应该访问登录页
  //   beforeEnter: (to, from, next) => {
  //     // 可以在主页组件中检测路由参数，决定是否显示登录模态框
  //     next();
  //   }
  // },
  // {
  //   path: '/login',
  //   redirect: '/'
  // },

  // 注册路由
  // { 
  //   path: '/register', 
  //   name: 'Register', 
  //   component: Register,
  //   meta: { hideForAuth: true } // 已登录用户不应该访问登录页
  // },
  
  // 论文相关路由
  // { 
  //   path: '/papers', 
  //   name: 'PaperList', 
  //   component: PaperList,
  //   meta: { requiresAuth: true }
  // },
  // { 
  //   path: '/papers/create', 
  //   name: 'PaperCreate', 
  //   component: PaperEdit,
  //   meta: { requiresAuth: true }
  // },
  // { 
  //   path: '/papers/:id/edit', 
  //   name: 'PaperEdit', 
  //   component: PaperEdit,
  //   meta: { requiresAuth: true }
  // },
  // { 
  //   path: '/papers/:id/result', 
  //   name: 'PaperResult', 
  //   component: PaperResult,
  //   meta: { requiresAuth: true }
  // },
  
  // AI功能路由
  // { 
  //   path: '/ai/generate', 
  //   name: 'AIGenerate', 
  //   component: AIGenerate,
  //   meta: { requiresAuth: true }
  // },
  // { 
  //   path: '/ai/check', 
  //   name: 'AICheck', 
  //   component: AICheck,
  //   meta: { requiresAuth: true }
  // }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
import axios from 'axios'
import { useUserStore } from '@/store/user/index'

const service = axios.create({
  baseURL: import.meta.env.VITE_PROXY_PATH || '/api', // 后端 API 前缀
  timeout: import.meta.env.VITE_TIMEOUT,
})

// 请求拦截器（添加 Token）
service.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截
service.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    const userStore = useUserStore()

    if (error.response?.status === 401) {
      // 尝试刷新token
      const refreshed = await userStore.checkAndRefreshToken()

      if (refreshed) {
        // 重新发送原始请求
        error.config.headers['Authorization'] = `Bearer ${userStore.token}`
        return service(error.config)
      } else {
        // 刷新失败，跳转到登录页
        ElMessage.error('登录已过期，请重新登录')
        userStore.clearToken()
        window.location.href = '/login' // 或 router.push('/login')
      }
    }

    return Promise.reject(error)
  }
)

export default service

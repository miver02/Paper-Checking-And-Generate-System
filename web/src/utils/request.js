// src/api/index.js（Axios 实例）
import axios from 'axios'
import { useUserStore } from '@/store/user'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_PATH || '/api', // 后端 API 前缀
  timeout: import.meta.env.VITE_TIMEOUT
})

// 请求拦截器（添加 Token）
service.interceptors.request.use(config => {
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`
  }
  return config
})

// 响应拦截
service.interceptors.response.use(
  res => res.data,
  err => {
    if (err.response?.status === 401) {
      window.dispatchEvent(new Event('open-login'))
    }
    return Promise.reject(err)
  }
)

export default service
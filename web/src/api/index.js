// src/api/index.js（Axios 实例）
import axios from 'axios'
import { useUserStore } from '../store/modules/user'

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api', // 后端 API 前缀
  timeout: 10000
})

// 请求拦截器（添加 Token）
axiosInstance.interceptors.request.use(config => {
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`
  }
  return config
})

export default axiosInstance
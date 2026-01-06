// src/store/modules/user.js
import { defineStore } from 'pinia'
import { refreshToken, verifyToken } from '@/api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    // 登录状态
    token: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    userInfo: null,
    refreshTimer: null, // 定时器句柄
    // 模态框显示状态
    isLoginModalVisible: false,
    isRegisterModalVisible: false
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    getToken: (state) => state.token
  },
  actions: {
    setToken(accessToken, refresh, userInfo = null) {
      this.token = accessToken
      this.refreshToken = refresh
      this.userInfo = userInfo
      
      // 存储到localStorage
      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('refresh_token', refresh)
      if (userInfo) {
        localStorage.setItem('user', JSON.stringify(userInfo))
      }
    },

    // 登出
    clearToken() {
      this.token = null
      this.refreshToken = null
      this.user = null
      
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    },

    
    // 每50分钟检查一次token（比60分钟的token有效期短）
    startTokenRefreshTimer() {
      this.refreshTimer = setInterval(async () => {
        if (this.isAuthenticated) {
          await this.checkAndRefreshToken()
        }
      }, 50 * 60 * 1000) // 50分钟
    },

    stopTokenRefreshTimer() {
      if (this.refreshTimer) {
        clearInterval(this.refreshTimer)
        this.refreshTimer = null
      }
    },

    // 从localStorage加载token
    loadTokens() {
      const accessToken = localStorage.getItem('access_token')
      const refreshToken = localStorage.getItem('refresh_token')
      const user = localStorage.getItem('user')
      
      if (accessToken && refreshToken) {
        this.token = accessToken
        this.refreshToken = refreshToken
        this.user = user ? JSON.parse(user) : null
      }
    },

    // 刷新token
    async refreshTokenAction() {
      if (!this.refreshToken) {
        this.clearToken()
        return false
      }

      try {
        const response = await refreshToken({
          refresh: this.refreshToken
        })

        if (response.data.access) {
          this.token = response.data.access
          // 更新localStorage中的access token
          localStorage.setItem('access_token', response.data.access)
          return true
        }
      } catch (error) {
        console.error('Token refresh failed:', error)
        this.clearToken()
        return false
      }
    },

    // 检查token是否需要刷新（在过期前10分钟刷新）
    async checkAndRefreshToken() {
      if (!this.token) return false

      try {
        // 验证当前token
        await verifyToken({ token: this.token })
        return true
      } catch (error) {
        // 如果验证失败，尝试刷新
        if (this.refreshToken) {
          return await this.refreshTokenAction()
        } else {
          this.clearToken()
          return false
        }
      }
    },

    // 控制模态框显示
    toggleLoginModal(visible) {
      this.isLoginModalVisible = visible
    },
    toggleRegisterModal(visible) {
      this.isRegisterModalVisible = visible
    }
  }
})
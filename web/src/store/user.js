// src/store/modules/user.js
import { defineStore } from 'pinia'
import { refreshToken, verifyToken } from '@/api/auth'

function parseJwt(token) {
  try {
    const base64 = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    return JSON.parse(atob(base64))
  } catch {
    return null
  }
}

export const useUserStore = defineStore('user', {
  state: () => ({
    // 登录状态
    token: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    userInfo: null,
    refreshTimer: null, // 定时器句柄
    refreshingPromise: null, // refresh锁 --> 避免重复请求
    // 模态框显示状态
    isLoginModalVisible: false,
    isRegisterModalVisible: false,
  }),
  getters: {
    isAuthenticated: state => !!state.token,
    getToken: state => state.token,
  },
  actions: {
    setToken(accessToken, refreshToken, userInfo = null) {
      this.token = accessToken
      this.refreshToken = refreshToken
      this.userInfo = userInfo

      // 存储到localStorage
      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('refresh_token', refreshToken)
      if (userInfo) {
        localStorage.setItem('userInfo', JSON.stringify(userInfo))
      }

      this.scheduleTokenRefresh()
    },

    // 从localStorage加载token
    loadTokens() {
      const accessToken = localStorage.getItem('access_token')
      const refreshToken = localStorage.getItem('refresh_token')
      const userInfo = localStorage.getItem('userInfo')

      if (accessToken && refreshToken) {
        this.token = accessToken
        this.refreshToken = refreshToken
        this.userInfo = userInfo ? JSON.parse(userInfo) : null

        this.scheduleTokenRefresh()
      }
    },

    scheduleTokenRefresh() {
      if (!this.token) return

      // 清理旧定时器
      if (this.refreshTimer) {
        clearTimeout(this.refreshTimer)
        this.refreshTimer = null
      }

      const payload = parseJwt(this.token)
      if (!payload?.exp) return

      const now = Date.now()
      const refreshAt = payload.exp * 1000 - 5 * 60 * 1000 // 提前5分钟
      const delay = Math.max(refreshAt - now, 0)

      if (delay === 0) {
        // 防止多 tab 同步 refresh
        this.refreshTokenAction()
        return
      }

      this.refreshTimer = setTimeout(async () => {
        await this.refreshTokenAction()
      }, delay)
    },

    // 刷新token
    async refreshTokenAction() {
      if (this.refreshingPromise) {
        return this.refreshingPromise
      }
      if (!this.refreshToken) {
        this.clearToken()
        return false
      }

      this.refreshingPromise = (async () => {
        try {
          const response = await refreshToken({
            refresh: this.refreshToken,
          })

          if (response.data.access) {
            this.token = response.data.access
            localStorage.setItem('access_token', response.data.access)

            // ⭐ 新增
            this.scheduleTokenRefresh()

            return true
          }

          throw new Error('No access token')
        } catch (error) {
          console.error('Token refresh failed:', error)
          this.clearToken()
          return false
        } finally {
          // ⭐ 无论成功失败，释放锁
          this.refreshingPromise = null
        }
      })()

      return this.refreshingPromise
    },

    // 登出
    clearToken() {
      this.token = null
      this.refreshToken = null
      this.userInfo = null

      this.stopTokenRefreshTimer()

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('userInfo')
    },

    // 清理定时器
    stopTokenRefreshTimer() {
      if (this.refreshTimer) {
        clearTimeout(this.refreshTimer)
        this.refreshTimer = null
      }
    },

    // 控制模态框显示
    toggleLoginModal(visible) {
      this.isLoginModalVisible = visible
    },

    toggleRegisterModal(visible) {
      this.isRegisterModalVisible = visible
    },
  },
})

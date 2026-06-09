// src/store/user/actions/auth.js
import { refreshToken, logout as logoutRequest } from '@/api/auth'
import { parseJwt } from '../utils'

export default {
  async setToken(accessToken, refreshToken) {
    this.token = accessToken
    this.refreshToken = refreshToken

    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)

    await this.getUserInfo()
    this.scheduleTokenRefresh()
  },

  async loadTokens() {
    const accessToken = localStorage.getItem('access_token')
    const refreshToken = localStorage.getItem('refresh_token')

    if (accessToken && refreshToken) {
      this.token = accessToken
      this.refreshToken = refreshToken

      this.scheduleTokenRefresh()
      await this.getUserInfo()
    }
  },

  scheduleTokenRefresh() {
    if (!this.token) return

    if (this.refreshTimer) {
      clearTimeout(this.refreshTimer)
      this.refreshTimer = null
    }

    const payload = parseJwt(this.token)
    if (!payload?.exp) return

    const refreshAt = payload.exp * 1000 - 5 * 60 * 1000
    const delay = Math.max(refreshAt - Date.now(), 0)

    if (delay === 0) {
      this.refreshTokenAction()
      return
    }

    this.refreshTimer = setTimeout(() => {
      this.refreshTokenAction()
    }, delay)
  },

  async refreshTokenAction() {
    if (this.refreshingPromise) return this.refreshingPromise
    if (!this.refreshToken) return this.clearToken()

    this.refreshingPromise = (async () => {
      try {
        const { data } = await refreshToken({ refresh: this.refreshToken })
        if (data?.access) {
          this.token = data.access
          localStorage.setItem('access_token', data.access)
          this.scheduleTokenRefresh()
          return true
        }
        throw new Error()
      } catch {
        this.clearToken()
        return false
      } finally {
        this.refreshingPromise = null
      }
    })()

    return this.refreshingPromise
  },

  async checkAndRefreshToken() {
    return this.refreshTokenAction()
  },

  async logoutAction() {
    try {
      await logoutRequest()
    } finally {
      this.clearToken()
    }
  },

  clearToken() {
    this.token = null
    this.refreshToken = null
    this.userInfo = null

    this.stopTokenRefreshTimer()

    localStorage.clear()
  },

  stopTokenRefreshTimer() {
    if (this.refreshTimer) {
      clearTimeout(this.refreshTimer)
      this.refreshTimer = null
    }
  },
}

// src/store/modules/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null,
    isLoginModalVisible: false,
    isRegisterModalVisible: false
  }),
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
    },
    async login(credentials) {
      try {
        const response = await api.login(credentials)
        this.setToken(response.data.token)
        await this.fetchUserInfo()
        console.log('登录成功')
      } catch (error) {
        console.error('登录失败:', error)
      }
    },
    async fetchUserInfo() {
      try {
        const response = await api.getUserInfo()
        this.userInfo = response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    },
    toggleLoginModal(visible) {
      this.isLoginModalVisible = visible
    },
    toggleRegisterModal(visible) {
      this.isRegisterModalVisible = visible
    }
  }
})
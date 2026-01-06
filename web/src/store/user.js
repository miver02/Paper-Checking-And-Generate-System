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
    setToken(token, userInfo) {
      this.token = token
      this.userInfo = userInfo
      localStorage.setItem('token', token)
    },
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
    },
    toggleLoginModal(visible) {
      this.isLoginModalVisible = visible
    },
    toggleRegisterModal(visible) {
      this.isRegisterModalVisible = visible
    }
  }
})
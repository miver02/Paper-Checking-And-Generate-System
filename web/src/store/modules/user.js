// src/store/modules/user.js
import { defineStore } from 'pinia'

/**
 * 定义用户状态管理仓库
 * @param {string} 'user' - 仓库名称标识符
 * @param {Object} options - 仓库配置选项
 * @param {Function} options.state - 返回初始状态的对象
 * @param {Object} options.actions - 包含状态修改方法的对象
 * @returns {Object} 返回定义好的状态管理仓库实例
 */
export const useUserStore = defineStore('user', {
  /**
   * 定义仓库的初始状态
   * @returns {Object} 包含token和userInfo的状态对象
   */
  state: () => ({
    // 从localStorage中获取token，如果不存在则设置为空字符串
    token: localStorage.getItem('token') || '',
    // 用户信息初始化为null
    userInfo: null
  }),
  actions: {
    /**
     * 设置用户token并保存到localStorage
     * @param {string} token - 用户认证令牌
     */
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    /**
     * 用户退出登录，清除token信息
     */
    logout() {
      this.token = ''
      localStorage.removeItem('token')
    }
  }
})
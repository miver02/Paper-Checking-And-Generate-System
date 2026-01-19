// src/store/user/state.js
export default () => ({
  // 登录状态
  token: localStorage.getItem('access_token') || null,
  refreshToken: localStorage.getItem('refresh_token') || null,
  userInfo: null,

  refreshTimer: null,
  refreshingPromise: null,

  // 模态框状态
  isLoginModalVisible: false,
  isRegisterModalVisible: false,
  isProfileModalVisible: false,

  // 默认头像
  defaultAvatar: 'http://localhost:8000/static/avatars/default.png',
})

// src/store/user/getters.js
export default {
  isAuthenticated: state => !!state.token,
  getToken: state => state.token,
  user: state => state.userInfo || {},
}

// src/store/user/actions/ui.js
export default {
  toggleLoginModal(visible) {
    this.isLoginModalVisible = visible
  },
  toggleRegisterModal(visible) {
    this.isRegisterModalVisible = visible
  },
  toggleProfileModal(visible) {
    this.isProfileModalVisible = visible
  },
}

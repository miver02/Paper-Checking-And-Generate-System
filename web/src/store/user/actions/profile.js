// src/store/user/actions/profile.js
import { getProfile } from '@/api/user'

export default {
  async getUserInfo() {
    try {
      const { data } = await getProfile()
      if (data?.code === 200) {
        this.userInfo = data.data || null
        localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
        return this.userInfo
      }
      throw new Error()
    } catch (err) {
      this.userInfo = null
      localStorage.removeItem('userInfo')
      throw err
    }
  },
}

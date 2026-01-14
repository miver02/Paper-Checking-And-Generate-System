<template>
  <!-- 个人信息模态框 -->
  <el-dialog
    v-model="profileVisible"
    title="用户信息"
    width="400px"
    :show-close="true"
  >
    <Profile />
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/store/user/index'

import Profile from './Profile.vue'

const userStore = useUserStore()

// 自动加载模态框
const profileVisible = computed({
  get: () => userStore.isProfileModalVisible,
  set: val => userStore.toggleProfileModal(val),
})
</script>

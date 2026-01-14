<template>
  <el-card class="w-full max-w-md mx-auto border-none">
    <div class="flex items-center gap-4">
      <!-- 头像 -->
      <el-avatar
        :size="64"
        :src="user.avatar || userStore.defaultAvatar"
        class="shrink-0"
      />

      <!-- 基本信息 -->
      <div class="flex-1">
        <div class="text-[1.2rem] font-600 text-[var(--el-text-color-primary)]">
          {{ user.display_name || '-' }}
        </div>

        <div
          v-for="item in baseInfo"
          :key="item.label"
          class="mt-1 text-sm text-[var(--el-text-color-regular)] ml-15 text-left"
        >
          {{ item.label }}：{{ item.value || '-' }}
        </div>
      </div>
    </div>

    <el-divider class="my-4" />

    <!-- 详细信息 -->
    <div class="space-y-2 text-sm text-[var(--el-text-color-regular)]">
      <div
        v-for="item in detailInfo"
        :key="item.label"
        class="flex justify-between"
      >
        <span>{{ item.label }}</span>
        <span>{{ item.value || '-' }}</span>
      </div>
    </div>
  </el-card>

  <!-- 按钮 -->
  <div class="text-center mt-4">
    <el-button type="success" round @click="goProfile"> 更改信息 </el-button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user/index'

const router = useRouter()
const userStore = useUserStore()

const user = computed(() => userStore.user)

// 基础信息
const baseInfo = computed(() => [
  { label: '标识符', value: user.value.username },
  { label: '手机号', value: user.value.phone },
])
// 详细信息
const detailInfo = computed(() => [
  { label: '邮箱', value: user.value.email },
  { label: '个人介绍', value: user.value.bio },
])

// 跳转到profile页面
const goProfile = () => {
  router.push({
    path: '/user/profile',
  })
}
</script>

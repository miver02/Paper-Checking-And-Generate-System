<template>
  <el-card class="profile-card">
    <!-- 顶部：头像 + 昵称 -->
    <div class="flex items-center gap-4">
      <el-avatar
        :size="72"
        :src="user.avatar || userStore.defaultAvatar"
        class="shadow shrink-0"
      />

      <div class="flex-1">
        <div class="text-lg font-semibold text-[var(--el-text-color-primary)]">
          {{ user.display_name || '-' }}
        </div>

        <div class="mt-1 space-y-1">
          <div
            v-for="item in baseInfo"
            :key="item.label"
            class="text-sm text-[var(--el-text-color-regular)]"
          >
            {{ item.label }}：{{ item.value || '-' }}
          </div>
        </div>
      </div>
    </div>

    <el-divider class="my-4" />

    <!-- 详细信息 -->
    <div class="info-list">
      <div
        v-for="item in detailInfo"
        :key="item.label"
        class="info-item"
      >
        <span class="label">{{ item.label }}</span>
        <span class="value">{{ item.value || '-' }}</span>
      </div>
    </div>

    <!-- 操作 -->
    <div class="text-center mt-6">
      <el-button
        type="primary"
        round
        class="px-8"
        @click="goProfile"
      >
        编辑资料
      </el-button>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const user = computed(() => userStore.user || {})

const baseInfo = computed(() => [
  { label: '用户标识符', value: user.value.username },
  { label: '手机号', value: user.value.phone },
])

const detailInfo = computed(() => [
  { label: '邮箱', value: user.value.email },
  { label: '个人介绍', value: user.value.bio },
])

const goProfile = () => {
  router.push('/user/profile')
}
</script>

<style scoped>
.profile-card {
  max-width: 420px;
  margin: 0 auto;
  border-radius: 16px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: var(--el-text-color-secondary);
}

.value {
  max-width: 60%;
  text-align: right;
  color: var(--el-text-color-regular);
  word-break: break-all;
}
</style>


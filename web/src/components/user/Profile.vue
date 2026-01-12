<template>
  <el-card w-full max-w-md mx-auto border-none>
    <div flex items-center gap-4>
      <!-- 头像 -->
      <el-avatar
        :size="64"
        :src="user.avatar"
        class="shrink-0"
      />

      <!-- 基本信息 -->
      <div class="flex-1">
        <div class="text-[1.2rem] font-600 text-[var(--el-text-color-primary)]">
          {{ user.display_name || user.phone }}
        </div>

        <div class="mt-1 text-sm text-[var(--el-text-color-regular)]">
          手机号：{{ user.phone }}
        </div>
      </div>
    </div>

    <!-- 分割线 -->
    <el-divider class="my-4" />

    <!-- 详细信息 -->
    <div class="space-y-2 text-sm text-[var(--el-text-color-regular)]">
      <div class="flex justify-between">
        <span>邮箱</span>
        <span>{{ user.email }}</span>
      </div>

      <div class="flex justify-between">
        <span>加入时间</span>
        <span>{{ user.createdAt }}</span>
      </div>

      <!-- 关闭按钮 -->
      <div class="mt-4 flex justify-end">
        <el-button @click="closeModel">关闭</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { getProfile } from '@/api/user'
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['close'])
const closeModel = () => emit('close')
const user = ref({})

onMounted(() => {
    fetchUserProfile()
})

const fetchUserProfile = async () => {
    try {
        const res = await getProfile()
        if (res.data.code === 200) {
          user.value = res.data.data
        }
    } catch (error) {
        ElMessage.error('获取用户信息失败')
    }
}
</script>


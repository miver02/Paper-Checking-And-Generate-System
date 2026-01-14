<template>
  <el-card class="max-w-md mx-auto">
    <el-form label-width="80px">
      <el-form-item label="用户名">
        <el-input v-model="form.display_name" />
      </el-form-item>

      <el-form-item label="邮箱">
        <el-input v-model="form.email" />
      </el-form-item>

      <el-form-item label="手机号">
        <el-input v-model="form.phone" />
      </el-form-item>

      <el-form-item label="介绍">
        <el-input v-model="form.bio" type="textarea" :rows="3" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submit"> 保存 </el-button>
        <el-button @click="$router.back()"> 取消 </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { updateProfile } from '@/api/user'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  avatar: userStore.defaultAvatar,
  username: '',
  phone: '',
  email: '',
  display_name: '',
  bio: '',
})

// 当 store.user 有值时，同步到表单
watch(
  () => userStore.user,
  user => {
    Object.assign(form, {
      avatar: user.avatar,
      username: user.username,
      email: user.email,
      phone: user.phone,
      display_name: user.display_name,
      bio: user.bio,
    })
  },
  { immediate: true }
)

// 保存
const submit = async () => {
  try {
    await updateProfile(form)

    // 保存成功后，重新拉用户信息
    await userStore.getUserInfo()

    ElMessage.success('修改成功')
    router.back()
  } catch {
    ElMessage.error('保存失败')
  }
}
</script>

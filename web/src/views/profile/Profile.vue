<template>
  <el-card class="profile-edit-card">
    <!-- 头像区域 -->
    <div class="flex flex-col items-center mb-6">
      <el-avatar
        :size="80"
        :src="form.avatar || userStore.defaultAvatar"
        class="shadow mb-2 cursor-pointer"
        @click="triggerAvatarUpload"
      />
      <el-button type="primary" link @click="triggerAvatarUpload">
        更换头像
      </el-button>

      <!-- 隐藏文件选择 -->
      <input 
        ref="avatarInputRef"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleAvatarChange"
      >
    </div>

    <el-form
      label-width="80px"
      label-position="left"
      class="space-y-2"
    >
      <el-form-item label="昵称">
        <el-input
          v-model="form.display_name"
          placeholder="请输入昵称"
          clearable
        />
      </el-form-item>

      <el-form-item label="邮箱">
        <div class="flex items-center gap-2 w-full">
          <el-input
            v-model="form.email"
            :disabled="!editAuth.email"
          />
          <el-button
            type="primary"
            link
            @click="toggleEdit('email')"
          >
            {{ editAuth.email ? '取消' : '修改' }}
          </el-button>
        </div>

        <div v-if="editAuth.email" class="mt-2 flex gap-2">
          <el-input
            v-model="authCode.email"
            placeholder="请输入邮箱验证码"
          />
          <el-button @click="sendCode('email')">
            发送验证码
          </el-button>
        </div>
      </el-form-item>

      <el-form-item label="手机号">
        <div class="flex items-center gap-2 w-full">
          <el-input
            v-model="form.phone"
            :disabled="!editAuth.phone"
            clearable
          />
          <el-button
            type="primary"
            link
            @click="toggleEdit('phone')"
          >
            {{ editAuth.phone ? '取消' : '修改' }}
          </el-button>
        </div>

        <div v-if="editAuth.phone" class="mt-2 flex gap-2">
          <el-input
            v-model="authCode.phone"
            placeholder="请输入手机验证码"
          />
          <el-button @click="sendCode('phone')">
            发送验证码
          </el-button>
        </div>
      </el-form-item>


      <el-form-item label="个人介绍">
        <el-input
          v-model="form.bio"
          type="textarea"
          :rows="4"
          placeholder="简单介绍一下自己吧～"
          show-word-limit
          maxlength="200"
        />
      </el-form-item>

      <el-form-item class="mt-6">
        <el-button
          type="primary"
          :loading="loading"
          class="px-8"
          @click="submit"
        >
          保存修改
        </el-button>
        <el-button
          class="ml-2"
          @click="$router.back()"
        >
          取消
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { reactive, watch, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { updateProfile, updateAuthProfile, getAvatarUrl } from '@/api/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)

// 头像上传
const avatarInputRef = ref(null)

const triggerAvatarUpload = () => {
  avatarInputRef.value?.click() // 触发点击
}

// 获取用户信息
const form = reactive({
  avatar: '',
  username: '',
  phone: '',
  email: '',
  display_name: '',
  bio: '',
})

// 编辑权限
const editAuth = reactive({
  email: false,
  phone: false,
})

const authCode = reactive({
  email: '',
  phone: '',
})

// 切换编辑权限
const toggleEdit = type => {
  editAuth[type] = !editAuth[type]
  authCode[type] = ''

  // 取消编辑时回滚
  if (!editAuth[type]) {
    form[type] = userStore.user[type]
  }
}

// 用户信息回显
watch(
  () => userStore.user,
  user => {
    if (!user) return

    Object.assign(form, {
      avatar: user.avatar,
      display_name: user.display_name,
      bio: user.bio,
      email: user.email,
      phone: user.phone,
    })
  },
  { immediate: true }
)

// 头像上传处理
const avatarFile = ref(null)
const handleAvatarChange = e => {
  const file = e.target.files?.[0] // 获取文佳
  if (!file) return

  // 基础效验头像
  if (!file.type.startsWith('image/')) {
    ElMessage.error('只能上传图片')
    return
  }

  if (file.size > 2 * 1024 *1024) {
    ElMessage.error('图片大小不能超过 2MB')
    return
  }

  // 本地保存
  avatarFile.value = file

  // 本地预览
  form.avatar = URL.createObjectURL(file)

  // 允许上传同一张照片
  e.target.value = ''
}

const sendCode = type => {
  ElMessage.success(
    `验证码已发送到${type === 'email' ? '邮箱' : '手机'}`
  )
}

// 提交
const submit = async () => {
  // 更新用户信息
  try {
    loading.value = true

    // 提交时,将头像上传到服务器
    if (avatarFile.value !== null) {
      const formData = new FormData()
      formData.append('avatar', avatarFile.value)
      
      const data = await getAvatarUrl(formData) // 获取图片URL
      
      form.avatar = data.url // 使用后端返回的地址
    }

    /** 普通资料接口 */
    const profilePayload = {}

    if (form.display_name !== userStore.user.display_name) {
      profilePayload.display_name = form.display_name
    }

    if (form.bio !== userStore.user.bio) {
      profilePayload.bio = form.bio
    }

    if (form.avatar !== userStore.user.avatar) {
      profilePayload.avatar = form.avatar
    }

    /** 安全资料接口 */
    const authPayload = {}

    if (
      editAuth.email &&
      form.email !== userStore.user.email &&
      authCode.email
    ) {
      authPayload.email = form.email
      authPayload.email_code = authCode.email
    }

    if (
      editAuth.phone &&
      form.phone !== userStore.user.phone &&
      authCode.phone
    ) {
      authPayload.phone = form.phone
      authPayload.phone_code = authCode.phone
    }

    if (Object.keys(profilePayload).length) {
      await updateProfile(profilePayload) // 更新普通用户信息
    }

    if (Object.keys(authPayload).length) {
      await updateAuthProfile(authPayload) // 更新普通用户重要信息
    }

    await userStore.getUserInfo()
    ElMessage.success('修改成功')
    router.back()
  } catch (e) {
    ElMessage.error('保存失败' + e.message)
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>
.profile-edit-card {
  max-width: 420px;
  margin: 0 auto;
  padding: 24px 20px;
  border-radius: 16px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}
</style>

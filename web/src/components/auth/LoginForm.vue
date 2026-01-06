<!-- src/components/auth/LoginForm.vue -->
<template>
  <el-form 
    ref="loginFormRef"
    :model="loginForm"
    :rules="loginRules"
    label-position="top"
    @submit.prevent="handleLogin"
  >
    <el-form-item label="手机号" prop="phone">
      <el-input 
        v-model="loginForm.phone"
        placeholder="请输入手机号"
        clearable
      />
    </el-form-item>
    
    <el-form-item label="密码" prop="password">
      <el-input
        v-model="loginForm.password"
        type="password"
        placeholder="请输入密码"
        show-password
      />
    </el-form-item>
    
    <el-form-item v-if="errorMessage">
      <el-alert
        :title="errorMessage"
        type="error"
        show-icon
        closable
        @close="errorMessage = ''"
      />
    </el-form-item>
    
    <el-form-item>
      <el-button 
        type="primary" 
        native-type="submit"
        :loading="loading"
        style="width: 100%"
      >
        登录
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/user'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

const router = useRouter()
const emit = defineEmits(['success'])

const loginFormRef = ref()
const loading = ref(false)
const errorMessage = ref('')

const loginForm = reactive({
  phone: '',
  password: ''
})

const loginRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const userStore = useUserStore()

const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      loading.value = true

      const res = await login({
        phone: loginForm.phone,
        password: loginForm.password
      })

      // 根据你后端的返回结构判断
      if (res.code === 200) {
        ElMessage.success('登录成功')

        // 存 token（常见做法）
        userStore.setToken(res.data.token, res.data.user)

        emit('success')
        router.push('/')
      } else {
        ElMessage.error(res.msg || '登录失败')
      }
    } catch (err) {
      ElMessage.error('网络错误')
    } finally {
      loading.value = false
    }
  })
}
</script>
<!-- src/components/auth/LoginForm.vue -->
<template>
  <el-form 
    ref="loginFormRef"
    :model="loginForm"
    :rules="loginRules"
    label-position="top"
    @submit.prevent="handleLogin"
  >
    <el-form-item label="用户名" prop="username">
      <el-input 
        v-model="loginForm.username"
        placeholder="请输入用户名"
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

const router = useRouter()
const emit = defineEmits(['success'])

const loginFormRef = ref()
const loading = ref(false)
const errorMessage = ref('')

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      // 模拟登录请求
      setTimeout(() => {
        loading.value = false
        // 登录成功后触发事件
        emit('success')
        router.push('/')
      }, 1000)
    }
  })
}
</script>
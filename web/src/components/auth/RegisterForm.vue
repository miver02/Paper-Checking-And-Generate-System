<!-- src/components/auth/RegisterForm.vue -->
<template>
  <el-form 
    ref="registerFormRef"
    :model="registerForm"
    :rules="registerRules"
    label-position="top"
    @submit.prevent="handleRegister"
  >
    <el-form-item label="手机号" prop="phone">
      <el-input 
        v-model="registerForm.phone"
        placeholder="请输入用户名"
        clearable
      />
    </el-form-item>
    
    <el-form-item label="密码" prop="password">
      <el-input
        v-model="registerForm.password"
        type="password"
        placeholder="请输入密码"
        show-password
      />
    </el-form-item>
    
    <el-form-item label="密码" prop="confirm_password">
      <el-input
        v-model="registerForm.confirm_password"
        type="password"
        placeholder="请再次输入密码"
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
        注册
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/user'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()
const emit = defineEmits(['success'])

const registerFormRef = ref()
const loading = ref(false)
const errorMessage = ref('')

const registerForm = reactive({
  phone: '',
  password: '',
  confirm_password: '',
})

const registerRules = {
  phone: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请再次输入密码', trigger: 'blur' }
  ],
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  await registerFormRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      loading.value = true

      const res = await register(registerForm)

      if (res.code === 200) {
        ElMessage.success('注册成功')

        userStore.setToken(res.data.token, res.data.user)

        emit('success')
        router.push('/')
      } else {
        ElMessage.error(res.message || '注册失败')
      }
    } catch (err) {
      ElMessage.error('网络错误')
    } finally {
      loading.value = false
    }
  })
  

}
</script>
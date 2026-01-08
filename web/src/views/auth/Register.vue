<!-- src/views/auth/Register.vue -->
<template>
  <MainLayout>
    <div class="auth-container">
      <el-row justify="center">
        <el-col :span="12">
          <el-card class="auth-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon :size="24"><User /></el-icon>
                <span>用户注册</span>
              </div>
            </template>

            <el-form
              ref="registerFormRef"
              :model="registerForm"
              :rules="registerRules"
              label-position="top"
              @submit.prevent="handleRegister"
            >
              <el-form-item label="用户名" prop="username">
                <el-input
                  v-model="registerForm.username"
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

              <el-form-item label="确认密码" prop="confirmPassword">
                <el-input
                  v-model="registerForm.confirmPassword"
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

            <div class="auth-footer">
              <p>已有账户？ <router-link to="/login">立即登录</router-link></p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User } from '@element-plus/icons-vue'
import MainLayout from '@/components/layout/MainLayout.vue'

const router = useRouter()
const registerFormRef = ref()

const loading = ref(false)
const errorMessage = ref('')

const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
})

const registerRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  await registerFormRef.value.validate(valid => {
    if (valid) {
      loading.value = true
      // 模拟注册请求
      setTimeout(() => {
        loading.value = false
        // 注册成功后跳转到登录页
        router.push('/login')
      }, 1000)
    }
  })
}
</script>

<style scoped>
.auth-container {
  padding: 50px 0;
}

.auth-card {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 1.2rem;
  font-weight: 500;
}

.auth-footer {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}
</style>

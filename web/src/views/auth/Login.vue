<!-- src/views/Auth/Login.vue -->
<template>
  <MainLayout>
    <div class="auth-container">
      <el-row justify="center">
        <el-col :span="12">
          <el-card class="auth-card" shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon :size="24"><User /></el-icon>
                <span>用户登录</span>
              </div>
            </template>

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

            <div class="auth-footer">
              <p>
                还没有账户？ <router-link to="/register">立即注册</router-link>
              </p>
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
const loginFormRef = ref()

const loading = ref(false)
const errorMessage = ref('')

const loginForm = reactive({
  username: '',
  password: '',
})

const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(valid => {
    if (valid) {
      loading.value = true
      // 模拟登录请求
      setTimeout(() => {
        loading.value = false
        // 登录成功后跳转
        router.push('/dashboard')
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

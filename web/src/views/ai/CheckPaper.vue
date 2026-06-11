<template>
  <MainLayout :messages="messages">
    <div class="check-paper-page">
      <el-card class="check-card" shadow="never">
        <div class="check-hero">
          <div class="eyebrow">功能占位</div>
          <h1>查重检测</h1>
          <p>
            该页面目前只保留入口，后续可以复用同样的异步任务模式接入查重流程。
          </p>
        </div>

        <div class="check-actions">
          <el-button type="primary" size="large" @click="goGenerate">
            去生成论文
          </el-button>
          <el-button size="large" @click="goHome">返回首页</el-button>
        </div>
      </el-card>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import MainLayout from '@/components/layout/MainLayout.vue'

const messages = ref([])
const router = useRouter()

const goGenerate = () => {
  router.push('/ai/generate')
}

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.check-paper-page {
  padding: 28px 0 24px;
}

.check-card {
  max-width: 900px;
  margin: 0 auto;
  border-radius: 24px;
  background:
    radial-gradient(circle at top right, rgba(16, 185, 129, 0.14), transparent 30%),
    linear-gradient(135deg, #f8fafc 0%, #ffffff 60%, #eff6ff 100%);
  border: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
}

.check-hero {
  max-width: 660px;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(16, 185, 129, 0.12);
  color: #047857;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

h1 {
  margin: 14px 0 0;
  font-size: clamp(28px, 4vw, 42px);
  color: #0f172a;
}

p {
  margin: 12px 0 0;
  color: #475569;
  line-height: 1.8;
}

.check-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
}

@media (max-width: 640px) {
  .check-actions {
    flex-direction: column;
  }

  .check-actions :deep(.el-button) {
    width: 100%;
  }
}
</style>

<!-- src/views/home/HomeFeatures.vue -->
<template>
  <div class="features-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="feature-card" shadow="hover">
          <div class="card-content">
            <el-icon :size="48" color="#409eff" class="card-icon"
              ><EditPen
            /></el-icon>
            <h3 class="card-title">论文生成</h3>
            <p class="card-description">使用AI模型根据您的要求生成学术论文</p>
            <el-button type="primary" @click="navigate('/generate')"
              >开始生成</el-button
            >
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="feature-card" shadow="hover">
          <div class="card-content">
            <el-icon :size="48" color="#67c23a" class="card-icon"
              ><Search
            /></el-icon>
            <h3 class="card-title">查重检测</h3>
            <p class="card-description">检测论文的原创性和相似度</p>
            <el-button type="success" @click="navigate('/check')"
              >开始检测</el-button
            >
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="feature-card" shadow="hover">
          <div class="card-content">
            <el-icon :size="48" color="#409eff" class="card-icon"
              ><Odometer
            /></el-icon>
            <h3 class="card-title">个人中心</h3>
            <p class="card-description">查看您的论文和检测历史</p>
            <el-button type="primary" plain @click="navigate('/dashboard')"
              >进入中心</el-button
            >
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { EditPen, Search, Odometer } from '@element-plus/icons-vue'

const emit = defineEmits(['navigate'])

const navigate = path => {
  emit('navigate', path)
}
</script>

<style scoped>
.features-container {
  margin-bottom: 40px;
}

.feature-card {
  height: 100%;
  border: none;
}

.card-content {
  text-align: center;
  padding: 20px;
}

.card-icon {
  margin-bottom: 20px;
}

.card-title {
  margin-bottom: 15px;
  font-size: 1.3rem;
  color: #303133;
}

.card-description {
  margin-bottom: 20px;
  color: #606266;
  line-height: 1.6;
}
</style>

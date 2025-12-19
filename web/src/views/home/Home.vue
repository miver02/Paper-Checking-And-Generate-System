<!-- src/views/Home/Home.vue -->
<template>
  <MainLayout 
    :messages="messages"
  >
    <div class="home-container">
      <div class="hero-section">
        <h1 class="hero-title">
          <el-icon :size="48" color="#409eff"><Reading /></el-icon>
          论文生成和查重系统
        </h1>
        <p class="hero-description">利用AI技术帮助您快速生成高质量论文并进行查重检测</p>
      </div>
      
      <HomeFeatures 
        @navigate="handleNavigation"
      />
      
      <!-- 功能介绍 -->
      <div class="features-section">
        <h2 class="section-title">系统特色</h2>
        <el-row :gutter="20">
          <el-col :span="6" v-for="feature in features" :key="feature.title">
            <div class="feature-card">
              <el-icon :size="32" :color="feature.color" class="feature-icon">
                <component :is="feature.icon" />
              </el-icon>
              <h3 class="feature-title">{{ feature.title }}</h3>
              <p class="feature-description">{{ feature.description }}</p>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user.js'
import {
  Reading,
  Cpu,
  DocumentChecked,
  Clock,
  UserFilled
} from '@element-plus/icons-vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import HomeFeatures from './HomeFeatures.vue'

const router = useRouter()
const userStore = useUserStore()
const messages = ref([])

const features = ref([
  {
    icon: Cpu,
    title: 'AI智能生成',
    description: '基于先进的AI模型，生成高质量学术论文',
    color: '#409eff'
  },
  {
    icon: DocumentChecked,
    title: '专业查重',
    description: '采用专业查重API，确保论文原创性',
    color: '#67c23a'
  },
  {
    icon: Clock,
    title: '快速高效',
    description: '异步处理，快速生成和检测结果',
    color: '#e6a23c'
  },
  {
    icon: UserFilled,
    title: '安全可靠',
    description: '用户数据安全保护，隐私有保障',
    color: '#409eff'
  }
])

const handleNavigation = (path) => {
  router.push(path)
}

</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 40px 0;
}

.hero-title {
  font-size: 2.5rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.hero-description {
  font-size: 1.2rem;
  color: #606266;
  margin-bottom: 40px;
}

.features-section {
  margin-top: 60px;
}

.section-title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 40px;
  color: #303133;
}

.feature-card {
  text-align: center;
  padding: 30px 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
}

.feature-icon {
  margin-bottom: 20px;
}

.feature-title {
  margin-bottom: 15px;
  color: #303133;
}

.feature-description {
  color: #909399;
  line-height: 1.6;
}
</style>
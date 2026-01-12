<!-- src/views/Home/Home.vue -->
<template>
  <MainLayout :messages="messages">
    <div class="max-w-7xl mx-auto">
      <div class="text-center py-10">
        <h1
          text-2.5rem
          mb-5
          flex
          items-center
          justify-center
          gap-3.75
          class="hero-title"
        >
          <el-icon :size="48" color="#409eff"><Reading /></el-icon>
          论文生成和查重系统
        </h1>
        <p text-1.2rem text-[#606266] mb-10 class="hero-description">
          利用AI技术帮助您快速生成高质量论文并进行查重检测
        </p>
      </div>

      <Contents @navigate="handleNavigation" />

      <!-- 功能介绍 -->
      <div mt-60px class="features-section">
        <h2
          text-center
          mb-2.5rem
          text-[#303133]
          text-1.8rem
          class="section-title"
        >
          系统特色
        </h2>
        <el-row :gutter="20">
          <el-col :span="6" v-for="feature in features" :key="feature.title">
            <div
              text-center
              py-30px
              px-20px
              bg-white
              rounded-8px
              shadow-[0_2px_12px_0_rgba(0,0,0,0.1)]
              transition-all
              duration-300
              ease
              class="feature-card"
            >
              <el-icon
                :size="32"
                :color="feature.color"
                mb-1.25rem
                class="feature-icon"
              >
                <component :is="feature.icon" />
              </el-icon>
              <h3 mb-1rem text-[#303133] class="feature-title">
                {{ feature.title }}
              </h3>
              <p text-[#909399] leading-1.6 class="feature-description">
                {{ feature.description }}
              </p>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import {
  Reading,
  Cpu,
  DocumentChecked,
  Clock,
  UserFilled,
} from '@element-plus/icons-vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import Contents from './Contents.vue'

const router = useRouter()
const messages = ref([])

const features = ref([
  {
    icon: markRaw(Cpu),
    title: 'AI智能生成',
    description: '基于先进的AI模型，生成高质量学术论文',
    color: '#409eff',
  },
  {
    icon: markRaw(DocumentChecked),
    title: '专业查重',
    description: '采用专业查重API，确保论文原创性',
    color: '#67c23a',
  },
  {
    icon: markRaw(Clock),
    title: '快速高效',
    description: '异步处理，快速生成和检测结果',
    color: '#e6a23c',
  },
  {
    icon: markRaw(UserFilled),
    title: '安全可靠',
    description: '用户数据安全保护，隐私有保障',
    color: '#409eff',
  },
])
const handleNavigation = path => {
  router.push(path)
}
</script>

<style scoped>
.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
}
</style>

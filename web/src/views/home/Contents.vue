<!-- src/views/home/Contents.vue -->
<template>
  <div mb- class="features-container">
    <el-row :gutter="20">
      <el-col v-for="item in features" :key="item.path" :span="8">
        <el-card border-none h-full class="feature-card" shadow="hover">
          <div text-center p-5 class="card-content">
            <el-icon mb-5 :size="48" :color="item.iconColor" class="card-icon">
              <component :is="item.icon" />
            </el-icon>
            <h3 mb-[15px] text-[1.3rem] text-[#303133] class="card-title">
              {{ item.title }}
            </h3>
            <p mb-5 text-[#606266] leading-[1.6] class="card-description">
              {{ item.description }}
            </p>
            <el-button
              :type="item.buttonType"
              :plain="item.plain"
              @click="navigate(item.path)"
              >{{ item.buttonText }}</el-button
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

const features = [
  {
    title: '论文生成',
    description: '使用AI模型根据您的要求生成学术论文',
    icon: EditPen,
    iconColor: '#409eff',
    buttonType: 'primary',
    buttonText: '生成论文',
    path: '/ai/generate',
    plain: false,
  },
  {
    title: '查重检测',
    description: '检测论文的原创性和相似度',
    icon: Search,
    iconColor: '#67c23a',
    buttonType: 'success',
    buttonText: '开始检测',
    path: '/ai/check',
    plain: false,
  },
  {
    title: '个人中心',
    description: '查看您的论文和检测历史',
    icon: Odometer,
    iconColor: '#409eff',
    buttonText: '进入中心',
    buttonType: 'primary',
    plain: true,
    path: '/user/profile',
  },
]
</script>

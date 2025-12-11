
<template>
  <div class="ai-generate">
    <el-form :model="form" label-width="120px">
      <el-form-item label="论文标题">
        <el-input v-model="form.title"></el-input>
      </el-form-item>
      <el-form-item label="关键词">
        <el-input v-model="form.keywords" placeholder="用逗号分隔"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleGenerate">生成论文</el-button>
      </el-form-item>
    </el-form>

    <!-- 任务状态与结果 -->
    <el-card v-if="taskId">
      <el-progress :percentage="progress" v-if="progress < 100"></el-progress>
      <div v-else>
        <h3>生成结果：</h3>
        <el-input type="textarea" :rows="10" v-model="paperContent"></el-input>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { generatePaper, getGenerateResult } from '../../api/ai'
import { ElMessage } from 'element-plus'

const form = ref({ title: '', keywords: '' })
const taskId = ref('')
const progress = ref(0)
const paperContent = ref('')

const handleGenerate = async () => {
  try {
    // 提交生成任务（后端返回任务 ID）
    const res = await generatePaper(form.value)
    taskId.value = res.data.task_id
    ElMessage.success('生成任务已提交')
    // 轮询查询结果
    checkResult()
  } catch (err) {
    ElMessage.error('提交失败：' + err.message)
  }
}

const checkResult = async () => {
  if (!taskId.value) return
  try {
    const res = await getGenerateResult(taskId.value)
    progress.value = res.data.progress
    if (progress.value < 100) {
      // 未完成，1秒后重试
      setTimeout(checkResult, 1000)
    } else {
      paperContent.value = res.data.content
    }
  } catch (err) {
    ElMessage.error('查询结果失败')
  }
}
</script>
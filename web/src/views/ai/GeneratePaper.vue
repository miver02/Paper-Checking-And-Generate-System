<template>
  <MainLayout :messages="messages">
    <div class="generate-paper-page">
      <section class="hero-banner">
        <div class="hero-copy">
          <div class="eyebrow">Celery 异步任务</div>
          <h1>论文生成</h1>
          <p>
            提交后立即返回任务 ID，后台异步生成，页面自动轮询状态并在完成后展示结果。
          </p>
        </div>

        <div class="hero-metrics">
          <div class="metric">
            <span class="metric-value">3</span>
            <span class="metric-label">次重试</span>
          </div>
          <div class="metric">
            <span class="metric-value">100%</span>
            <span class="metric-label">状态可见</span>
          </div>
          <div class="metric">
            <span class="metric-value">48</span>
            <span class="metric-label">位随机任务号</span>
          </div>
        </div>
      </section>

      <el-row :gutter="24" class="page-grid">
        <el-col :xs="24" :lg="14">
          <el-card class="glass-card form-card" shadow="never">
            <template #header>
              <div class="card-header">
                <div>
                  <div class="card-title">生成配置</div>
                  <div class="card-subtitle">填写主题、要求和可选模板后开始生成</div>
                </div>

                <el-button text type="primary" @click="fillExample">
                  填充示例
                </el-button>
              </div>
            </template>

            <el-form
              ref="formRef"
              :model="form"
              :rules="rules"
              label-position="top"
              class="paper-form"
            >
              <el-row :gutter="16">
                <el-col :xs="24" :md="12">
                  <el-form-item label="论文主题" prop="topic">
                    <el-input
                      v-model="form.topic"
                      placeholder="例如：人工智能在教育中的应用"
                      maxlength="80"
                      show-word-limit
                      clearable
                    />
                  </el-form-item>
                </el-col>

                <el-col :xs="24" :md="12">
                  <el-form-item label="论文标题">
                    <el-input
                      v-model="form.title"
                      placeholder="留空时默认使用论文主题"
                      maxlength="100"
                      show-word-limit
                      clearable
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="生成要求" prop="requirements">
                <el-input
                  v-model="form.requirements"
                  type="textarea"
                  :rows="6"
                  placeholder="请输入字数、结构、研究重点、写作风格等要求"
                  maxlength="2000"
                  show-word-limit
                />
              </el-form-item>

              <el-collapse v-model="expandedPanels" class="template-collapse">
                <el-collapse-item name="templates">
                  <template #title>
                    <div class="collapse-title">
                      <span>高级模板</span>
                      <el-tag size="small" effect="plain">可选</el-tag>
                    </div>
                  </template>

                  <el-row :gutter="16" class="template-grid">
                    <el-col :xs="24" :md="12">
                      <el-form-item label="摘要模板">
                        <el-input
                          v-model="form.templateAbstract"
                          type="textarea"
                          :rows="4"
                          placeholder="输入摘要模板或约束条件"
                          maxlength="1000"
                          show-word-limit
                        />
                      </el-form-item>
                    </el-col>

                    <el-col :xs="24" :md="12">
                      <el-form-item label="正文模板">
                        <el-input
                          v-model="form.templateBody"
                          type="textarea"
                          :rows="4"
                          placeholder="输入正文模板或章节提示"
                          maxlength="1000"
                          show-word-limit
                        />
                      </el-form-item>
                    </el-col>

                    <el-col :xs="24" :md="12">
                      <el-form-item label="总结模板">
                        <el-input
                          v-model="form.templateSummary"
                          type="textarea"
                          :rows="4"
                          placeholder="输入总结模板"
                          maxlength="1000"
                          show-word-limit
                        />
                      </el-form-item>
                    </el-col>

                    <el-col :xs="24" :md="12">
                      <el-form-item label="致谢模板">
                        <el-input
                          v-model="form.templateAcknowledgement"
                          type="textarea"
                          :rows="4"
                          placeholder="输入致谢模板"
                          maxlength="1000"
                          show-word-limit
                        />
                      </el-form-item>
                    </el-col>

                    <el-col :xs="24">
                      <el-form-item label="参考文献模板">
                        <el-input
                          v-model="form.templateReference"
                          type="textarea"
                          :rows="4"
                          placeholder="输入参考文献模板"
                          maxlength="1000"
                          show-word-limit
                        />
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-collapse-item>
              </el-collapse>

              <div class="form-actions">
                <el-button size="large" @click="resetForm">清空表单</el-button>
                <el-button
                  type="primary"
                  size="large"
                  :loading="submitting"
                  @click="submitGeneration"
                >
                  开始生成
                </el-button>
              </div>
            </el-form>
          </el-card>
        </el-col>

        <el-col :xs="24" :lg="10">
          <div class="side-stack">
            <el-card class="glass-card status-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <div>
                    <div class="card-title">任务状态</div>
                    <div class="card-subtitle">轮询当前论文生成进度</div>
                  </div>
                  <el-button
                    text
                    type="primary"
                    :disabled="!activePaperId"
                    :loading="polling"
                    @click="refreshStatus"
                  >
                    刷新
                  </el-button>
                </div>
              </template>

              <div class="status-top">
                <div class="status-badge">
                  <div class="status-icon" :class="`is-${statusMeta.tagType}`">
                    <el-icon :size="22">
                      <component :is="statusMeta.icon" />
                    </el-icon>
                  </div>

                  <div class="status-copy">
                    <div class="status-label">{{ statusMeta.label }}</div>
                    <div class="status-desc">{{ statusMeta.description }}</div>
                  </div>
                </div>
              </div>

              <el-steps :active="stepIndex" align-center finish-status="success">
                <el-step title="排队中" description="任务已创建" />
                <el-step title="生成中" description="worker 正在执行" />
                <el-step title="完成" description="结果已可查看" />
              </el-steps>

              <div class="progress-wrap">
                <el-progress
                  :percentage="statusMeta.progress"
                  :status="progressStatus"
                  :stroke-width="10"
                />
              </div>

              <div class="meta-list">
                <div class="meta-item">
                  <span>paper_id</span>
                  <strong>{{ activePaperId || '-' }}</strong>
                </div>
                <div class="meta-item">
                  <span>task_id</span>
                  <strong>{{ currentTask?.task_id || '-' }}</strong>
                </div>
                <div class="meta-item">
                  <span>更新时间</span>
                  <strong>{{ formatTime(currentTask?.updated_at) }}</strong>
                </div>
              </div>

              <el-alert
                v-if="taskError || currentTask?.failed_reason"
                class="mt-4"
                type="error"
                :title="taskError || currentTask?.failed_reason"
                show-icon
                :closable="false"
              />
            </el-card>

            <el-card class="glass-card result-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <div>
                    <div class="card-title">结果预览</div>
                    <div class="card-subtitle">生成完成后自动展示全文</div>
                  </div>
                  <el-tag :type="statusMeta.tagType" effect="plain">
                    {{ statusMeta.label }}
                  </el-tag>
                </div>
              </template>

              <template v-if="currentTask">
                <template v-if="currentTask.status === 'completed'">
                  <el-tabs v-model="activeTab" class="result-tabs">
                    <el-tab-pane label="摘要" name="abstract">
                      <ResultBlock title="中文摘要" :content="currentTask.abstract" />
                      <ResultBlock title="英文摘要" :content="currentTask.abstract_en" />
                    </el-tab-pane>

                    <el-tab-pane label="正文" name="content">
                      <ResultBlock title="论文正文" :content="currentTask.content" />
                    </el-tab-pane>

                    <el-tab-pane label="总结" name="summary">
                      <ResultBlock title="论文总结" :content="currentTask.summary" />
                    </el-tab-pane>

                    <el-tab-pane label="致谢" name="thank_words">
                      <ResultBlock title="致谢内容" :content="currentTask.thank_words" />
                    </el-tab-pane>

                    <el-tab-pane label="参考文献" name="literature">
                      <div v-if="literatureList.length" class="reference-list">
                        <ol>
                          <li v-for="(item, index) in literatureList" :key="index">
                            {{ typeof item === 'string' ? item : JSON.stringify(item) }}
                          </li>
                        </ol>
                      </div>
                      <el-empty v-else description="暂无参考文献" />
                    </el-tab-pane>
                  </el-tabs>
                </template>

                <template v-else>
                  <el-empty
                    :image-size="120"
                    :description="
                      currentTask.status === 'failed'
                        ? '任务失败，请查看状态卡中的错误信息'
                        : '任务正在生成中，结果会在完成后自动展示'
                    "
                  />
                </template>
              </template>

              <el-empty v-else description="提交任务后在这里查看生成结果" />
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>
  </MainLayout>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Clock,
  Loading,
  CircleCheckFilled,
  CircleCloseFilled,
} from '@element-plus/icons-vue'

import MainLayout from '@/components/layout/MainLayout.vue'
import ResultBlock from '@/components/ai/ResultBlock.vue'
import { generatePaper, getPaperStatus } from '@/api/generate_paper'
import { useAITask } from '@/hooks/useAITask'

const messages = ref([])
const formRef = ref(null)
const submitting = ref(false)
const expandedPanels = ref(['templates'])
const activePaperId = ref('')
const activeTab = ref('abstract')
const storageKey = 'generated-paper:last-paper-id'

const form = reactive({
  topic: '',
  title: '',
  requirements: '',
  templateAbstract: '',
  templateBody: '',
  templateSummary: '',
  templateAcknowledgement: '',
  templateReference: '',
})

const rules = {
  topic: [{ required: true, message: '请输入论文主题', trigger: 'blur' }],
  requirements: [
    { required: true, message: '请输入生成要求', trigger: 'blur' },
  ],
}

const fetchTaskStatus = async paperId => {
  const response = await getPaperStatus(paperId)
  const payload = response?.data

  if (payload?.code !== 200) {
    throw new Error(payload?.message || '查询任务状态失败')
  }

  return payload.data || null
}

const {
  task,
  polling,
  error: taskError,
  pollStatus,
  reset: resetTaskState,
} = useAITask(fetchTaskStatus, {
  interval: 3000,
  finishedStatuses: ['completed', 'failed'],
})

const currentTask = computed(() => task.value)
const literatureList = computed(() =>
  Array.isArray(currentTask.value?.literature) ? currentTask.value.literature : []
)

const statusMeta = computed(() => {
  const status = currentTask.value?.status || 'idle'

  const map = {
    idle: {
      label: '未开始',
      description: '提交任务后会在这里显示执行状态',
      tagType: 'info',
      icon: Clock,
      progress: 0,
    },
    queued: {
      label: '排队中',
      description: '任务已入队，等待 Celery worker 执行',
      tagType: 'info',
      icon: Clock,
      progress: 20,
    },
    generating: {
      label: '生成中',
      description: 'AI 正在生成论文内容',
      tagType: 'warning',
      icon: Loading,
      progress: 65,
    },
    completed: {
      label: '已完成',
      description: '论文已经生成完成',
      tagType: 'success',
      icon: CircleCheckFilled,
      progress: 100,
    },
    failed: {
      label: '生成失败',
      description: '任务执行失败，请查看错误信息',
      tagType: 'danger',
      icon: CircleCloseFilled,
      progress: 100,
    },
  }

  return map[status] || map.idle
})

const stepIndex = computed(() => {
  const status = currentTask.value?.status

  if (status === 'completed') return 2
  if (status === 'generating' || status === 'failed') return 1
  if (status === 'queued') return 0
  return 0
})

const progressStatus = computed(() => {
  const status = currentTask.value?.status
  if (status === 'completed') return 'success'
  if (status === 'failed') return 'exception'
  if (status === 'generating') return 'warning'
  return undefined
})

const formatTime = value => {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return String(value)
  return date.toLocaleString()
}

const syncTaskFromStorage = async () => {
  const savedPaperId = localStorage.getItem(storageKey)
  if (!savedPaperId) return

  activePaperId.value = savedPaperId
  try {
    await pollStatus(savedPaperId)
  } catch {
    // 错误已经在轮询 hook 中记录
  }
}

const fillExample = () => {
  Object.assign(form, {
    topic: '人工智能在教育场景中的应用研究',
    title: '人工智能在教育场景中的应用研究',
    requirements:
      '请生成一篇结构完整的论文，包含摘要、正文、总结、致谢和参考文献。字数不少于6000字，语言正式，适合本科毕业论文。',
    templateAbstract: '摘要部分请突出研究背景、方法、结论与意义。',
    templateBody: '正文部分包含引言、现状分析、方案设计、案例分析与结论。',
    templateSummary: '总结部分需归纳研究成果、局限性与未来展望。',
    templateAcknowledgement: '致谢部分简洁正式，表达对指导老师和家人的感谢。',
    templateReference: '参考文献请列出不少于5条规范学术文献。',
  })
}

const resetForm = () => {
  formRef.value?.resetFields?.()
  Object.assign(form, {
    topic: '',
    title: '',
    requirements: '',
    templateAbstract: '',
    templateBody: '',
    templateSummary: '',
    templateAcknowledgement: '',
    templateReference: '',
  })
  activePaperId.value = ''
  activeTab.value = 'abstract'
  localStorage.removeItem(storageKey)
  resetTaskState()
}

const refreshStatus = async () => {
  if (!activePaperId.value) return
  await pollStatus(activePaperId.value)
}

const submitGeneration = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  submitting.value = true
  taskError.value = ''

  try {
    const response = await generatePaper({
      topic: form.topic,
      title: form.title,
      requirements: form.requirements,
      template_abstract: form.templateAbstract,
      template_body: form.templateBody,
      template_summary: form.templateSummary,
      template_acknowledgement: form.templateAcknowledgement,
      template_reference: form.templateReference,
    })

    const payload = response?.data
    if (payload?.code !== 200) {
      throw new Error(payload?.message || '任务创建失败')
    }

    const nextTask = payload.data || {}
    activePaperId.value = String(nextTask.paper_id || '')
    localStorage.setItem(storageKey, activePaperId.value)
    task.value = nextTask
    activeTab.value = 'abstract'

    ElMessage.success('任务已创建，正在轮询状态')

    if (activePaperId.value) {
      await pollStatus(activePaperId.value)
    }
  } catch (err) {
    ElMessage.error(err?.message || '论文生成任务创建失败')
  } finally {
    submitting.value = false
  }
}

watch(
  () => currentTask.value?.status,
  status => {
    if (status === 'completed') {
      activeTab.value = 'content'
    }
  }
)

onMounted(() => {
  syncTaskFromStorage()
})
</script>

<style scoped>
.generate-paper-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 4px 0 24px;
}

.hero-banner {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: stretch;
  padding: 28px;
  border-radius: 24px;
  color: #eff6ff;
  background:
    radial-gradient(circle at top right, rgba(96, 165, 250, 0.35), transparent 28%),
    radial-gradient(circle at left bottom, rgba(14, 165, 233, 0.22), transparent 26%),
    linear-gradient(135deg, #0f172a 0%, #1e293b 48%, #0b1220 100%);
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.24);
}

.hero-copy {
  max-width: 720px;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding: 6px 12px;
  border-radius: 999px;
  color: #bfdbfe;
  background: rgba(59, 130, 246, 0.14);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero-copy h1 {
  margin: 0;
  font-size: clamp(30px, 4vw, 48px);
  font-weight: 800;
  line-height: 1.05;
}

.hero-copy p {
  margin: 14px 0 0;
  max-width: 66ch;
  color: rgba(226, 232, 240, 0.88);
  font-size: 16px;
}

.hero-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(72px, 1fr));
  gap: 12px;
  min-width: min(360px, 100%);
}

.metric {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;
  padding: 16px;
  border-radius: 18px;
  background: rgba(15, 23, 42, 0.48);
  border: 1px solid rgba(148, 163, 184, 0.2);
  backdrop-filter: blur(12px);
}

.metric-value {
  font-size: 28px;
  font-weight: 800;
  line-height: 1;
}

.metric-label {
  color: rgba(226, 232, 240, 0.78);
  font-size: 13px;
}

.page-grid {
  align-items: stretch;
}

.glass-card {
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(14px);
  box-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
}

.form-card,
.status-card,
.result-card {
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}

.card-subtitle {
  margin-top: 4px;
  color: #64748b;
  font-size: 13px;
}

.paper-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.collapse-title {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.template-grid {
  margin-top: 12px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

.side-stack {
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: 100%;
}

.status-top {
  margin-bottom: 18px;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 14px;
}

.status-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 14px;
  color: #fff;
}

.status-icon.is-info {
  background: linear-gradient(135deg, #38bdf8, #2563eb);
}

.status-icon.is-warning {
  background: linear-gradient(135deg, #f59e0b, #f97316);
}

:deep(.status-icon.is-warning svg) {
  animation: status-spin 1s linear infinite;
  transform-origin: center;
}

.status-icon.is-success {
  background: linear-gradient(135deg, #22c55e, #16a34a);
}

.status-icon.is-danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.status-copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.status-label {
  font-size: 17px;
  font-weight: 700;
  color: #0f172a;
}

.status-desc {
  color: #64748b;
  font-size: 13px;
}

.progress-wrap {
  margin: 20px 0 10px;
}

.meta-list {
  display: grid;
  gap: 12px;
  margin-top: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 14px;
  border-radius: 14px;
  background: #f8fafc;
  color: #334155;
  font-size: 13px;
}

.meta-item strong {
  font-weight: 700;
  color: #0f172a;
  word-break: break-all;
  text-align: right;
}

.result-tabs {
  margin-top: -6px;
}

.reference-list {
  padding: 4px 0 0 20px;
  color: #334155;
}

.reference-list li + li {
  margin-top: 10px;
}

:deep(.el-card__header) {
  border-bottom: 1px solid rgba(148, 163, 184, 0.14);
}

:deep(.el-form-item__label) {
  color: #0f172a;
  font-weight: 600;
}

:deep(.el-input__wrapper),
:deep(.el-textarea__inner) {
  border-radius: 14px;
}

:deep(.el-collapse) {
  border-top: 1px solid rgba(148, 163, 184, 0.16);
  border-bottom: 1px solid rgba(148, 163, 184, 0.16);
}

:deep(.el-empty__description p) {
  color: #64748b;
}

:deep(.result-block) {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

:deep(.result-title) {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}

:deep(.result-content) {
  margin: 0;
  padding: 16px;
  border-radius: 16px;
  background: #f8fafc;
  color: #334155;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.8;
  font-family: inherit;
}

@media (max-width: 992px) {
  .hero-banner {
    flex-direction: column;
  }

  .hero-metrics {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .hero-banner {
    padding: 20px;
  }

  .hero-metrics {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .form-actions :deep(.el-button) {
    width: 100%;
  }
}

@keyframes status-spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>

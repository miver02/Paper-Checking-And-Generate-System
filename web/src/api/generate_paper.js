// src/api/ai.js（AI 生成论文接口）
import service from '@/utils/request'

export const generatePaper = params => {
  return service.post('/ai/generate/', params)
}

export const getGenerateResult = taskId => {
  return service.get(`/ai/generate/result/${taskId}/`)
}

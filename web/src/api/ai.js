// src/api/ai.js（AI 生成论文接口）
import axiosInstance from './index'

export const generatePaper = (params) => {
  return axiosInstance.post('/ai/generate/', params)
}

export const getGenerateResult = (taskId) => {
  return axiosInstance.get(`/ai/generate/result/${taskId}/`)
}
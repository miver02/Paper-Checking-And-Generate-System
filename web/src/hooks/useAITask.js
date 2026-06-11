import { onBeforeUnmount, ref } from 'vue'

export function useAITask(fetchTaskStatus, options = {}) {
  const interval = options.interval ?? 3000
  const finishedStatuses = new Set(
    options.finishedStatuses ?? ['completed', 'failed']
  )

  const task = ref(null)
  const loading = ref(false)
  const polling = ref(false)
  const error = ref('')

  let timer = null

  const clearTimer = () => {
    if (timer) {
      clearTimeout(timer)
      timer = null
    }
  }

  const stopPolling = () => {
    polling.value = false
    clearTimer()
  }

  const scheduleNext = paperId => {
    clearTimer()
    timer = setTimeout(() => {
      pollStatus(paperId)
    }, interval)
  }

  const pollStatus = async paperId => {
    if (!paperId) return null

    loading.value = true
    polling.value = true
    error.value = ''

    try {
      const latestTask = await fetchTaskStatus(paperId)
      task.value = latestTask

      if (!finishedStatuses.has(latestTask?.status)) {
        scheduleNext(paperId)
      } else {
        stopPolling()
      }

      return latestTask
    } catch (err) {
      error.value = err?.message || '查询任务状态失败'
      stopPolling()
      throw err
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    stopPolling()
    task.value = null
    error.value = ''
    loading.value = false
  }

  onBeforeUnmount(() => {
    clearTimer()
  })

  return {
    task,
    loading,
    polling,
    error,
    pollStatus,
    stopPolling,
    reset,
  }
}

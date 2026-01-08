<!-- src/components/Common/MessageAlert.vue -->
<template>
  <el-alert
    :title="message.text"
    :type="getMessageType(message.tags)"
    :closable="true"
    show-icon
    @close="handleClose"
  />
</template>

<script setup>
const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['close'])

// 根据消息类型返回 Element Plus 对应的类型
const getMessageType = tags => {
  if (!tags) return 'info'

  if (tags.includes('error')) return 'error'
  if (tags.includes('warning')) return 'warning'
  if (tags.includes('success')) return 'success'
  return 'info'
}

const handleClose = () => {
  emit('close')
}
</script>

<style scoped>
.el-alert {
  margin-bottom: 10px;
}
</style>

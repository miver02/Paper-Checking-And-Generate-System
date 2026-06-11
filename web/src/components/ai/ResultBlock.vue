<template>
  <div class="result-block">
    <div v-if="title" class="result-title">{{ title }}</div>
    <pre class="result-content">{{ content || '暂无内容' }}</pre>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: '',
  },
  content: {
    type: [String, Number],
    default: '',
  },
})
</script>

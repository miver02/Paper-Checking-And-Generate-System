// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')  // 别名 @ 指向 src
    }
  },
  server: {
    proxy: {
      // 代理 /api 开头的请求到 Django 后端（假设后端端口 6666）
      '/api': {
        target: 'http://localhost:6666',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
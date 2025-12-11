// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store';
import './router/guard'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './style.css'

const app = createApp(App)

// 注册 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
// app.use(store)
app.use(ElementPlus)
app.mount('#app')
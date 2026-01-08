import { defineConfig, presetUno, presetAttributify, presetIcons } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
    presetAttributify(), // 支持 <div flex gap-2 />
    presetIcons({
      scale: 1.2,
      warn: true,
    }),
  ],
})

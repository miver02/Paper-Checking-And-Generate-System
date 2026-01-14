// vite.config.js
import path from 'path'
import { defineConfig, loadEnv } from 'vite'
import Vue from '@vitejs/plugin-vue'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import UnoCSS from 'unocss/vite'

const pathSrc = path.resolve(__dirname, 'src')

export default defineConfig(({ mode }) => {
  // 👇 关键：手动加载 env
  const env = loadEnv(mode, process.cwd())

  // 防御式检查（强烈推荐）
  if (!env.VITE_BASE_SERVER_URL || !env.VITE_BASE_SERVER_PORT) {
    throw new Error(
      'VITE_BASE_SERVER_URL or VITE_BASE_SERVER_PORT is not defined'
    )
  }

  const target = `${env.VITE_BASE_SERVER_URL}:${env.VITE_BASE_SERVER_PORT}`

  return {
    plugins: [
      Vue(),
      UnoCSS(),

      AutoImport({
        imports: ['vue'],
        resolvers: [ElementPlusResolver(), IconsResolver({ prefix: 'Icon' })],
        dts: path.resolve(pathSrc, 'auto-imports.d.ts'),
      }),

      Components({
        resolvers: [
          IconsResolver({
            prefix: 'Icon',
            enabledCollections: ['ep'],
          }),
          ElementPlusResolver(),
        ],
        dts: path.resolve(pathSrc, 'components.d.ts'),
      }),

      Icons({
        autoInstall: true,
      }),
    ],

    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },

    server: {
      proxy: {
        [env.VITE_PROXY_PATH || '/api']: {
          target,
          changeOrigin: true,
          rewrite: p =>
            p.replace(new RegExp(`^${env.VITE_PROXY_PATH || '/api'}`), ''),
        },
      },
    },
  }
})

import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import tailwindcss from "@tailwindcss/vite";
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default ({ mode }) => {
  // Load environment variables for the current mode (e.g. 'development')
  const env = loadEnv(mode, process.cwd())
  
  return defineConfig({
    base: env.VITE_REPO_NAME,
    plugins: [
      tailwindcss(),
      vue(),
      vueDevTools(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    preview: {
      port: 5173,
    },
  })
}

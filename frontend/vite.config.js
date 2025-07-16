import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import tailwindcss from "@tailwindcss/vite";
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
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
  server: {
    // Proxy API requests during development to the FastAPI backend
    // This avoids CORS issues by making requests appear same-origin
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
      },
    },
  },
})

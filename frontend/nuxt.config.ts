// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/styles/global.scss'],
  runtimeConfig: {
    public: {
      // Переопределяется через NUXT_PUBLIC_API_BASE
      apiBase: 'http://localhost:8000/api/v1'
    }
  },
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          // SCSS-переменные палитры доступны во всех компонентах
          additionalData: '@use "~/assets/styles/style.scss" as *;\n'
        }
      }
    }
  }
})

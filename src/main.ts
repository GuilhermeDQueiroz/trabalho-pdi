// Vue
import App from './App.vue'
import { createApp } from 'vue'
const app = createApp(App)

// Pinia
import { createPinia } from 'pinia'
app.use(createPinia())

// Router
import router from './router'
app.use(router)

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'monochromeDark',
    themes: {
      monochromeDark: {
        dark: true,
        colors: {
          background: '#0d0d0d',
          surface: '#181818',
          'surface-bright': '#262626',
          'surface-light': '#333333',
          'surface-variant': '#404040',
          'on-surface-variant': '#f0f0f0',
          primary: '#ffffff',
          'primary-darken-1': '#cccccc',
          secondary: '#8c8c8c',
          'secondary-darken-1': '#595959',
          accent: '#e0e0e0',
          error: '#737373',
          info: '#a6a6a6',
          success: '#d9d9d9',
          warning: '#bfbfbf',
        }
      }
    }
  }
})
app.use(vuetify)

// MDI icons
import '@mdi/font/css/materialdesignicons.css'

// Style global (importado após Vuetify para precedência no cascade do Design System)
import '@/style/index.css'

// ApexCharts
import VueApexCharts from 'vue3-apexcharts'
app.use(VueApexCharts)

app.mount('#app')

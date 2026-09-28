import { createRouter, createWebHistory } from 'vue-router'
import { cROTAS_DASHBOARD, cROTAS_ERROR } from './ConfigRotas'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('../layouts/Layout.vue'),
      children: [
        {
          path: '',
          name: cROTAS_DASHBOARD.dashboard.name,
          component: cROTAS_DASHBOARD.dashboard.component
        },
        {
          path: 'dashboard',
          redirect: '/'
        }
      ]
    },
    {
      path: cROTAS_ERROR.error404.path,
      name: cROTAS_ERROR.error404.name,
      component: cROTAS_ERROR.error404.component
    }
  ]
})

export default router

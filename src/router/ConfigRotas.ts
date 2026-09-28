export const cROTAS_DASHBOARD = {
  dashboard: {
    name: 'dashboard',
    path: '/',
    component: () => import('../views/dashboard/Dashboard.vue')
  }
}

export const cROTAS_ERROR = {
  error404: {
    path: '/:pathMatch(.*)*',
    name: 'error404',
    component: () => import('../views/error/Error404Page.vue')
  }
}

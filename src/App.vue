<template>
  <!-- Loading -->
  <Loading :mensagem="layoutStore.loading.mensagem" :percentual="layoutStore.loading.percentual" />
  <RouterView />
</template>

<script setup lang="ts">
// Router
import { RouterView } from 'vue-router'

// Components
import Loading from '@/components/Loading.vue'

// Store
import { useLayoutStore } from '@/stores/LayoutStore'
const layoutStore = useLayoutStore()
</script>

<style scoped></style>

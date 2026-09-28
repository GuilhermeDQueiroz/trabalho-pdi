<template>
  <v-locale-provider>
    <v-app :class="[]">
      <!-- Header -->

      <Loading />

      <MessageDialog
        v-if="layout.messageDialog.show"
        v-model="layout.messageDialog.show"
        :title="layout.messageDialog.titulo"
        :message="layout.messageDialog.mensagem"
        :type="layout.messageDialog.tipo"
        :ok-callback="callback"
        :cancel-callback="callback"
      />

      <v-main>
        <div class="LStyleLayoutPage">
          <!-- Conteúdo -->

          <RouterView />
        </div>

        <div>
          <!-- <Footer /> -->
        </div>
      </v-main>
    </v-app>
  </v-locale-provider>
</template>

<script setup lang="ts">
// Store
import { useLayoutStore } from '@/stores/LayoutStore'
const layout = useLayoutStore()

// Components
import Loading from '@/components/Loading.vue'
import MessageDialog from '@/components/MessageDialog.vue'

function callback() {
  useLayoutStore().messageDialog.show = !useLayoutStore().messageDialog.show
}
</script>

<style scoped></style>

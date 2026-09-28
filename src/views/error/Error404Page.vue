<template>
  <v-row no-gutters class="overflow-hidden bg-containerBg" style="min-height: 100vh">
    <v-col class="d-flex align-center justify-center">
      <div class="text-center">
        <div class="LCardMediaWrapper">
          <img src="./assets/Error404.png" alt="404" />
          <div class="CardMediaBuild">
            <img src="./assets/TwoCone.png" alt="grid" class="w-100" />
          </div>
        </div>
        <h1 class="text-h1 mt-16">Página não encontrada</h1>
        <p class="text-h6 text-lightText">
          A página que você está procurando foi movida, removida, renomeada ou nunca existiu!
        </p>
        <v-btn :variant="'flat'" :color="'primary'" class="mt-2" @click="onVoltarPaginaAnterior()">
          Voltar a página anterior</v-btn
        >
      </div>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
//Router
import { useRouter } from 'vue-router'
const router = useRouter()

function onVoltarPaginaAnterior() {
  router.back()
}
</script>

<style scoped>
.LCardMediaWrapper {
  max-width: 720px;
  margin: 0 auto;
  position: relative;
  > img {
    @media (min-width: 0px) {
      width: 250px;
      height: 130px;
    }
    @media (min-width: 768px) {
      width: 590px;
      height: 300px;
    }
  }
}
.CardMediaBuild {
  position: absolute;
  top: 60px;
  @media (min-width: 0px) {
    width: 130px;
    height: 115px;
    right: -14%;
  }
  @media (min-width: 768px) {
    width: 390px;
    height: 330px;
    right: -60%;
  }
}
</style>

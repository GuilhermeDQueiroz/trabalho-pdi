<template>
  <v-app-bar class="LStyleToolbar" :elevation="0" :height="64">
    <!-- Identidade: Ícone + Título "Trabalho PDI" -->
    <div class="d-flex align-center pl-4 pr-2">
      <router-link to="/" class="LStyleBrandLink" v-tooltip="'Ir para o topo'">
        <div class="LStyleLogoIcon mr-3">
          <v-icon size="small" color="#ffffff">mdi-image-filter-black-white</v-icon>
        </div>
        <span class="LStyleBrandTitle">Trabalho PDI</span>
      </router-link>
    </div>

    <v-spacer></v-spacer>

    <slot></slot>

    <!-- Ações da Barra: Galeria de Teste + Filtros -->
    <div class="pr-4 d-flex align-center ga-2">
      <!-- Botão Galeria para Teste Rápido -->
      <v-btn
        v-tooltip="'Abrir galeria com 13 imagens de teste padrão'"
        variant="outlined"
        class="LStyleGalleryBtn mr-2"
        @click="onClickGaleria()"
      >
        <v-icon class="mr-2" size="small">mdi-image-multiple-outline</v-icon>
        <span>Galeria de Teste</span>
        <span class="LStyleGalleryCountBadge">13</span>
      </v-btn>

      <!-- Botão de Ação do Pipeline de Filtros -->
      <v-btn
        v-tooltip="'Abrir painel e montar a fila de filtros PDI'"
        variant="elevated"
        class="LStyleFilterBtn"
        @click="onClickFiltros()"
      >
        <v-icon class="mr-2" size="small">mdi-filter-cog-outline</v-icon>
        <span>Filtros</span>
        <span v-if="props.filtrosCount > 0" class="LStyleFilterBadge">
          {{ props.filtrosCount }}
        </span>
      </v-btn>
    </div>
  </v-app-bar>
</template>

<script setup lang="ts">
const emit = defineEmits(['onClickFiltros', 'onClickGaleria'])

interface PropTypes {
  filtrosCount?: number
}

const props = withDefaults(defineProps<PropTypes>(), {
  filtrosCount: 0
})

function onClickFiltros() {
  emit('onClickFiltros')
}

function onClickGaleria() {
  emit('onClickGaleria')
}
</script>

<style scoped>
.LStyleToolbar {
  background-color: rgba(14, 14, 18, 0.94) !important;
  border-bottom: 1px solid var(--pdi-border-subtle) !important;
  backdrop-filter: blur(14px) !important;
  z-index: 200;
}

.LStyleBrandLink {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
  transition: opacity 0.2s ease;
}

.LStyleBrandLink:hover {
  opacity: 0.85;
}

.LStyleLogoIcon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: #242429;
  border: 1px solid var(--pdi-border-default);
  display: grid;
  place-items: center;
}

.LStyleBrandTitle {
  font-size: 1.05rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.02em;
}

.LStyleFilterBtn {
  background-color: var(--pdi-accent-white) !important;
  color: var(--pdi-accent-contrast) !important;
  font-weight: 700 !important;
  font-size: 0.86rem !important;
  border: 1px solid #ffffff !important;
  height: 40px !important;
  padding: 0 16px !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: 0 2px 10px rgba(255, 255, 255, 0.12) !important;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.LStyleFilterBtn:hover {
  background-color: #e4e4e7 !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(255, 255, 255, 0.22) !important;
}

.LStyleFilterBadge {
  background-color: #000000;
  color: #ffffff;
  font-size: 0.7rem;
  font-weight: 800;
  padding: 1px 7px;
  border-radius: var(--radius-full);
  margin-left: 6px;
  line-height: 1.3;
}

.LStyleGalleryBtn {
  border: 1px solid var(--pdi-border-default) !important;
  color: var(--pdi-text-secondary) !important;
  font-weight: 600 !important;
  font-size: 0.86rem !important;
  height: 40px !important;
  padding: 0 14px !important;
  border-radius: var(--radius-sm) !important;
  background-color: rgba(24, 24, 28, 0.6) !important;
  display: inline-flex;
  align-items: center;
}

.LStyleGalleryBtn:hover {
  background-color: rgba(255, 255, 255, 0.08) !important;
  border-color: var(--pdi-border-hover) !important;
  color: #ffffff !important;
  transform: translateY(-1px);
}

.LStyleGalleryCountBadge {
  background-color: #242429;
  color: #a1a1aa;
  font-size: 0.68rem;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: var(--radius-full);
  margin-left: 6px;
  border: 1px solid #383840;
}
</style>

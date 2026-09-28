<template>
  <div class="LStyleFabContainer">

    <!-- Grupo 2: Rotações Geométricas FAB -->
    <div>
      <v-speed-dial location="left center" transition="fade-transition">
        <template v-slot:activator="{ props: activatorProps }">
          <v-btn
            v-bind="activatorProps"
            icon
            size="large"
            class="LStyleSpeedDialMain"
            v-tooltip:left="'Transformações e Rotações Geométricas'"
          >
            <v-icon size="22">mdi-rotate-3d-variant</v-icon>
          </v-btn>
        </template>

        <v-btn
          key="rot-90-cw"
          icon
          size="default"
          class="LStyleSpeedDialChild"
          v-tooltip:top="'Girar 90º Sentido Horário'"
          @click="onClickRotacao90Horario()"
        >
          <v-icon size="19">mdi-rotate-right</v-icon>
        </v-btn>

        <v-btn
          key="rot-90-ccw"
          icon
          size="default"
          class="LStyleSpeedDialChild"
          v-tooltip:top="'Girar 90º Sentido Anti-Horário'"
          @click="onClickRotacao90AntiHorario()"
        >
          <v-icon size="19">mdi-rotate-left</v-icon>
        </v-btn>

        <v-btn
          key="rot-180"
          icon
          size="default"
          class="LStyleSpeedDialChild"
          v-tooltip:top="'Inversão Matricial 180º'"
          @click="onClickRotacao180()"
        >
          <v-icon size="19">mdi-restore</v-icon>
        </v-btn>
      </v-speed-dial>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits([
  'onClickRotacao90Horario',
  'onClickRotacao90AntiHorario',
  'onClickRotacao180'
])

function onClickRotacao180() {
  emit('onClickRotacao180')
}

function onClickRotacao90Horario() {
  emit('onClickRotacao90Horario')
}

function onClickRotacao90AntiHorario() {
  emit('onClickRotacao90AntiHorario')
}
</script>

<style scoped>
.LStyleFabContainer {
  position: fixed;
  right: clamp(16px, 3vw, 40px);
  bottom: clamp(16px, 3vw, 36px);
  z-index: 150;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.LStyleSpeedDialMain {
  background: #1e1e24 !important;
  color: #ffffff !important;
  border: 1px solid var(--pdi-border-default) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.08) !important;
  border-radius: var(--radius-full) !important;
  transition: var(--pdi-transition-fast) !important;
}

.LStyleSpeedDialMain:hover {
  background: #2a2a33 !important;
  border-color: #52525b !important;
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.8), 0 0 16px rgba(255, 255, 255, 0.12) !important;
}

.LStyleSpeedDialChild {
  background: #18181d !important;
  color: #e4e4e7 !important;
  border: 1px solid var(--pdi-border-default) !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5) !important;
  border-radius: var(--radius-full) !important;
  transition: var(--pdi-transition-fast) !important;
}

.LStyleSpeedDialChild:hover {
  background: #2b2b34 !important;
  color: #ffffff !important;
  border-color: #71717a !important;
  transform: scale(1.1);
}
</style>

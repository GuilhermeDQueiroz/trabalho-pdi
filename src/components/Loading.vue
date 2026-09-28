<template>
  <v-dialog
    :persistent="true"
    :fullscreen="true"
    :transition="transition"
    v-model="exibeLoading"
    :reverse-transition="reverseTransition"
    class="LStyleLoadingDialog"
  >
    <div class="LStyleLoadingBackdrop">
      <div class="LStyleLoadingCard">
        <v-progress-circular
          :width="4"
          :rotate="360"
          :size="props.size"
          color="#ffffff"
          v-model="props.percentual"
          :indeterminate="true"
        >
          <template v-slot:default v-if="exibePercentual">
            <span class="LStylePercentText">{{ props.percentual }}%</span>
          </template>
        </v-progress-circular>

        <span class="LStyleLoadingMsg mt-5">
          {{ props.mensagem || 'Processando algoritmos no motor Python...' }}
        </span>
        <span class="LStyleLoadingSub mt-1">
          Aguarde a finalização dos cálculos matriciais
        </span>
      </div>
    </div>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface PropTypes {
  mensagem?: string
  percentual?: number
  size?: number
}

const props = withDefaults(defineProps<PropTypes>(), {
  size: 64,
  mensagem: '',
  percentual: 0
})

const transition = ref<string>('fade-transition')
const reverseTransition = ref<string>('fade-transition')

const exibeLoading = computed(() => {
  return props.mensagem !== ''
})

const exibePercentual = computed(() => {
  return props.percentual !== undefined && props.percentual > 0
})
</script>

<style scoped>
.LStyleLoadingBackdrop {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(9, 9, 11, 0.78);
  backdrop-filter: blur(10px);
}

.LStyleLoadingCard {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 40px;
  background: rgba(24, 24, 28, 0.95);
  border: 1px solid var(--pdi-border-default);
  border-radius: var(--radius-lg);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
  text-align: center;
  max-width: 420px;
}

.LStylePercentText {
  font-size: 0.85rem;
  font-weight: 700;
  color: #ffffff;
}

.LStyleLoadingMsg {
  font-size: 0.96rem;
  font-weight: 600;
  color: #ffffff;
  letter-spacing: -0.01em;
}

.LStyleLoadingSub {
  font-size: 0.76rem;
  color: var(--pdi-text-muted);
}
</style>

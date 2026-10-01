<template>
  <v-card class="LStyleFilterItemCard" elevation="0">
    <div class="LStyleFilterItemHeader">
      <div class="d-flex align-center gap-2">
        <div class="LStyleDragHandle" v-tooltip="'Arraste para reordenar a execução'">
          <v-icon size="small" color="#71717a">mdi-drag</v-icon>
        </div>
        <span class="LStyleOrderBadge">#{{ props.ordem }}</span>
        <h4 class="LStyleItemTitle">{{ props.titulo }}</h4>
      </div>

      <div class="d-flex align-center ga-2">
        <v-btn
          size="small"
          variant="tonal"
          color="error"
          class="LStyleDeleteBtn"
          v-tooltip="'Excluir este filtro da fila'"
          @click.stop="onDeleteItem(props.index)"
        >
          <v-icon size="16" class="mr-1">mdi-trash-can-outline</v-icon>
          <span>Excluir</span>
        </v-btn>
      </div>
    </div>

    <!-- Inputs reativos para os parâmetros -->
    <div v-if="temParametros" class="LStyleFilterItemBody">
      <v-row class="g-2">
        <v-col
          v-for="(param, index) in params"
          :sm="4"
          :cols="12"
          :key="index"
          class="py-1"
        >
          <v-file-input
            v-if="String(index) === 'imagem'"
            color="primary"
            variant="outlined"
            density="compact"
            label="Carregar 2ª Imagem"
            prepend-icon=""
            append-inner-icon="mdi-upload"
            accept="image/png, image/jpeg, image/bmp"
            @change="onImageParametroChange(String(index), $event)"
            hide-details
            class="LStyleParamInput"
            v-tooltip="'Selecione uma segunda imagem para somar com porcentagem'"
          ></v-file-input>

          <v-text-field
            v-else
            variant="outlined"
            density="compact"
            v-model="params[index]"
            :label="obterLabelParametro(String(index))"
            @input="atualizarParametro(String(index), param)"
            hide-details
            class="LStyleParamInput"
          />
        </v-col>
      </v-row>
    </div>
  </v-card>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

const emit = defineEmits(['onDelete'])

const props = defineProps({
  titulo: { type: String, required: true },
  subtitulo: { type: String, required: false },
  ordem: { type: Number, required: true },
  index: { type: Number, required: true }
})

const params = defineModel<any>('params', {
  required: true
})

const temParametros = computed(() => {
  return params.value && Object.keys(params.value).length > 0
})

function onDeleteItem(pIndex: number) {
  emit('onDelete', pIndex)
}

function obterLabelParametro(nome: string): string {
  switch (nome) {
    case 'gamma':
      return 'Gamma γ (ex: 2.0)'
    case 'tamanhoMascara':
      return 'Tamanho da Máscara (3, 5, 7)'
    case 'a':
      return 'Fator de Ganho (a)'
    case 'b':
      return 'Deslocamento (b)'
    case 'porcentagemImagem1':
      return '% Imagem 1 (0 a 100)'
    case 'ampliacao':
      return 'Fator A (Nitidez ≥ 1)'
    default:
      return `Parâmetro: ${nome}`
  }
}

function atualizarParametro(pIndexCampo: string, pValor: any) {
  if (params.value) {
    params.value[pIndexCampo] = pValor
  }
}

function onImageParametroChange(pIndex: string, pEvent: Event) {
  try {
    const target = pEvent.target as HTMLInputElement
    const file = target.files?.[0]

    if (file) {
      const reader = new FileReader()
      reader.onload = () => {
        const base64 = reader.result as string
        atualizarParametro(pIndex, base64)
      }
      reader.readAsDataURL(file)
    }
  } catch (error) {
    console.error('Erro ao carregar imagem para soma:', error)
  }
}
</script>

<style scoped>
.LStyleFilterItemCard {
  background-color: #17171b !important;
  border: 1px solid var(--pdi-border-subtle) !important;
  border-radius: var(--radius-sm);
  overflow: hidden;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.LStyleFilterItemCard:hover {
  border-color: var(--pdi-border-default) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.LStyleFilterItemHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background-color: #1c1c22;
  border-bottom: 1px solid var(--pdi-border-subtle);
}

.LStyleDragHandle {
  cursor: grab;
  padding: 2px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  transition: color 0.15s ease;
}

.LStyleDragHandle:active {
  cursor: grabbing;
}

.LStyleDragHandle:hover .v-icon {
  color: #ffffff !important;
}

.LStyleOrderBadge {
  font-size: 0.72rem;
  font-weight: 800;
  color: #a1a1aa;
  background: #27272e;
  padding: 1px 7px;
  border-radius: 4px;
  border: 1px solid #383842;
}

.LStyleItemTitle {
  margin: 0;
  font-size: 0.88rem;
  font-weight: 600;
  color: #ffffff;
}

.LStyleInfoBadgeBtn {
  font-size: 0.74rem !important;
  color: #a1a1aa !important;
  background-color: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: var(--radius-xs) !important;
  height: 28px !important;
  padding: 0 8px !important;
  text-transform: none !important;
  letter-spacing: 0.01em !important;
  transition: all 0.2s ease !important;
}

.LStyleInfoBadgeBtn:hover {
  color: #ffffff !important;
  background-color: rgba(255, 255, 255, 0.12) !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
}

.LStyleFilterInfoCard {
  background-color: #16161a !important;
  border: 1px solid #33333d !important;
  border-radius: var(--radius-md) !important;
}

.LStyleCategoryBadge {
  font-size: 0.68rem;
  font-weight: 700;
  color: #a1a1aa;
  background-color: #27272f;
  padding: 2px 8px;
  border-radius: 12px;
  border: 1px solid #3f3f4e;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.LStyleFormulaBox {
  background-color: #0d0d10;
  border: 1px solid #26262e;
  border-radius: 6px;
  padding: 6px 12px;
}

.LStyleFormulaBox code {
  color: #ffffff;
  font-family: 'Fira Code', monospace;
  font-size: 0.84rem;
  font-weight: 600;
}

.LStyleDeleteBtn {
  color: #fca5a5 !important;
  background-color: rgba(239, 68, 68, 0.14) !important;
  border: 1px solid rgba(239, 68, 68, 0.35) !important;
  font-weight: 600 !important;
  font-size: 0.74rem !important;
  text-transform: none !important;
  letter-spacing: 0.02em !important;
  border-radius: var(--radius-xs) !important;
  height: 28px !important;
  padding: 0 10px !important;
  transition: var(--pdi-transition-fast) !important;
}

.LStyleDeleteBtn:hover {
  color: #ffffff !important;
  background-color: #dc2626 !important;
  border-color: #ef4444 !important;
}

.LStyleFilterItemBody {
  padding: 12px 14px;
  background-color: #141417;
}

.LStyleParamInput :deep(.v-field) {
  background-color: #1a1a20 !important;
  font-size: 0.82rem;
}
</style>

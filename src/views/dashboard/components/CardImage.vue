<template>
  <div class="LStyleCardWrapper">
    <v-card class="LStyleImageCard" elevation="0">
      <!-- Cabeçalho Técnico do Card -->
      <div class="LStyleCardHeader">
        <div>
          <div class="d-flex align-center">
            <v-icon class="mr-2" size="20" color="#ffffff">
              {{ props.titulo.toLowerCase().includes('entrada') ? 'mdi-image-outline' : 'mdi-image-auto-adjust' }}
            </v-icon>
            <h3 class="LStyleCardTitle">{{ props.titulo }}</h3>
          </div>
          <span v-if="exibindoHistograma" class="LStyleMetaTag mt-1">
            Histograma de Níveis de Cinza (256 NC)
          </span>
          <span v-else-if="dimensoes.w > 0" class="LStyleMetaTag mt-1">
            {{ dimensoes.w }} × {{ dimensoes.h }} px • 8-bit monocromático
          </span>
          <span v-else class="LStyleMetaTag mt-1">Aguardando entrada</span>
        </div>

        <div class="d-flex align-center">
          <!-- Botão / Tooltip Informativo dos Filtros Aplicados -->
          <v-menu
            v-if="props.filtrosAplicados && props.filtrosAplicados.length > 0"
            location="bottom end"
            :close-on-content-click="false"
            max-width="480"
          >
            <template #activator="{ props: menuProps }">
              <v-btn
                v-bind="menuProps"
                variant="tonal"
                size="small"
                class="LStyleAppliedFiltersBtn mr-2"
                v-tooltip="'Ver detalhes de como os filtros foram aplicados nesta imagem'"
              >
                <v-icon size="16" class="mr-1.5" color="#ffffff">mdi-layers-outline</v-icon>
                <span>{{ props.filtrosAplicados.length }} {{ props.filtrosAplicados.length === 1 ? 'Filtro Aplicado' : 'Filtros Aplicados' }}</span>
                <v-icon size="14" class="ml-1" color="#a1a1aa">mdi-information-outline</v-icon>
              </v-btn>
            </template>

            <v-card class="LStyleAppliedFiltersPopover pa-4" elevation="12">
              <div class="d-flex align-center justify-space-between mb-3 border-b pb-2" style="border-color: #27272e !important">
                <div class="d-flex align-center ga-2">
                  <v-icon color="#ffffff" size="18">mdi-tune-vertical-variant</v-icon>
                  <span class="text-subtitle-2 font-weight-bold" style="color: #ffffff">Filtros Aplicados na Imagem</span>
                </div>
                <span class="LStylePipelineCountBadge">{{ props.filtrosAplicados.length }} na sequência</span>
              </div>

              <div class="LStyleAppliedFiltersList">
                <div
                  v-for="(filtro, idx) in props.filtrosAplicados"
                  :key="idx"
                  class="LStyleAppliedFilterItem mb-3"
                >
                  <div class="d-flex align-center justify-space-between mb-1.5 flex-wrap ga-2">
                    <div class="d-flex align-center ga-1.5">
                      <span class="LStyleStepNumberBadge">#{{ idx + 1 }}</span>
                      <strong class="text-caption font-weight-bold" style="color: #ffffff">{{ obterInfoFiltro(filtro.tipo).titulo }}</strong>
                      <span class="LStyleCategoryChip">{{ obterInfoFiltro(filtro.tipo).categoria }}</span>
                    </div>
                    <code class="LStyleMiniFormula">{{ obterInfoFiltro(filtro.tipo).formula }}</code>
                  </div>

                  <div class="LStyleAppliedFilterDetails pa-2.5">
                    <p class="mb-1 text-caption" style="color: #e4e4e7">
                      <strong style="color: #a1a1aa">O que aplicou:</strong> {{ obterInfoFiltro(filtro.tipo).oQueAplica }}
                    </p>
                    <p class="mb-0 text-caption" style="color: #a1a1aa">
                      <strong style="color: #71717a">Como aplicou (Matemática):</strong> {{ obterInfoFiltro(filtro.tipo).comoAplica }}
                    </p>
                  </div>
                </div>
              </div>
            </v-card>
          </v-menu>

          <!-- Botão de Alternância Direta: Imagem <-> Histograma -->
          <v-btn
            variant="tonal"
            size="small"
            :class="['LStyleHistToggleBtn', { 'LStyleHistToggleBtnActive': exibindoHistograma }]"
            :disabled="!imagem"
            @click="toggleHistograma"
            v-tooltip="exibindoHistograma ? 'Voltar para a exibição da imagem' : 'Alternar para Histograma de Níveis de Cinza'"
          >
            <v-icon size="17" class="mr-1.5">
              {{ exibindoHistograma ? 'mdi-image-outline' : 'mdi-chart-bell-curve' }}
            </v-icon>
            <span>{{ exibindoHistograma ? 'Ver Imagem' : 'Histograma' }}</span>
          </v-btn>
        </div>
      </div>

      <!-- Área de Visualização da Imagem / Histograma -->
      <div class="LStylePreviewContainer">
        <!-- Modo Histograma -->
        <div v-if="exibindoHistograma" class="LStyleHistogramViewport">
          <div v-if="carregandoHistograma" class="LStyleHistLoading">
            <v-progress-circular :width="3" :size="48" color="#ffffff" indeterminate />
            <span class="mt-3 text-caption" style="color: #a1a1aa">
              Computando frequências no motor Python...
            </span>
          </div>

          <div v-else class="w-100 pa-3">
            <div class="LStyleHistStatsBar mb-3">
              <div class="LStyleStatChip">
                <span class="text-caption" style="color: #71717a">Níveis:</span>
                <strong>256 NC</strong>
              </div>
              <div v-if="dadosHistograma.totalPixels > 0" class="LStyleStatChip">
                <span class="text-caption" style="color: #71717a">Total Pixels:</span>
                <strong>{{ dadosHistograma.totalPixels.toLocaleString('pt-BR') }} px</strong>
              </div>
              <div class="LStyleStatChip">
                <span class="text-caption" style="color: #71717a">Motor:</span>
                <strong>Python Puro</strong>
              </div>
            </div>

            <GraficoDeBarras
              :key="keyGrafico"
              :labels="dadosHistograma.labels"
              :valores="dadosHistograma.valores"
              :titulo="'Histograma - ' + props.titulo"
            />
          </div>
        </div>

        <!-- Modo Imagem (Padrão) -->
        <div v-else class="LStyleImageViewport">
          <img
            v-if="imagem"
            :id="'ImagePreview-' + uid"
            :src="imagem"
            :alt="props.titulo"
            class="LStyleUploadedImage"
            @mousemove="onMouseMove"
            @mouseleave="onMouseLeave"
            @load="onImageLoad"
          />

          <!-- Estado Vazio Intuitivo -->
          <div v-else class="LStyleEmptyState">
            <div class="LStyleEmptyIconBox mb-3">
              <v-icon size="36" color="#ffffff">mdi-image-plus-outline</v-icon>
            </div>
            <h4 class="LStyleEmptyTitle">Nenhuma imagem carregada</h4>
            <p class="LStyleEmptySubtitle">Selecione um arquivo de imagem para visualizar e processar</p>
            <div class="d-flex align-center justify-center mt-2">
              <span class="LStyleFormatBadge mr-2">PNG</span>
              <span class="LStyleFormatBadge mr-2">JPG</span>
              <span class="LStyleFormatBadge">BMP</span>
            </div>
          </div>

          <!-- HUD Flutuante da Ponta de Prova (Coordenadas x, y e Nível de Cinza) -->
          <transition name="fade">
            <div v-if="imagem && coordenadasAtivas && nivelCinza !== null" class="LStyleProbeHud">
              <div class="LStyleProbeSwatch mr-2" :style="{ backgroundColor: `rgb(${nivelCinza}, ${nivelCinza}, ${nivelCinza})` }"></div>
              <div class="d-flex flex-column">
                <span class="LStyleProbeCoords">X: {{ coordenadas.x }} &nbsp;|&nbsp; Y: {{ coordenadas.y }}</span>
                <span class="LStyleProbeNC">Nível de Cinza (NC): <strong>{{ nivelCinza }}</strong></span>
              </div>
            </div>
          </transition>
        </div>

        <!-- Dica de Rodapé da Ponta de Prova / Histograma -->
        <div v-if="imagem && !exibindoHistograma" class="LStyleProbeStatus mt-2">
          <v-icon size="14" class="mr-1">mdi-crosshairs-gps</v-icon>
          <span>Ponta de Prova ativa: passe o mouse sobre a imagem para inspecionar intensidade e coordenadas</span>
        </div>
        <div v-else-if="imagem && exibindoHistograma" class="LStyleProbeStatus mt-2">
          <v-icon size="14" class="mr-1">mdi-chart-bar</v-icon>
          <span>Histograma de níveis de cinza [0, 255] gerado matematicamente pelo Python</span>
        </div>
      </div>

      <!-- Rodapé de Ações do Card -->
      <div class="LStyleCardActions">
        <slot name="actions"></slot>
      </div>
    </v-card>
  </div>
</template>

<script setup lang="ts">
// Vue
import { ref, watch, onMounted } from 'vue'

// Components
import GraficoDeBarras from '@/components/GraficoDeBarras.vue'

// Service Python
import { PythonPdiService } from '@/services/PythonPdiService'

// Explicação dos Filtros
import { obterInfoFiltro } from '@/utils/pdiInfoFiltros'

export interface IItemFiltroAplicado {
  tipo: number
  titulo: string
  params?: any
}

interface PropTypes {
  titulo?: string
  maxWidhtCard?: string
  colunasCard?: number
  imagemMatriz?: number[][]
  filtrosAplicados?: IItemFiltroAplicado[]
}

const props = withDefaults(defineProps<PropTypes>(), {
  titulo: 'Painel de Imagem',
  colunasCard: 12,
  maxWidhtCard: '100%',
  imagemMatriz: () => [],
  filtrosAplicados: () => []
})

const imagem = defineModel<string | null>('imagem', {
  default: null
})

const uid = Math.random().toString(36).substr(2, 9)
const coordenadas = ref({ x: 0, y: 0 })
const nivelCinza = ref<number | null>(null)
const coordenadasAtivas = ref(false)
const dimensoes = ref({ w: 0, h: 0 })

// Estado do Histograma no Card
const exibindoHistograma = ref<boolean>(false)
const carregandoHistograma = ref<boolean>(false)
const dadosHistograma = ref<{ labels: string[]; valores: number[]; totalPixels: number }>({
  labels: [],
  valores: [],
  totalPixels: 0
})
const keyGrafico = ref(0)

const canvas = ref<HTMLCanvasElement | null>(null)
const imageElement = ref<HTMLImageElement | null>(null)
const context = ref<CanvasRenderingContext2D | null>(null)

onMounted(() => {
  imageElement.value = document.getElementById(`ImagePreview-${uid}`) as HTMLImageElement
  onImageLoad()
})

watch(
  () => [imagem.value, props.imagemMatriz],
  ([newImg]) => {
    if (newImg) {
      setTimeout(onImageLoad, 50)
      if (exibindoHistograma.value) {
        carregarHistograma()
      }
    } else {
      dimensoes.value = { w: 0, h: 0 }
      coordenadasAtivas.value = false
      exibindoHistograma.value = false
    }
  }
)

function onImageLoad() {
  imageElement.value = document.getElementById(`ImagePreview-${uid}`) as HTMLImageElement
  if (imageElement.value && imageElement.value.naturalWidth > 0) {
    canvas.value = document.createElement('canvas')
    context.value = canvas.value.getContext('2d')

    const natW = imageElement.value.naturalWidth
    const natH = imageElement.value.naturalHeight
    dimensoes.value = { w: natW, h: natH }

    canvas.value.width = natW
    canvas.value.height = natH

    context.value?.drawImage(imageElement.value, 0, 0, natW, natH)
  }
}

async function carregarHistograma() {
  if (!imagem.value) return

  try {
    carregandoHistograma.value = true
    const fonte = (props.imagemMatriz && props.imagemMatriz.length > 0)
      ? props.imagemMatriz
      : imagem.value

    const res = await PythonPdiService.obterHistograma(fonte)
    dadosHistograma.value = {
      labels: res.labels,
      valores: res.valores,
      totalPixels: res.total_pixels || (dimensoes.value.w * dimensoes.value.h)
    }
    keyGrafico.value += 1
  } catch (error) {
    console.error('Erro ao calcular histograma no card:', error)
  } finally {
    carregandoHistograma.value = false
  }
}

function toggleHistograma() {
  if (!imagem.value) return
  exibindoHistograma.value = !exibindoHistograma.value
  if (exibindoHistograma.value) {
    carregarHistograma()
  }
}

function onMouseMove(event: MouseEvent) {
  if (canvas.value && context.value && imageElement.value) {
    const rect = imageElement.value.getBoundingClientRect()
    const natW = imageElement.value.naturalWidth || imageElement.value.width
    const natH = imageElement.value.naturalHeight || imageElement.value.height

    if (rect.width > 0 && rect.height > 0) {
      const scaleX = natW / rect.width
      const scaleY = natH / rect.height

      const posX = Math.min(natW - 1, Math.max(0, Math.floor((event.clientX - rect.left) * scaleX)))
      const posY = Math.min(natH - 1, Math.max(0, Math.floor((event.clientY - rect.top) * scaleY)))

      coordenadas.value.x = posX
      coordenadas.value.y = posY

      try {
        const imgData = context.value.getImageData(posX, posY, 1, 1).data
        const [r, g, b] = imgData
        nivelCinza.value = Math.floor((r + g + b) / 3)
        coordenadasAtivas.value = true
      } catch (e) {
        console.error('Erro na leitura da ponta de prova', e)
      }
    }
  }
}

function onMouseLeave() {
  coordenadasAtivas.value = false
}
</script>

<style scoped>
.LStyleCardWrapper {
  width: 100%;
  display: flex;
}

.LStyleImageCard {
  width: 100%;
  background-color: var(--pdi-bg-card) !important;
  border: 1px solid var(--pdi-border-subtle) !important;
  border-radius: var(--radius-lg);
  box-shadow: var(--pdi-shadow-md);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: var(--pdi-transition-normal);
}

.LStyleImageCard:hover {
  border-color: var(--pdi-border-default) !important;
  box-shadow: var(--pdi-shadow-lg);
}

.LStyleCardHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background-color: #141418;
  border-bottom: 1px solid var(--pdi-border-subtle);
}

.LStyleCardTitle {
  margin: 0;
  font-size: 0.98rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.01em;
  display: inline-flex;
  align-items: center;
}

.LStyleMetaTag {
  display: block;
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--pdi-text-muted);
  letter-spacing: 0.02em;
  margin-left: 28px;
}

.LStyleHistToggleBtn {
  background-color: #1e1e24 !important;
  color: #e4e4e7 !important;
  border: 1px solid var(--pdi-border-default) !important;
  border-radius: var(--radius-sm) !important;
  text-transform: none !important;
  letter-spacing: 0.01em !important;
  font-weight: 600 !important;
  transition: var(--pdi-transition-fast) !important;
}

.LStyleHistToggleBtn:hover:not(:disabled) {
  background-color: #27272e !important;
  color: #ffffff !important;
  border-color: #71717a !important;
}

.LStyleHistToggleBtnActive {
  background-color: #2c2c36 !important;
  color: #ffffff !important;
  border-color: #ffffff !important;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.15) !important;
}

.LStyleHistogramViewport {
  width: 100%;
  min-height: clamp(340px, 48vh, 600px);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #121216;
  border: 1px solid var(--pdi-border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.LStyleHistLoading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 340px;
}

.LStyleHistStatsBar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.LStyleStatChip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background-color: #1c1c22;
  border: 1px solid var(--pdi-border-subtle);
  border-radius: var(--radius-sm);
  font-size: 0.74rem;
  color: #e4e4e7;
}

.LStylePreviewContainer {
  padding: 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.LStyleImageViewport {
  width: 100%;
  min-height: clamp(340px, 48vh, 600px);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at 50% 40%, #151519 0%, #0d0d10 80%);
  border: 1px solid var(--pdi-border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.LStyleUploadedImage {
  max-width: 100%;
  max-height: min(60vh, 640px);
  object-fit: contain;
  cursor: crosshair;
  display: block;
}

.LStyleEmptyState {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 32px 20px;
}

.LStyleEmptyIconBox {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background: #1f1f24;
  border: 1px solid var(--pdi-border-default);
  display: grid;
  place-items: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
}

.LStyleEmptyTitle {
  margin: 0 0 6px;
  font-size: 1.05rem;
  font-weight: 700;
  color: #ffffff;
}

.LStyleEmptySubtitle {
  margin: 0 0 12px;
  font-size: 0.84rem;
  color: var(--pdi-text-muted);
  max-width: 300px;
  line-height: 1.45;
}

.LStyleFormatBadge {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  background: #242429;
  border: 1px solid var(--pdi-border-default);
  color: var(--pdi-text-secondary);
}

/* HUD Ponta de Prova Flutuante */
.LStyleProbeHud {
  position: absolute;
  top: 14px;
  left: 14px;
  display: flex;
  align-items: center;
  background: rgba(14, 14, 18, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-sm);
  padding: 8px 14px;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
  pointer-events: none;
  z-index: 10;
}

.LStyleProbeSwatch {
  width: 22px;
  height: 22px;
  border-radius: 4px;
  border: 1.5px solid #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
  flex-shrink: 0;
}

.LStyleProbeCoords {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--pdi-text-muted);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.LStyleProbeNC {
  font-size: 0.82rem;
  color: #ffffff;
  line-height: 1.2;
}

.LStyleProbeStatus {
  font-size: 0.74rem;
  color: var(--pdi-text-subtle);
  display: flex;
  align-items: center;
}

.LStyleCardActions {
  padding: 14px 18px;
  background-color: #141417;
  border-top: 1px solid var(--pdi-border-subtle);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.LStyleAppliedFiltersBtn {
  background-color: rgba(255, 255, 255, 0.08) !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.18) !important;
  border-radius: var(--radius-sm) !important;
  text-transform: none !important;
  font-weight: 600 !important;
  letter-spacing: 0.01em !important;
  transition: all 0.2s ease !important;
}

.LStyleAppliedFiltersBtn:hover {
  background-color: rgba(255, 255, 255, 0.16) !important;
  border-color: rgba(255, 255, 255, 0.35) !important;
}

.LStyleAppliedFiltersPopover {
  background-color: #151519 !important;
  border: 1px solid #2f2f38 !important;
  border-radius: var(--radius-md) !important;
  max-height: 80vh;
  overflow-y: auto;
}

.LStylePipelineCountBadge {
  font-size: 0.68rem;
  font-weight: 700;
  color: #a1a1aa;
  background-color: #24242c;
  border: 1px solid #363642;
  padding: 2px 8px;
  border-radius: 12px;
}

.LStyleAppliedFilterItem {
  background-color: #1a1a20;
  border: 1px solid #282832;
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.LStyleStepNumberBadge {
  font-size: 0.7rem;
  font-weight: 800;
  color: #000000;
  background-color: #ffffff;
  padding: 1px 6px;
  border-radius: 4px;
}

.LStyleCategoryChip {
  font-size: 0.65rem;
  font-weight: 700;
  color: #a1a1aa;
  background-color: #24242e;
  border: 1px solid #383844;
  padding: 1px 6px;
  border-radius: 10px;
  text-transform: uppercase;
}

.LStyleMiniFormula {
  font-family: 'Fira Code', monospace;
  font-size: 0.74rem;
  color: #ffffff;
  background-color: #0d0d10;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #22222a;
}

.LStyleAppliedFilterDetails {
  background-color: #121216;
  border-top: 1px solid #24242c;
}
</style>

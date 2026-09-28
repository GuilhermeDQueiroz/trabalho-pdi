<template>
  <ToolbarDashboard
    :filtrosCount="filtrosCount"
    @onClickFiltros="onClickFiltros()"
    @onClickGaleria="exibirGaleria = true"
  />

  <main class="LStyleImageWorkspace">
    <!-- Grid de Imagens: Sempre exibe entrada e saída lado a lado -->
    <v-row v-if="showCardImagens" class="LStyleImageGrid">
      <!-- Painel 1: Imagem de Entrada -->
      <v-col :cols="$vuetify.display.mdAndUp ? 6 : 12" class="LStyleImageColumn">
        <CardImage
          :titulo="'Imagem de Entrada'"
          v-model:imagem="imagemEntradaBase64"
          :imagemMatriz="imagemEntradaMatriz"
          :maxWidhtCard="widhtImage"
        >
          <template #actions>
              <v-file-input
                color="primary"
                variant="outlined"
                density="comfortable"
                prepend-icon=""
                append-inner-icon="mdi-tray-arrow-up"
                label="Carregar Imagem de Entrada (PNG, JPG, BMP)"
                accept="image/png, image/jpeg, image/bmp"
                v-model="inputFile"
                @change="onImageEntradaChange($event)"
                @click:clear="onClearImagem()"
                hide-details
                class="LStyleFileInput"
                v-tooltip="'Selecione um arquivo de imagem para iniciar a demonstração'"
              ></v-file-input>

              <div class="mt-2 text-center">
                <v-btn
                  variant="text"
                  size="small"
                  class="LStyleQuickGalleryLink"
                  @click="exibirGaleria = true"
                  v-tooltip="'Abrir galeria com 13 imagens de amostra para testes rápidos'"
                >
                  <v-icon size="small" class="mr-1.5" color="#a1a1aa">mdi-image-multiple-outline</v-icon>
                  <span>Ou escolha da Galeria de Teste (13 amostras)</span>
                </v-btn>
              </div>
            </template>
        </CardImage>
      </v-col>

      <!-- Painel 2: Imagem Resultante -->
      <v-col :cols="$vuetify.display.mdAndUp ? 6 : 12" class="LStyleImageColumn">
        <CardImage
          :maxWidhtCard="widhtImage"
          :titulo="'Imagem Resultante'"
          v-model:imagem="imagemResultadoBase64"
          :imagemMatriz="imagemResultadoMatriz"
        >
          <template #actions>
            <v-btn
              variant="elevated"
              class="LStyleDownloadBtn w-100"
              size="large"
              :disabled="!imagemResultadoBase64"
              v-tooltip="imagemResultadoBase64 ? 'Baixar a imagem resultante em formato PNG' : 'Carregue e processe uma imagem primeiro'"
              @click="onClickBaixarImagem()"
            >
              <v-icon class="mr-2">mdi-download</v-icon>
              Baixar Imagem Resultante (PNG)
            </v-btn>
          </template>
        </CardImage>
      </v-col>
    </v-row>
  </main>

  <!-- Modal do Pipeline de Filtros -->
  <FormFiltros
    v-model:exibirDialog="exibirFiltros"
    :imagemEntrada="imagemEntradaMatriz"
    :imagemEntradaBase64="imagemEntradaBase64"
    v-model:imagem="imagemResultadoMatriz"
    @update:filtrosCount="filtrosCount = $event"
    @onImagemAtualizada="onImagemAtualizada($event)"
  />

  <!-- Botões Flutuantes (FAB - Rotações Geométricas) -->
  <SpeedDial
    @onClickRotacao180="onClickRotacao180()"
    @onClickRotacao90Horario="onClickRotacao90Horario()"
    @onClickRotacao90AntiHorario="onClickRotacao90AntiHorario()"
  />

  <!-- Modal da Galeria para Teste Rápido (13 Amostras BMP) -->
  <GaleriaAmostras
    v-model:exibirDialog="exibirGaleria"
    v-model:amostraAtiva="amostraAtiva"
    @selecionar="onAmostraSelecionada($event)"
  />
</template>

<script setup lang="ts">
// Vue
import { ref, computed } from 'vue'

// Store
import { useLayoutStore } from '@/stores/LayoutStore'
const layout = useLayoutStore()

// Components
import SpeedDial from './components/SpeedDial.vue'
import CardImage from './components/CardImage.vue'
import FormFiltros from './components/FormFiltros.vue'
import ToolbarDashboard from './components/ToolbarDashboard.vue'
import GaleriaAmostras, { type IPayloadAmostra } from './components/GaleriaAmostras.vue'

// Service Python
import { PythonPdiService } from '@/services/PythonPdiService'
import { base64ToMatriz, matrizToBase64 } from '@/utils/imageUtils'

// Propriedades reativas
const inputFile = ref<any>(null)
const amostraAtiva = ref<string | null>(null)
const showCardImagens = ref<boolean>(true)
const exibirFiltros = ref<boolean>(false)
const exibirGaleria = ref<boolean>(false)
const filtrosCount = ref<number>(0)

const imagemEntradaMatriz = ref<number[][]>([])
const imagemResultadoMatriz = ref<number[][]>([])
const imagemEntradaBase64 = ref<string | null>(null)
const imagemResultadoBase64 = ref<string | null>(null)

// Manipula o evento de mudança de imagem
async function onImageEntradaChange(event: Event) {
  onClearImagem()

  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (file) {
    const reader = new FileReader()

    reader.onload = async () => {
      const b64 = reader.result as string
      imagemEntradaBase64.value = b64
      imagemResultadoBase64.value = b64

      // Converte imagem para matriz de pixels
      const mat = await base64ToMatriz(b64 || '')
      imagemEntradaMatriz.value = mat
      imagemResultadoMatriz.value = mat
    }

    reader.readAsDataURL(file)
  } else {
    onClearImagem()
  }

  showCardImagens.value = false
  setTimeout(() => {
    showCardImagens.value = true
  }, 100)
}

function onClickBaixarImagem() {
  if (imagemResultadoBase64.value) {
    const link = document.createElement('a')
    const dataUrl = imagemResultadoBase64.value
    const mimeType = dataUrl.split(';')[0].split(':')[1]
    const byteString = atob(dataUrl.split(',')[1])
    const arrayBuffer = new ArrayBuffer(byteString.length)
    const intArray = new Uint8Array(arrayBuffer)

    for (let i = 0; i < byteString.length; i++) {
      intArray[i] = byteString.charCodeAt(i)
    }

    const blob = new Blob([intArray], { type: mimeType })
    const url = URL.createObjectURL(blob)
    link.href = url
    link.download = 'pdi_resultado_python.png'
    link.click()
    URL.revokeObjectURL(url)
  }
}

function onClearImagem() {
  imagemEntradaBase64.value = null
  imagemResultadoBase64.value = null
  imagemEntradaMatriz.value = []
  imagemResultadoMatriz.value = []
  amostraAtiva.value = null
  inputFile.value = null
}

function onAmostraSelecionada(payload: IPayloadAmostra) {
  imagemEntradaBase64.value = payload.base64
  imagemResultadoBase64.value = payload.base64
  imagemEntradaMatriz.value = payload.matriz
  imagemResultadoMatriz.value = payload.matriz
  inputFile.value = payload.file
  amostraAtiva.value = payload.nome

  showCardImagens.value = false
  setTimeout(() => {
    showCardImagens.value = true
  }, 50)
}

function onClickFiltros() {
  exibirFiltros.value = !exibirFiltros.value
}


async function onImagemAtualizada(dados: any) {
  try {
    if (dados.matriz && dados.base64) {
      imagemResultadoMatriz.value = dados.matriz
      imagemResultadoBase64.value = dados.base64
    } else if (Array.isArray(dados)) {
      imagemResultadoMatriz.value = dados
      imagemResultadoBase64.value = await matrizToBase64(imagemResultadoMatriz.value)
    }
  } catch (error) {
    exibirMensagem('Erro ao atualizar imagem resultante', error)
  }
}

async function onClickRotacao180() {
  if (!imagemResultadoMatriz.value || imagemResultadoMatriz.value.length === 0) {
    exibirMensagem('Aviso', 'Carregue uma imagem antes de rotacionar.')
    return
  }

  try {
    layout.loading.mensagem = 'Rotacionando matriz 180º no Python...'
    await new Promise((resolve) => setTimeout(resolve, 50))

    const res = await PythonPdiService.rotacionar(imagemResultadoMatriz.value, '180')
    imagemResultadoMatriz.value = res.matriz
    imagemResultadoBase64.value = res.imagem_base64
  } catch (error) {
    exibirMensagem('Erro ao rotacionar imagem no Python', error)
  } finally {
    layout.loading.mensagem = ''
  }
}

async function onClickRotacao90Horario() {
  if (!imagemResultadoMatriz.value || imagemResultadoMatriz.value.length === 0) {
    exibirMensagem('Aviso', 'Carregue uma imagem antes de rotacionar.')
    return
  }

  try {
    layout.loading.mensagem = 'Rotacionando matriz 90º Horário no Python...'
    await new Promise((resolve) => setTimeout(resolve, 50))

    const res = await PythonPdiService.rotacionar(imagemResultadoMatriz.value, '90_horario')
    imagemResultadoMatriz.value = res.matriz
    imagemResultadoBase64.value = res.imagem_base64
  } catch (error) {
    exibirMensagem('Erro ao rotacionar imagem no Python', error)
  } finally {
    layout.loading.mensagem = ''
  }
}

async function onClickRotacao90AntiHorario() {
  if (!imagemResultadoMatriz.value || imagemResultadoMatriz.value.length === 0) {
    exibirMensagem('Aviso', 'Carregue uma imagem antes de rotacionar.')
    return
  }

  try {
    layout.loading.mensagem = 'Rotacionando matriz 90º Anti-Horário no Python...'
    await new Promise((resolve) => setTimeout(resolve, 50))

    const res = await PythonPdiService.rotacionar(imagemResultadoMatriz.value, '90_antihorario')
    imagemResultadoMatriz.value = res.matriz
    imagemResultadoBase64.value = res.imagem_base64
  } catch (error) {
    exibirMensagem('Erro ao rotacionar imagem no Python', error)
  } finally {
    layout.loading.mensagem = ''
  }
}


function exibirMensagem(pTitulo: string = 'Erro', pErro: string | any) {
  useLayoutStore().messageDialog.show = true
  useLayoutStore().messageDialog.titulo = pTitulo
  useLayoutStore().messageDialog.mensagem = pErro instanceof Error ? pErro.message : String(pErro)
}

const widhtImage = computed(() => {
  return '100%'
})
</script>

<style scoped>
.LStyleImageWorkspace {
  width: min(100%, var(--workspace-max-width));
  margin: 0 auto;
  padding: var(--space-section) var(--space-page) 4rem;
}

.LStyleWorkspaceIntro {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 24px;
}

.LStyleSectionLabel {
  display: block;
  margin-bottom: 6px;
  color: var(--pdi-text-subtle);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.LStyleMainHeading {
  margin: 0;
  color: #ffffff;
  font-size: clamp(1.4rem, 2.2vw, 1.95rem);
  font-weight: 700;
  letter-spacing: -0.03em;
}

.LStyleWorkspaceDesc {
  max-width: 440px;
  margin: 0;
  color: var(--pdi-text-muted);
  font-size: 0.86rem;
  line-height: 1.5;
  text-align: right;
}

.LStyleImageGrid {
  margin: 0 -12px;
}

.LStyleImageColumn {
  display: flex;
}

.LStyleFileInput {
  background-color: #1a1a20;
  border-radius: var(--radius-sm);
}

.LStyleFileInput :deep(.v-field) {
  background-color: #1a1a20 !important;
}

.LStyleDownloadBtn {
  background-color: var(--pdi-accent-white) !important;
  color: var(--pdi-accent-contrast) !important;
  font-weight: 700 !important;
  border: 1px solid #ffffff !important;
  height: 48px !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: 0 4px 14px rgba(255, 255, 255, 0.12) !important;
  transition: var(--pdi-transition-fast) !important;
}

.LStyleDownloadBtn:hover:not(:disabled) {
  background-color: #e4e4e7 !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(255, 255, 255, 0.22) !important;
}

.LStyleQuickGalleryLink {
  color: var(--pdi-text-muted) !important;
  font-size: 0.76rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.01em !important;
  border-radius: var(--radius-xs) !important;
  padding: 0 8px !important;
  height: 28px !important;
  text-transform: none !important;
}

.LStyleQuickGalleryLink:hover {
  color: #ffffff !important;
  background-color: rgba(255, 255, 255, 0.06) !important;
}

@media (max-width: 960px) {
  .LStyleWorkspaceIntro {
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
  }

  .LStyleWorkspaceDesc {
    text-align: left;
  }
}
</style>

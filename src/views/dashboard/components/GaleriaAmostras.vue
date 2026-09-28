<template>
  <v-dialog
    v-model="exibirDialog"
    :max-width="920"
    transition="dialog-bottom-transition"
    class="LStyleGalleryDialog"
  >
    <v-card class="LStyleGalleryModal">
      <!-- Cabeçalho do Modal -->
      <div class="LStyleGalleryHeader">
        <div class="d-flex align-center">
          <div class="LStyleGalleryIconCircle mr-3">
            <v-icon size="24" color="#ffffff">mdi-image-multiple-outline</v-icon>
          </div>
          <div>
            <div class="d-flex align-center ga-2 flex-wrap">
              <h2 class="LStyleGalleryModalTitle">Galeria para Teste Rápido</h2>
              <span class="LStyleGalleryBadge">{{ amostras.length }} Amostras PDI</span>
              <span v-if="amostraAtivaNome" class="LStyleActiveBadge">
                <v-icon size="12" class="mr-1" color="#ffffff">mdi-check</v-icon>
                {{ amostraAtivaNome }}
              </span>
            </div>
            <p class="LStyleGallerySubtitle mt-1">
              Selecione uma das 13 imagens acadêmicas padrão (256×256 px) para carregar instantaneamente na bancada
            </p>
          </div>
        </div>

        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          class="LStyleCloseBtn"
          v-tooltip="'Fechar galeria'"
          @click="onClickFecharDialog"
        />
      </div>

      <!-- Grid de Miniaturas com Rolagem -->
      <v-card-text class="LStyleGalleryBody">
        <v-row class="g-3">
          <v-col
            v-for="item in amostras"
            :key="item.id"
            :cols="6"
            :sm="4"
            :md="3"
            class="d-flex"
          >
            <div
              class="LStyleSampleCard w-100"
              :class="{ 'LStyleSampleCard--active': amostraAtivaNome === item.nome }"
              @click="onSelecionarAmostra(item)"
              v-tooltip="`Clique para carregar ${item.nome} no workbench`"
            >
              <!-- Container da Imagem com Preview nítido -->
              <div class="LStyleSampleImgContainer">
                <img
                  :src="item.url"
                  :alt="item.nome"
                  class="LStyleSampleImg"
                  loading="lazy"
                />

                <!-- Badge Ativo / Checkmark -->
                <div v-if="amostraAtivaNome === item.nome" class="LStyleSampleActivePill">
                  <v-icon size="12" color="#000000">mdi-check</v-icon>
                  <span>Ativa</span>
                </div>

                <!-- Spinner de Carregamento -->
                <div v-if="carregandoId === item.id" class="LStyleSampleLoadingOverlay">
                  <v-progress-circular indeterminate size="24" width="2" color="#ffffff" />
                </div>
              </div>

              <!-- Informações da Imagem -->
              <div class="LStyleSampleMeta">
                <div class="LStyleSampleName">{{ item.label }}</div>
                <div class="LStyleSampleFile">{{ item.nome }} • 256×256</div>
              </div>

              <!-- Ação de Seleção -->
              <div class="LStyleSampleAction">
                <v-btn
                  size="small"
                  variant="outlined"
                  class="LStyleSelectBtn w-100"
                  :class="{ 'LStyleSelectBtn--active': amostraAtivaNome === item.nome }"
                  @click.stop="onSelecionarAmostra(item)"
                >
                  <v-icon size="small" class="mr-1">
                    {{ amostraAtivaNome === item.nome ? 'mdi-check' : 'mdi-arrow-right' }}
                  </v-icon>
                  {{ amostraAtivaNome === item.nome ? 'Em Uso' : 'Carregar' }}
                </v-btn>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-card-text>

      <!-- Rodapé do Modal -->
      <div class="LStyleGalleryFooter">
        <span class="LStyleFooterHint">
          <v-icon size="14" class="mr-1" color="#a1a1aa">mdi-information-outline</v-icon>
          Imagens clássicas de teste monocromático em escala de cinza (8 bits por pixel)
        </span>
        <v-btn
          variant="outlined"
          class="LStyleCloseFooterBtn"
          @click="onClickFecharDialog"
        >
          Fechar
        </v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { base64ToMatriz } from '@/utils/imageUtils'

interface IAmostra {
  id: string
  nome: string
  label: string
  numero: number
  url: string
}

export interface IPayloadAmostra {
  nome: string
  base64: string
  matriz: number[][]
  file: File
}

const emit = defineEmits<{
  (e: 'selecionar', payload: IPayloadAmostra): void
}>()

const exibirDialog = defineModel<boolean>('exibirDialog', {
  default: false
})

const amostraAtivaNome = defineModel<string | null>('amostraAtiva', {
  default: null
})

const carregandoId = ref<string | null>(null)

// Carrega dinamicamente todas as 13 imagens .bmp da pasta via import.meta.glob
const modulosImagens = import.meta.glob<string>('@/assets/Imagens/*.bmp', {
  eager: true,
  import: 'default'
})

// Mapeia e ordena naturalmente de teste1 a teste13
const amostras = computed<IAmostra[]>(() => {
  const lista: IAmostra[] = []

  for (const [caminho, url] of Object.entries(modulosImagens)) {
    const nomeArquivo = caminho.split('/').pop() || ''
    const match = nomeArquivo.match(/teste(\d+)\.bmp/i)
    const numero = match ? parseInt(match[1], 10) : 999

    lista.push({
      id: nomeArquivo,
      nome: nomeArquivo,
      label: `Teste ${numero}`,
      numero,
      url
    })
  }

  return lista.sort((a, b) => a.numero - b.numero)
})

function onClickFecharDialog() {
  exibirDialog.value = false
}

async function onSelecionarAmostra(item: IAmostra) {
  if (carregandoId.value) return

  try {
    carregandoId.value = item.id

    // 1. Faz o download local via fetch da URL estática resolvida pelo Vite
    const response = await fetch(item.url)
    const blob = await response.blob()

    // 2. Converte para Data URL (Base64)
    const base64 = await new Promise<string>((resolve, reject) => {
      const reader = new FileReader()
      reader.onloadend = () => resolve(reader.result as string)
      reader.onerror = reject
      reader.readAsDataURL(blob)
    })

    // 3. Converte Base64 para matriz numérica 2D para o motor de PDI
    const matriz = await base64ToMatriz(base64)

    // 4. Cria arquivo File compatível com v-file-input
    const file = new File([blob], item.nome, { type: blob.type || 'image/bmp' })

    amostraAtivaNome.value = item.nome

    emit('selecionar', {
      nome: item.nome,
      base64,
      matriz,
      file
    })

    // Fecha o modal automaticamente após selecionar
    exibirDialog.value = false
  } catch (error) {
    console.error('Falha ao processar amostra rápida:', error)
  } finally {
    carregandoId.value = null
  }
}
</script>

<style scoped>
.LStyleGalleryModal {
  background-color: var(--pdi-bg-card) !important;
  border: 1px solid var(--pdi-border-default) !important;
  border-radius: var(--radius-lg) !important;
  box-shadow: var(--pdi-shadow-lg);
  overflow: hidden;
}

.LStyleGalleryHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px;
  background-color: #17171c;
  border-bottom: 1px solid var(--pdi-border-subtle);
}

.LStyleGalleryIconCircle {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-sm);
  background: #242429;
  border: 1px solid var(--pdi-border-default);
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.LStyleGalleryModalTitle {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--pdi-text-primary);
  margin: 0;
  letter-spacing: -0.01em;
}

.LStyleGalleryBadge {
  font-size: 0.7rem;
  font-weight: 600;
  background-color: #202025;
  color: #a1a1aa;
  border: 1px solid var(--pdi-border-subtle);
  padding: 2px 8px;
  border-radius: var(--radius-full);
}

.LStyleActiveBadge {
  display: inline-flex;
  align-items: center;
  font-size: 0.68rem;
  font-weight: 700;
  background-color: #27272a;
  color: #ffffff;
  border: 1px solid #52525b;
  padding: 2px 8px;
  border-radius: var(--radius-full);
}

.LStyleGallerySubtitle {
  font-size: 0.78rem;
  color: var(--pdi-text-muted);
  margin: 0;
}

.LStyleCloseBtn {
  color: var(--pdi-text-muted) !important;
}

.LStyleCloseBtn:hover {
  color: #ffffff !important;
  background-color: rgba(255, 255, 255, 0.08) !important;
}

.LStyleGalleryBody {
  padding: 20px 24px;
  max-height: 560px;
  overflow-y: auto;
  background-color: #121215;
}

.LStyleSampleCard {
  background-color: #18181c;
  border: 1px solid var(--pdi-border-default);
  border-radius: var(--radius-md);
  padding: 10px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.LStyleSampleCard:hover {
  border-color: #71717a;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5), 0 0 12px rgba(255, 255, 255, 0.08);
}

.LStyleSampleCard--active {
  border: 2px solid #ffffff !important;
  background-color: #1f1f25;
  box-shadow: 0 0 16px rgba(255, 255, 255, 0.25);
}

.LStyleSampleImgContainer {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  background-color: #09090b;
  border-radius: var(--radius-sm);
  border: 1px solid var(--pdi-border-subtle);
  overflow: hidden;
  display: grid;
  place-items: center;
}

.LStyleSampleImg {
  width: 100%;
  height: 100%;
  object-fit: cover;
  image-rendering: -webkit-optimize-contrast;
  display: block;
  transition: transform 0.25s ease;
}

.LStyleSampleCard:hover .LStyleSampleImg {
  transform: scale(1.04);
}

.LStyleSampleActivePill {
  position: absolute;
  top: 6px;
  right: 6px;
  background-color: #ffffff;
  color: #000000;
  font-size: 0.65rem;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  gap: 3px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
}

.LStyleSampleLoadingOverlay {
  position: absolute;
  inset: 0;
  background-color: rgba(9, 9, 11, 0.75);
  display: grid;
  place-items: center;
}

.LStyleSampleMeta {
  margin-top: 10px;
  margin-bottom: 8px;
}

.LStyleSampleName {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--pdi-text-primary);
  line-height: 1.2;
}

.LStyleSampleFile {
  font-size: 0.7rem;
  color: var(--pdi-text-subtle);
  margin-top: 2px;
}

.LStyleSelectBtn {
  height: 30px !important;
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  border-color: var(--pdi-border-default) !important;
  color: var(--pdi-text-secondary) !important;
  border-radius: var(--radius-xs) !important;
}

.LStyleSelectBtn:hover {
  background-color: rgba(255, 255, 255, 0.08) !important;
  border-color: #ffffff !important;
  color: #ffffff !important;
}

.LStyleSelectBtn--active {
  background-color: #ffffff !important;
  color: #000000 !important;
  border-color: #ffffff !important;
  font-weight: 800 !important;
}

.LStyleGalleryFooter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
  background-color: #141418;
  border-top: 1px solid var(--pdi-border-subtle);
}

.LStyleFooterHint {
  font-size: 0.75rem;
  color: var(--pdi-text-subtle);
  display: flex;
  align-items: center;
}

.LStyleCloseFooterBtn {
  border-color: var(--pdi-border-default) !important;
  color: var(--pdi-text-secondary) !important;
  height: 36px !important;
  padding: 0 18px !important;
  font-size: 0.82rem !important;
  border-radius: var(--radius-sm) !important;
}

.LStyleCloseFooterBtn:hover {
  background-color: rgba(255, 255, 255, 0.06) !important;
  border-color: var(--pdi-border-hover) !important;
  color: #ffffff !important;
}
</style>

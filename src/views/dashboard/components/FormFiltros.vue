<template>
  <v-dialog
    v-model="exibirDialog"
    :max-width="880"
    transition="dialog-bottom-transition"
    class="LStyleFilterDialog"
  >
    <v-card class="LStyleFilterModal">
      <!-- Cabeçalho do Modal com Título e Fechamento -->
      <div class="LStyleFilterHeader">
        <div class="d-flex align-center">
          <v-icon class="mr-3" size="26" color="#ffffff">mdi-tune-vertical</v-icon>
          <div>
            <h2 class="LStyleModalTitle">Filtros</h2>
            <span class="LStyleModalSubtitle mt-1">
              Monte e ordene os filtros
            </span>
          </div>
        </div>

        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          class="LStyleCloseBtn"
          v-tooltip="'Fechar modal de filtros'"
          @click="onClickFecharDialog"
        />
      </div>

      <!-- Barra de Ação Rápida: Seleção + Adicionar -->
      <div class="LStyleAddToolbar">
        <v-row class="align-center g-3">
          <v-col :cols="12" :sm="8">
            <v-autocomplete
              density="comfortable"
              variant="outlined"
              item-title="texto"
              item-value="valor"
              :return-object="true"
              :items="opcoesFiltros"
              label="Selecionar Função / Filtro PDI"
              prepend-inner-icon="mdi-filter-variant"
              v-model="filtroSelecionado"
              hide-details
              class="LStyleAutoComplete"
            >
              <template #item="{ props: itemProps, item }">
                <v-list-item
                  v-bind="itemProps"
                  :title="item.raw.texto"
                  :class="{ 'LStyleItemAlreadyAdded': filtros.some(f => f.tipo === item.raw.valor) }"
                >
                  <template #prepend>
                    <v-icon
                      size="small"
                      class="mr-2"
                      :color="filtros.some(f => f.tipo === item.raw.valor) ? '#71717a' : '#a1a1aa'"
                    >
                      mdi-function-variant
                    </v-icon>
                  </template>
                  <template #append v-if="filtros.some(f => f.tipo === item.raw.valor)">
                    <div class="d-flex align-center gap-1">
                      <span class="LStyleAlreadyTag mr-1">Na fila</span>
                      <v-btn
                        size="x-small"
                        variant="tonal"
                        color="error"
                        class="LStyleRemoveFromListBtn"
                        @click.stop.prevent="onRemoverFiltroPorTipo(item.raw.valor)"
                        v-tooltip="'Remover este filtro da fila de execução'"
                      >
                        <v-icon size="14" class="mr-1">mdi-trash-can-outline</v-icon>
                        <span>Excluir</span>
                      </v-btn>
                    </div>
                  </template>
                </v-list-item>
              </template>
            </v-autocomplete>
          </v-col>

          <v-col :cols="12" :sm="4">
            <v-btn
              class="LStyleAddBtn"
              :class="{ 'LStyleAddBtn--already': filtroJaAdicionado }"
              variant="elevated"
              :disabled="!filtroSelecionado || filtroJaAdicionado"
              @click="onClickAdicionarFiltro"
              v-tooltip="
                filtroJaAdicionado
                  ? 'Este filtro já foi adicionado à fila de processamento'
                  : !filtroSelecionado
                  ? 'Selecione um filtro no menu ao lado'
                  : 'Inserir este filtro no final da fila'
              "
            >
              <v-icon class="mr-1.5" size="small">{{ filtroJaAdicionado ? 'mdi-check' : 'mdi-plus' }}</v-icon>
              {{ filtroJaAdicionado ? 'Já na Fila' : 'Adicionar à Fila' }}
            </v-btn>
          </v-col>
        </v-row>

        <!-- Painel Informativo Dinâmico do Filtro Selecionado -->
        <transition name="fade">
          <div v-if="filtroSelecionadoInfo" class="LStyleFilterExplainerBox mt-3 pa-3">
            <div class="d-flex align-center justify-space-between mb-1.5 flex-wrap ga-2">
              <div class="d-flex align-center ga-1.5">
                <v-icon size="16" color="#ffffff">mdi-information-outline</v-icon>
                <strong class="text-caption font-weight-bold" style="color: #ffffff">{{ filtroSelecionadoInfo.titulo }}</strong>
                <span class="LStyleCategoryChip">{{ filtroSelecionadoInfo.categoria }}</span>
              </div>
              <code class="LStyleFormulaSnippet">{{ filtroSelecionadoInfo.formula }}</code>
            </div>
            <p class="text-caption mb-1" style="color: #e4e4e7">
              <strong style="color: #a1a1aa">O que aplica na imagem:</strong> {{ filtroSelecionadoInfo.oQueAplica }}
            </p>
            <p class="text-caption mb-0" style="color: #a1a1aa">
              <strong style="color: #71717a">Como aplica (Matemática):</strong> {{ filtroSelecionadoInfo.comoAplica }}
            </p>
          </div>
        </transition>
      </div>

      <!-- Indicador Visual do Fluxo do Pipeline (4 Passos) -->
      <div class="LStyleFilterStepsBar">
        <div class="LStyleStep mr-2" :class="{ 'LStyleStep--active': !filtroSelecionado }">
          <span class="LStyleStepNum mr-1">1</span>
          <span>Selecionar</span>
        </div>
        <v-icon size="x-small" color="#52525b" class="mr-2">mdi-chevron-right</v-icon>
        <div class="LStyleStep mr-2" :class="{ 'LStyleStep--active': filtroSelecionado && filtros.length === 0 }">
          <span class="LStyleStepNum mr-1">2</span>
          <span>Adicionar</span>
        </div>
        <v-icon size="x-small" color="#52525b" class="mr-2">mdi-chevron-right</v-icon>
        <div class="LStyleStep mr-2" :class="{ 'LStyleStep--active': filtros.length > 1 }">
          <span class="LStyleStepNum mr-1">3</span>
          <span>Ordenar (Drag)</span>
        </div>
        <v-icon size="x-small" color="#52525b" class="mr-2">mdi-chevron-right</v-icon>
        <div class="LStyleStep" :class="{ 'LStyleStep--active': filtros.length > 0 }">
          <span class="LStyleStepNum mr-1">4</span>
          <span>Aplicar</span>
        </div>
      </div>

      <!-- Conteúdo Rolável da Fila de Filtros -->
      <v-card-text class="LStyleModalBody">
        <div class="LStyleScrollableContent">
          <div v-if="filtros.length > 0" class="LStyleQueueHeader mb-3">
            <div class="d-flex align-center">
              <v-icon size="small" color="#a1a1aa" class="mr-1">mdi-drag-vertical</v-icon>
              <span class="LStyleQueueTitle">Fila de Execução ({{ filtros.length }} {{ filtros.length === 1 ? 'filtro' : 'filtros' }})</span>
            </div>
            <span class="LStyleQueueHint">Arraste os cards para reorganizar a ordem de aplicação</span>
          </div>

          <v-row justify="center">
            <v-col v-if="filtros.length > 0" :cols="12">
              <VueDraggable v-model="filtros" :animation="150" handle=".LStyleDragHandle">
                <div v-for="(filtro, index) in filtros" :key="filtro.tipo || index" class="mb-2">
                  <InputGenerico
                    :index="index"
                    :ordem="index + 1"
                    :tipo="filtro.tipo"
                    :titulo="filtro.titulo"
                    v-model:params="filtro.params"
                    :subtitulo="filtro.subtitulo"
                    @onDelete="onDeleteFiltro(index)"
                  />
                </div>
              </VueDraggable>
            </v-col>

            <!-- Estado Vazio da Fila -->
            <v-col v-else :cols="12">
              <div class="LStyleEmptyQueue">
                <div class="LStyleEmptyIconCircle mb-3">
                  <v-icon size="32" color="#a1a1aa">mdi-filter-variant-remove</v-icon>
                </div>
                <h4 class="LStyleEmptyQueueTitle">Nenhum filtro selecionado</h4>
                <p class="LStyleEmptyQueueDesc">
                  Selecione um dos 18 filtros no seletor acima e clique em <strong>"Adicionar"</strong>
                </p>
              </div>
            </v-col>
          </v-row>
        </div>
      </v-card-text>

      <!-- Rodapé Fixo com Ações -->
      <div class="LStyleStickyFooter">
        <div class="d-flex align-center">
          <v-btn
            variant="outlined"
            class="LStyleSecondaryBtn mr-2"
            v-tooltip="'Fechar modal sem aplicar alterações'"
            @click="onClickFecharDialog"
          >
            Cancelar
          </v-btn>
          
          <v-btn
            v-if="filtros.length > 0"
            variant="text"
            class="LStyleClearBtn"
            v-tooltip="'Esvaziar todos os filtros da fila'"
            @click="onLimparFiltros"
          >
            <v-icon class="mr-1" size="small">mdi-delete-sweep-outline</v-icon>
            Limpar Fila
          </v-btn>
        </div>

        <v-btn
          class="LStyleApplyBtn"
          variant="elevated"
          v-tooltip="filtros.length === 0 ? 'Restaurar a imagem original de entrada' : 'Processar a imagem no motor Python com a fila de filtros'"
          @click="onAplicarFiltros"
        >
          <v-icon class="mr-1.5" size="small">{{ filtros.length === 0 ? 'mdi-restore' : 'mdi-check-all' }}</v-icon>
          <span>{{ filtros.length === 0 ? 'Salvar (Restaurar Original)' : 'Aplicar' }}</span>
        </v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
// Vue
import { ref, watch, computed } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'

const emit = defineEmits(['onImagemAtualizada', 'update:filtrosCount'])

// Store
import { useLayoutStore } from '@/stores/LayoutStore'

// Enums
import { ETipoFiltroPDI } from '@/enums/ETipoFiltroPDI'

// Types
import type IFiltroFormFiltro from './types/IFiltroFormFiltro'

// Service Python
import { PythonPdiService } from '@/services/PythonPdiService'

// Components
import InputGenerico from './InputGenerico.vue'

// Utilitários de Explicação de Filtros
import { obterInfoFiltro } from '@/utils/pdiInfoFiltros'

// Propriedades reativas
const ordem = ref<number>(0)
const filtros = ref<IFiltroFormFiltro[]>([])

const filtroSelecionadoInfo = computed(() => {
  if (!filtroSelecionado.value || !filtroSelecionado.value.valor) return null
  return obterInfoFiltro(filtroSelecionado.value.valor)
})

watch(
  () => filtros.value.length,
  (newCount) => {
    emit('update:filtrosCount', newCount)
  },
  { immediate: true }
)

const opcoesFiltros = ref<{ texto: string; valor: number }[]>([
  { texto: 'Filtro Negativo', valor: ETipoFiltroPDI.NEGATIVO },
  { texto: 'Filtro de Logaritmo (Unidade 3)', valor: ETipoFiltroPDI.LOGARITIMO },
  { texto: 'Filtro de Logaritmo Inverso (Unidade 3)', valor: ETipoFiltroPDI.LOGARITIMO_INVERSO },
  { texto: 'Filtro de Potência / Gamma (Unidade 3)', valor: ETipoFiltroPDI.POTENCIA },
  { texto: 'Filtro de Raiz / Gamma Inverso (Unidade 3)', valor: ETipoFiltroPDI.RAIZ },
  { texto: 'Ampliação Replicação 512x512 (Nearest Neighbor)', valor: ETipoFiltroPDI.AMPLIACAO_REPLICACAO_512X512 },
  { texto: 'Ampliação Replicação 1024x1024 (Nearest Neighbor)', valor: ETipoFiltroPDI.AMPLIACAO_REPLICACAO_1024X1024 },
  { texto: 'Ampliação Bilinear 512x512 (Bilinear Interpolation)', valor: ETipoFiltroPDI.AMPLIACAO_BILINEAR_512X512 },
  { texto: 'Ampliação Bilinear 1024x1024 (Bilinear Interpolation)', valor: ETipoFiltroPDI.AMPLIACAO_BILINEAR_1024X1024 },
  { texto: 'Equalização de Histograma (Unidade 3)', valor: ETipoFiltroPDI.EQUALIZACAO },
  { texto: 'Espelhamento Horizontal', valor: ETipoFiltroPDI.ESPELHAMENTO_HORIZONTAL },
  { texto: 'Espelhamento Vertical', valor: ETipoFiltroPDI.ESPELHAMENTO_VERTICAL },
  { texto: 'Filtro de Expansão (g = a*r + b)', valor: ETipoFiltroPDI.EXPANSAO },
  { texto: 'Filtro de Compressão (g = r / a - b)', valor: ETipoFiltroPDI.COMPRESSAO },
  { texto: 'Somar Duas Imagens com Porcentagem', valor: ETipoFiltroPDI.SOMAR_IMAGENS },
  { texto: 'Filtro da Média (Passa-Baixa)', valor: ETipoFiltroPDI.MEDIA },
  { texto: 'Filtro da Mediana (Ordem)', valor: ETipoFiltroPDI.MEDIANA },
  { texto: 'Filtro da Moda (Frequência)', valor: ETipoFiltroPDI.MODA },
  { texto: 'Filtro MÍNIMO (Erosão)', valor: ETipoFiltroPDI.MINIMO },
  { texto: 'Filtro MÁXIMO (Dilatação)', valor: ETipoFiltroPDI.MAXIMO },
  { texto: 'Operador Laplaciano (Segunda Derivada)', valor: ETipoFiltroPDI.LAPLACIANO },
  { texto: 'Operador High Boost (Nitidez A)', valor: ETipoFiltroPDI.HIGH_BOOST },
  { texto: 'Operador Prewitt (Gradiente)', valor: ETipoFiltroPDI.PREWITT },
  { texto: 'Operador Sobel (Gradiente Ponderado)', valor: ETipoFiltroPDI.SOBEL }
])

interface PropTypes {
  imagemEntrada?: number[][]
  imagemEntradaBase64?: string | null
}

const props = withDefaults(defineProps<PropTypes>(), {
  imagemEntrada: () => [],
  imagemEntradaBase64: null
})

const exibirDialog = defineModel('exibirDialog', {
  default: false
})

const filtroSelecionado = defineModel<{ texto: string; valor: number } | null>(
  'filtroSelecionado',
  {
    default: null
  }
)

const imagem = defineModel<any>('imagem', {
  default: []
})

function onDeleteFiltro(pIndex: number) {
  if (pIndex >= 0 && pIndex < filtros.value.length) {
    filtros.value.splice(pIndex, 1)
  }
}

function onRemoverFiltroPorTipo(pTipo: number) {
  const idx = filtros.value.findIndex((f) => f.tipo === pTipo)
  if (idx !== -1) {
    filtros.value.splice(idx, 1)
  }
}

function onLimparFiltros() {
  filtros.value = []
}

const filtroJaAdicionado = computed(() => {
  if (!filtroSelecionado.value || !filtroSelecionado.value.valor) return false
  return filtros.value.some((f) => f.tipo === filtroSelecionado.value?.valor)
})

function onClickFecharDialog() {
  exibirDialog.value = false
}

function onClickAdicionarFiltro() {
  try {
    if (!filtroSelecionado.value || filtroSelecionado.value.valor === 0) {
      return
    }

    const tipo = filtroSelecionado.value.valor

    // Impede a adição duplicada de um mesmo filtro
    const jaExiste = filtros.value.some((f) => f.tipo === tipo)
    if (jaExiste) {
      exibirMensagem(
        'Filtro Já Adicionado',
        `O filtro "${filtroSelecionado.value.texto}" já está presente na fila de execução. Cada filtro só pode ser aplicado uma vez no pipeline.`
      )
      return
    }

    let params: Record<string, any> = {}

    switch (tipo) {
      case ETipoFiltroPDI.POTENCIA:
        params = { gamma: 2.0 }
        break
      case ETipoFiltroPDI.RAIZ:
        params = { gamma: 2.0 }
        break
      case ETipoFiltroPDI.EXPANSAO:
        params = { a: 1.2, b: 10 }
        break
      case ETipoFiltroPDI.COMPRESSAO:
        params = { a: 1.5, b: 5 }
        break
      case ETipoFiltroPDI.SOMAR_IMAGENS:
        params = { imagem: '', porcentagemImagem1: 50 }
        break
      case ETipoFiltroPDI.MEDIA:
      case ETipoFiltroPDI.MEDIANA:
      case ETipoFiltroPDI.MODA:
      case ETipoFiltroPDI.MINIMO:
      case ETipoFiltroPDI.MAXIMO:
      case ETipoFiltroPDI.LAPLACIANO:
        params = { tamanhoMascara: 3 }
        break
      case ETipoFiltroPDI.HIGH_BOOST:
        params = { tamanhoMascara: 3, ampliacao: 1.5 }
        break
      default:
        params = {}
        break
    }

    const novoFiltro: IFiltroFormFiltro = {
      ordem: ordem.value++,
      subtitulo: '',
      params,
      tipo,
      titulo: filtroSelecionado.value.texto
    }

    filtros.value.push(novoFiltro)

    // Reseta a seleção para conveniência
    filtroSelecionado.value = null
  } catch (error) {
    console.error(error)
    exibirMensagem('Erro ao adicionar filtro', error)
  }
}

async function onAplicarFiltros() {
  try {
    if (filtros.value.length === 0) {
      if (props.imagemEntrada && props.imagemEntrada.length > 0) {
        useLayoutStore().loading.mensagem = 'Restaurando imagem original de entrada...'
        await new Promise((resolve) => setTimeout(resolve, 50))

        emit('onImagemAtualizada', {
          matriz: props.imagemEntrada,
          base64: props.imagemEntradaBase64,
          restauradoOriginal: true,
          filtrosAplicados: []
        })
      }
      exibirDialog.value = false
      return
    }

    const imagemBase = (props.imagemEntrada && props.imagemEntrada.length > 0)
      ? props.imagemEntrada
      : imagem.value

    if (!imagemBase || imagemBase.length === 0) {
      exibirMensagem('Erro ao aplicar filtros!', 'Nenhuma imagem foi carregada.')
      return
    }

    useLayoutStore().loading.mensagem = 'Processando pipeline de filtros no Python puro...'
    exibirDialog.value = false

    await new Promise((resolve) => setTimeout(resolve, 50))

    const filtrosOrdenados = filtros.value.sort((a, b) => a.ordem - b.ordem)
    const payloadFiltros = filtrosOrdenados.map((f) => ({
      tipo: f.tipo,
      params: f.params
    }))

    const resposta = await PythonPdiService.processar(imagemBase, payloadFiltros)

    emit('onImagemAtualizada', {
      matriz: resposta.matriz,
      base64: resposta.imagem_base64,
      histograma: resposta.histograma,
      filtrosAplicados: filtrosOrdenados.map((f) => ({
        tipo: f.tipo,
        titulo: f.titulo,
        params: f.params
      }))
    })
  } catch (error) {
    console.error('Erro na execução do backend Python:', error)
    exibirMensagem('Erro ao aplicar filtros no Python!', error)
  } finally {
    useLayoutStore().loading.mensagem = ''
  }
}

function exibirMensagem(pTitulo: string = 'Erro', pErro: string | any) {
  useLayoutStore().messageDialog.show = true
  useLayoutStore().messageDialog.titulo = pTitulo
  useLayoutStore().messageDialog.mensagem = pErro instanceof Error ? pErro.message : String(pErro)
  useLayoutStore().messageDialog.tipo = pTitulo.toLowerCase().includes('aviso') ? 'alert' : 'error'
}
</script>

<style scoped>
.LStyleFilterModal {
  background-color: var(--pdi-bg-card) !important;
  border: 1px solid var(--pdi-border-default) !important;
  border-radius: var(--radius-lg);
  box-shadow: var(--pdi-shadow-lg);
  overflow: hidden;
}

.LStyleFilterHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 16px;
  background-color: #141418;
  border-bottom: 1px solid var(--pdi-border-subtle);
}

.LStyleModalTitle {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.01em;
  line-height: 1.2;
}

.LStyleModalSubtitle {
  display: block;
  font-size: 0.78rem;
  color: var(--pdi-text-muted);
}

.LStyleCloseBtn {
  color: var(--pdi-text-muted) !important;
}

.LStyleCloseBtn:hover {
  color: #ffffff !important;
  background-color: rgba(255, 255, 255, 0.08) !important;
}

.LStyleAddToolbar {
  padding: 16px 24px;
  background-color: #17171c;
  border-bottom: 1px solid var(--pdi-border-subtle);
}

.LStyleAutoComplete {
  font-size: 0.86rem;
}

.LStyleAutoComplete :deep(.v-field) {
  background-color: #1f1f25 !important;
}

.LStyleAddBtn {
  background-color: #2b2b32 !important;
  color: #ffffff !important;
  border: 1px solid var(--pdi-border-default) !important;
  font-weight: 700 !important;
  font-size: 0.86rem !important;
  width: 100%;
  height: 44px !important;
  border-radius: var(--radius-sm) !important;
}

.LStyleAddBtn:hover:not(:disabled) {
  background-color: #3b3b45 !important;
  border-color: var(--pdi-border-hover) !important;
}

.LStyleFilterStepsBar {
  display: flex;
  align-items: center;
  padding: 10px 24px;
  background-color: #111114;
  border-bottom: 1px solid var(--pdi-border-subtle);
  overflow-x: auto;
}

.LStyleStep {
  display: flex;
  align-items: center;
  font-size: 0.74rem;
  font-weight: 600;
  color: var(--pdi-text-subtle);
}

.LStyleStep--active {
  color: #ffffff;
}

.LStyleStepNum {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #242429;
  border: 1px solid var(--pdi-border-subtle);
  display: grid;
  place-items: center;
  font-size: 0.65rem;
}

.LStyleStep--active .LStyleStepNum {
  background: #ffffff;
  color: #000000;
  border-color: #ffffff;
  font-weight: 800;
}

.LStyleModalBody {
  padding: 18px 24px;
}

.LStyleScrollableContent {
  min-height: 260px;
  max-height: 480px;
  overflow-y: auto;
  padding-right: 4px;
}

.LStyleQueueHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--pdi-border-subtle);
}

.LStyleQueueTitle {
  font-size: 0.84rem;
  font-weight: 700;
  color: var(--pdi-text-secondary);
}

.LStyleQueueHint {
  font-size: 0.72rem;
  color: var(--pdi-text-subtle);
}

.LStyleEmptyQueue {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 42px 20px;
  border: 1px dashed var(--pdi-border-default);
  border-radius: var(--radius-md);
  background-color: rgba(24, 24, 28, 0.4);
}

.LStyleEmptyIconCircle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #1f1f25;
  border: 1px solid var(--pdi-border-default);
  display: grid;
  place-items: center;
}

.LStyleEmptyQueueTitle {
  margin: 0 0 6px;
  font-size: 0.95rem;
  font-weight: 700;
  color: #e4e4e7;
}

.LStyleEmptyQueueDesc {
  margin: 0;
  font-size: 0.8rem;
  color: var(--pdi-text-muted);
  max-width: 380px;
  line-height: 1.5;
}

.LStyleStickyFooter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
  background-color: #141418;
  border-top: 1px solid var(--pdi-border-subtle);
}

.LStyleSecondaryBtn {
  border-color: var(--pdi-border-default) !important;
  color: var(--pdi-text-secondary) !important;
}

.LStyleClearBtn {
  color: #a1a1aa !important;
  font-size: 0.82rem !important;
}

.LStyleClearBtn:hover {
  color: #f87171 !important;
  background-color: rgba(248, 113, 113, 0.12) !important;
}

.LStyleApplyBtn {
  background-color: var(--pdi-accent-white) !important;
  color: var(--pdi-accent-contrast) !important;
  font-weight: 700 !important;
  font-size: 0.88rem !important;
  box-shadow: 0 4px 14px rgba(255, 255, 255, 0.15) !important;
  height: 42px !important;
  padding: 0 20px !important;
}

.LStyleApplyBtn:hover {
  background-color: #e4e4e7 !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(255, 255, 255, 0.25) !important;
}

.LStyleItemAlreadyAdded {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
}

.LStyleAlreadyTag {
  font-size: 0.65rem;
  font-weight: 700;
  color: #71717a;
  background-color: #242429;
  border: 1px solid var(--pdi-border-subtle);
  padding: 1px 6px;
  border-radius: var(--radius-xs);
  letter-spacing: 0.02em;
}

.LStyleRemoveFromListBtn {
  font-weight: 600 !important;
  font-size: 0.7rem !important;
  letter-spacing: 0.02em !important;
  text-transform: none !important;
  border-radius: var(--radius-xs) !important;
  height: 24px !important;
  padding: 0 8px !important;
  color: #fca5a5 !important;
  background-color: rgba(239, 68, 68, 0.16) !important;
  border: 1px solid rgba(239, 68, 68, 0.4) !important;
  cursor: pointer !important;
  pointer-events: auto !important;
  transition: var(--pdi-transition-fast) !important;
}

.LStyleRemoveFromListBtn:hover {
  background-color: #dc2626 !important;
  border-color: #ef4444 !important;
  color: #ffffff !important;
}

.LStyleAddBtn--already {
  background-color: #1f1f25 !important;
  color: #71717a !important;
  border: 1px solid #323238 !important;
  box-shadow: none !important;
}

.LStyleFilterExplainerBox {
  background-color: #121216;
  border: 1px solid #2f2f38;
  border-radius: var(--radius-sm);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
  animation: fadeIn 0.2s ease;
}

.LStyleCategoryChip {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #a1a1aa;
  background-color: #202027;
  border: 1px solid #383842;
  padding: 1px 7px;
  border-radius: 10px;
}

.LStyleFormulaSnippet {
  background-color: #0b0b0e;
  border: 1px solid #24242c;
  color: #ffffff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.78rem;
  font-family: 'Fira Code', monospace;
}
</style>

<template>
  <v-dialog v-if="show" @click:outside="setFocus" v-model="show" persistent :max-width="maxWidth">
    <v-card class="LStyleMessageCard" elevation="0">
      <div class="LStyleMessageHeader">
        <v-btn
          v-if="showCloseButton"
          class="LStyleMessageClose"
          variant="text"
          size="small"
          icon="mdi-close"
          v-tooltip="'Fechar aviso'"
          @click="evClickCloseButton"
          @focusin="$event.stopPropagation()"
        />
        <div :class="['LStyleMessageIconWrapper', `is-${props.type}`]">
          <!-- Ícone Colorido para Erro -->
          <svg v-if="props.type === 'error'" width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="errBgGrad" x1="10" y1="6" x2="42" y2="46" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#FF5252" />
                <stop offset="60%" stop-color="#E53935" />
                <stop offset="100%" stop-color="#B71C1C" />
              </linearGradient>
              <linearGradient id="errStrokeGrad" x1="26" y1="2" x2="26" y2="50" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#FFA39E" />
                <stop offset="100%" stop-color="#CF1322" />
              </linearGradient>
            </defs>
            <circle cx="26" cy="26" r="23" fill="url(#errBgGrad)" />
            <circle cx="26" cy="26" r="23" stroke="url(#errStrokeGrad)" stroke-width="1.8" />
            <path d="M18 18L34 34M34 18L18 34" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
          </svg>

          <!-- Ícone Colorido para Alerta / Aviso -->
          <svg v-else-if="props.type === 'alert'" width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="alertBgGrad" x1="10" y1="6" x2="42" y2="46" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#FBBF24" />
                <stop offset="60%" stop-color="#F59E0B" />
                <stop offset="100%" stop-color="#D97706" />
              </linearGradient>
              <linearGradient id="alertStrokeGrad" x1="26" y1="2" x2="26" y2="50" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#FDE68A" />
                <stop offset="100%" stop-color="#B45309" />
              </linearGradient>
            </defs>
            <circle cx="26" cy="26" r="23" fill="url(#alertBgGrad)" />
            <circle cx="26" cy="26" r="23" stroke="url(#alertStrokeGrad)" stroke-width="1.8" />
            <path d="M26 15V27M26 34V35" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" />
          </svg>

          <!-- Ícone Colorido para Sucesso -->
          <svg v-else-if="props.type === 'success'" width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="succBgGrad" x1="10" y1="6" x2="42" y2="46" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#34D399" />
                <stop offset="60%" stop-color="#10B981" />
                <stop offset="100%" stop-color="#059669" />
              </linearGradient>
              <linearGradient id="succStrokeGrad" x1="26" y1="2" x2="26" y2="50" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#A7F3D0" />
                <stop offset="100%" stop-color="#047857" />
              </linearGradient>
            </defs>
            <circle cx="26" cy="26" r="23" fill="url(#succBgGrad)" />
            <circle cx="26" cy="26" r="23" stroke="url(#succStrokeGrad)" stroke-width="1.8" />
            <path d="M16 26.5L23 33.5L36 19.5" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" />
          </svg>

          <!-- Ícone Colorido para Info -->
          <svg v-else-if="props.type === 'info'" width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="infoBgGrad" x1="10" y1="6" x2="42" y2="46" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#60A5FA" />
                <stop offset="60%" stop-color="#3B82F6" />
                <stop offset="100%" stop-color="#2563EB" />
              </linearGradient>
              <linearGradient id="infoStrokeGrad" x1="26" y1="2" x2="26" y2="50" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#BFDBFE" />
                <stop offset="100%" stop-color="#1D4ED8" />
              </linearGradient>
            </defs>
            <circle cx="26" cy="26" r="23" fill="url(#infoBgGrad)" />
            <circle cx="26" cy="26" r="23" stroke="url(#infoStrokeGrad)" stroke-width="1.8" />
            <path d="M26 17V18M26 24V35" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" />
          </svg>

          <!-- Ícone Colorido para Pergunta -->
          <svg v-else-if="props.type === 'question'" width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="questBgGrad" x1="10" y1="6" x2="42" y2="46" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#A78BFA" />
                <stop offset="60%" stop-color="#8B5CF6" />
                <stop offset="100%" stop-color="#6D28D9" />
              </linearGradient>
              <linearGradient id="questStrokeGrad" x1="26" y1="2" x2="26" y2="50" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#DDD6FE" />
                <stop offset="100%" stop-color="#5B21B6" />
              </linearGradient>
            </defs>
            <circle cx="26" cy="26" r="23" fill="url(#questBgGrad)" />
            <circle cx="26" cy="26" r="23" stroke="url(#questStrokeGrad)" stroke-width="1.8" />
            <path d="M21 21C21 18.2386 23.2386 16 26 16C28.7614 16 31 18.2386 31 21C31 23.0769 29.5 24.5 27.5 25.5C26.5 26 26 27 26 28.5V30M26 35V36" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" />
          </svg>

          <!-- Fallback genérico -->
          <v-icon v-else size="40" :color="iconColor">{{ iconTitle }}</v-icon>
        </div>
      </div>

      <v-card-text class="text-center px-6 py-4">
        <h3 class="LStyleMessageTitle">{{ title }}</h3>
        <div
          v-if="Boolean(treatedMessage)"
          class="LStyleMessageContent mt-2"
          v-html="treatedMessage"
        ></div>
      </v-card-text>

      <v-card-actions class="LStyleMessageActions px-6 pb-5 pt-2">
        <v-spacer />
        <v-btn
          v-if="showCancelBtn"
          variant="outlined"
          ref="cancelButtonRef"
          class="LStyleDialogCancelBtn mr-2"
          @click="choose(false)"
          @focusin="$event.stopPropagation()"
        >
          {{ appliedCancelLabel }}
        </v-btn>
        <v-btn
          variant="elevated"
          ref="okButtonRef"
          class="LStyleDialogOkBtn"
          @click="choose(true)"
          @focusin="$event.stopPropagation()"
        >
          {{ appliedOkLabel }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, type Ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = withDefaults(
  defineProps<{
    type: 'info' | 'success' | 'alert' | 'error' | 'question'
    question?: boolean
    extended?: boolean
    message?: string
    title?: string
    okLabel?: string
    cancelLabel?: string
    okCallback?: () => void
    cancelCallback?: () => void
    escEnabled?: boolean
    focusType?: 'none' | 'ok' | 'cancel'
    elementFocus?: HTMLElement | null
    elementFocusOK?: HTMLElement | null
    elementFocusCancel?: HTMLElement | null
    showCloseButton?: boolean
  }>(),
  {
    question: false,
    extended: false,
    message: '',
    title: '',
    okLabel: '',
    cancelLabel: '',
    okCallback: () => {},
    cancelCallback: () => {},
    escEnabled: true,
    elementFocus: null,
    elementFocusOK: null,
    elementFocusCancel: null,
    showCloseButton: false
  }
)

const maxWidth = computed(() => {
  if (props.message.length <= 80) return '380px'
  return '520px'
})

const treatedMessage = computed(() => {
  return props.message.replace(/[\r\n|\r|\n]/g, '<br>')
})

const okButtonRef: Ref<any> = ref()
const cancelButtonRef: Ref<any> = ref()

const show = ref(false)
const iconTitle = ref('')
const showCancelBtn = ref(false)
const appliedOkLabel = ref('')
const appliedCancelLabel = ref('')

const iconColor = computed(() => {
  switch (props.type) {
    case 'error':
      return '#ef4444'
    case 'alert':
      return '#f59e0b'
    case 'success':
      return '#10b981'
    case 'info':
      return '#3b82f6'
    case 'question':
      return '#8b5cf6'
    default:
      return '#ffffff'
  }
})

watch(show, (newValue) => {
  if (newValue) {
    nextTick(() => {
      setFocus()
    })
    return
  }

  document.dispatchEvent(new CustomEvent('afterClose'))
})

function setTypeConfig(type: string) {
  switch (type) {
    case 'info':
      iconTitle.value = 'mdi-information-outline'
      showCancelBtn.value = false
      appliedOkLabel.value = props.okLabel ? props.okLabel : 'Entendido'
      break
    case 'success':
      iconTitle.value = 'mdi-check-circle-outline'
      showCancelBtn.value = props.question
      appliedCancelLabel.value = props.cancelLabel ? props.cancelLabel : 'Não'
      appliedOkLabel.value = props.okLabel ? props.okLabel : (props.question ? 'Sim' : 'Concluir')
      break
    case 'alert':
      iconTitle.value = 'mdi-alert-circle-outline'
      showCancelBtn.value = props.question
      appliedCancelLabel.value = props.cancelLabel ? props.cancelLabel : 'Cancelar'
      appliedOkLabel.value = props.okLabel ? props.okLabel : (props.question ? 'Sim' : 'OK')
      break
    case 'error':
      iconTitle.value = 'mdi-alert-octagon-outline'
      showCancelBtn.value = props.question
      appliedCancelLabel.value = props.cancelLabel ? props.cancelLabel : 'Fechar'
      appliedOkLabel.value = props.okLabel ? props.okLabel : 'OK'
      break
    case 'question':
      iconTitle.value = 'mdi-help-circle-outline'
      showCancelBtn.value = true
      appliedOkLabel.value = props.okLabel ? props.okLabel : 'Sim'
      appliedCancelLabel.value = props.cancelLabel ? props.cancelLabel : 'Não'
      break
  }
}

function setFocus() {
  switch (props.focusType) {
    case 'ok':
      if (okButtonRef.value) {
        okButtonRef.value.$el.focus()
      }
      break
    case 'cancel':
      if (showCancelBtn.value && cancelButtonRef.value) {
        cancelButtonRef.value.$el.focus()
      }
      break
  }
}

function escutarEsc() {
  document.addEventListener('keydown', escEvent)
}

function pararEscutarEsc() {
  document.removeEventListener('keydown', escEvent)
}

function escEvent(event: KeyboardEvent) {
  if (event.key !== 'Escape') return

  if (props.escEnabled) {
    props.question ? choose(false) : choose(true)
  }
}

function choose(value: boolean) {
  value ? props.okCallback() : props.cancelCallback()
  show.value = false

  focusAfterClose(value)
}

function evClickCloseButton() {
  choose(!showCancelBtn.value)
}

function focusAfterClose(chooseValue: boolean) {
  if (chooseValue && props.elementFocusOK) {
    nextTick(() => props.elementFocusOK!.focus())
    return
  }

  if (!chooseValue && props.elementFocusCancel) {
    nextTick(() => props.elementFocusCancel!.focus())
    return
  }

  if (props.elementFocus) {
    nextTick(() => props.elementFocus!.focus())
  }
}

onMounted(() => {
  show.value = true
  setTypeConfig(props.type)
  escutarEsc()
})

onBeforeUnmount(() => {
  pararEscutarEsc()
})
</script>

<style scoped>
.LStyleMessageCard {
  background-color: var(--pdi-bg-card) !important;
  border: 1px solid var(--pdi-border-default) !important;
  border-radius: var(--radius-lg);
  box-shadow: var(--pdi-shadow-lg);
  overflow: hidden;
}

.LStyleMessageHeader {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  padding: 28px 20px 10px;
  background-color: #141418;
}

.LStyleMessageClose {
  position: absolute;
  top: 10px;
  right: 10px;
  color: var(--pdi-text-muted) !important;
}

.LStyleMessageClose:hover {
  color: #ffffff !important;
}

.LStyleMessageIconWrapper {
  width: 76px;
  height: 76px;
  border-radius: 50%;
  background: #222228;
  border: 1px solid var(--pdi-border-default);
  display: grid;
  place-items: center;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
  transition: all 0.3s ease;
}

.LStyleMessageIconWrapper.is-error {
  background: radial-gradient(circle, rgba(239, 68, 68, 0.20) 0%, rgba(220, 38, 38, 0.05) 70%, transparent 100%);
  border: 1px solid rgba(239, 68, 68, 0.38);
  box-shadow: 0 0 26px rgba(239, 68, 68, 0.25), 0 4px 18px rgba(0, 0, 0, 0.4);
}

.LStyleMessageIconWrapper.is-alert {
  background: radial-gradient(circle, rgba(245, 158, 11, 0.20) 0%, rgba(217, 119, 6, 0.05) 70%, transparent 100%);
  border: 1px solid rgba(245, 158, 11, 0.38);
  box-shadow: 0 0 26px rgba(245, 158, 11, 0.25), 0 4px 18px rgba(0, 0, 0, 0.4);
}

.LStyleMessageIconWrapper.is-success {
  background: radial-gradient(circle, rgba(16, 185, 129, 0.20) 0%, rgba(5, 150, 105, 0.05) 70%, transparent 100%);
  border: 1px solid rgba(16, 185, 129, 0.38);
  box-shadow: 0 0 26px rgba(16, 185, 129, 0.25), 0 4px 18px rgba(0, 0, 0, 0.4);
}

.LStyleMessageIconWrapper.is-info {
  background: radial-gradient(circle, rgba(59, 130, 246, 0.20) 0%, rgba(37, 99, 235, 0.05) 70%, transparent 100%);
  border: 1px solid rgba(59, 130, 246, 0.38);
  box-shadow: 0 0 26px rgba(59, 130, 246, 0.25), 0 4px 18px rgba(0, 0, 0, 0.4);
}

.LStyleMessageIconWrapper.is-question {
  background: radial-gradient(circle, rgba(139, 92, 246, 0.20) 0%, rgba(109, 40, 217, 0.05) 70%, transparent 100%);
  border: 1px solid rgba(139, 92, 246, 0.38);
  box-shadow: 0 0 26px rgba(139, 92, 246, 0.25), 0 4px 18px rgba(0, 0, 0, 0.4);
}

.LStyleMessageTitle {
  margin: 8px 0 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.01em;
}

.LStyleMessageContent {
  font-size: 0.88rem;
  color: var(--pdi-text-secondary);
  line-height: 1.5;
}

.LStyleMessageActions {
  justify-content: center;
}

.LStyleDialogCancelBtn {
  border-color: var(--pdi-border-default) !important;
  color: var(--pdi-text-secondary) !important;
  font-weight: 600 !important;
}

.LStyleDialogOkBtn {
  background-color: var(--pdi-accent-white) !important;
  color: var(--pdi-accent-contrast) !important;
  font-weight: 700 !important;
  padding: 0 24px !important;
}

.LStyleDialogOkBtn:hover {
  background-color: #e4e4e7 !important;
}
</style>

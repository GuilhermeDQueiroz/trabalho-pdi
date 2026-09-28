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
        <div class="LStyleMessageIconWrapper">
          <v-icon size="40" color="#ffffff">{{ iconTitle }}</v-icon>
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
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background: #222228;
  border: 1px solid var(--pdi-border-default);
  display: grid;
  place-items: center;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
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

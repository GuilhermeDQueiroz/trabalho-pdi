import { ref } from 'vue'
import { defineStore } from 'pinia'

type TLoading = {
  mensagem: string
  percentual?: number
}

type TMessageDialog = {
  show: boolean
  titulo: string
  mensagem: string
  tipo: 'info' | 'success' | 'alert' | 'error' | 'question'
}

export const useLayoutStore = defineStore('[LAYOUT]', () => {
  const loading = ref<TLoading>({ mensagem: '' })
  const messageDialog = ref<TMessageDialog>({
    show: false,
    titulo: '',
    mensagem: '',
    tipo: 'error'
  })

  return {
    loading,
    messageDialog
  }
})

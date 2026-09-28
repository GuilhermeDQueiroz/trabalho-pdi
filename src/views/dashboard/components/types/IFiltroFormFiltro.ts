import type { ETipoFiltroPDI } from '@/enums/ETipoFiltroPDI'

export default interface IFiltroFormFiltro {
  tipo: ETipoFiltroPDI
  titulo: string
  subtitulo: string
  ordem: number
  params: any
}

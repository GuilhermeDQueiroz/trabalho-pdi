/**
 * ============================================================================
 * SERVIÇO TYPESCRIPT: PythonPdiService
 * ============================================================================
 * Camada de comunicação assíncrona entre o front-end Vue 3 e a API REST do FastAPI.
 * Responsável por despachar requisições para processamento matemático de PDI em Python puro.
 */

export interface IRespostaPDI {
  sucesso: boolean              // Flag indicando êxito do processamento
  imagem_base64: string         // Imagem resultante em formato data:image/png;base64,...
  matriz: number[][]            // Matriz bidimensional de intensidades [altura][largura]
  largura: number               // Largura real da matriz em pixels
  altura: number                // Altura real da matriz em pixels
  histograma?: {                // Histograma recalculado da imagem resultante
    labels: string[]            // Níveis de cinza ['0', '1', ..., '255']
    valores: number[]           // Frequências absolutas de cada nível
    total_pixels?: number       // Total de pixels (altura * largura)
  }
  extras?: any[]                // Dados suplementares retornados por pipelines
}

export interface IItemFiltroReq {
  tipo: number                  // Código numérico do enum ETipoFiltroPDI (1 a 28)
  params?: Record<string, any>  // Dicionário de hiperparâmetros (gamma, a, b, mascara, etc.)
}

// Prefixo base para as rotas da API:
// Em desenvolvimento: roteado pelo proxy do Vite para 'http://localhost:8000/api'
// Em produção: servido diretamente pelo FastAPI na mesma porta
const BASE_URL = '/api'

export class PythonPdiService {
  /**
   * Processa a imagem no backend Python aplicando a fila sequencial de filtros.
   * Rota: POST /api/processar
   *
   * @param imagem String Base64 ou Matriz 2D de níveis de cinza
   * @param filtros Lista ordenada de filtros e seus parâmetros
   * @returns Promessa com o resultado do processamento, imagem Base64 e histograma
   */
  public static async processar(
    imagem: string | number[][],
    filtros: IItemFiltroReq[]
  ): Promise<IRespostaPDI> {
    const payload = {
      imagem,
      filtros
    }

    const response = await fetch(`${BASE_URL}/processar`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }))
      throw new Error(err.detail || 'Erro ao processar imagem no backend Python')
    }

    return await response.json()
  }

  /**
   * Executa rotação geométrica matricial no servidor Python.
   * Rota: POST /api/rotacao
   *
   * @param imagem Imagem de entrada
   * @param tipo Modo de rotação ('90_horario', '90_antihorario' ou '180')
   */
  public static async rotacionar(
    imagem: string | number[][],
    tipo: '90_horario' | '90_antihorario' | '180'
  ): Promise<IRespostaPDI> {
    const response = await fetch(`${BASE_URL}/rotacao`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ imagem, tipo })
    })

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }))
      throw new Error(err.detail || 'Erro ao rotacionar imagem no backend Python')
    }

    return await response.json()
  }

  /**
   * Requisita o cálculo estatístico do histograma de níveis de cinza [0, 255].
   * Rota: POST /api/histograma
   *
   * @param imagem Imagem a ser analisada
   */
  public static async obterHistograma(imagem: string | number[][]): Promise<{
    labels: string[]
    valores: number[]
    total_pixels: number
  }> {
    const response = await fetch(`${BASE_URL}/histograma`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ imagem })
    })

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }))
      throw new Error(err.detail || 'Erro ao calcular histograma no backend Python')
    }

    return await response.json()
  }

  /**
   * Executa a equalização de histograma baseada na CDF e LUT no backend Python.
   * Rota: POST /api/equalizacao
   *
   * @param imagem Imagem de entrada
   * @returns Imagem equalizada e o respectivo histograma resultante
   */
  public static async equalizar(imagem: string | number[][]): Promise<IRespostaPDI> {
    const response = await fetch(`${BASE_URL}/equalizacao`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ imagem })
    })

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }))
      throw new Error(err.detail || 'Erro ao equalizar imagem no backend Python')
    }

    return await response.json()
  }

  /**
   * Consulta as coordenadas espaciais (x, y) e o Nível de Cinza (NC) pontual na matriz.
   * Rota: POST /api/ponta-de-prova
   *
   * @param imagem Imagem inspecionada
   * @param x Coordenada horizontal (coluna)
   * @param y Coordenada vertical (linha)
   */
  public static async pontaDeProva(
    imagem: string | number[][],
    x: number,
    y: number
  ): Promise<{
    x: number
    y: number
    nc: number
    valido: boolean
    largura: number
    altura: number
  }> {
    const response = await fetch(`${BASE_URL}/ponta-de-prova`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ imagem, x, y })
    })

    if (!response.ok) {
      return { x, y, nc: 0, valido: false, largura: 0, altura: 0 }
    }

    return await response.json()
  }
}


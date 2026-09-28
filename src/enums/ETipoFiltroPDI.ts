/**
 * ============================================================================
 * ENUM ETipoFiltroPDI: Identificadores Numéricos das 18 Operações de PDI
 * ============================================================================
 * Cada constante numérica corresponde exatamente a um algoritmo implementado
 * no motor Python do backend.
 */
export enum ETipoFiltroPDI {
  NEGATIVO = 1,                       // s = 255 - r (Inversão linear de intensidades)
  LOGARITIMO = 2,                     // s = c * ln(1 + r) (Expansão de escuros e compressão de claros)
  LOGARITIMO_INVERSO = 3,             // s = exp(r / c) - 1 (Inverso da curva logarítmica)
  POTENCIA = 4,                       // s = c * r^gamma (Correção de Gamma / Lei de Potência)
  RAIZ = 5,                           // s = c * r^(1 / gamma) (Raiz gamma-ésima, clareia sombras)
  AMPLIACAO_REPLICACAO_512X512 = 6,   // Reamostragem 512x512 por Vizinho Mais Próximo (Nearest Neighbor)
  AMPLIACAO_REPLICACAO_1024X1024 = 7, // Reamostragem 1024x1024 por Vizinho Mais Próximo
  AMPLIACAO_BILINEAR_512X512 = 8,     // Reamostragem 512x512 por Interpolação Bilinear contínua
  AMPLIACAO_BILINEAR_1024X1024 = 9,   // Reamostragem 1024x1024 por Interpolação Bilinear contínua
  HISTOGRAMA = 10,                    // Contagem de frequências h(r_k) = n_k para k ∈ [0, 255]
  EQUALIZACAO = 11,                   // Equalização de contraste global via CDF acumulada e Look-Up Table
  ESPELHAMENTO_HORIZONTAL = 12,       // Flip Horizontal: I_novo(y, x) = I_orig(y, W - 1 - x)
  ESPELHAMENTO_VERTICAL = 13,         // Flip Vertical: I_novo(y, x) = I_orig(H - 1 - y, x)
  ROTACAO_90_GRAUS_HORARIO = 14,      // Rotação 90° CW: I_novo(y', x') = I_orig(H - 1 - x', y')
  ROTACAO_90_GRAUS_ANTIHORARIO = 15,  // Rotação 90° CCW: I_novo(y', x') = I_orig(x', W - 1 - y')
  ROTACAO_180_GRAUS = 16,             // Rotação 180°: I_novo(y, x) = I_orig(H - 1 - y, W - 1 - x)
  EXPANSAO = 17,                      // Expansão Linear: g = a * r + b (ajuste de ganho e brilho)
  COMPRESSAO = 18,                    // Compressão Linear: g = (r / a) - b (redução da faixa dinâmica)
  SOMAR_IMAGENS = 19,                 // Blending Ponderado: g = p * I1 + (1 - p) * I2
  MEDIA = 20,                         // Filtro Passa-Baixa da Média: g(x, y) = (1/M) * ∑ f(x+s, y+t)
  MEDIANA = 21,                       // Filtro Não-Linear da Mediana: g(x, y) = mediana(vizinhos)
  MODA = 22,                          // Filtro da Moda: g(x, y) = valor mais frequente na vizinhança
  MINIMO = 23,                        // Filtro Mínimo (Erosão em cinza): g(x, y) = min(vizinhos)
  MAXIMO = 24,                        // Filtro Máximo (Dilatação em cinza): g(x, y) = max(vizinhos)
  LAPLACIANO = 25,                    // Operador Laplaciano de Segunda Derivada: ∇²f = ∂²f/∂x² + ∂²f/∂y²
  HIGH_BOOST = 26,                    // Filtro High Boost: f_hb = A * f - f_suavizada
  PREWITT = 27,                       // Detecção de Bordas Prewitt: M = √(Gx² + Gy²)
  SOBEL = 28                          // Detecção de Bordas Sobel: M = √(Gx² + Gy²) com peso central 2
}


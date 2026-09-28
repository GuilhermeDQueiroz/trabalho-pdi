import { ETipoFiltroPDI } from '@/enums/ETipoFiltroPDI'

export interface IInfoFiltroPDI {
  tipo: number
  titulo: string
  categoria: 'Pontual' | 'Geométrico' | 'Espacial' | 'Histograma'
  formula: string
  oQueAplica: string
  comoAplica: string
}

export const cINFO_FILTROS_PDI: Record<number, IInfoFiltroPDI> = {
  [ETipoFiltroPDI.NEGATIVO]: {
    tipo: ETipoFiltroPDI.NEGATIVO,
    titulo: 'Filtro Negativo',
    categoria: 'Pontual',
    formula: 's = 255 - r',
    oQueAplica: 'Inverte linearmente as intensidades da imagem. Tons pretos tornam-se brancos e tons brancos tornam-se pretos, simulando o negativo de um filme fotográfico.',
    comoAplica: 'Aplica a fórmula s = (L - 1) - r pixel a pixel, onde L = 256. Subtrai o valor do pixel de 255 sem alterar a resolução espacial.'
  },
  [ETipoFiltroPDI.LOGARITIMO]: {
    tipo: ETipoFiltroPDI.LOGARITIMO,
    titulo: 'Filtro de Logaritmo (Unidade 3)',
    categoria: 'Pontual',
    formula: 's = c · ln(1 + r)',
    oQueAplica: 'Expande a faixa dinâmica de tons escuros (baixas intensidades) e comprime as altas intensidades, revelando detalhes ocultos em sombras profundas.',
    comoAplica: 'Calcula s = c * ln(1 + r) para cada pixel, com constante de escala c = 255 / ln(256) ≈ 45.98. O termo "+ 1" impede indefinição matemática quando r = 0.'
  },
  [ETipoFiltroPDI.LOGARITIMO_INVERSO]: {
    tipo: ETipoFiltroPDI.LOGARITIMO_INVERSO,
    titulo: 'Filtro de Logaritmo Inverso (Unidade 3)',
    categoria: 'Pontual',
    formula: 's = exp(r / c) - 1',
    oQueAplica: 'Operação inversa ao logaritmo (exponencial). Comprime os tons escuros e expande a faixa dinâmica dos tons claros.',
    comoAplica: 'Aplica a função exponencial inversa s = exp(r / c) - 1 com c = 255 / ln(256), mapeando a curva e garantindo clamping no intervalo [0, 255].'
  },
  [ETipoFiltroPDI.POTENCIA]: {
    tipo: ETipoFiltroPDI.POTENCIA,
    titulo: 'Filtro de Potência / Gamma (Unidade 3)',
    categoria: 'Pontual',
    formula: 's = c · r^γ',
    oQueAplica: 'Correção de Gamma. Quando γ > 1, escurece a imagem e acentua o contraste em áreas claras; quando γ < 1, clareia áreas escuras.',
    comoAplica: 'Eleva a intensidade de cada pixel à potência gamma (s = 255 * (r / 255)^γ), gerando curvas de transferência côncavas ou convexas de acordo com o valor configurado.'
  },
  [ETipoFiltroPDI.RAIZ]: {
    tipo: ETipoFiltroPDI.RAIZ,
    titulo: 'Filtro de Raiz / Gamma Inverso (Unidade 3)',
    categoria: 'Pontual',
    formula: 's = c · r^(1 / γ)',
    oQueAplica: 'Aplica a raiz γ-ésima sobre os pixels, expandindo os níveis de cinza escuros e clareando gradualmente sombras sem estourar as altas luzes.',
    comoAplica: 'Mapeia cada pixel pela raiz gamma: s = 255 * (r / 255)^(1 / γ), produzindo uma curva convexa suave que eleva a luminosidade geral.'
  },
  [ETipoFiltroPDI.AMPLIACAO_REPLICACAO_512X512]: {
    tipo: ETipoFiltroPDI.AMPLIACAO_REPLICACAO_512X512,
    titulo: 'Ampliação Replicação 512×512 (Nearest Neighbor)',
    categoria: 'Geométrico',
    formula: 'I_novo(y\', x\') = I_orig(round(y\' · fy), round(x\' · fx))',
    oQueAplica: 'Dobra as dimensões espaciais da imagem de 256×256 para 512×512 pixels utilizando a técnica do Vizinho Mais Próximo.',
    comoAplica: 'Para cada coordenada da imagem de destino (512×512), calcula a posição inversa correspondente na matriz original e repete o pixel em blocos discretos 2×2.'
  },
  [ETipoFiltroPDI.AMPLIACAO_REPLICACAO_1024X1024]: {
    tipo: ETipoFiltroPDI.AMPLIACAO_REPLICACAO_1024X1024,
    titulo: 'Ampliação Replicação 1024×1024 (Nearest Neighbor)',
    categoria: 'Geométrico',
    formula: 'I_novo(y\', x\') = I_orig(round(y\' · fy), round(x\' · fx))',
    oQueAplica: 'Quadruplica as dimensões espaciais de 256×256 para 1024×1024 pixels pelo método do Vizinho Mais Próximo.',
    comoAplica: 'Mapeia a nova malha com fator de escala 4×, replicando cada pixel original em blocos quadrados 4×4 sem interpolação de gradientes.'
  },
  [ETipoFiltroPDI.AMPLIACAO_BILINEAR_512X512]: {
    tipo: ETipoFiltroPDI.AMPLIACAO_BILINEAR_512X512,
    titulo: 'Ampliação Bilinear 512×512 (Bilinear Resampling)',
    categoria: 'Geométrico',
    formula: 'I = (1-dx)(1-dy)I₁₁ + dx(1-dy)I₂₁ + (1-dx)dy I₁₂ + dx·dy I₂₂',
    oQueAplica: 'Amplia para 512×512 com interpolação suave e contínua, eliminando artefatos de blocagem ("pixelização") nas bordas.',
    comoAplica: 'Calcula a média ponderada dos 4 vizinhos mais próximos na malha contínua, usando as distâncias fracionárias dx e dy como pesos de interpolação linear nos eixos X e Y.'
  },
  [ETipoFiltroPDI.AMPLIACAO_BILINEAR_1024X1024]: {
    tipo: ETipoFiltroPDI.AMPLIACAO_BILINEAR_1024X1024,
    titulo: 'Ampliação Bilinear 1024×1024 (Bilinear Resampling)',
    categoria: 'Geométrico',
    formula: 'I = (1-dx)(1-dy)I₁₁ + dx(1-dy)I₂₁ + (1-dx)dy I₁₂ + dx·dy I₂₂',
    oQueAplica: 'Amplia para 1024×1024 com alta fidelidade visual, produzindo transições graduais e contornos suaves.',
    comoAplica: 'Executa a ponderação bilinear bidimensional sobre a malha expandida em 4×, combinando linearmente os 4 pontos de amostragem discretos circundantes.'
  },
  [ETipoFiltroPDI.HISTOGRAMA]: {
    tipo: ETipoFiltroPDI.HISTOGRAMA,
    titulo: 'Histograma de Níveis de Cinza',
    categoria: 'Histograma',
    formula: 'h(rₖ) = nₖ,  k ∈ [0, 255]',
    oQueAplica: 'Gera a distribuição de frequências das intensidades luminosas da imagem em 256 níveis de cinza (NC).',
    comoAplica: 'Varre a matriz bidimensional completa e contabiliza a ocorrência absoluta de cada intensidade entre 0 e 255, exibindo o gráfico de barras estatístico.'
  },
  [ETipoFiltroPDI.EQUALIZACAO]: {
    tipo: ETipoFiltroPDI.EQUALIZACAO,
    titulo: 'Equalização de Histograma (Unidade 3)',
    categoria: 'Histograma',
    formula: 'sₖ = round((L - 1)/(M · N) · ∑ nⱼ)',
    oQueAplica: 'Maximiza o contraste global da cena, redistribuindo os tons de cinza de forma homogênea e plana ao longo de toda a escala [0, 255].',
    comoAplica: 'Calcula o histograma bruto, acumula a Função de Distribuição Acumulada (CDF) e cria uma Look-Up Table (LUT) para remapear cada pixel instantaneamente.'
  },
  [ETipoFiltroPDI.ESPELHAMENTO_HORIZONTAL]: {
    tipo: ETipoFiltroPDI.ESPELHAMENTO_HORIZONTAL,
    titulo: 'Espelhamento Horizontal',
    categoria: 'Geométrico',
    formula: 'I_novo(y, x) = I_orig(y, W - 1 - x)',
    oQueAplica: 'Inverte a imagem horizontalmente da esquerda para a direita (efeito espelho / flip horizontal).',
    comoAplica: 'Permuta as colunas de cada linha da matriz mantendo os índices verticais y inalterados.'
  },
  [ETipoFiltroPDI.ESPELHAMENTO_VERTICAL]: {
    tipo: ETipoFiltroPDI.ESPELHAMENTO_VERTICAL,
    titulo: 'Espelhamento Vertical',
    categoria: 'Geométrico',
    formula: 'I_novo(y, x) = I_orig(H - 1 - y, x)',
    oQueAplica: 'Inverte a imagem verticalmente de cima para baixo (ponta-cabeça / flip vertical).',
    comoAplica: 'Permuta as linhas da matriz de modo que a primeira linha vire a última, mantendo as colunas x inalteradas.'
  },
  [ETipoFiltroPDI.ROTACAO_90_GRAUS_HORARIO]: {
    tipo: ETipoFiltroPDI.ROTACAO_90_GRAUS_HORARIO,
    titulo: 'Rotação 90° Horário',
    categoria: 'Geométrico',
    formula: 'I_novo(y\', x\') = I_orig(H - 1 - x\', y\')',
    oQueAplica: 'Gira a imagem em 90 graus no sentido dos ponteiros do relógio.',
    comoAplica: 'Transpõe a matriz original e inverte a ordem das colunas, ajustando as dimensões de altura e largura.'
  },
  [ETipoFiltroPDI.ROTACAO_90_GRAUS_ANTIHORARIO]: {
    tipo: ETipoFiltroPDI.ROTACAO_90_GRAUS_ANTIHORARIO,
    titulo: 'Rotação 90° Anti-Horário',
    categoria: 'Geométrico',
    formula: 'I_novo(y\', x\') = I_orig(x\', W - 1 - y\')',
    oQueAplica: 'Gira a imagem em 90 graus no sentido anti-horário.',
    comoAplica: 'Transpõe a matriz original e inverte a ordem das linhas, reorganizando as coordenadas espaciais.'
  },
  [ETipoFiltroPDI.ROTACAO_180_GRAUS]: {
    tipo: ETipoFiltroPDI.ROTACAO_180_GRAUS,
    titulo: 'Rotação 180°',
    categoria: 'Geométrico',
    formula: 'I_novo(y, x) = I_orig(H - 1 - y, W - 1 - x)',
    oQueAplica: 'Gira a imagem completamente de cabeça para baixo em 180 graus.',
    comoAplica: 'Inverte simultaneamente a ordem das linhas e das colunas da matriz bidimensional.'
  },
  [ETipoFiltroPDI.EXPANSAO]: {
    tipo: ETipoFiltroPDI.EXPANSAO,
    titulo: 'Filtro de Expansão (g = a·r + b)',
    categoria: 'Pontual',
    formula: 'g(x, y) = a · r(x, y) + b',
    oQueAplica: 'Ajuste linear de ganho e brilho. Se a > 1 aumenta o contraste; se b > 0 adiciona brilho uniforme a todos os pixels.',
    comoAplica: 'Multiplica a intensidade original pelo ganho "a" e soma o offset "b", aplicando clamping estrito no intervalo [0, 255].'
  },
  [ETipoFiltroPDI.COMPRESSAO]: {
    tipo: ETipoFiltroPDI.COMPRESSAO,
    titulo: 'Filtro de Compressão (g = r/a - b)',
    categoria: 'Pontual',
    formula: 'g(x, y) = (r(x, y) / a) - b',
    oQueAplica: 'Comprime a faixa dinâmica das intensidades, diminuindo a diferença entre as áreas mais claras e mais escuras.',
    comoAplica: 'Divide a intensidade original pelo fator divisor "a" e subtrai o deslocamento "b", com proteção contra divisão por zero e clamping.'
  },
  [ETipoFiltroPDI.SOMAR_IMAGENS]: {
    tipo: ETipoFiltroPDI.SOMAR_IMAGENS,
    titulo: 'Somar Duas Imagens com Porcentagem',
    categoria: 'Pontual',
    formula: 'g = (p / 100)·I₁ + ((100 - p) / 100)·I₂',
    oQueAplica: 'Fusão ponderada (blending / cross-dissolve) entre a imagem atual e uma segunda imagem carregada pelo usuário.',
    comoAplica: 'Realiza a combinação linear convexa ponto a ponto. Como os pesos normalizados somam 1.0 (p1 + p2 = 1), a soma é imune a overflow (nunca estoura 255).'
  },
  [ETipoFiltroPDI.MEDIA]: {
    tipo: ETipoFiltroPDI.MEDIA,
    titulo: 'Filtro da Média (Passa-Baixa)',
    categoria: 'Espacial',
    formula: 'g(x, y) = (1 / N²) · ∑ ∑ f(x+s, y+t)',
    oQueAplica: 'Filtro passa-baixa de suavização (desfoque/blur). Reduz ruídos aleatórios finos atenuando altas frequências da imagem.',
    comoAplica: 'Convoluciona a imagem com máscara quadrada N×N (3×3, 5×5, etc.), substituindo cada pixel central pela média aritmética dos vizinhos com replicação de bordas.'
  },
  [ETipoFiltroPDI.MEDIANA]: {
    tipo: ETipoFiltroPDI.MEDIANA,
    titulo: 'Filtro da Mediana (Ordem)',
    categoria: 'Espacial',
    formula: 'g(x, y) = mediana { vizinhança N×N }',
    oQueAplica: 'Filtro não-linear altamente eficaz na remoção de ruídos impulsivos ("Sal e Pimenta"), preservando bordas com mais nitidez que a média.',
    comoAplica: 'Extrai todos os pixels da janela N×N, ordena-os numericamente em ordem crescente e atribui o elemento central (mediana) ao pixel analisado.'
  },
  [ETipoFiltroPDI.MODA]: {
    tipo: ETipoFiltroPDI.MODA,
    titulo: 'Filtro da Moda (Frequência)',
    categoria: 'Espacial',
    formula: 'g(x, y) = argmax { contagem(v) na janela N×N }',
    oQueAplica: 'Filtro estatístico de frequência. Homogeneíza texturas atribuindo o nível de cinza dominante da região.',
    comoAplica: 'Constrói um histograma local na janela N×N em torno do pixel e seleciona o valor com maior número de repetições na vizinhança.'
  },
  [ETipoFiltroPDI.MINIMO]: {
    tipo: ETipoFiltroPDI.MINIMO,
    titulo: 'Filtro MÍNIMO (Erosão em Cinza)',
    categoria: 'Espacial',
    formula: 'g(x, y) = min { f(x+s, y+t) }',
    oQueAplica: 'Estatística de ordem mínima (análogo à erosão morfológica). Elimina ruídos claros pontuais ("sal") e expande áreas escuras.',
    comoAplica: 'Varre a vizinhança N×N e substitui o pixel central pelo menor valor de intensidade encontrado na janela.'
  },
  [ETipoFiltroPDI.MAXIMO]: {
    tipo: ETipoFiltroPDI.MAXIMO,
    titulo: 'Filtro MÁXIMO (Dilatação em Cinza)',
    categoria: 'Espacial',
    formula: 'g(x, y) = max { f(x+s, y+t) }',
    oQueAplica: 'Estatística de ordem máxima (análogo à dilatação morfológica). Elimina ruídos escuros pontuais ("pimenta") e expande regiões claras.',
    comoAplica: 'Varre a vizinhança N×N e substitui o pixel central pelo maior valor de intensidade presente na janela.'
  },
  [ETipoFiltroPDI.LAPLACIANO]: {
    tipo: ETipoFiltroPDI.LAPLACIANO,
    titulo: 'Operador Laplaciano (Segunda Derivada)',
    categoria: 'Espacial',
    formula: '∇²f = ∂²f/∂x² + ∂²f/∂y²',
    oQueAplica: 'Detector de bordas isotrópico (invariante à rotação). Destaca linhas finas e transições bruscas de intensidade em todas as direções.',
    comoAplica: 'Convoluciona com máscara derivativa de soma zero (centro N² - 1 e periferia -1), identificando passagens por zero (zero-crossings) da segunda derivada.'
  },
  [ETipoFiltroPDI.HIGH_BOOST]: {
    tipo: ETipoFiltroPDI.HIGH_BOOST,
    titulo: 'Operador High Boost (Nitidez A)',
    categoria: 'Espacial',
    formula: 'f_hb = (A - 1)·f + (f - f_suavizada),  A ≥ 1',
    oQueAplica: 'Realce acentuado de nitidez (unsharp masking amplificado). Destaca detalhes e bordas sem perder a informação de baixa frequência da imagem original.',
    comoAplica: 'Subtrai a versão suavizada da imagem original para obter a máscara de nitidez e adiciona à imagem original multiplicada pelo fator de ampliação A configurado.'
  },
  [ETipoFiltroPDI.PREWITT]: {
    tipo: ETipoFiltroPDI.PREWITT,
    titulo: 'Operador Prewitt (Gradiente)',
    categoria: 'Espacial',
    formula: 'M = √(Gx² + Gy²),  Gx e Gy com máscaras 3×3',
    oQueAplica: 'Detecção direcional de bordas por derivadas de primeira ordem horizontais e verticais.',
    comoAplica: 'Aplica a máscara horizontal Gx e vertical Gy simultaneamente sobre cada pixel e computa a magnitude euclidiana combinada do gradiente espacial.'
  },
  [ETipoFiltroPDI.SOBEL]: {
    tipo: ETipoFiltroPDI.SOBEL,
    titulo: 'Operador Sobel (Gradiente Ponderado)',
    categoria: 'Espacial',
    formula: 'M = √(Gx² + Gy²),  máscaras com peso 2 no centro',
    oQueAplica: 'Detecção de bordas refinada. A ponderação central suaviza a imagem enquanto diferencia, oferecendo maior resistência a ruídos que o Prewitt.',
    comoAplica: 'Convoluciona com máscaras 3×3 onde a linha/coluna central possui peso dobrado (2 e -2) e combina as derivadas parciais na magnitude euclidiana final.'
  }
}

/**
 * Retorna as informações explicativas completas de um filtro pelo seu código numérico ou título.
 */
export function obterInfoFiltro(tipo: number): IInfoFiltroPDI {
  if (cINFO_FILTROS_PDI[tipo]) {
    return cINFO_FILTROS_PDI[tipo]
  }

  return {
    tipo,
    titulo: 'Filtro PDI',
    categoria: 'Espacial',
    formula: 's = T(r)',
    oQueAplica: 'Transformação algorítmica sobre as intensidades da matriz de entrada.',
    comoAplica: 'Executa o algoritmo correspondente em Python puro sobre a imagem digital.'
  }
}

"""
===============================================================================
MÓDULO: HISTOGRAMA E EQUALIZAÇÃO DE IMAGENS (PDI - UNIDADE 3)
===============================================================================
O histograma de uma imagem digital em níveis de cinza fornece uma descrição global
da distribuição estatística de intensidades de luminosidade na cena.

Conceitos Fundamentais:
1. Histograma Não-Normalizado:
   - Contagem absoluta n_k de pixels que possuem cada nível de cinza r_k.
2. Histograma Normalizado / Função Densidade de Probabilidade (PDF Discreta):
   - p(r_k) = n_k / (M * N), onde M * N é o número total de pixels.
   - Representa a probabilidade empírica de ocorrência de um pixel de intensidade r_k.
3. Função de Distribuição Acumulada (CDF Discreta):
   - CDF(k) = ∑_{j=0..k} p(r_j)
   - É monotônica crescente e varia no intervalo [0, 1].

4. Teorema da Equalização de Histograma:
   - Em teoria contínua, transformar uma variável aleatória r pela sua própria CDF
     s = T(r) = (L - 1) ∫_0^r p_r(w) dw produz uma variável aleatória s com densidade
     uniforme (plana).
   - Na prática discreta, aproxima-se essa distribuição uniforme espalhando os níveis
     de cinza ao longo de todo o espectro [0, 255], maximizando o contraste e a entropia.
"""

from typing import List, Dict, Any, Tuple
from .utils import clamp


# =============================================================================
# 1. CÁLCULO DO HISTOGRAMA DE NÍVEIS DE CINZA
# =============================================================================
def calcular_histograma(matriz: List[List[int]]) -> Dict[str, Any]:
    """
    Cálculo do Histograma Discreto de Intensidades:
    -----------------------------------------------
    Fórmula Matemática:
        h(r_k) = n_k
        onde:
            - r_k: Nível de cinza avaliado, k ∈ [0, 255]
            - n_k: Quantidade total de pixels na matriz onde f(x, y) = r_k
            - Propriedade: ∑_{k=0}^{255} n_k = M * N (área total da imagem)

    Fundamentação Teórica:
        - Imagens subexpostas (muito escuras) concentram suas barras na região esquerda (próximo a 0).
        - Imagens superexpostas (muito claras) concentram suas barras na região direita (próximo a 255).
        - Imagens com baixo contraste apresentam barras aglomeradas em uma faixa estreita.
        - Imagens com alto contraste possuem distribuição ampla cobrindo quase todo o eixo horizontal.

    Retorna:
        Dicionário com labels ['0', '1', ..., '255'], contagens absolutas e metadados.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0
    total_pixels = altura * largura

    # Vetor de 256 posições (uma para cada nível de cinza [0..255]) inicializado com 0
    frequencias = [0] * 256

    # Varredura completa da matriz bidimensional
    for y in range(altura):
        for x in range(largura):
            # Garante que o índice pertença rigorosamente ao intervalo [0, 255]
            val = clamp(matriz[y][x])
            # Incrementa o contador de ocorrência daquele tom de cinza
            frequencias[val] += 1

    # Rótulos textuais de '0' a '255' para alimentar gráficos no front-end
    labels = [str(i) for i in range(256)]

    return {
        "labels": labels,
        "valores": frequencias,
        "total_pixels": total_pixels,
        "largura": largura,
        "altura": altura,
    }


# =============================================================================
# 2. EQUALIZAÇÃO DE HISTOGRAMA E GERAÇÃO DO HISTOGRAMA RESULTANTE
# =============================================================================
def equalizar_histograma(matriz: List[List[int]]) -> Tuple[List[List[int]], Dict[str, Any]]:
    """
    Equalização de Histograma (Unidade 3):
    --------------------------------------
    Objetivo:
        Distribuir uniformemente as intensidades de cinza ao longo de toda a escala [0, 255],
        aumentando significativamente o contraste dinâmico de detalhes pouco visíveis.

    Passo a Passo Matemático:
        Passo 1 (Cálculo do Histograma Bruto):
            h(k) = n_k, para k = 0, 1, ..., 255

        Passo 2 (Cálculo da Função de Distribuição Acumulada - CDF):
            CDF(k) = ∑_{j=0}^{k} h(j)
            Representa o total acumulado de pixels com intensidade menor ou igual a k.

        Passo 3 (Mapeamento Normalizado por Look-Up Table - LUT):
            Para evitar que a intensidade mínima existente seja mapeada acima de zero,
            subtrai-se CDF_min (primeiro valor não-nulo da CDF):
                s_k = round( ((CDF(k) - CDF_min) / (total_pixels - CDF_min)) * 255 )
            Se CDF_min == total_pixels (imagem homogênea de cor única):
                s_k = round( (CDF(k) / total_pixels) * 255 )

        Passo 4 (Aplicação O(1) via Tabela de Mapeamento):
            Cada pixel original r(y, x) é substituído instantaneamente por s = mapa[r].

        Passo 5 (Recálculo do Histograma):
            Gera o novo histograma resultante da imagem já equalizada para exibição gráfica.

    Retorna:
        Tupla (matriz_equalizada, dados_histograma_resultante)
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0
    total_pixels = altura * largura

    # Caso especial: imagem vazia
    if total_pixels == 0:
        return [], {"labels": [str(i) for i in range(256)], "valores": [0] * 256}

    # 1. Histograma de frequências discretas h(k)
    hist = [0] * 256
    for y in range(altura):
        for x in range(largura):
            hist[clamp(matriz[y][x])] += 1

    # 2. Cálculo da Função de Distribuição Acumulada: CDF(k) = ∑_{j=0}^{k} h(j)
    cdf = [0] * 256
    acumulado = 0
    for i in range(256):
        acumulado += hist[i]
        cdf[i] = acumulado

    # Localiza o primeiro valor estritamente positivo da CDF (CDF_min)
    # Esse é o valor acumulado associado ao menor nível de cinza presente na imagem
    cdf_min = 0
    for v in cdf:
        if v > 0:
            cdf_min = v
            break

    # 3. Construção da Tabela de Mapeamento (Look-Up Table - LUT): mapa[r] -> s
    mapa = [0] * 256
    denominador = total_pixels - cdf_min

    for i in range(256):
        if denominador > 0:
            # Fórmula padrão da equalização discreta normalizada pela CDF mínima
            valor_eq = round(((cdf[i] - cdf_min) / float(denominador)) * 255.0)
        else:
            # Caso de salvaguarda quando todos os pixels da imagem possuem o mesmo valor
            valor_eq = round((cdf[i] / float(total_pixels)) * 255.0)

        mapa[i] = clamp(valor_eq)

    # 4. Substituição das intensidades na matriz (mapeamento pixel a pixel)
    imagem_equalizada: List[List[int]] = []
    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            orig = clamp(matriz[y][x])
            # Busca direta no mapa pré-calculado: O(1) de complexidade por pixel
            linha.append(mapa[orig])
        imagem_equalizada.append(linha)

    # 5. Cálculo do histograma da imagem final resultante
    hist_resultante = calcular_histograma(imagem_equalizada)

    return imagem_equalizada, hist_resultante

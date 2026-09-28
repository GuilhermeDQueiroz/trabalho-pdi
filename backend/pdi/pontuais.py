"""
===============================================================================
MÓDULO: TRANSFORMACÕES E FILTROS PONTUAIS (PDI - UNIDADE 3)
===============================================================================
Em processamento digital de imagens, uma transformação pontual opera diretamente
sobre cada pixel individual f(x, y), produzindo um novo valor s = T(r),
onde:
    - 'r' representa a intensidade do pixel na imagem de entrada (0 <= r <= 255)
    - 's' representa a intensidade resultante na imagem de saída (0 <= s <= 255)
    - 'T' é a função de transferência ou transformação matemática.

Este módulo NÃO utiliza bibliotecas de terceiros (como OpenCV ou SciPy).
Todas as fórmulas foram implementadas passo a passo em Python puro.
"""

import math
from typing import List
from .utils import clamp


# =============================================================================
# 1. FILTRO NEGATIVO
# =============================================================================
def filtro_negativo(matriz: List[List[int]]) -> List[List[int]]:
    """
    Filtro Negativo:
    ----------------
    Fórmula Matemática:
        s = (L - 1) - r
        Para imagens digitais de 8 bits (L = 256 níveis de cinza no intervalo [0, 255]):
        s = 255 - r

    Variáveis:
        - r: Intensidade original do pixel de entrada, r ∈ [0, 255]
        - s: Intensidade invertida do pixel de saída, s ∈ [0, 255]
        - L: Número total de níveis de cinza discretos (L = 2⁸ = 256)

    Fundamentação Teórica:
        - Inverte linearmente a escala de cinza: o valor mínimo 0 (preto) é transformado
          em 255 (branco), e o valor máximo 255 (branco) é transformado em 0 (preto).
        - Tons médios (ex: 128) permanecem quase inalterados: 255 - 128 = 127.
        - Aplicação Prática: Realce de detalhes em regiões escuras cercadas por áreas claras,
          amplamente utilizado em radiografias (raios-X) e mamografias para visualização médica.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    resultado: List[List[int]] = []

    # Itera sobre cada linha (eixo y) da imagem
    for y in range(altura):
        linha: List[int] = []
        # Itera sobre cada coluna (eixo x) da linha
        for x in range(largura):
            r = matriz[y][x]  # Intensidade do pixel de entrada

            # Aplicação direta da fórmula da inversão: s = 255 - r
            s = 255 - r

            # Garante que o valor resultante esteja restrito à faixa de 8 bits [0, 255]
            linha.append(clamp(s))
        resultado.append(linha)

    return resultado


# =============================================================================
# 2. FILTRO DE LOGARITMO (UNIDADE 3)
# =============================================================================
def filtro_logaritmo(matriz: List[List[int]], c: float | None = None) -> List[List[int]]:
    """
    Transformação Logarítmica:
    --------------------------
    Fórmula Matemática:
        s = c * ln(1 + r)

    Determinação da Constante de Normalização 'c':
        Para garantir que a amplitude total de entrada [0, 255] seja mapeada
        integralmente para a faixa de saída [0, 255]:
            255 = c * ln(1 + 255)
            c = 255 / ln(256) ≈ 45.9858673

    Variáveis:
        - r: Nível de cinza de entrada, r ∈ [0, 255]
        - s: Nível de cinza resultante, s ∈ [0, 255]
        - ln: Logaritmo natural (base e)
        - O termo '+ 1' no argumento (1 + r) é crucial: quando r = 0, ln(1 + 0) = ln(1) = 0,
          evitando a indeterminação matemática ln(0) -> -∞.

    Fundamentação Teórica:
        - A derivada da função logarítmica d/dr[ln(1 + r)] = 1 / (1 + r) é muito alta
          próximo de zero e decresce conforme 'r' cresce.
        - Portanto, o filtro EXPANDE a faixa dinâmica dos tons escuros (baixas intensidades)
          e COMPRIME os tons claros (altas intensidades).
        - Aplicação Clássica: Exibição da magnitude da Transformada de Fourier 2D, cujos valores
          no componente DC (frequência zero) podem atingir ordens de magnitude na casa dos
          milhões, ofuscando as altas frequências sem a compressão logarítmica.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    # Se a constante 'c' não for informada, calcula o valor de normalização ideal para 8 bits
    if c is None or c <= 0:
        c = 255.0 / math.log(1.0 + 255.0)  # c ≈ 45.986

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            r = matriz[y][x]

            # É somado 1 ao pixel (1 + r) para evitar log(0), que seria indefinido (-infinito)
            # max(0, r) previne qualquer valor negativo acidental
            s = c * math.log(1.0 + max(0, r))

            # Arredonda e limita para [0, 255]
            linha.append(clamp(s))
        resultado.append(linha)

    return resultado


# =============================================================================
# 3. FILTRO DE LOGARITMO INVERSO / EXPONENCIAL (UNIDADE 3)
# =============================================================================
def filtro_logaritmo_inverso(matriz: List[List[int]], c: float | None = None) -> List[List[int]]:
    """
    Transformação de Logaritmo Inverso (Função Exponencial):
    -------------------------------------------------------
    Dedução Algébrica a partir do Logaritmo:
        Partindo de:
            s = c * ln(1 + r)
        Isolando 'r' em termos de 's':
            s / c = ln(1 + r)
            e^(s / c) = 1 + r
            r = e^(s / c) - 1

        Aplicando agora essa relação sobre o pixel de entrada 'r':
            s = exp(r / c) - 1

    Variáveis:
        - r: Intensidade de entrada, r ∈ [0, 255]
        - s: Intensidade resultante de saída, s ∈ [0, 255]
        - c: Fator de escala, c = 255 / ln(256) ≈ 45.986

    Fundamentação Teórica:
        - Atua de maneira estritamente oposta ao logaritmo:
          COMPRIME os valores escuros e EXPANDE a faixa dinâmica dos tons claros.
        - Se uma imagem tiver baixíssimo contraste nas áreas claras (altas intensidades),
          o logaritmo inverso espalha esses tons, revelando variações sutis no branco.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    if c is None or c <= 0:
        c = 255.0 / math.log(1.0 + 255.0)

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            r = matriz[y][x]

            # Aplicação da transformação exponencial inversa: s = e^(r/c) - 1
            s = math.exp(r / c) - 1.0

            linha.append(clamp(s))
        resultado.append(linha)

    return resultado


# =============================================================================
# 4. FILTRO DE POTÊNCIA (CORREÇÃO DE GAMMA - UNIDADE 3)
# =============================================================================
def filtro_potencia(matriz: List[List[int]], gamma: float = 1.0) -> List[List[int]]:
    """
    Transformação de Potência (Lei de Potência / Correção de Gamma):
    --------------------------------------------------------------
    Fórmula Matemática:
        s = c * (r ^ gamma)

    Determinação da Constante de Normalização 'c':
        Para garantir o mapeamento do intervalo [0, 255] para [0, 255]:
            255 = c * (255 ^ gamma)
            c = 255 / (255 ^ gamma)

    Fundamentação Teórica da Curva Gamma:
        - gamma = 1: A transformação é uma reta identidade (s = r), imagem inalterada.
        - gamma > 1: A curva se projeta para baixo da diagonal. Comprime os tons escuros
          e escurece a imagem como um todo. Aumenta a separação de contraste nas altas luzes.
        - gamma < 1: A curva se projeta para cima da diagonal. Expande a faixa de tons escuros,
          clareando a imagem e realçando detalhes ocultos em sombras.
        - Relevância Prática: Tubos CRT, monitores LCD e sensores de câmeras possuem respostas
          não-lineares à luz que seguem leis de potência. A correção de gamma calibra a exibição
          fiel das imagens nesses dispositivos.
    """
    if gamma <= 0:
        raise ValueError("O parâmetro Gamma deve ser estritamente maior que 0.")

    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    # Constante de escala c para garantir saída máxima de 255 quando entrada for 255
    c = 255.0 / math.pow(255.0, gamma)

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            r = max(0, matriz[y][x])

            # Aplicação da lei de potência: s = c * r^gamma
            s = c * math.pow(r, gamma)

            linha.append(clamp(s))
        resultado.append(linha)

    return resultado


# =============================================================================
# 5. FILTRO DE RAIZ (CORREÇÃO DE GAMMA INVERSA - UNIDADE 3)
# =============================================================================
def filtro_raiz(matriz: List[List[int]], gamma: float = 2.0) -> List[List[int]]:
    """
    Transformação de Raiz (Raiz de Índice Gamma):
    --------------------------------------------
    Fórmula Matemática:
        s = c * (r ^ (1 / gamma))
        onde c = 255 / (255 ^ (1 / gamma)).

    Relação com a Lei de Potência:
        - Matematicamente, a raiz de índice γ de um número é identicamente igual à
          potência com expoente fracionário (1 / γ):
              ⁿ√r = r^(1/n)
        - Portanto, quando o usuário seleciona gamma = 2, aplica-se a raiz quadrada (r^0.5).
        - Quando o usuário seleciona gamma = 3, aplica-se a raiz cúbica (r^(1/3)).
        - Efeito Visual: Por possuir expoente efetivo menor que 1, a raiz sempre produz
          uma curva convexa que clareia as sombras e expande detalhes escuros.
    """
    if gamma <= 0:
        raise ValueError("O parâmetro Gamma para a raiz deve ser maior que 0.")

    # Reutiliza a função de potência passando o expoente inverso (1.0 / gamma)
    return filtro_potencia(matriz, gamma=1.0 / gamma)


# =============================================================================
# 6. FILTRO DE EXPANSÃO LINEAR: g = a * r + b
# =============================================================================
def filtro_expansao(matriz: List[List[int]], a: float = 1.0, b: float = 0.0) -> List[List[int]]:
    """
    Filtro de Expansão Linear (Ajuste de Ganho e Offset):
    -----------------------------------------------------
    Fórmula Matemática:
        g(x, y) = a * r(x, y) + b

    Parâmetros:
        - 'a' (Coeficiente Angular / Ganho):
            Multiplica a intensidade original. Se a > 1, afasta os níveis de cinza
            uns dos outros, AUMENTANDO O CONTRASTE da imagem.
            Se a < 1, aproxima os níveis de cinza, reduzindo o contraste.
        - 'b' (Coeficiente Linear / Offset / Deslocamento):
            Adiciona um valor constante a todos os pixels. Controla o BRILHO geral.
            Se b > 0, clareia uniformemente a cena. Se b < 0, escurece uniformemente.

    Tratamento de Overflow:
        - Quaisquer valores resultantes g > 255 são truncados (clamping) em 255.
        - Quaisquer valores g < 0 são truncados em 0.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            r = matriz[y][x]

            # g = a * r + b (ampliação linear de contraste com adição de brilho)
            g = a * r + b

            linha.append(clamp(g))
        resultado.append(linha)

    return resultado


# =============================================================================
# 7. FILTRO DE COMPRESSÃO LINEAR: g = (r / a) - b
# =============================================================================
def filtro_compressao(matriz: List[List[int]], a: float = 1.0, b: float = 0.0) -> List[List[int]]:
    """
    Filtro de Compressão Linear:
    ----------------------------
    Fórmula Matemática:
        g(x, y) = (r(x, y) / a) - b

    Parâmetros:
        - 'a' (Fator Divisor de Escala, a ≠ 0):
            Reduz a amplitude dinâmica da imagem por um fator 'a'.
            Se a > 1, diminui a diferença de luminosidade entre o pixel mais claro
            e o mais escuro, COMPRIMINDO o contraste.
        - 'b' (Deslocamento de Redução de Brilho):
            Subtrai uma quantidade constante após a divisão, rebaixando a média geral.

    Fundamentação Teórica:
        - Comprime o histograma para uma faixa mais estreita de tons.
        - Útil para preparar imagens para canais com limitação de bits ou quantização reduzida.
    """
    if a == 0:
        raise ValueError("O coeficiente divisor 'a' na compressão não pode ser zero.")

    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            r = matriz[y][x]

            # g = (r / a) - b (compressão dinâmica do contraste com subtração de offset)
            g = (r / a) - b

            linha.append(clamp(g))
        resultado.append(linha)

    return resultado


# =============================================================================
# 8. SOMA DE DUAS IMAGENS COM OPÇÃO DE PORCENTAGEM (BLENDING PONDERADO)
# =============================================================================
def somar_imagens(
    matriz1: List[List[int]],
    matriz2: List[List[int]],
    porcentagem: float = 50.0
) -> List[List[int]]:
    """
    Soma Ponderada de Duas Imagens (Combinação Linear Convexa / Image Blending):
    --------------------------------------------------------------------------
    Fórmula Matemática:
        p1 = porcentagem / 100.0
        p2 = (100.0 - porcentagem) / 100.0 = 1.0 - p1

        g(x, y) = p1 * I1(x, y) + p2 * I2(x, y)

    Propriedade da Combinação Convexa:
        - Como p1 >= 0, p2 >= 0 e p1 + p2 = 1.0, o valor máximo possível de g(x, y)
          é garantidamente menor ou igual ao valor máximo das imagens de entrada:
              max(g) = p1 * 255 + p2 * 255 = (p1 + p2) * 255 = 255
        - Isso previne matematicamente o problema de 'estouro' ou overflow (soma > 255)
          que ocorreria em uma soma aritmética ingênua I1 + I2.

    Aplicações Práticas:
        1. Efeito de fusão suave / transição gradual (Cross-Dissolve) em edição de vídeo.
        2. Média temporal para redução de ruído: somar N fotos estáticas atenua o ruído
           aleatório por um fator de √N.
        3. Marca d'água digital e sobreposição gráfica.
    """
    if not (0.0 <= porcentagem <= 100.0):
        raise ValueError("A porcentagem deve estar estritamente no intervalo de 0 a 100.")

    altura1 = len(matriz1)
    largura1 = len(matriz1[0]) if altura1 > 0 else 0

    altura2 = len(matriz2)
    largura2 = len(matriz2[0]) if altura2 > 0 else 0

    if altura1 == 0 or largura1 == 0:
        return []

    # Pesos normalizados de cada imagem no intervalo [0.0, 1.0]
    peso1 = porcentagem / 100.0
    peso2 = (100.0 - porcentagem) / 100.0

    resultado: List[List[int]] = []

    for y in range(altura1):
        linha: List[int] = []
        # Reamostragem proporcional de coordenadas caso a imagem 2 tenha dimensões diferentes
        y2 = min(altura2 - 1, int(y * altura2 / altura1)) if altura2 > 0 else 0

        for x in range(largura1):
            x2 = min(largura2 - 1, int(x * largura2 / largura1)) if largura2 > 0 else 0

            val1 = matriz1[y][x]
            val2 = matriz2[y2][x2] if (altura2 > 0 and largura2 > 0) else 0

            # Combinação linear ponderada: g = p1 * I1 + p2 * I2
            valor_combinado = peso1 * val1 + peso2 * val2

            linha.append(clamp(valor_combinado))
        resultado.append(linha)

    return resultado


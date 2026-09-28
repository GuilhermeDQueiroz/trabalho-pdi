"""
===============================================================================
MÓDULO: TRANSFORMAÇÕES GEOMÉTRICAS E REAMOSTRAGEM (PDI - UNIDADE 2)
===============================================================================
Em PDI, as transformações geométricas alteram a relação espacial entre os pixels.
Consistem em duas operações centrais:
    1. Transformação de coordenadas espaciais: (x, y) = T{(x', y')}
    2. Reamostragem / Interpolação de intensidade: atribuição do valor de cinza
       aos pixels da nova malha discretizada.

Este módulo implementa do zero:
    - Ampliação por Replicação de Pixels (Nearest Neighbor) para 512x512 e 1024x1024
    - Ampliação por Interpolação Bilinear (Bilinear Resampling) para 512x512 e 1024x1024
    - Espelhamento Horizontal e Vertical
    - Rotações de 90° (Horário e Anti-Horário) e 180°
"""

import math
from typing import List
from .utils import clamp


# =============================================================================
# 1. AMPLIAÇÃO POR REPLICAÇÃO DE PIXELS (NEAREST NEIGHBOR RESAMPLING)
# =============================================================================
def ampliacao_replicacao(
    matriz: List[List[int]],
    nova_largura: int = 512,
    nova_altura: int = 512
) -> List[List[int]]:
    """
    Ampliação por Replicação de Pixels (Vizinho Mais Próximo - Unidade 2):
    ---------------------------------------------------------------------
    Estratégia de Mapeamento Inverso (Inverse Mapping):
        Para evitar 'buracos' (lacunas de pixels não preenchidos) na imagem gerada,
        o algoritmo itera sobre cada posição da imagem de DESTINO (y', x') e busca
        sua coordenada correspondente na imagem de ORIGEM (y, x).

    Fórmula Matemática do Mapeamento Discreto:
        Dadas as dimensões de entrada (W_in, H_in) e de saída (W_out, H_out):
            fator_y = (H_in - 1) / (H_out - 1)
            fator_x = (W_in - 1) / (W_out - 1)

        Coordenadas mapeadas no espaço original:
            y = round(y' * fator_y)
            x = round(x' * fator_x)

        Atribuição direta de intensidade:
            I_novo(y', x') = I_orig(y, x)

    Fundamentação Teórica:
        - Para cada pixel da nova malha, seleciona o pixel discreto espacialmente mais próximo
          na malha original.
        - Por exemplo, na ampliação de 256x256 para 512x512, cada pixel original é repetido
          em um bloco de 2x2 pixels; para 1024x1024, em blocos de 4x4.
        - Vantagem: Altíssima eficiência computacional (apenas arredondamentos de ponto flutuante).
        - Desvantagem: Introduz artefatos de blocagem ("pixelização") e serrilhamento visual
          acentuado ao longo de bordas inclinadas.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    if altura == 0 or largura == 0:
        return []

    resultado: List[List[int]] = []

    # Fatores de escala para normalizar o mapeamento contínuo entre [0, dim_out - 1] e [0, dim_in - 1]
    fator_y = (altura - 1) / float(nova_altura - 1) if nova_altura > 1 else 0.0
    fator_x = (largura - 1) / float(nova_largura - 1) if nova_largura > 1 else 0.0

    # Varredura sobre as linhas da imagem de destino
    for y_novo in range(nova_altura):
        linha: List[int] = []

        # Calcula a linha mais próxima na matriz original com arredondamento
        y_orig = min(altura - 1, int(round(y_novo * fator_y)))

        # Varredura sobre as colunas da imagem de destino
        for x_novo in range(nova_largura):
            # Calcula a coluna mais próxima na matriz original com arredondamento
            x_orig = min(largura - 1, int(round(x_novo * fator_x)))

            # Atribui o valor do pixel mais próximo
            linha.append(matriz[y_orig][x_orig])

        resultado.append(linha)

    return resultado


# =============================================================================
# 2. AMPLIAÇÃO POR INTERPOLAÇÃO BILINEAR (BILINEAR RESAMPLING)
# =============================================================================
def ampliacao_bilinear(
    matriz: List[List[int]],
    nova_largura: int = 512,
    nova_altura: int = 512
) -> List[List[int]]:
    """
    Ampliação por Interpolação Bilinear (Unidade 2):
    -----------------------------------------------
    Fundamentação Teórica:
        A interpolação bilinear estima a intensidade de um ponto contínuo (x_cont, y_cont)
        a partir de uma média ponderada dos 4 vizinhos discretos mais próximos que o cercam.

    Etapas e Fórmulas Matemáticas:
        1. Mapeamento para coordenadas contínuas no espaço original:
           y_cont = y' * (H_in - 1) / (H_out - 1)
           x_cont = x' * (W_in - 1) / (W_out - 1)

        2. Localização dos 4 vértices inteiros do quadrado unitário envolvente:
           y1 = ⌊y_cont⌋ ,  y2 = min(y1 + 1, H_in - 1)
           x1 = ⌊x_cont⌋ ,  x2 = min(x1 + 1, W_in - 1)

        3. Cálculo dos pesos de distância fracionária normalizados em [0, 1):
           dy = y_cont - y1  (proximidade vertical da borda inferior)
           dx = x_cont - x1  (proximidade horizontal da borda direita)

        4. Interpolação ponderada bidimensional (combinação bilinear):
           f(y', x') = (1 - dx) * (1 - dy) * I(y1, x1)  [peso vértice sup. esquerdo]
                     + dx       * (1 - dy) * I(y1, x2)  [peso vértice sup. direito]
                     + (1 - dx) * dy       * I(y2, x1)  [peso vértice inf. esquerdo]
                     + dx       * dy       * I(y2, x2)  [peso vértice inf. direito]

    Efeito Visual:
        - A soma dos 4 pesos: (1-dx)(1-dy) + dx(1-dy) + (1-dx)dy + dx*dy = 1.0 (garante conservação de energia).
        - Produz gradientes contínuos e suaves entre pixels.
        - Elimina completamente o aspecto quadriculado do vizinho mais próximo,
          sendo o padrão para redimensionamento de alta qualidade em computação gráfica e PDI.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    if altura == 0 or largura == 0:
        return []

    resultado: List[List[int]] = []

    fator_y = (altura - 1) / float(nova_altura - 1) if nova_altura > 1 else 0.0
    fator_x = (largura - 1) / float(nova_largura - 1) if nova_largura > 1 else 0.0

    for y_novo in range(nova_altura):
        linha: List[int] = []

        # Posição vertical contínua na matriz de origem
        y_cont = y_novo * fator_y
        y1 = int(math.floor(y_cont))
        y2 = min(y1 + 1, altura - 1)
        dy = y_cont - y1  # Fração decimal de deslocamento vertical em [0, 1)

        for x_novo in range(nova_largura):
            # Posição horizontal contínua na matriz de origem
            x_cont = x_novo * fator_x
            x1 = int(math.floor(x_cont))
            x2 = min(x1 + 1, largura - 1)
            dx = x_cont - x1  # Fração decimal de deslocamento horizontal em [0, 1)

            # Leitura das intensidades dos 4 vizinhos adjacentes
            v11 = matriz[y1][x1]  # Vértice (y1, x1): superior esquerdo
            v12 = matriz[y1][x2]  # Vértice (y1, x2): superior direito
            v21 = matriz[y2][x1]  # Vértice (y2, x1): inferior esquerdo
            v22 = matriz[y2][x2]  # Vértice (y2, x2): inferior direito

            # Aplicação da fórmula bilinear completa
            interpolado = (
                (1.0 - dx) * (1.0 - dy) * v11
                + dx * (1.0 - dy) * v12
                + (1.0 - dx) * dy * v21
                + dx * dy * v22
            )

            # Trunca e converte para número inteiro [0, 255]
            linha.append(clamp(interpolado))
        resultado.append(linha)

    return resultado


# =============================================================================
# 3. ESPELHAMENTO HORIZONTAL (FLIP HORIZONTAL)
# =============================================================================
def espelhamento_horizontal(matriz: List[List[int]]) -> List[List[int]]:
    """
    Espelhamento Horizontal:
    ------------------------
    Fórmula Matemática:
        I_novo(y, x) = I_orig(y, W - 1 - x)

    Fundamentação Teórica:
        - Reflete a imagem em relação ao eixo vertical central (como olhar num espelho).
        - A ordem das colunas de cada linha é invertida, mantendo as linhas inalteradas.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    resultado: List[List[int]] = []
    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            # Pega o pixel simétrico no eixo horizontal
            linha.append(matriz[y][largura - 1 - x])
        resultado.append(linha)
    return resultado


# =============================================================================
# 4. ESPELHAMENTO VERTICAL (FLIP VERTICAL)
# =============================================================================
def espelhamento_vertical(matriz: List[List[int]]) -> List[List[int]]:
    """
    Espelhamento Vertical:
    ----------------------
    Fórmula Matemática:
        I_novo(y, x) = I_orig(H - 1 - y, x)

    Fundamentação Teórica:
        - Reflete a imagem de ponta-cabeça em relação ao eixo horizontal central.
        - As linhas são invertidas (a primeira vira a última), mantendo as colunas.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    resultado: List[List[int]] = []
    for y in range(altura):
        linha: List[int] = []
        # Linha simétrica de baixo para cima
        y_invertido = altura - 1 - y
        for x in range(largura):
            linha.append(matriz[y_invertido][x])
        resultado.append(linha)
    return resultado


# =============================================================================
# 5. ROTAÇÃO 90º HORÁRIO (CLOCKWISE)
# =============================================================================
def rotacao_90_horario(matriz: List[List[int]]) -> List[List[int]]:
    """
    Rotação de 90° no Sentido Horário:
    ----------------------------------
    Fórmula Geométrica:
        Dada uma imagem de dimensões H x W:
        A imagem resultante terá dimensões W x H (largura e altura são trocadas).

        Mapeamento de coordenadas:
            Para cada linha y' e coluna x' na nova imagem:
            I_novo(y', x') = I_orig(H - 1 - x', y')

    Fundamentação Teórica:
        - Matematicamente equivale a transpor a matriz e depois espelhar horizontalmente:
          Rot90 = FlipH(Transposta(M)).
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    nova_altura = largura
    nova_largura = altura

    resultado: List[List[int]] = []
    for y_novo in range(nova_altura):
        linha: List[int] = []
        for x_novo in range(nova_largura):
            linha.append(matriz[altura - 1 - x_novo][y_novo])
        resultado.append(linha)
    return resultado


# =============================================================================
# 6. ROTAÇÃO 90º ANTI-HORÁRIO (COUNTER-CLOCKWISE)
# =============================================================================
def rotacao_90_antihorario(matriz: List[List[int]]) -> List[List[int]]:
    """
    Rotação de 90° no Sentido Anti-Horário:
    --------------------------------------
    Fórmula Geométrica:
        Nova imagem com dimensões W x H:
        I_novo(y', x') = I_orig(x', W - 1 - y')

    Fundamentação Teórica:
        - Equivale a girar 270° no sentido horário ou girar -90°.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    nova_altura = largura
    nova_largura = altura

    resultado: List[List[int]] = []
    for y_novo in range(nova_altura):
        linha: List[int] = []
        for x_novo in range(nova_largura):
            linha.append(matriz[x_novo][largura - 1 - y_novo])
        resultado.append(linha)
    return resultado


# =============================================================================
# 7. ROTAÇÃO 180º
# =============================================================================
def rotacao_180(matriz: List[List[int]]) -> List[List[int]]:
    """
    Rotação de 180°:
    ----------------
    Fórmula Geométrica:
        As dimensões permanecem H x W:
        I_novo(y, x) = I_orig(H - 1 - y, W - 1 - x)

    Fundamentação Teórica:
        - Equivale a realizar um espelhamento horizontal seguido de um espelhamento vertical
          (inversão central em relação ao centro geométrico da imagem).
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    resultado: List[List[int]] = []
    for y in range(altura):
        linha: List[int] = []
        y_invertido = altura - 1 - y
        for x in range(largura):
            linha.append(matriz[y_invertido][largura - 1 - x])
        resultado.append(linha)
    return resultado

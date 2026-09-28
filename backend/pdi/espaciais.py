"""
===============================================================================
MÓDULO: FILTROS ESPACIAIS E OPERADORES DE BORDAS (PDI - UNIDADE 3 / 4)
===============================================================================
Em Processamento Digital de Imagens (PDI), a filtragem espacial é uma técnica que
opera diretamente sobre a vizinhança local de cada pixel na imagem, utilizando uma
matriz de coeficientes denominada "máscara", "kernel", "filtro" ou "janela".

Diferença entre Filtragem Linear e Não-Linear:
1. Filtros Lineares (ex: Média, Laplaciano, Prewitt, Sobel):
   - A operação matemática realizada é a convolução/correlação discreta bidimensional.
   - O valor de saída é uma soma ponderada linear dos pixels vizinhos.
2. Filtros Não-Lineares / Filtros de Ordem (ex: Mediana, Moda, Mínimo, Máximo):
   - Baseiam-se na ordenação estatística ou análise de frequência dos pixels vizinhos.
   - Não podem ser expressos como uma simples soma ponderada por coeficientes fixos.

Tratamento de Bordas:
   - Nas bordas da imagem, a máscara espacial ultrapassaria os limites da matriz.
   - Adota-se aqui a técnica de "Replicação de Bordas" (Clamping/Border Replication),
     onde as coordenadas fora do limite são projetadas para o pixel de borda mais próximo.

Fórmulas implementadas em Python puro (sem bibliotecas externas de PDI).
"""

import math
from typing import List, Dict
from .utils import clamp


def _obter_vizinhanca(
    matriz: List[List[int]],
    y: int,
    x: int,
    raio: int,
    altura: int,
    largura: int
) -> List[int]:
    """
    Função Auxiliar: Extrai os valores dos pixels vizinhos em uma janela quadrada (2*raio + 1) x (2*raio + 1).

    Tratamento de Condições de Contorno (Bordas):
        - Utiliza a técnica de 'Replicação de Borda' (Nearest Border Clamping).
        - Para qualquer deslocamento (dy, dx) que resulte em coordenada fora da imagem:
            py = max(0, min(altura - 1, y + dy))
            px = max(0, min(largura - 1, x + dx))
        - Isso evita artefatos pretos nas bordas e garante que a janela sempre tenha
          exatamente (2*raio + 1)^2 elementos válidos.

    Parâmetros:
        matriz: Matriz bidimensional da imagem [altura][largura]
        y, x: Coordenadas centrais do pixel sob análise
        raio: Metade do tamanho da máscara (ex: tamanho 3 -> raio 1; tamanho 5 -> raio 2)
        altura, largura: Dimensões totais da matriz

    Retorna:
        Lista linear contendo as intensidades de todos os pixels na vizinhança.
    """
    vizinhos: List[int] = []

    # Itera sobre o deslocamento vertical no intervalo [-raio, +raio]
    for dy in range(-raio, raio + 1):
        # Trunca a coordenada vertical para permanecer dentro de [0, altura - 1]
        py = max(0, min(altura - 1, y + dy))

        # Itera sobre o deslocamento horizontal no intervalo [-raio, +raio]
        for dx in range(-raio, raio + 1):
            # Trunca a coordenada horizontal para permanecer dentro de [0, largura - 1]
            px = max(0, min(largura - 1, x + dx))

            # Adiciona o pixel vizinho correspondente à lista
            vizinhos.append(matriz[py][px])

    return vizinhos


# =============================================================================
# 1. FILTRO DA MÉDIA (PASSA-BAIXA LINEAR)
# =============================================================================
def filtro_media(matriz: List[List[int]], tamanho_mascara: int = 3) -> List[List[int]]:
    """
    Filtro da Média (Passa-Baixa / Suavização Espacial):
    ---------------------------------------------------
    Fórmula Matemática:
        g(x, y) = (1 / M) * ∑ ∑ f(x + s, y + t)
                  onde (s, t) ∈ S e M = N * N (área da máscara)

    Representação da Máscara N x N (todos os pesos iguais a 1/N²):
        Para máscara 3x3 (M = 9):
            w = (1/9) * [ 1  1  1 ]
                        [ 1  1  1 ]
                        [ 1  1  1 ]

    Fundamentação Teórica:
        - O filtro da média substitui o valor de cada pixel pela média aritmética
          das intensidades de seus vizinhos definidos pela janela de tamanho N x N.
        - Efeito no Domínio da Frequência: É um filtro Passa-Baixa (Low-Pass Filter).
          Atenua componentes de altas frequências (bordas, texturas finas e ruídos)
          e preserva componentes de baixas frequências (regiões homogêneas).
        - Efeito Visual: Produz suavização ("blurring" ou desfoque), reduz ruídos
          aleatórios gaussianos, mas em contrapartida borra as bordas dos objetos.
        - Parâmetro: 'tamanho_mascara' deve ser um inteiro ímpar positivo (3, 5, 7, etc.).
    """
    # Validação e garantia de máscara ímpar positiva (3, 5, 7...)
    tamanho_mascara = int(tamanho_mascara)
    if tamanho_mascara < 1 or tamanho_mascara % 2 == 0:
        tamanho_mascara = 3

    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    # Raio da máscara: raio = floor(tamanho_mascara / 2) (ex: 3 -> raio 1; 5 -> raio 2)
    raio = tamanho_mascara // 2

    # Área total da máscara: M = N² (número de pixels abrangidos pela janela)
    area = float(tamanho_mascara * tamanho_mascara)

    resultado: List[List[int]] = []

    # Varredura linha por linha (eixo y)
    for y in range(altura):
        linha: List[int] = []

        # Varredura coluna por coluna (eixo x)
        for x in range(largura):
            # Coleta os N² pixels dentro da janela centrada em (y, x)
            vizinhos = _obter_vizinhanca(matriz, y, x, raio, altura, largura)

            # Somatório dos valores de intensidade: ∑ f(x + s, y + t)
            soma = sum(vizinhos)

            # Cálculo da média aritmética ponderada: g(x, y) = soma / M
            media = round(soma / area)

            # Garante que o nível de cinza resultante esteja no intervalo [0, 255]
            linha.append(clamp(media))

        resultado.append(linha)

    return resultado


# =============================================================================
# 2. FILTRO DA MEDIANA (ESTATÍSTICO NÃO-LINEAR DE ORDEM)
# =============================================================================
def filtro_mediana(matriz: List[List[int]], tamanho_mascara: int = 3) -> List[List[int]]:
    """
    Filtro da Mediana (Estatístico de Ordem):
    -----------------------------------------
    Fórmula Matemática:
        g(x, y) = mediana { f(x + s, y + t) : (s, t) ∈ S }

    Processo Algorítmico:
        1. Coleta todos os N² valores de intensidade na vizinhança S.
        2. Ordena esses valores em ordem crescente:
           v_ord = [v_(1) <= v_(2) <= ... <= v_(k) <= ... <= v_(N²)]
        3. Seleciona o elemento central de índice meio = ⌊N² / 2⌋:
           g(x, y) = v_ord[meio]

    Fundamentação Teórica:
        - Ao contrário do filtro da média, a mediana NÃO cria novos valores de níveis
          de cinza (sempre escolhe um valor já existente na vizinhança).
        - Propriedade Chave: É extremamente eficaz na remoção de ruídos impulsivos
          bipolares (conhecidos como 'Ruído Sal e Pimenta' ou salt-and-pepper noise),
          onde pixels isolados assumem valores extremos (0 ou 255). Como 0 e 255
          ficam nas pontas do vetor ordenado, a mediana quase nunca os seleciona.
        - Preservação de Bordas: Mantém a nitidez de descontinuidades e transições
          abruptas muito melhor do que filtros lineares de suavização (como a média).
    """
    tamanho_mascara = int(tamanho_mascara)
    if tamanho_mascara < 1 or tamanho_mascara % 2 == 0:
        tamanho_mascara = 3

    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0
    raio = tamanho_mascara // 2

    # Posição do elemento mediano central após a ordenação (índice 4 em máscara 3x3 com 9 elementos)
    meio = (tamanho_mascara * tamanho_mascara) // 2

    resultado: List[List[int]] = []

    # Percorre cada linha da imagem
    for y in range(altura):
        linha: List[int] = []

        # Percorre cada coluna da imagem
        for x in range(largura):
            # Extrai os N² pixels da vizinhança quadrada
            vizinhos = _obter_vizinhanca(matriz, y, x, raio, altura, largura)

            # Ordena os valores vizinhos em ordem não-decrescente
            vizinhos.sort()

            # O valor resultante é o elemento estritamente central da lista ordenada
            linha.append(vizinhos[meio])

        resultado.append(linha)

    return resultado


# =============================================================================
# 3. FILTRO DA MODA (ESTATÍSTICO DE FREQUÊNCIA)
# =============================================================================
def filtro_moda(matriz: List[List[int]], tamanho_mascara: int = 3) -> List[List[int]]:
    """
    Filtro da Moda (Estatístico de Frequência):
    ------------------------------------------
    Fórmula Matemática:
        g(x, y) = argmax_v { Contagem(v) : v ∈ Vizinhança(x, y) }

    Fundamentação Teórica:
        - Substitui o pixel central pelo nível de cinza mais frequente (de maior ocorrência)
          dentro da máscara local N x N.
        - Caso haja empate na contagem máxima, a implementação mantém preferencialmente o
          valor original do pixel central f(x, y) para evitar alterações desnecessárias.
        - Efeito Visual: Promove homogeneização de regiões texturizadas e atua como uma
          ferramenta de segmentação/agrupamento local de tons predominantes.
    """
    tamanho_mascara = int(tamanho_mascara)
    if tamanho_mascara < 1 or tamanho_mascara % 2 == 0:
        tamanho_mascara = 3

    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0
    raio = tamanho_mascara // 2

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            # Coleta os pixels da janela centrada em (y, x)
            vizinhos = _obter_vizinhanca(matriz, y, x, raio, altura, largura)

            # Constrói o histograma de frequência local (dicionário valor -> contagem)
            contagens: Dict[int, int] = {}
            for v in vizinhos:
                contagens[v] = contagens.get(v, 0) + 1

            # Inicializa a moda com o valor atual do pixel central
            moda = matriz[y][x]
            max_contagem = contagens.get(moda, 0)

            # Busca o valor com a frequência estritamente maior
            for val, qtd in contagens.items():
                if qtd > max_contagem:
                    max_contagem = qtd
                    moda = val

            linha.append(moda)
        resultado.append(linha)

    return resultado


# =============================================================================
# 4. FILTRO MÍNIMO (EROSÃO / ESTATÍSTICA DE ORDEM MÍNIMA)
# =============================================================================
def filtro_minimo(matriz: List[List[int]], tamanho_mascara: int = 3) -> List[List[int]]:
    """
    Filtro MÍNIMO (Estatística de Ordem Mínima / Análogo à Erosão Morfológica em Cinza):
    ----------------------------------------------------------------------------------
    Fórmula Matemática:
        g(x, y) = min { f(x + s, y + t) : (s, t) ∈ S }

    Fundamentação Teórica:
        - Atribui à posição central o menor nível de cinza presente na vizinhança N x N.
        - Efeito em Ruídos: Elimina completamente ruídos impulsivos claros e isolados
          (ruído tipo 'Sal' - pontos brancos de intensidade 255).
        - Efeito Visual: Provoca o escurecimento geral da imagem e o espessamento/expansão
          de estruturas e regiões escuras (reduzindo áreas claras).
    """
    tamanho_mascara = int(tamanho_mascara)
    if tamanho_mascara < 1 or tamanho_mascara % 2 == 0:
        tamanho_mascara = 3

    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0
    raio = tamanho_mascara // 2

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            # Obtém a vizinhança local
            vizinhos = _obter_vizinhanca(matriz, y, x, raio, altura, largura)

            # Seleciona o valor mínimo entre todos os vizinhos
            linha.append(min(vizinhos))
        resultado.append(linha)

    return resultado


# =============================================================================
# 5. FILTRO MÁXIMO (DILATAÇÃO / ESTATÍSTICA DE ORDEM MÁXIMA)
# =============================================================================
def filtro_maximo(matriz: List[List[int]], tamanho_mascara: int = 3) -> List[List[int]]:
    """
    Filtro MÁXIMO (Estatística de Ordem Máxima / Análogo à Dilatação Morfológica em Cinza):
    -------------------------------------------------------------------------------------
    Fórmula Matemática:
        g(x, y) = max { f(x + s, y + t) : (s, t) ∈ S }

    Fundamentação Teórica:
        - Atribui à posição central o maior nível de cinza presente na vizinhança N x N.
        - Efeito em Ruídos: Elimina completamente ruídos impulsivos escuros e isolados
          (ruído tipo 'Pimenta' - pontos pretos de intensidade 0).
        - Efeito Visual: Provoca o clareamento geral da imagem e a expansão de estruturas
          claras (reduzindo áreas escuras).
    """
    tamanho_mascara = int(tamanho_mascara)
    if tamanho_mascara < 1 or tamanho_mascara % 2 == 0:
        tamanho_mascara = 3

    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0
    raio = tamanho_mascara // 2

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            # Obtém a vizinhança local
            vizinhos = _obter_vizinhanca(matriz, y, x, raio, altura, largura)

            # Seleciona o valor máximo entre todos os vizinhos
            linha.append(max(vizinhos))
        resultado.append(linha)

    return resultado


# =============================================================================
# 6. OPERADOR LAPLACIANO (DETECÇÃO DE BORDAS DE SEGUNDA DERIVADA)
# =============================================================================
def filtro_laplaciano(matriz: List[List[int]], tamanho_mascara: int = 3) -> List[List[int]]:
    """
    Operador Laplaciano (Segunda Derivada / Realce Isotrópico de Bordas):
    -------------------------------------------------------------------
    Fórmula Contínua:
        ∇²f = ∂²f/∂x² + ∂²f/∂y²

    Aproximação por Diferenças Finitas Discretas (incluindo diagonais):
        ∇²f(x, y) = ∑ ∑ w(s, t) * f(x + s, y + t)

    Máscara Padrão 3x3 Isotrópica (todas as 8 direções):
        w = [ -1  -1  -1 ]
            [ -1   8  -1 ]
            [ -1  -1  -1 ]
        Note que a soma de todos os coeficientes da máscara é 0 (-1*8 + 8 = 0),
        o que garante resposta nula em áreas homogêneas de intensidade constante.

    Generalização para Máscara N x N Ímpar:
        - Coeficiente Central: w_centro = N² - 1
        - Demais Coeficientes: w_periferia = -1

    Fundamentação Teórica:
        - O Laplaciano é um operador derivativo isotrópico (invariante à rotação).
        - A segunda derivada produz passagens por zero (zero-crossings) exatamente
          no centro das bordas de descontinuidade de intensidade.
        - Realça transições abruptas, detalhes finos e linhas finas, mas também
          amplifica ruídos de alta frequência presentes na imagem.
    """
    tamanho_mascara = int(tamanho_mascara)
    if tamanho_mascara < 1 or tamanho_mascara % 2 == 0:
        tamanho_mascara = 3

    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0
    raio = tamanho_mascara // 2
    meio = raio

    # Construção da máscara Laplaciana generalizada N x N
    # Centro = N² - 1; Todos os outros elementos = -1
    mascara: List[List[int]] = []
    for i in range(tamanho_mascara):
        linha_m: List[int] = []
        for j in range(tamanho_mascara):
            if i == meio and j == meio:
                linha_m.append(tamanho_mascara * tamanho_mascara - 1)
            else:
                linha_m.append(-1)
        mascara.append(linha_m)

    resultado: List[List[int]] = []

    # Itera sobre cada pixel da imagem
    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            soma = 0
            # Convolução espacial 2D com a máscara Laplaciana
            for dy in range(-raio, raio + 1):
                py = max(0, min(altura - 1, y + dy))
                for dx in range(-raio, raio + 1):
                    px = max(0, min(largura - 1, x + dx))
                    peso = mascara[dy + raio][dx + raio]
                    soma += matriz[py][px] * peso

            # Aplica clamp para garantir faixa válida [0, 255] (cortando respostas negativas)
            linha.append(clamp(soma))
        resultado.append(linha)

    return resultado


# =============================================================================
# 7. FILTRO HIGH BOOST (REALCE DE ALTAS FREQUÊNCIAS COM GANHO 'A')
# =============================================================================
def filtro_high_boost(
    matriz: List[List[int]],
    tamanho_mascara: int = 3,
    ampliacao: float = 1.5
) -> List[List[int]]:
    """
    Filtro High Boost (Unsharp Masking com Ganho A):
    ------------------------------------------------
    Fórmula Matemática:
        Passo 1 (Máscara de Nitidez):
            f_mask(x, y) = f(x, y) - f_suavizada(x, y)
            onde f_suavizada(x, y) é obtida aplicando o filtro da média.

        Passo 2 (Adição da Máscara Amplificada):
            f_hb(x, y) = f(x, y) + k * f_mask(x, y)
                       = f(x, y) + (A - 1) * (f(x, y) - f_suavizada(x, y))

    Equivalência Teórica:
        f_hb(x, y) = A * f(x, y) - f_suavizada(x, y)

    Análise do Fator de Ampliação 'A':
        - Se A = 1 (k = 0): Não há realce de máscara, equivale à imagem original.
        - Se A > 1 (k = A - 1 > 0): Filtro High Boost tradicional. Preserva a tonalidade
          e brilho de fundo da imagem original, adicionando um reforço pronunciado
          nas bordas e componentes de alta frequência.
        - Diferença em relação à máscara de nitidez pura: A máscara de nitidez pura pode
          gerar imagens com fundo escurecido; o High Boost mantém o nível médio de cinza.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    # 1. Gera a versão suavizada (passa-baixa) da imagem usando o filtro da média
    suavizada = filtro_media(matriz, tamanho_mascara=tamanho_mascara)

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            orig = matriz[y][x]           # Pixel original f(x, y)
            suav = suavizada[y][x]        # Pixel suavizado f_suav(x, y)

            # Aplicação da fórmula High Boost:
            # f_hb = f_orig + (A - 1) * (f_orig - f_suav)
            val = orig + (ampliacao - 1.0) * (orig - suav)

            # Limita ao intervalo [0, 255]
            linha.append(clamp(val))
        resultado.append(linha)

    return resultado


# =============================================================================
# 8. OPERADOR DE PREWITT (GRADIENTE DIRECIONAL DE PRIMEIRA DERIVADA)
# =============================================================================
def filtro_prewitt(matriz: List[List[int]]) -> List[List[int]]:
    """
    Operador Prewitt de Detecção de Bordas (Primeira Derivada):
    ----------------------------------------------------------
    Fundamentação Matemática do Gradiente Contínuo:
        ∇f = [ ∂f/∂x , ∂f/∂y ]^T
        Magnitude: M(x, y) = ||∇f|| = √( (∂f/∂x)² + (∂f/∂y)² )

    Máscaras de Convolução 3x3 de Prewitt:
        Gx (Gradiente Horizontal - detecta bordas verticais):
            Gx = [ -1   0   1 ]
                 [ -1   0   1 ]
                 [ -1   0   1 ]

        Gy (Gradiente Vertical - detecta bordas horizontais):
            Gy = [ -1  -1  -1 ]
                 [  0   0   0 ]
                 [  1   1   1 ]

    Fórmula da Magnitude Combinada:
        M(x, y) = √( Gx(x, y)² + Gy(x, y)² )

    Fundamentação Teórica:
        - O operador Prewitt estima as derivadas espaciais parciais usando diferenças
          finitas centradas combinadas com uma média simples na direção ortogonal.
        - Realça contornos e bordas onde a variação de intensidade é rápida.
        - Saída delimitada ao intervalo de níveis de cinza [0, 255].
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    # Máscara do gradiente horizontal Gx (coluna direita menos coluna esquerda)
    gx_mask = [
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ]

    # Máscara do gradiente vertical Gy (linha inferior menos linha superior)
    gy_mask = [
        [-1, -1, -1],
        [ 0,  0,  0],
        [ 1,  1,  1]
    ]

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            gx = 0
            gy = 0

            # Convolução com as janelas 3x3 no entorno de (y, x)
            for dy in (-1, 0, 1):
                # Replicação de borda nas extremidades
                py = max(0, min(altura - 1, y + dy))
                for dx in (-1, 0, 1):
                    px = max(0, min(largura - 1, x + dx))
                    pixel = matriz[py][px]

                    # Multiplicação pelos pesos das máscaras direcionais
                    gx += pixel * gx_mask[dy + 1][dx + 1]
                    gy += pixel * gy_mask[dy + 1][dx + 1]

            # Cálculo da magnitude do vetor gradiente: M = √(Gx² + Gy²)
            magnitude = math.sqrt(gx * gx + gy * gy)

            linha.append(clamp(magnitude))
        resultado.append(linha)

    return resultado


# =============================================================================
# 9. OPERADOR DE SOBEL (GRADIENTE COM PONDERAÇÃO CENTRAL)
# =============================================================================
def filtro_sobel(matriz: List[List[int]]) -> List[List[int]]:
    """
    Operador Sobel de Detecção de Bordas (Primeira Derivada Ponderada):
    -----------------------------------------------------------------
    Máscaras de Convolução 3x3 de Sobel:
        Gx (Gradiente Horizontal - bordas verticais com peso 2 no centro):
            Gx = [ -1   0   1 ]
                 [ -2   0   2 ]
                 [ -1   0   1 ]

        Gy (Gradiente Vertical - bordas horizontais com peso 2 no centro):
            Gy = [  1   2   1 ]
                 [  0   0   0 ]
                 [ -1  -2  -1 ]

    Fórmula da Magnitude:
        M(x, y) = √( Gx(x, y)² + Gy(x, y)² )

    Diferença Fundamental em Relação ao Prewitt:
        - O operador Sobel introduz um peso maior (2) no pixel central das linhas e
          colunas vizinhas, conferindo uma suavização gaussiana leve integrada à derivação.
        - Isso confere ao Sobel uma IMUNIDADE A RUÍDO superior à do Prewitt, tornando-o
          um dos detectores de bordas baseados em gradiente mais utilizados na prática.
    """
    altura = len(matriz)
    largura = len(matriz[0]) if altura > 0 else 0

    # Máscara Gx com coeficiente central ampliado (peso 2)
    gx_mask = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]

    # Máscara Gy com coeficiente central ampliado (peso 2)
    gy_mask = [
        [ 1,  2,  1],
        [ 0,  0,  0],
        [-1, -2, -1]
    ]

    resultado: List[List[int]] = []

    for y in range(altura):
        linha: List[int] = []
        for x in range(largura):
            gx = 0
            gy = 0

            # Convolução 3x3 centrada em (y, x)
            for dy in (-1, 0, 1):
                py = max(0, min(altura - 1, y + dy))
                for dx in (-1, 0, 1):
                    px = max(0, min(largura - 1, x + dx))
                    pixel = matriz[py][px]

                    gx += pixel * gx_mask[dy + 1][dx + 1]
                    gy += pixel * gy_mask[dy + 1][dx + 1]

            # Magnitude Euclidiana do vetor gradiente: M = √(Gx² + Gy²)
            magnitude = math.sqrt(gx * gx + gy * gy)

            linha.append(clamp(magnitude))
        resultado.append(linha)

    return resultado

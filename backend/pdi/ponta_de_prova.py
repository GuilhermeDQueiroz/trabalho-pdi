"""
===============================================================================
MÓDULO: FUNÇÃO PONTA DE PROVA / PROBE TOOL (PDI - UNIDADE 1 / 2)
===============================================================================
Em Processamento Digital de Imagens (PDI), uma imagem monocromática digital é
formalmente modelada como uma matriz ou função discreta bidimensional:
    f(x, y)
onde:
    - x é a coordenada horizontal (coluna), variando no intervalo discreto [0, W - 1]
    - y é a coordenada vertical (linha), variando no intervalo discreto [0, H - 1]
    - W é a largura (width) e H é a altura (height) da imagem em pixels.
    - O valor f(x, y) representa o Nível de Cinza (NC) ou intensidade luminosa naquele ponto,
      quantizado em 8 bits no intervalo [0, 255] (onde 0 = preto absoluto e 255 = branco absoluto).

A ferramenta Ponta de Prova (Probe Tool) permite inspecionar interativamente
qualquer pixel específico da matriz da imagem, retornando suas coordenadas exatas e seu NC.
"""

from typing import List, Dict, Any


def obter_ponta_de_prova(matrix: List[List[int]], x: int, y: int) -> Dict[str, Any]:
    """
    Obtém o Nível de Cinza (NC) e as coordenadas espaciais do pixel inspecionado.

    Fundamentação Teórica:
        - Valida se o ponto (x, y) requisitado pelo usuário está contido no domínio discreto
          válido da imagem: 0 <= x < largura e 0 <= y < altura.
        - Se estiver dentro do domínio, acessa a posição indexada da matriz como matrix[y][x]
          (lembrando que em estruturas bidimensionais o primeiro índice representa a linha 'y'
           e o segundo índice representa a coluna 'x').
        - Retorna o valor de intensidade luminosa pontual NC = f(x, y).

    Parâmetros:
        matrix: Matriz bidimensional da imagem [altura][largura], com valores em [0, 255]
        x: Coordenada horizontal (coluna, 0 <= x < largura)
        y: Coordenada vertical (linha, 0 <= y < altura)

    Retorno:
        Dicionário contendo:
            - x: Coordenada horizontal inteira consultada
            - y: Coordenada vertical inteira consultada
            - nc: Nível de Cinza (0 a 255) recuperado
            - valido: Booleano indicando se o ponto estava dentro dos limites da imagem
            - largura, altura: Dimensões espaciais da matriz
    """
    height = len(matrix)
    if height == 0:
        return {"x": x, "y": y, "nc": 0, "valido": False, "largura": 0, "altura": 0}
    width = len(matrix[0])

    # Verifica se as coordenadas satisfazem o domínio de definição da imagem: 0 <= y < H e 0 <= x < W
    if 0 <= y < height and 0 <= x < width:
        # Acesso pontual: matrix[linha][coluna] = matrix[y][x]
        nc = int(matrix[y][x])
        return {
            "x": int(x),
            "y": int(y),
            "nc": nc,
            "valido": True,
            "largura": width,
            "altura": height,
        }
    else:
        # Ponto fora dos limites da matriz
        return {
            "x": int(x),
            "y": int(y),
            "nc": 0,
            "valido": False,
            "largura": width,
            "altura": height,
        }

"""
===============================================================================
MÓDULO: UTILITÁRIOS E CONVERSÃO DE FORMATOS (PDI)
===============================================================================
Funções auxiliares para:
1. Saturação / Truncamento numérico (Clamp) para garantir integridade da faixa [0, 255].
2. Decodificação de arquivos gráficos (PNG, JPEG, BMP) e conversão RGB -> Escala de Cinza.
3. Codificação de matrizes bidimensionais em strings Base64 para tráfego via API REST.

OBSERVAÇÃO IMPORTANTE SOBRE CONFORMIDADE:
- Nenhuma biblioteca de processamento de imagens (como OpenCV, PIL ImageFilter ou SciPy)
  é usada para executar os filtros ou algoritmos de PDI.
- A biblioteca Pillow (PIL) é utilizada estritamente na borda do sistema para decodificar
  o arquivo bruto em bytes recebido pela rede e recodificar a matriz resultante em PNG.
"""

import base64
import io
from typing import List, Tuple
from PIL import Image


def clamp(val: float, min_val: int = 0, max_val: int = 255) -> int:
    """
    Função de Saturação Numérica (Clamping / Truncamento):
    -----------------------------------------------------
    Fórmula Matemática:
        clamp(v) = { min_val,   se round(v) < min_val
                   { max_val,   se round(v) > max_val
                   { round(v),  caso contrário

    Fundamentação Teórica:
        - Em processamento digital de imagens com representação inteira de 8 bits (uint8),
          as operações de filtros (ex: convoluções com pesos negativos como Laplaciano,
          Prewitt, Sobel, ou somas e expansões lineares) podem produzir valores que
          extrapolam o intervalo válido:
            * Respostas negativas (< 0): causariam underflow.
            * Respostas maiores que 255 (> 255): causariam overflow.
        - A função 'clamp' satura os valores nos limites estritos [0, 255], garantindo
          a estabilidade numérica e visual da matriz de níveis de cinza.
    """
    if val < min_val:
        return min_val
    if val > max_val:
        return max_val
    return int(round(val))


def base64_to_matrix(base64_str: str) -> List[List[int]]:
    """
    Converte uma string codificada em Base64 para uma matriz bidimensional de cinza.

    Processo:
        1. Remove o cabeçalho URI 'data:image/...;base64,' se presente.
        2. Decodifica a sequência Base64 para o fluxo binário original da imagem.
        3. Delega para bytes_to_matrix para geração da matriz 2D.
    """
    if "," in base64_str:
        base64_str = base64_str.split(",", 1)[1]

    img_bytes = base64.b64decode(base64_str)
    return bytes_to_matrix(img_bytes)


def bytes_to_matrix(img_bytes: bytes) -> List[List[int]]:
    """
    Carrega o fluxo binário de uma imagem e a converte para uma matriz 2D de níveis de cinza.

    Fórmula de Conversão RGB -> Escala de Cinza:
        I(x, y) = round( (R(x, y) + G(x, y) + B(x, y)) / 3.0 )

    Fundamentação Teórica:
        - Cada pixel colorido possui 3 componentes de cor: Vermelho (R), Verde (G) e Azul (B).
        - A média aritmética dos três canais produz o nível de intensidade de cinza monocromático,
          quantizado em [0, 255].
    """
    # Abre a imagem a partir do buffer de memória e garante espaço de cores RGB
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    width, height = img.size
    pixels = img.load()

    matrix: List[List[int]] = []

    # Constrói a matriz linha por linha (eixo y)
    for y in range(height):
        row: List[int] = []
        for x in range(width):
            r, g, b = pixels[x, y]
            # Média aritmética direta dos três canais primários de cor
            cinza = int(round((r + g + b) / 3.0))
            row.append(cinza)
        matrix.append(row)

    return matrix


def matrix_to_base64(matrix: List[List[int]], fmt: str = "PNG") -> str:
    """
    Converte a matriz bidimensional de níveis de cinza [altura][largura]
    em uma string Base64 formatada para exibição direta em tags <img> HTML/Vue.

    Processo:
        1. Cria um bitmap em escala de cinza de 8 bits (modo 'L' do Pillow).
        2. Preenche os pixels aplicando 'clamp' para segurança.
        3. Salva a imagem comprimida em memória (PNG sem perdas).
        4. Retorna a URI com prefixo 'data:image/png;base64,...'.
    """
    height = len(matrix)
    if height == 0:
        return ""
    width = len(matrix[0])

    # Cria nova imagem em modo 'L' (Luminance / 8-bit pixels em tons de cinza)
    img = Image.new("L", (width, height))
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            pixels[x, y] = clamp(matrix[y][x])

    buffer = io.BytesIO()
    img.save(buffer, format=fmt)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/{fmt.lower()};base64,{encoded}"


def get_matrix_dimensions(matrix: List[List[int]]) -> Tuple[int, int]:
    """Retorna a tupla (largura, altura) da matriz de imagem."""
    height = len(matrix)
    width = len(matrix[0]) if height > 0 else 0
    return width, height

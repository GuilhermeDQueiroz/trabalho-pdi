"""
===============================================================================
PACOTE PDI - PROCESSAMENTO DIGITAL DE IMAGENS EM PYTHON PURO
===============================================================================
Este pacote reúne todas as 18 operações de Processamento Digital de Imagens
especificadas na disciplina, implementadas estritamente em Python puro (sem OpenCV,
sem PIL ImageFilter e sem SciPy).

Categorias das Funções Exportadas:
1. Ferramentas de Inspeção:
   - obter_ponta_de_prova (Probe Tool para leitura de f(x, y) = NC)

2. Transformações Pontuais (s = T(r)):
   - filtro_negativo: s = 255 - r
   - filtro_logaritmo: s = c * ln(1 + r)
   - filtro_logaritmo_inverso: s = exp(r / c) - 1
   - filtro_potencia: s = c * r^gamma
   - filtro_raiz: s = c * r^(1 / gamma)
   - filtro_expansao: g = a * r + b
   - filtro_compressao: g = (r / a) - b
   - somar_imagens: g = p * I1 + (1 - p) * I2

3. Transformações Geométricas e Reamostragem:
   - ampliacao_replicacao: Vizinho mais próximo (Nearest Neighbor)
   - ampliacao_bilinear: Interpolação bilinear bidimensional
   - espelhamento_horizontal e espelhamento_vertical
   - rotacao_90_horario, rotacao_90_antihorario e rotacao_180

4. Estatística e Realce de Contraste:
   - calcular_histograma: PDF discreta das intensidades [0..255]
   - equalizar_histograma: CDF acumulada e mapeamento por LUT

5. Filtros Espaciais e Operadores de Bordas:
   - filtro_media: Passa-baixa linear uniforme N x N
   - filtro_mediana: Estatístico de ordem para ruído impulsivo (sal e pimenta)
   - filtro_moda: Estatístico de máxima frequência
   - filtro_minimo: Erosão morfológica em níveis de cinza
   - filtro_maximo: Dilatação morfológica em níveis de cinza
   - filtro_laplaciano: Segunda derivada ∇²f (isotrópico)
   - filtro_high_boost: Nitidez ampliada com ganho A (A*f - f_suav)
   - filtro_prewitt: Gradiente de primeira derivada |Gx| e |Gy|
   - filtro_sobel: Gradiente com ponderação central (imunidade a ruído)
"""

from .ponta_de_prova import obter_ponta_de_prova
from .pontuais import (
    filtro_negativo,
    filtro_logaritmo,
    filtro_logaritmo_inverso,
    filtro_potencia,
    filtro_raiz,
    filtro_expansao,
    filtro_compressao,
    somar_imagens,
)
from .geometricos import (
    ampliacao_replicacao,
    ampliacao_bilinear,
    espelhamento_horizontal,
    espelhamento_vertical,
    rotacao_90_horario,
    rotacao_90_antihorario,
    rotacao_180,
)
from .histograma import (
    calcular_histograma,
    equalizar_histograma,
)
from .espaciais import (
    filtro_media,
    filtro_mediana,
    filtro_moda,
    filtro_minimo,
    filtro_maximo,
    filtro_laplaciano,
    filtro_high_boost,
    filtro_prewitt,
    filtro_sobel,
)
from .processador import (
    aplicar_filtro_individual,
    executar_pipeline,
)
from .utils import (
    base64_to_matrix,
    matrix_to_base64,
    clamp,
)


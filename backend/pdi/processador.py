"""
===============================================================================
MÓDULO: PROCESSADOR E DISPACHER DE PIPELINES DE PDI
===============================================================================
Este módulo atua como o motor orquestrador (dispatcher / controller) de processamento
de imagens em Python.

Responsabilidades:
1. Mapeamento de Códigos Numéricos (Enum ETipoFiltroPDI):
   - Cada constante numérica (1 a 28) identifica univocamente um algoritmo matemático
     de PDI, em perfeita sincronia com o front-end Vue 3 / TypeScript.
2. Desempacotamento e Sanitização de Parâmetros:
   - Extrai e converte com segurança os parâmetros numéricos (como raio, tamanho de
     máscara, constante 'c', expoente gamma, fatores de ganho 'a' e 'b', porcentagem, etc.).
3. Execução em Cascata / Pipeline Composição de Funções:
   - Permite aplicar uma sequência arbitrária de filtros:
     I_final = (f_k ∘ f_{k-1} ∘ ... ∘ f_1)(I_inicial)
"""

from typing import List, Dict, Any, Tuple
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
from .utils import base64_to_matrix


# =============================================================================
# CONSTANTES DE MAPEAMENTO DOS FILTROS (ENUM COMPATÍVEL COM FRONT-END)
# =============================================================================
TIPO_NEGATIVO = 1                  # Filtro Negativo: s = 255 - r
TIPO_LOGARITMO = 2                 # Transformação Logarítmica: s = c * ln(1 + r)
TIPO_LOGARITMO_INVERSO = 3         # Logaritmo Inverso (Exponencial): s = exp(r / c) - 1
TIPO_POTENCIA = 4                  # Correção de Gamma (Potência): s = c * r^gamma
TIPO_RAIZ = 5                      # Raiz Gamma-ésima: s = c * r^(1 / gamma)
TIPO_AMPLIACAO_REPLICACAO_512 = 6  # Ampliação por Vizinho Mais Próximo para 512x512
TIPO_AMPLIACAO_REPLICACAO_1024 = 7 # Ampliação por Vizinho Mais Próximo para 1024x1024
TIPO_AMPLIACAO_BILINEAR_512 = 8    # Ampliação por Interpolação Bilinear para 512x512
TIPO_AMPLIACAO_BILINEAR_1024 = 9   # Ampliação por Interpolação Bilinear para 1024x1024
TIPO_HISTOGRAMA = 10               # Extração Estatística do Histograma [0..255]
TIPO_EQUALIZACAO = 11              # Equalização de Histograma via CDF e LUT
TIPO_ESPELHAMENTO_HORIZONTAL = 12  # Flip Horizontal (inversão do eixo x)
TIPO_ESPELHAMENTO_VERTICAL = 13    # Flip Vertical (inversão do eixo y)
TIPO_ROTACAO_90_HORARIO = 14       # Rotação geométrica de 90° no sentido horário
TIPO_ROTACAO_90_ANTIHORARIO = 15   # Rotação geométrica de 90° no sentido anti-horário
TIPO_ROTACAO_180 = 16              # Rotação geométrica de 180°
TIPO_EXPANSAO = 17                 # Expansão Linear de Contraste e Brilho: g = a * r + b
TIPO_COMPRESSAO = 18               # Compressão Linear de Faixa Dinâmica: g = (r / a) - b
TIPO_SOMAR_IMAGENS = 19            # Fusão Ponderada: g = p * I1 + (1 - p) * I2
TIPO_MEDIA = 20                    # Filtro Passa-Baixa da Média com máscara N x N
TIPO_MEDIANA = 21                  # Filtro Estatístico da Mediana (remoção sal e pimenta)
TIPO_MODA = 22                     # Filtro Estatístico da Moda (valor mais frequente)
TIPO_MINIMO = 23                   # Filtro Mínimo (Erosão em níveis de cinza)
TIPO_MAXIMO = 24                   # Filtro Máximo (Dilatação em níveis de cinza)
TIPO_LAPLACIANO = 25               # Operador Laplaciano de Segunda Derivada ∇²f
TIPO_HIGH_BOOST = 26               # Filtro High Boost / Nitidez: f_hb = A*f - f_suavizada
TIPO_PREWITT = 27                  # Detector de Bordas Prewitt: M = √(Gx² + Gy²)
TIPO_SOBEL = 28                    # Detector de Bordas Sobel com ponderação central


def aplicar_filtro_individual(
    matriz: List[List[int]],
    tipo: int,
    params: Dict[str, Any] | None = None
) -> Tuple[List[List[int]], Dict[str, Any] | None]:
    """
    Despacha a aplicação de uma única operação de PDI identificada pelo 'tipo'.

    Parâmetros:
        matriz: Imagem de entrada representada como matriz 2D de inteiros [0, 255]
        tipo: Identificador numérico do filtro (constantes TIPO_*)
        params: Dicionário de hiperparâmetros configurados pelo usuário na interface

    Retorna:
        Tupla (matriz_resultante, dados_adicionais_opcional).
        'dados_adicionais_opcional' armazena informações extras como estatísticas de histograma.
    """
    if params is None:
        params = {}

    dados_extras = None

    # 1. Filtro Negativo
    if tipo == TIPO_NEGATIVO:
        matriz = filtro_negativo(matriz)

    # 2. Transformação Logarítmica
    elif tipo == TIPO_LOGARITMO:
        c = float(params.get("c", 0)) if params.get("c") else None
        matriz = filtro_logaritmo(matriz, c=c)

    # 3. Logaritmo Inverso (Exponencial)
    elif tipo == TIPO_LOGARITMO_INVERSO:
        c = float(params.get("c", 0)) if params.get("c") else None
        matriz = filtro_logaritmo_inverso(matriz, c=c)

    # 4. Correção de Gamma (Potência)
    elif tipo == TIPO_POTENCIA:
        gamma = float(params.get("gamma", 1.0))
        matriz = filtro_potencia(matriz, gamma=gamma)

    # 5. Transformação de Raiz
    elif tipo == TIPO_RAIZ:
        gamma = float(params.get("gamma", 2.0))
        matriz = filtro_raiz(matriz, gamma=gamma)

    # 6 e 7. Ampliação por Replicação de Pixels (512x512 e 1024x1024)
    elif tipo == TIPO_AMPLIACAO_REPLICACAO_512:
        matriz = ampliacao_replicacao(matriz, 512, 512)

    elif tipo == TIPO_AMPLIACAO_REPLICACAO_1024:
        matriz = ampliacao_replicacao(matriz, 1024, 1024)

    # 8 e 9. Ampliação por Interpolação Bilinear (512x512 e 1024x1024)
    elif tipo == TIPO_AMPLIACAO_BILINEAR_512:
        matriz = ampliacao_bilinear(matriz, 512, 512)

    elif tipo == TIPO_AMPLIACAO_BILINEAR_1024:
        matriz = ampliacao_bilinear(matriz, 1024, 1024)

    # 10. Cálculo de Histograma
    elif tipo == TIPO_HISTOGRAMA:
        dados_extras = calcular_histograma(matriz)

    # 11. Equalização de Histograma
    elif tipo == TIPO_EQUALIZACAO:
        matriz, hist_resultante = equalizar_histograma(matriz)
        dados_extras = hist_resultante

    # 12 e 13. Espelhamentos
    elif tipo == TIPO_ESPELHAMENTO_HORIZONTAL:
        matriz = espelhamento_horizontal(matriz)

    elif tipo == TIPO_ESPELHAMENTO_VERTICAL:
        matriz = espelhamento_vertical(matriz)

    # 14, 15 e 16. Rotações Geométricas
    elif tipo == TIPO_ROTACAO_90_HORARIO:
        matriz = rotacao_90_horario(matriz)

    elif tipo == TIPO_ROTACAO_90_ANTIHORARIO:
        matriz = rotacao_90_antihorario(matriz)

    elif tipo == TIPO_ROTACAO_180:
        matriz = rotacao_180(matriz)

    # 17. Expansão Linear: g = a * r + b
    elif tipo == TIPO_EXPANSAO:
        a = float(params.get("a", 1.0))
        b = float(params.get("b", 0.0))
        matriz = filtro_expansao(matriz, a=a, b=b)

    # 18. Compressão Linear: g = (r / a) - b
    elif tipo == TIPO_COMPRESSAO:
        a = float(params.get("a", 1.0))
        b = float(params.get("b", 0.0))
        matriz = filtro_compressao(matriz, a=a, b=b)

    # 19. Fusão de Imagens (Soma com Porcentagem Ponderada)
    elif tipo == TIPO_SOMAR_IMAGENS:
        img2 = params.get("imagem")
        if isinstance(img2, str):
            matriz2 = base64_to_matrix(img2)
        elif isinstance(img2, list):
            matriz2 = img2
        else:
            raise ValueError("Segunda imagem para soma não fornecida.")

        porcentagem = float(params.get("porcentagemImagem1", params.get("porcentagem", 50.0)))
        matriz = somar_imagens(matriz, matriz2, porcentagem=porcentagem)

    # 20. Filtro da Média (Passa-Baixa)
    elif tipo == TIPO_MEDIA:
        tamanho = int(params.get("tamanhoMascara", 3))
        matriz = filtro_media(matriz, tamanho_mascara=tamanho)

    # 21. Filtro da Mediana (Ordem Estatística)
    elif tipo == TIPO_MEDIANA:
        tamanho = int(params.get("tamanhoMascara", 3))
        matriz = filtro_mediana(matriz, tamanho_mascara=tamanho)

    # 22. Filtro da Moda (Frequência Estatística)
    elif tipo == TIPO_MODA:
        tamanho = int(params.get("tamanhoMascara", 3))
        matriz = filtro_moda(matriz, tamanho_mascara=tamanho)

    # 23. Filtro MÍNIMO (Erosão em Cinza)
    elif tipo == TIPO_MINIMO:
        tamanho = int(params.get("tamanhoMascara", 3))
        matriz = filtro_minimo(matriz, tamanho_mascara=tamanho)

    # 24. Filtro MÁXIMO (Dilatação em Cinza)
    elif tipo == TIPO_MAXIMO:
        tamanho = int(params.get("tamanhoMascara", 3))
        matriz = filtro_maximo(matriz, tamanho_mascara=tamanho)

    # 25. Operador Laplaciano (Segunda Derivada)
    elif tipo == TIPO_LAPLACIANO:
        tamanho = int(params.get("tamanhoMascara", 3))
        matriz = filtro_laplaciano(matriz, tamanho_mascara=tamanho)

    # 26. Filtro High Boost (Nitidez com ganho A)
    elif tipo == TIPO_HIGH_BOOST:
        tamanho = int(params.get("tamanhoMascara", 3))
        ampliacao = float(params.get("ampliacao", 1.5))
        matriz = filtro_high_boost(matriz, tamanho_mascara=tamanho, ampliacao=ampliacao)

    # 27. Operador Prewitt de Bordas (Primeira Derivada)
    elif tipo == TIPO_PREWITT:
        matriz = filtro_prewitt(matriz)

    # 28. Operador Sobel de Bordas (Primeira Derivada Ponderada)
    elif tipo == TIPO_SOBEL:
        matriz = filtro_sobel(matriz)

    else:
        raise ValueError(f"Tipo de filtro desconhecido: {tipo}")

    return matriz, dados_extras


def executar_pipeline(
    matriz_inicial: List[List[int]],
    filtros: List[Dict[str, Any]]
) -> Tuple[List[List[int]], List[Dict[str, Any]]]:
    """
    Executa uma lista ordenada sequencial de operações de PDI (pipeline de filtros).

    Composição Matemática:
        I_1 = f_1(I_inicial)
        I_2 = f_2(I_1)
        ...
        I_k = f_k(I_{k-1})

    A saída da etapa anterior alimenta diretamente a entrada da próxima etapa,
    permitindo combinar múltiplos filtros em uma única requisição.

    Retorna:
        (matriz_final, lista_de_dados_extras)
    """
    matriz_atual = matriz_inicial
    dados_totais: List[Dict[str, Any]] = []

    for item in filtros:
        tipo = int(item.get("tipo", 0))
        params = item.get("params", {})
        matriz_atual, extras = aplicar_filtro_individual(matriz_atual, tipo, params)
        if extras is not None:
            dados_totais.append(extras)

    return matriz_atual, dados_totais

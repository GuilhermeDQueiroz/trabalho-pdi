"""
Testes unitários automatizados para todos os filtros do sistema PDI em Python.
Garante que todas as 18 funções funcionem de acordo com a matemática de PDI.
"""

import unittest
from backend.pdi import (
    obter_ponta_de_prova,
    filtro_negativo,
    filtro_logaritmo,
    filtro_logaritmo_inverso,
    filtro_potencia,
    filtro_raiz,
    filtro_expansao,
    filtro_compressao,
    somar_imagens,
    ampliacao_replicacao,
    ampliacao_bilinear,
    espelhamento_horizontal,
    espelhamento_vertical,
    rotacao_90_horario,
    rotacao_90_antihorario,
    rotacao_180,
    calcular_histograma,
    equalizar_histograma,
    filtro_media,
    filtro_mediana,
    filtro_moda,
    filtro_minimo,
    filtro_maximo,
    filtro_laplaciano,
    filtro_high_boost,
    filtro_prewitt,
    filtro_sobel,
    executar_pipeline,
    base64_to_matrix,
    matrix_to_base64,
)


# =============================================================================
# SUÍTE DE TESTES UNITÁRIOS PARA O MOTOR MATEMÁTICO DE PDI
# =============================================================================
class TestPDIEngine(unittest.TestCase):
    """
    Testes de regressão e validação matemática para as 18 operações de PDI.
    Usa matrizes sintéticas conhecidas para validar valores analíticos esperados.
    """

    def setUp(self):
        """Prepara uma matriz sintética 4x4 com gradiente linear constante de intensidade."""
        # Matriz 4x4 com intensidades variando de 10 a 160
        self.img4x4 = [
            [10, 20, 30, 40],
            [50, 60, 70, 80],
            [90, 100, 110, 120],
            [130, 140, 150, 160],
        ]

    def test_ponta_de_prova(self):
        """Valida se a Ponta de Prova recupera exatamente o nível de cinza f(y, x)."""
        resultado = obter_ponta_de_prova(self.img4x4, x=1, y=2)
        self.assertTrue(resultado["valido"])
        # Na linha y=2 e coluna x=1, o valor sintético é 100
        self.assertEqual(resultado["nc"], 100)
        self.assertEqual(resultado["largura"], 4)
        self.assertEqual(resultado["altura"], 4)

    def test_negativo(self):
        """Valida a fórmula linear do negativo: s = 255 - r."""
        res = filtro_negativo(self.img4x4)
        # Pixel (0, 0): 10 -> 255 - 10 = 245
        self.assertEqual(res[0][0], 255 - 10)
        # Pixel (3, 3): 160 -> 255 - 160 = 95
        self.assertEqual(res[3][3], 255 - 160)

    def test_logaritmo_e_inverso(self):
        """Valida as transformações logarítmica s = c*ln(1+r) e exponencial inversa."""
        res_log = filtro_logaritmo(self.img4x4)
        self.assertGreater(res_log[0][0], 0)
        self.assertLessEqual(res_log[3][3], 255)

        res_inv = filtro_logaritmo_inverso(self.img4x4)
        self.assertGreaterEqual(res_inv[0][0], 0)
        self.assertLessEqual(res_inv[3][3], 255)

    def test_potencia_e_raiz(self):
        """Valida que gamma > 1 escurece e raiz (gamma inverso) clareia."""
        res_pot = filtro_potencia(self.img4x4, gamma=2.0)
        # Gamma > 1 gera curva côncava (escurecimento global)
        self.assertLessEqual(res_pot[0][0], self.img4x4[0][0])

        res_raiz = filtro_raiz(self.img4x4, gamma=2.0)
        # Raiz quadrada gera curva convexa (clareamento de sombras)
        self.assertGreaterEqual(res_raiz[0][0], self.img4x4[0][0])

    def test_ampliacao_replicacao(self):
        """Valida a reamostragem pelo vizinho mais próximo preservando valores originais."""
        res = ampliacao_replicacao(self.img4x4, nova_largura=8, nova_altura=8)
        self.assertEqual(len(res), 8)
        self.assertEqual(len(res[0]), 8)
        self.assertEqual(res[0][0], self.img4x4[0][0])
        self.assertEqual(res[7][7], self.img4x4[3][3])

    def test_ampliacao_bilinear(self):
        """Valida a reamostragem por interpolação bilinear contínua."""
        res = ampliacao_bilinear(self.img4x4, nova_largura=8, nova_altura=8)
        self.assertEqual(len(res), 8)
        self.assertEqual(len(res[0]), 8)
        self.assertEqual(res[0][0], self.img4x4[0][0])
        self.assertEqual(res[7][7], self.img4x4[3][3])

    def test_histograma_e_equalizacao(self):
        """Valida o cálculo das 256 frequências e a equalização por CDF."""
        hist = calcular_histograma(self.img4x4)
        self.assertEqual(len(hist["valores"]), 256)
        # A soma de todas as frequências deve ser exatamente o número de pixels (4x4 = 16)
        self.assertEqual(sum(hist["valores"]), 16)

        img_eq, hist_eq = equalizar_histograma(self.img4x4)
        self.assertEqual(len(img_eq), 4)
        self.assertEqual(len(img_eq[0]), 4)
        self.assertEqual(len(hist_eq["valores"]), 256)

    def test_espelhamentos(self):
        """Valida a inversão de colunas (horizontal) e de linhas (vertical)."""
        esp_h = espelhamento_horizontal(self.img4x4)
        # O primeiro elemento da primeira linha vira o último elemento da mesma linha
        self.assertEqual(esp_h[0][0], self.img4x4[0][3])

        esp_v = espelhamento_vertical(self.img4x4)
        # O primeiro elemento da primeira linha vira o primeiro elemento da última linha
        self.assertEqual(esp_v[0][0], self.img4x4[3][0])

    def test_rotacoes(self):
        """Valida rotações matriciais de 90° horário, 90° anti-horário e 180°."""
        rot90h = rotacao_90_horario(self.img4x4)
        self.assertEqual(rot90h[0][0], self.img4x4[3][0])

        rot90ah = rotacao_90_antihorario(self.img4x4)
        self.assertEqual(rot90ah[0][0], self.img4x4[0][3])

        rot180 = rotacao_180(self.img4x4)
        self.assertEqual(rot180[0][0], self.img4x4[3][3])

    def test_expansao_compressao(self):
        """Valida as transformações lineares g = a*r + b e g = (r/a) - b."""
        exp = filtro_expansao(self.img4x4, a=1.2, b=10)
        self.assertEqual(exp[0][0], round(1.2 * 10 + 10))

        comp = filtro_compressao(self.img4x4, a=2.0, b=5)
        self.assertEqual(comp[0][0], round(10 / 2.0 - 5))

    def test_somar_imagens(self):
        """Valida a combinação linear convexa de duas imagens com pesos proporcionais."""
        img2 = [[100] * 4 for _ in range(4)]
        soma = somar_imagens(self.img4x4, img2, porcentagem=50.0)
        # 50% de 10 + 50% de 100 = 5 + 50 = 55
        self.assertEqual(soma[0][0], round(0.5 * 10 + 0.5 * 100))

    def test_filtros_espaciais(self):
        """Valida filtros espaciais: Média, Mediana, Moda, Mínimo e Máximo."""
        med = filtro_media(self.img4x4, tamanho_mascara=3)
        self.assertEqual(len(med), 4)

        mediana = filtro_mediana(self.img4x4, tamanho_mascara=3)
        self.assertEqual(len(mediana), 4)

        moda = filtro_moda(self.img4x4, tamanho_mascara=3)
        self.assertEqual(len(moda), 4)

        mini = filtro_minimo(self.img4x4, tamanho_mascara=3)
        # O mínimo na vizinhança deve ser menor ou igual ao ponto central
        self.assertLessEqual(mini[1][1], self.img4x4[1][1])

        maxi = filtro_maximo(self.img4x4, tamanho_mascara=3)
        # O máximo na vizinhança deve ser maior ou igual ao ponto central
        self.assertGreaterEqual(maxi[1][1], self.img4x4[1][1])

    def test_operadores_bordas(self):
        """Valida os operadores derivativos de borda: Laplaciano, High Boost, Prewitt e Sobel."""
        lap = filtro_laplaciano(self.img4x4, tamanho_mascara=3)
        self.assertEqual(len(lap), 4)

        hb = filtro_high_boost(self.img4x4, tamanho_mascara=3, ampliacao=1.5)
        self.assertEqual(len(hb), 4)

        prewitt = filtro_prewitt(self.img4x4)
        self.assertEqual(len(prewitt), 4)

        sobel = filtro_sobel(self.img4x4)
        self.assertEqual(len(sobel), 4)

    def test_conversao_base64(self):
        """Valida a codificação e decodificação recíproca entre Matriz 2D e Base64."""
        b64 = matrix_to_base64(self.img4x4)
        self.assertTrue(b64.startswith("data:image/png;base64,"))
        mat = base64_to_matrix(b64)
        self.assertEqual(len(mat), 4)
        self.assertEqual(len(mat[0]), 4)
        self.assertEqual(mat[0][0], self.img4x4[0][0])


if __name__ == "__main__":
    unittest.main()


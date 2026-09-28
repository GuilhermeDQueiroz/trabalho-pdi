---
name: algoritmos-pdi
description: Padrões de implementação e formulações matemáticas de algoritmos de Processamento Digital de Imagens em Python puro (sem OpenCV/SciPy).
---

# Skill: Algoritmos de PDI em Python Puro

Esta skill orienta o desenvolvimento e manutenção dos algoritmos matemáticos fundamentais de PDI.

---

## 1. Padrão de Função de Clamping
Em todas as operações que envolvem cálculos com ponto flutuante, aplique a função utilitária `clamp`:
```python
def clamp(valor: float) -> int:
    """Restringe o valor ao intervalo válido de 8 bits [0, 255]."""
    return max(0, min(255, round(valor)))
```

---

## 2. Padrão de Convolução Espacial Bidimensional
Ao aplicar filtros espaciais lineares (Média, Laplaciano, Prewitt, Sobel) com máscara $K$ de tamanho $M \times M$ ($M$ ímpar):
```python
def convolucao_2d(matriz: List[List[int]], kernel: List[List[float]]) -> List[List[int]]:
    H = len(matriz)
    W = len(matriz[0]) if H > 0 else 0
    k_size = len(kernel)
    raio = k_size // 2

    saida = [[0 for _ in range(W)] for _ in range(H)]

    for y in range(H):
        for x in range(W):
            soma = 0.0
            for ky in range(k_size):
                for kx in range(k_size):
                    py = min(max(y + ky - raio, 0), H - 1)
                    px = min(max(x + kx - raio, 0), W - 1)
                    soma += matriz[py][px] * kernel[ky][kx]
            saida[y][x] = clamp(soma)

    return saida
```

---

## 3. Padrão de Filtros Estatísticos Não-Lineares
Para Mediana, Moda, Mínimo e Máximo:
1. Extraia os vizinhos na janela $N \times N$ com espelhamento de borda.
2. Calcule a estatística desejada:
   - **Mediana**: Ordene os valores e tome o elemento central.
   - **Moda**: Conte a frequência dos valores e pegue o de maior ocorrência (ou média dos empates).
   - **Mínimo / Máximo**: `min(vizinhos)` / `max(vizinhos)`.

---

## 4. Equalização Global por CDF
1. Calcule o histograma $h(k)$ para $k \in [0, 255]$.
2. Calcule a função de distribuição acumulada $CDF(k) = \sum_{i=0}^k h(i)$.
3. Crie uma LUT (Look-Up Table) mapeando $k \to \text{round}\left(\frac{CDF(k) - CDF_{min}}{Total - CDF_{min}} \times 255\right)$.
4. Mapeie cada pixel da imagem de entrada pela LUT.

# Memória Técnica do Motor PDI (pdi-engine.md)

Este documento registra as 18 funções e operadores implementados no motor matemático puro.

---

## 🔬 Tabela de Operadores Matemáticos

| # | Operador | Fórmula / Lógica | Módulo |
|---|---|---|---|
| 1 | **Ponta de Prova** | Retorna $(x, y)$ e $NC = I(y, x)$ se $0 \le x < W$ e $0 \le y < H$ | `ponta_de_prova.py` |
| 2 | **Negativo** | $s = 255 - r$ | `pontuais.py` |
| 3 | **Logaritmo** | $s = c \cdot \ln(1 + r)$, onde $c = \frac{255}{\ln(1 + 255)} \approx 45.986$ | `pontuais.py` |
| 4 | **Inverso do Log** | $s = \exp(r / c) - 1$ | `pontuais.py` |
| 5 | **Potência (Gamma)** | $s = c \cdot r^\gamma$, com $c = \frac{255}{255^\gamma}$ | `pontuais.py` |
| 6 | **Raiz (Gamma < 1)**| $s = c \cdot r^{1/\gamma}$ | `pontuais.py` |
| 7 | **Expansão Linear**| $g = \text{clamp}(a \cdot r + b)$ | `pontuais.py` |
| 8 | **Compressão Linear**| $g = \text{clamp}(\frac{r}{a} - b)$ | `pontuais.py` |
| 9 | **Soma Linear**| $g = \text{clamp}\left(\frac{p}{100} I_1 + \frac{100 - p}{100} I_2\right)$ | `pontuais.py` |
| 10 | **Replicação** | $I_{nova}(y, x) = I_{orig}(\lfloor y / s_y \rfloor, \lfloor x / s_x \rfloor)$ | `geometricos.py` |
| 11 | **Bilinear** | Interpolação ponderada dos 4 vizinhos com pesos $(1 - dx)(1 - dy)$ | `geometricos.py` |
| 12 | **Espelhamento H/V** | Horizontal: $x' = W - 1 - x$; Vertical: $y' = H - 1 - y$ | `geometricos.py` |
| 13 | **Rotações 90° e 180°** | Horário: $x' = H - 1 - y, y' = x$; 180°: $x' = W - 1 - x, y' = H - 1 - y$ | `geometricos.py` |
| 14 | **Histograma** | Contagem $h(k) = \sum \delta(I(y, x), k)$ para $k \in [0, 255]$ | `histograma.py` |
| 15 | **Equalização CDF**| $s_k = \text{round}\left(\frac{CDF(k) - CDF_{min}}{N \cdot M - CDF_{min}} \cdot 255\right)$ | `histograma.py` |
| 16 | **Filtro da Média** | Convolução com kernel normalizado de $1 / (N \cdot N)$ | `espaciais.py` |
| 17 | **Estatísticos** | Mediana, Moda, Mínimo e Máximo na vizinhança $N \times N$ | `espaciais.py` |
| 18 | **Laplaciano e High Boost** | Segunda derivada com kernel $\nabla^2$ e realce $f_{hb} = (A - 1)f + (f - f_{suav})$ | `espaciais.py` |
| 19 | **Prewitt e Sobel** | Gradientes $G_x, G_y$ com magnitude $M = \sqrt{G_x^2 + G_y^2}$ | `espaciais.py` |

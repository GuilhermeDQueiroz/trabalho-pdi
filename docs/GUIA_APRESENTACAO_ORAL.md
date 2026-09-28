# 📖 Guia de Apresentação Oral - Trabalho de Processamento Digital de Imagens (PDI)

Este documento foi elaborado para auxiliar na **avaliação individual e apresentação oral** do trabalho prático de PDI, detalhando a fundamentação teórica, fórmulas matemáticas e detalhes de implementação de cada uma das 18 funções desenvolvidas em **Python puro**.

---

## 🏛️ Arquitetura e Decisões de Projeto

- **Linguagem Backend:** Python 3.14 (FastAPI + Uvicorn).
- **Front-end:** Vue 3, Vuetify 3 e Vite, estilizado estritamente nas cores **PRETO, BRANCO E CINZA** (monocromático).
- **Conformidade com os Requisitos:** **Nenhuma biblioteca de terceiros de PDI** (como OpenCV, PIL ImageFilter ou SciPy ndimage) foi utilizada para processamento. Todas as matrizes, convoluções, cálculos estatísticos e reamostragens foram implementados manualmente a partir dos fundamentos matemáticos.

---

## 🔬 Fundamentação Teórica das 18 Funções

### 1. Função Ponta de Prova (Probe Tool)
- **Objetivo:** Inspecionar interativamente qualquer ponto da imagem.
- **Teoria:** Uma imagem digital em níveis de cinza é uma função discreta $f(x, y)$, onde $x \in [0, W-1]$ e $y \in [0, H-1]$. O Nível de Cinza (NC) quantifica a intensidade luminosa naquele ponto, variando tipicamente de 0 (preto absoluto) a 255 (branco absoluto).
- **Implementação:** O front-end captura as coordenadas do cursor e mapeia da resolução do elemento de tela para as dimensões reais da matriz da imagem ($W \times H$). O backend Python valida os limites e recupera o valor pontual $NC = f(y, x)$.

---

### 2. Filtro Negativo
- **Fórmula Matemática:**
  $$s = L - 1 - r = 255 - r$$
- **Teoria:** Inversão linear de intensidades. Realça detalhes escuros imersos em grandes regiões claras, similar a um filme negativo fotográfico.
- **Aplicação Prática:** Análise de exames médicos (como raios-X e mamografias).

---

### 3. Filtro de Logaritmo e Logaritmo Inverso (Unidade 3)
- **Fórmula do Logaritmo:**
  $$s = c \cdot \ln(1 + r), \quad \text{onde } c = \frac{255}{\ln(1 + 255)} \approx 45.986$$
  - **Teoria:** A transformação logarítmica expande a faixa de valores de baixa intensidade (tons escuros) e comprime a faixa de valores altos (tons claros). Muito usada para visualizar espectros de Fourier que possuem dinâmica muito ampla.
- **Fórmula do Logaritmo Inverso (Exponencial):**
  $$s = \exp\left(\frac{r}{c}\right) - 1$$
  - **Teoria:** Realiza a operação oposta: comprime os tons escuros e expande os tons claros.

---

### 4. Filtro de Potência e Raiz (Correção de Gamma - Unidade 3)
- **Fórmula da Potência:**
  $$s = c \cdot r^\gamma, \quad c = \frac{255}{255^\gamma}$$
  - **Teoria:** Quando $\gamma > 1$, comprime tons escuros e escurece a imagem como um todo. Quando $\gamma < 1$, atua no sentido inverso.
- **Fórmula da Raiz:**
  $$s = c \cdot r^{1/\gamma}, \quad c = \frac{255}{255^{1/\gamma}}$$
  - **Teoria:** Equivale a aplicar o inverso da potência (exponencial fracionária). O usuário informa o parâmetro $\gamma$ desejado na interface.

---

### 5. Ampliação por Replicação de Pixels (Nearest Neighbor Resampling - Unidade 2)
- **Teoria:** Reamostragem geométrica pelo vizinho mais próximo. Cada pixel $(y', x')$ na imagem de destino (512x512 ou 1024x1024) recebe o valor do pixel de coordenadas discretas mais próximas na imagem de origem:
  $$y = \text{round}\left(y' \cdot \frac{H - 1}{H' - 1}\right), \quad x = \text{round}\left(x' \cdot \frac{W - 1}{W' - 1}\right)$$
  $$I_{novo}(y', x') = I_{orig}(y, x)$$
- **Efeito Visual:** Produz artefatos de blocagem ("pixelização"), preservando bordas duras mas sem suavização.

---

### 6. Ampliação por Interpolação Bilinear (Bilinear Interpolation Resampling - Unidade 2)
- **Teoria:** Utiliza os 4 vizinhos mais próximos $(y_1, x_1), (y_1, x_2), (y_2, x_1), (y_2, x_2)$ ponderados pela distância fracionária $(dx, dy)$ às coordenadas contínuas:
  $$f(y', x') = (1 - dx)(1 - dy) I(y_1, x_1) + dx(1 - dy) I(y_1, x_2) + (1 - dx)dy I(y_2, x_1) + dx dy I(y_2, x_2)$$
- **Efeito Visual:** Gera transições muito mais suaves e naturais que a replicação de pixels, evitando o serrilhado abrupto.

---

### 7. Histograma Gráfico da Imagem
- **Fórmula:**
  $$h(r_k) = n_k, \quad k \in [0, 255]$$
  onde $n_k$ é a quantidade total de pixels na imagem com nível de cinza igual a $r_k$.
- **Importância:** O histograma descreve a distribuição de probabilidade de brilho e contraste da imagem. Imagens com baixo contraste apresentam histogramas concentrados em faixas estreitas.

---

### 8. Equalização da Imagem e Histograma Resultante (Unidade 3)
- **Teoria e Passos:**
  1. Computa o histograma normalizado (função densidade de probabilidade): $p(r_k) = \frac{n_k}{N}$.
  2. Calcula a Função de Distribuição Acumulada (CDF):
     $$CDF(k) = \sum_{j=0}^k p(r_j)$$
  3. Aplica a função de mapeamento de equalização:
     $$s_k = \text{round}\left(\frac{CDF(k) - CDF_{min}}{1 - CDF_{min}} \times 255\right)$$
  4. Substitui cada pixel original $r$ pelo valor mapeado $s$.
  5. Computa o histograma resultante da imagem já equalizada, demonstrando o espalhamento das frequências ao longo de toda a escala $[0, 255]$.

---

### 9 e 10. Espelhamento Horizontal e Vertical
- **Horizontal:** Inverte a ordem das colunas: $I(y, x) \rightarrow I(y, W - 1 - x)$.
- **Vertical:** Inverte a ordem das linhas: $I(y, x) \rightarrow I(H - 1 - y, x)$.

---

### 11 e 12. Rotações de 90° (Horário e Anti-Horário) e 180°
- **Rotação 90° Horário:** A matriz é transposta e invertida horizontalmente:
  $$I_{novo}(y', x') = I_{orig}(H - 1 - x', y')$$
- **Rotação 90° Anti-Horário:**
  $$I_{novo}(y', x') = I_{orig}(x', W - 1 - y')$$
- **Rotação 180°:**
  $$I_{novo}(y, x) = I_{orig}(H - 1 - y, W - 1 - x)$$

---

### 13. Filtros de Expansão e Compressão Linear
- **Expansão:** $g = a \cdot r + b$
  - Ajusta o contraste multiplicando pelo fator de ganho $a$ e o brilho somando o deslocamento $b$.
- **Compressão:** $g = \frac{r}{a} - b$
  - Reduz a amplitude da faixa dinâmica dividindo por $a$ e ajusta o nível mínimo subtraindo $b$.
- Ambos possuem parâmetros $a$ e $b$ configurados pelo usuário na interface.

---

### 14. Somar Duas Imagens com Opção de Porcentagem
- **Fórmula:**
  $$g(x, y) = \text{clamp}\left( \frac{p}{100} \cdot I_1(x, y) + \frac{100 - p}{100} \cdot I_2(x, y) \right)$$
- O usuário informa a porcentagem da primeira imagem ($p \in [0, 100]$) e carrega a segunda imagem diretamente no modal de filtros.

---

### 15. Filtro da Média (Passa-Baixa)
- **Fórmula:** Convolução espacial 2D com máscara de tamanho $N \times N$ (ex: 3x3, 5x5, 7x7) onde todos os pesos valem $\frac{1}{N^2}$:
  $$g(x, y) = \frac{1}{N^2} \sum_{s=-R}^{R} \sum_{t=-R}^{R} f(x + s, y + t)$$
- **Efeito:** Suavização espacial e redução de ruídos de alta frequência.

---

### 16. Filtros de Ordem: Mediana, Moda, MÍN e MÁX
- Para cada pixel na vizinhança quadrada $N \times N$:
  - **Mediana:** Ordena os valores vizinhos e seleciona o elemento central. Altamente eficaz contra ruído impulsivo (*sal e pimenta*), sem borrar bordas nítidas.
  - **Moda:** Seleciona o valor de intensidade com maior frequência na janela.
  - **MÍNIMO (Erosão):** Seleciona o menor valor da vizinhança, reduzindo áreas claras.
  - **MÁXIMO (Dilatação):** Seleciona o maior valor da vizinhança, expandindo áreas claras.

---

### 17. Operadores Laplaciano e High Boost
- **Laplaciano:** Operador isotrópico de segunda derivada:
  $$\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$$
  Máscara com coeficiente central $N^2 - 1$ e coeficientes periféricos $-1$.
- **High Boost:**
  $$f_{hb}(x, y) = A \cdot f(x, y) - f_{suavizado}(x, y) = (A - 1) f(x, y) + (f(x, y) - f_{suavizado}(x, y))$$
  Onde $A \ge 1$ é o fator de ampliação informado pelo usuário. Preserva a luminosidade geral da imagem ao mesmo tempo que acentua as bordas.

---

### 18. Operadores Prewitt e Sobel
- **Prewitt:** Máscaras direcionais de primeira derivada horizontal e vertical:
  $$G_x = \begin{bmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{bmatrix}, \quad G_y = \begin{bmatrix} -1 & -1 & -1 \\ 0 & 0 & 0 \\ 1 & 1 & 1 \end{bmatrix}$$
  Magnitude do gradiente: $M = \sqrt{G_x^2 + G_y^2}$.
- **Sobel:** Similar ao Prewitt, porém confere maior peso aos pixels centrais mais próximos:
  $$G_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}, \quad G_y = \begin{bmatrix} 1 & 2 & 1 \\ 0 & 0 & 0 \\ -1 & -2 & -1 \end{bmatrix}$$
  Magnitude do gradiente: $M = \sqrt{G_x^2 + G_y^2}$.

# 🖼️ Sistema de Processamento Digital de Imagens (PDI) em Python

Aplicação desenvolvida para processamento, computação e exibição de transformações e filtros clássicos de **Processamento Digital de Imagens (PDI)**. Possui motor matemático implementado em **Python puro**, API RESTful de alta performance com **FastAPI** e interface web moderna SPA (Single Page Application) em **Vue 3 / Vuetify 3** no tema estritamente **monocromático (preto, branco e cinza)**.

---

## 🎯 Destaques do Projeto

- **Algoritmos Matemáticos Puros em Python:** Conforme as diretrizes acadêmicas, **não foram utilizadas bibliotecas prontas de PDI** (como OpenCV `cv2`, PIL `ImageFilter` ou `scipy.ndimage`). Todos os 18 filtros e operadores foram desenvolvidos do zero a partir de suas formulações matemáticas fundamentais sobre matrizes numéricas bidimensionais.
- **Interface Monocromática e Moderna:** Front-end estilizado em tons de cinza escuro, grafite e preto (`#0a0a0a` / `#121214`), com acentos em branco puro e alto contraste.
- **Galeria para Teste Rápido Integrada:** Modal com 13 imagens de amostra acadêmicas padrão em formato `.bmp` (256×256 px) para carregamento instantâneo no workbench com 1 clique.
- **Histograma Integrado no Card da Imagem:** Alternância rápida entre visualização da imagem e gráfico de histograma de frequências dos 256 níveis de cinza (NC) com 1 clique diretamente no card.
- **Pipeline de Filtros Não-Destrutivo:** Permite encadear múltiplos filtros em uma fila ordenada de execução com suporte a reorganização via **Drag & Drop**, prevenção de filtros duplicados e **exclusão individual (1 por vez)** tanto no card da fila quanto no menu de seleção.
- **Função Ponta de Prova Precisa:** Inspeciona em tempo real as coordenadas $(x, y)$ nativas da imagem e o Nível de Cinza ($NC \in [0, 255]$) sob o cursor do mouse.
- **Transformações Rápidas no SpeedDial:** Ações rápidas de rotação matricial (90° horário, 90° anti-horário e 180°).
- **Documentação Acadêmica Completa:**
  - [`docs/GUIA_APRESENTACAO_ORAL.md`](docs/GUIA_APRESENTACAO_ORAL.md): Roteiro teórico, formulações matemáticas e perguntas frequentes para a apresentação oral.
  - [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md): Especificação arquitetural, fluxo de dados e endpoints da API.

---

## 📋 Lista das 18 Funções Implementadas

| # | Função / Filtro | Descrição / Fórmula Teórica | Módulo Python |
|---|-----------------|-----------------------------|---------------|
| 1 | **Função Ponta de Prova** | Coordenadas $(x, y)$ nativas e Nível de Cinza ($NC \in [0, 255]$) sob o mouse | `ponta_de_prova.py` |
| 2 | **Filtro Negativo** | Inversão linear de intensidades: $s = 255 - r$ | `pontuais.py` |
| 3 | **Filtro de Logaritmo e Inverso (Unidade 3)** | $s = c \cdot \ln(1 + r)$ com $c = \frac{255}{\ln(1 + 255)}$ e $s = \exp(r/c) - 1$ | `pontuais.py` |
| 4 | **Filtro de Potência e Raiz (Gamma - Unidade 3)** | $s = c \cdot r^\gamma$ e $s = c \cdot r^{1/\gamma}$ com $\gamma > 0$ configurável | `pontuais.py` |
| 5 | **Ampliação por Replicação (Nearest Neighbor)** | Reamostragem 512×512 e 1024×1024 por pixel mais próximo | `geometricos.py` |
| 6 | **Ampliação Bilinear (Bilinear Resampling)** | Interpolação ponderada dos 4 vizinhos para 512×512 e 1024×1024 | `geometricos.py` |
| 7 | **Histograma Gráfico** | Gráfico de distribuição de frequências para os 256 níveis de cinza | `histograma.py` |
| 8 | **Equalização de Histograma (Unidade 3)** | Maximização do contraste via CDF e histograma resultante | `histograma.py` |
| 9 | **Espelhamento Horizontal** | Inversão horizontal: $I(y, W - 1 - x)$ | `geometricos.py` |
| 10 | **Espelhamento Vertical** | Inversão vertical: $I(H - 1 - y, x)$ | `geometricos.py` |
| 11 | **Rotação de 90° (Horário e Anti-Horário)** | Transposição e rotação matricial nos dois sentidos | `geometricos.py` |
| 12 | **Rotação de 180°** | Inversão bidimensional de eixos | `geometricos.py` |
| 13 | **Filtros de Expansão e Compressão** | Expansão: $g = a \cdot r + b$ e Compressão: $g = \frac{r}{a} - b$ ($a$ e $b$ definidos pelo usuário) | `pontuais.py` |
| 14 | **Soma de Imagens com Porcentagem** | Combinação linear: $g = \frac{p}{100} I_1 + \frac{100 - p}{100} I_2$ com upload da 2ª imagem | `pontuais.py` |
| 15 | **Filtro da Média (Passa-Baixa)** | Convolução espacial com máscara quadrada ímpar ($N \times N$) configurável | `espaciais.py` |
| 16 | **Filtros de Mediana, Moda, MÍN e MÁX** | Filtros estatísticos de vizinhança com máscara configurável | `espaciais.py` |
| 17 | **Operadores Laplaciano e High Boost** | Segunda derivada e realce de nitidez $f_{hb} = (A - 1)f + (f - f_{suav})$ ($A \ge 1$) | `espaciais.py` |
| 18 | **Operadores Prewitt e Sobel** | Detecção de bordas por gradientes direcionais com magnitude $\sqrt{G_x^2 + G_y^2}$ | `espaciais.py` |

---

## 📁 Estrutura do Projeto

```
trab-pdi-main/
├── .agents/                      # Regras globais, personas e skills do Antigravity
├── backend/
│   ├── pdi/                      # Motor de algoritmos matemáticos puros em Python
│   │   ├── __init__.py           # Exportação e registro dos algoritmos de PDI
│   │   ├── utils.py              # Conversão Base64 <-> Matriz e clamp [0, 255]
│   │   ├── ponta_de_prova.py     # Inspeção de pixel nativo e coordenadas (x, y)
│   │   ├── pontuais.py           # Negativo, Log, Potência, Raiz, Expansão, Compressão, Soma
│   │   ├── geometricos.py        # Replicação, Bilinear, Espelhamentos, Rotações
│   │   ├── histograma.py         # Histograma e Equalização por CDF / LUT
│   │   ├── espaciais.py          # Média, Mediana, Moda, MÍN, MÁX, Laplaciano, High Boost, Prewitt, Sobel
│   │   └── processador.py        # Orquestrador da fila sequencial de filtros
│   ├── tests/
│   │   └── test_pdi.py           # Suíte de testes unitários automatizados dos algoritmos
│   └── app.py                    # Servidor FastAPI com endpoints REST e entrega do front-end
├── dist/                         # Build de produção do front-end servido pelo FastAPI
├── docs/                         # Documentação técnica e acadêmica
│   ├── ARQUITETURA.md            # Especificação da arquitetura e fluxo de dados
│   └── GUIA_APRESENTACAO_ORAL.md # Roteiro teórico e perguntas para avaliação oral
├── scripts/                      # Scripts utilitários de automação em lote
│   ├── build.bat                 # Compilação do front-end Vue 3 para dist/
│   ├── dev.bat                   # Execução em modo de desenvolvimento simultâneo
│   ├── iniciar.bat               # Inicializador do backend e navegador
│   └── test.bat                  # Execução da suíte de testes unitários em Python
├── src/                          # Código-fonte da interface Vue 3 / TypeScript
│   ├── assets/
│   │   └── Imagens/              # 13 Imagens de teste acadêmicas (teste1.bmp a teste13.bmp)
│   ├── components/               # Componentes visuais globais (GraficoDeBarras, Loading, Dialogs)
│   ├── enums/                    # Enums TypeScript (ETipoFiltroPDI, EOpcoesVisualizacao)
│   ├── layouts/                  # Layout padrão da aplicação
│   ├── router/                   # Configuração das rotas SPA
│   ├── services/                 # PythonPdiService (integração REST com FastAPI)
│   ├── stores/                   # Pinia store para estado global (loading, modais)
│   ├── style/                    # CSS global e tokens do tema monocromático
│   ├── utils/                    # Utilitários de manipulação de imagem e canvas
│   └── views/
│       └── dashboard/            # Bancada interativa principal de PDI
│           ├── components/       # CardImage, FormFiltros, GaleriaAmostras, InputGenerico, SpeedDial
│           └── Dashboard.vue     # View principal do Workbench
├── iniciar.bat                   # Inicializador rápido com 1 clique
├── run.py                        # Ponto de entrada do servidor ASGI Python (Uvicorn)
├── requirements.txt              # Dependências Python (FastAPI, Uvicorn, Pillow, Pydantic)
├── package.json                  # Dependências e scripts do front-end (Vue 3, Vuetify, Vite)
└── README.md                     # Documentação oficial do projeto
```

---

## 🚀 Como Executar

### Pré-requisitos
- **Python 3.10+** (Testado e homologado no Python 3.14).
- **Node.js 20+** (necessário apenas para recompilar o front-end).

Instale as dependências do backend Python:
```bash
pip install -r requirements.txt
```

---

### Execução em 1 Clique (Recomendado no Windows)
Dê um duplo clique no arquivo:
```bat
iniciar.bat
```
O script iniciará o servidor FastAPI e abrirá automaticamente o navegador em:
👉 **[http://localhost:8000](http://localhost:8000)**

---

### Execução Manual via Terminal
No diretório raiz do projeto, execute:
```bash
python run.py
```
Em seguida, acesse no navegador:
- **Aplicação Web:** [http://localhost:8000](http://localhost:8000)
- **Documentação Swagger da API:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Modo de Desenvolvimento do Front-End (Opcional)
Para desenvolvimento ativo com Hot-Module Replacement (HMR):
```bash
# Terminal 1 - Iniciar a API Python
python run.py

# Terminal 2 - Iniciar o servidor Vite
npm run dev
```
Acesse: [http://localhost:5173](http://localhost:5173).

---

## 🧪 Validação dos Testes Unitários

Para comprovar a corretude matemática de todos os 18 algoritmos implementados do zero:
```bash
python -m unittest backend/tests/test_pdi.py
```
Ou dê um duplo clique em:
```bat
scripts/test.bat
```

Saída esperada:
```
..............
----------------------------------------------------------------------
Ran 14 tests in 0.050s

OK
```

---

## 🌐 Deploy na Vercel (Produção em Nuvem)

O projeto está totalmente preparado e configurado para deploy automático na **Vercel** com arquitetura híbrida (Frontend estático na CDN + Backend Python Serverless):

1. Acesse o [Vercel Dashboard](https://vercel.com/dashboard) e clique em **"Add New..." > "Project"**.
2. Conecte sua conta do GitHub e importe o repositório **`trabalho-pdi`**.
3. A Vercel detectará automaticamente as configurações através do arquivo [`vercel.json`](vercel.json):
   - **Framework Preset:** Vite
   - **Root Directory:** `./`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Clique em **"Deploy"**. A Vercel provisionará a interface web e as funções Python Serverless em [`api/index.py`](api/index.py) automaticamente.


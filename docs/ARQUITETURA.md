# Arquitetura do Sistema de Processamento Digital de Imagens (PDI)

Este documento descreve detalhadamente a arquitetura de software, fluxo de dados, separação de responsabilidades e padrões de engenharia adotados no projeto.

---

## 1. Visão Geral da Arquitetura

O sistema é estruturado como uma aplicação web desacoplada de alto desempenho, dividida em três pilares principais:

```
┌─────────────────────────────────────────────────────────────┐
│                   Front-end (SPA Vue 3)                     │
│  - Vuetify 3 (Tema Monocromático: Dark/Cinza/Branco)        │
│  - TypeScript & Pinia Store (LayoutStore)                   │
│  - HTML5 Canvas (Ponta de Prova, Inspeção x, y, NC)         │
│  - ApexCharts (Histograma de 256 Níveis de Cinza)           │
└──────────────────────────────┬──────────────────────────────┘
                               │ JSON via HTTP REST (porta 8000)
                               │ (Base64 ou Matriz 2D de pixels)
┌──────────────────────────────▼──────────────────────────────┐
│                    API Gateway / FastAPI                     │
│  - FastAPI (backend/app.py) + Uvicorn ASGI                  │
│  - Validação de Payloads com Pydantic v2                    │
│  - Roteamento de Endpoints: /api/processar, /api/rotacao,   │
│    /api/histograma, /api/equalizacao, /api/ponta-de-prova   │
│  - Entrega de SPA Estática compilada (dist/)                │
└──────────────────────────────┬──────────────────────────────┘
                               │ Matrizes bidimensionais List[List[int]]
                               │ Inteiros [0, 255]
┌──────────────────────────────▼──────────────────────────────┐
│            Motor Matemático Puro de PDI (Python)            │
│                 (backend/pdi/)                              │
│  - pontuais.py      -> Negativo, Log, Potência, Soma, etc.  │
│  - geometricos.py   -> Replicação, Bilinear, Espelho, Giro  │
│  - espaciais.py     -> Média, Mediana, Moda, Sobel, Prewitt │
│  - histograma.py    -> Contagem de frequências, CDF e LUT   │
│  - processador.py   -> Pipeline encadeado não-destrutivo    │
│  - ponta_de_prova.py-> Inspeção precisa de coordenadas      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Princípio da Pureza Matemática (Zero OpenCV / Zero SciPy)

Uma exigência primordial do projeto é o desenvolvimento de **todos os 18 algoritmos e filtros a partir de suas formulações matemáticas fundamentais**, sem o uso de bibliotecas prontas de processamento de imagem (como OpenCV `cv2`, PIL `ImageFilter` ou `scipy.ndimage`).

- A biblioteca **Pillow (PIL)** é restrita unicamente à conversão de formato de imagem codificada em Base64 para matriz de pixels bidimensional (e vice-versa) no módulo `backend/pdi/utils.py`.
- Todas as convoluções espaciais, kernels (Sobel, Prewitt, Laplaciano), interpolações (Nearest Neighbor e Bilinear), cálculo de CDF para equalização e transformações geométricas operam diretamente sobre listas de listas de inteiros (`List[List[int]]`) em Python nativo.

---

## 3. Pipeline de Filtros Não-Destrutivo

A arquitetura do processamento segue o padrão de **Pipeline Sequencial Ordenado**:

1. **Imagem Original Imutável:** A imagem carregada pelo usuário no início permanece inalterada na memória do front-end (`imagemOriginal`).
2. **Fila de Filtros:** O usuário adiciona operadores na lista sequencial (ex: `Filtro da Média 3x3` -> `Negativo` -> `Realce High Boost`).
3. **Recálculo Dinâmico:** Sempre que um filtro é adicionado, reordenado ou excluído da fila, o front-end envia a **imagem original** juntamente com a lista atualizada de filtros para `/api/processar`.
4. **Isolamento de Erros:** Caso o usuário esvazie a fila ou use a ação *Limpar Filtros*, o estado original é restaurado instantaneamente sem resíduos acumulados.

---

## 4. Estrutura de Diretórios do Projeto

```
trab-pdi-main/
├── .agents/                  # Configurações, personas, memórias e skills do AG Kit
│   ├── AGENTS.md             # Regras globais, arquitetura e governança do projeto
│   ├── ARCHITECTURE.md       # Catálogo de agentes, skills e workflows
│   ├── agent/                # Agentes especialistas (@especialista-pdi, @frontend-specialist)
│   ├── memory/               # Memória persistente, catálogo dos 18 algoritmos e convenções
│   ├── rules/                # Regras obrigatórias e protocolo de algoritmos puros
│   ├── skills/               # Skills acionáveis (algoritmos-pdi, pipeline-filtros, etc.)
│   └── workflows/            # Workflows estruturados (executar, testar, compilar)
├── backend/                  # Servidor de API e motor matemático de PDI
│   ├── pdi/                  # 18 Algoritmos puros implementados em Python
│   ├── tests/                # Suíte de testes unitários automatizados (14 suítes)
│   └── app.py                # Servidor FastAPI com rotas REST e entrega do front-end
├── dist/                     # Build de produção do front-end servido pelo FastAPI
├── docs/                     # Documentação técnica e guia de apresentação oral
│   ├── ARQUITETURA.md        # Este documento de arquitetura
│   └── GUIA_APRESENTACAO_ORAL.md # Roteiro teórico e prático para avaliação oral
├── public/                   # Arquivos estáticos públicos do Vite
├── scripts/                  # Scripts utilitários de build, teste e automação
├── src/                      # Código-fonte da interface Vue 3 / Vuetify
│   ├── components/           # Componentes UI (gráfico de barras, loaders, diálogos)
│   ├── enums/                # Enums tipados de filtros e opções de visualização
│   ├── layouts/              # Layout base monocromático da aplicação
│   ├── router/               # Configuração de rotas vue-router (Home, Dashboard, 404)
│   ├── services/             # PythonPdiService (comunicação REST com FastAPI)
│   ├── stores/               # Gerenciamento de estado Pinia (LayoutStore)
│   ├── style/                # Estilos globais e tokens monocromáticos
│   ├── types/                # Declarações e interfaces TypeScript
│   ├── utils/                # Conversão HTML5 Canvas, Base64 e matrizes
│   └── views/                # Telas (Home e Dashboard de processamento)
├── iniciar.bat               # Inicializador com 1 clique (servidor + navegador)
├── run.py                    # Ponto de entrada do backend Python (Uvicorn)
├── requirements.txt          # Dependências do Python (FastAPI, Uvicorn, Pillow, Pydantic)
├── package.json              # Dependências e scripts do Node.js
└── vite.config.ts            # Configuração do Vite com proxy reverso para /api
```

---

## 5. Fluxo de Dados e Comunicação

1. **Upload da Imagem:**
   - O usuário seleciona um arquivo de imagem na tela inicial ou no Dashboard.
   - O front-end carrega a imagem em um elemento `<canvas>` HTML5 offscreen e extrai sua matriz bidimensional em tons de cinza via `imageUtils.ts`.
2. **Disparo do Processamento:**
   - `PythonPdiService.processarImagem(imagemOriginal, filtros)` envia uma requisição `POST /api/processar`.
   - O payload contém a imagem em Base64 ou matriz e o array ordenado de filtros com seus respectivos parâmetros.
3. **Processamento no Backend:**
   - O FastAPI recebe o payload validado pelo modelo Pydantic `RequisicaoProcessar`.
   - `executar_pipeline()` itera sobre os filtros sequencialmente aplicando cada transformação na matriz.
   - O resultado é codificado de volta para Base64 e o histograma é recalculado.
4. **Atualização da Interface:**
   - O front-end renderiza a imagem resultante na área central.
   - O componente `GraficoDeBarras.vue` (ApexCharts) exibe a distribuição de frequências dos 256 níveis de cinza.
   - A ponta de prova permite inspecionar interativamente cada pixel $(x, y)$ da imagem resultante.

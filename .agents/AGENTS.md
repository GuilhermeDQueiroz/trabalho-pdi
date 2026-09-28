---
name: Regras Globais do Projeto (Sistema PDI)
description: Diretrizes absolutas, arquitetura matemática e regras do Sistema de Processamento Digital de Imagens (Python Puro + FastAPI + Vue 3).
---

# Regras Globais do Projeto (AGENTS.md)

Este documento contém as diretrizes e regras absolutas que todos os agentes e skills do Antigravity devem seguir neste projeto de Processamento Digital de Imagens (PDI).

---

## 1. Contexto do Projeto
- **Domínio**: Sistema acadêmico e profissional de Processamento Digital de Imagens (PDI).
- **Abordagem Matemática**: Motor analítico desenvolvido em **Python puro**, sem uso de bibliotecas de terceiros para operações de PDI (proibido o uso de OpenCV `cv2`, PIL `ImageFilter` ou `scipy.ndimage`).
- **Arquitetura Geral**:
  - **Backend**: Python 3.14 + FastAPI + Uvicorn ASGI (`backend/`).
  - **Motor PDI**: Módulos matemáticos dedicados (`backend/pdi/`).
  - **Frontend**: Single Page Application (SPA) com Vue 3 (Composition API + TypeScript), Vuetify 3, Pinia e ApexCharts (`src/`).
  - **Tema Visual**: Interface estritamente **monocromática** (preto, cinza escuro, cinza médio e branco), com alto contraste e sem cores legadas.

---

## 2. Regras Críticas de PDI e Pureza Algorítmica (TIER 0)

### 2.1 Proibição de Bibliotecas de Alto Nível de PDI
- Todos os 18 filtros e operadores de PDI devem ser implementados **do zero a partir de suas formulações matemáticas fundamentais**.
- A biblioteca **Pillow (PIL)** só é permitida no módulo `backend/pdi/utils.py` para decodificar imagens Base64 em matrizes bidimensionais numéricas e codificar matrizes resultantes de volta para PNG/Base64.
- Convoluções espaciais, kernels, vizinhanças (3x3, 5x5, NxN), interpolações (Bilinear, Nearest Neighbor), rotações e histogramas devem operar diretamente sobre listas de inteiros `List[List[int]]` com valores restritos a $[0, 255]$ via clamping.

### 2.2 Pipeline Não-Destrutivo
- A imagem de entrada carregada pelo usuário (`imagemOriginal`) é **estritamente imutável**.
- Filtros adicionados pelo usuário formam uma fila/pipeline ordenada.
- Ao adicionar, reordenar ou remover qualquer filtro (ou clicar em *Limpar Filtros*), a imagem resultante deve ser recalculada a partir da imagem original, garantindo reversão perfeita sem degradação acumulada.

### 2.3 Função Ponta de Prova
- A ponta de prova deve inspecionar as coordenadas $(x, y)$ nativas da matriz da imagem (não as coordenadas escaladas do monitor) e retornar com precisão o Nível de Cinza ($NC \in [0, 255]$).

---

## 3. Stack Tecnológica & Organização de Código

### 3.1 Backend (`backend/`)
- **FastAPI**: Endpoints REST tipados com Pydantic v2 em `backend/app.py`.
- **Rotas Oficiais**:
  - `GET /api/status`: Health check e diagnóstico do motor de PDI.
  - `POST /api/processar`: Execução do pipeline sequencial de filtros.
  - `POST /api/rotacao`: Rota especializada para giros matriciais (90° horário, 90° anti-horário e 180°).
  - `POST /api/histograma`: Contagem de frequências dos 256 níveis de cinza.
  - `POST /api/equalizacao`: Equalização via CDF (Função de Distribuição Acumulada).
  - `POST /api/ponta-de-prova`: Consulta rápida de pixel $(x, y)$ e $NC$.
- **Serviço Estático**: Serve automaticamente o frontend compilado em `dist/` quando presente.

### 3.2 Frontend (`src/`)
- **Vue 3**: Composition API com `<script setup lang="ts">`.
- **Vuetify 3**: Componentes de interface adaptados para o tema monocromático.
- **ApexCharts**: Visualização do histograma com 256 barras verticais.
- **Canvas HTML5**: Exibição da imagem e rastreamento de mouse para ponta de prova.

---

## 4. Diretrizes de UI/UX & Design Monocromático
- **Fundo Principal**: Preto e cinza grafite muito escuro (`#0a0a0a` / `#121212` / `#141414`).
- **Superfícies / Cards**: `#1a1a1a` com bordas sutis em `#2d2d2d` ou `#333333`.
- **Textos Primários**: `#ffffff` (alto contraste).
- **Textos Secundários / Legendas**: `#8c8c8c` / `#a0a0a0`.
- **Acentos**: Branco puro (`#ffffff`) ou cinza claro (`#e0e0e0`) em estados ativos e seleções.

---

## 5. Governança de Testes e Validação
- O backend possui suíte de testes unitários em `backend/tests/test_pdi.py`.
- Toda alteração em algoritmos matemáticos deve ser validada via:
  ```bash
  python -m unittest backend/tests/test_pdi.py
  ```
- O frontend deve compilar sem erros de TypeScript:
  ```bash
  npm run build
  ```

---

## 6. Orquestração de Agentes Locais
- `@especialista-pdi`: Implementações matemáticas, convoluções, interpolações e filtros em Python puro.
- `@frontend-specialist`: Componentes Vue 3, manipulação do Canvas, Vuetify e gráficos ApexCharts.
- `@orchestrator`: Gestão global da arquitetura, pipeline e integração cliente-servidor.

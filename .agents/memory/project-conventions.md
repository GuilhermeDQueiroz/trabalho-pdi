# Convenções de Projeto (project-conventions.md)

Este documento estabelece as convenções de estilo, tipagem e organização de código.

---

## 🐍 Backend Python
1. **Padrão de Código**: Seguir PEP 8 para nomenclatura de variáveis e funções (`snake_case`).
2. **Type Hints**: Sempre tipar parâmetros e retornos das funções:
   ```python
   def aplicar_filtro(matriz: List[List[int]], parametro: float) -> List[List[int]]:
   ```
3. **Imutabilidade de Entrada**: Funções matemáticas não devem modificar a matriz de entrada in-place, retornando sempre uma nova matriz (`[[0 for _ in range(W)] for _ in range(H)]`).
4. **Testes Unitários**: Manter os testes de cada módulo em `backend/tests/test_pdi.py`.

---

## ⚡ Frontend Vue 3 + TypeScript
1. **Composition API**: Uso exclusivo de `<script setup lang="ts">`.
2. **Componentização**:
   - Componentes visuais atômicos em `src/components/`.
   - Componentes de domínio de tela em `src/views/<nome>/components/`.
3. **Nomenclatura**:
   - Arquivos `.vue` em `PascalCase` (ex: `CardImage.vue`, `GraficoDeBarras.vue`).
   - Serviços em `PascalCase` com sufixo `Service` (ex: `PythonPdiService.ts`).
   - Stores em `PascalCase` com sufixo `Store` (ex: `LayoutStore.ts`).

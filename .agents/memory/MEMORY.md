# Memória Persistente do Projeto (MEMORY.md)

Este arquivo registra o histórico arquitetural, decisões fundamentais e o estado do sistema PDI.

---

## 📌 Contexto e Identidade
- **Nome do Projeto**: Sistema de Processamento Digital de Imagens (PDI).
- **Finalidade**: Aplicação acadêmica e analítica com algoritmos matemáticos puros em Python para visualização de transformações de imagens.
- **Diferencial Crítico**: Não utiliza OpenCV ou SciPy ndimage. Todos os 18 filtros operam diretamente sobre matrizes bidimensionais nativas de inteiros.

---

## 🎯 Decisões Técnicas Registradas

1. **Separação de Camadas**:
   - Backend Python 3.14 com FastAPI na porta 8000.
   - Frontend Vue 3 + Vuetify + TypeScript, compilado para `dist/`.
   - Em produção, o FastAPI serve diretamente os arquivos de `dist/`.
   - Em desenvolvimento, o Vite roda na porta 5173 com proxy para `/api` na porta 8000.
2. **Correção de Array no Frontend (27/09/2026)**:
   - Em `src/utils/imageUtils.ts`, o uso incorreto de `row.append` foi substituído pelo padrão `row.push(intensity)`.
3. **Compatibilidade de Encoding no Windows**:
   - `run.py` configura `sys.stdout.reconfigure(encoding='utf-8')` e `iniciar.bat` usa `chcp 65001` para evitar erros de charset CP1252.
4. **Organização das Pastas**:
   - Documentações acadêmicas em `docs/`.
   - Scripts utilitários em `scripts/` (`build.bat`, `test.bat`, `dev.bat`).
   - AG Kit completo em `.agents/`.

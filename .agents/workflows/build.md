---
description: Procedimento operacional para compilar o front-end Vue 3 / Vite para entrega pelo FastAPI.
---

# Workflow: Compilar Front-end (Build)

## Execução da Compilação

1. No terminal na raiz do projeto:
   ```bash
   npm run build
   ```
   *(Ou execute `scripts/build.bat`).*

## O que este comando faz:
1. Executa verificação de tipos com TypeScript via `vue-tsc --build --force`.
2. Compila a aplicação Vue 3 com Vite para a pasta `dist/`.
3. Gera assets otimizados e minificados prontos para serem servidos pelo backend FastAPI.

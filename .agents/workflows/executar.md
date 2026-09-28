---
description: Procedimento operacional para inicializar o backend e frontend integrados.
---

# Workflow: Executar o Projeto PDI

## 1. Modo Integrado (Produção Local - Porta 8000)

1. Certifique-se de que o front-end foi compilado para `dist/`:
   ```bash
   npm run build
   ```
2. Inicie o servidor FastAPI:
   ```bash
   python run.py
   ```
   *(Ou execute `iniciar.bat` diretamente na raiz).*
3. Abra o navegador em: [http://localhost:8000](http://localhost:8000).

---

## 2. Modo Desenvolvimento (Hot-Reload - Porta 5173 + 8000)

1. Terminal 1 (Backend):
   ```bash
   python run.py
   ```
2. Terminal 2 (Frontend Vite):
   ```bash
   npm run dev
   ```
   *(Ou execute `scripts/dev.bat`).*
3. Acesse: [http://localhost:5173](http://localhost:5173).

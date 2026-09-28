"""
===============================================================================
SCRIPT DE INICIALIZAÇÃO DO BACKEND (PONTO DE ENTRADA / RUN.PY)
===============================================================================
Inicia o servidor ASGI Uvicorn para servir a aplicação FastAPI com suporte a:
- Recarregamento automático (hot-reload) durante o desenvolvimento.
- Documentação interativa OpenAPI/Swagger acessível em: http://localhost:8000/docs
- Documentação alternativa ReDoc acessível em: http://localhost:8000/redoc
"""

import sys
import uvicorn

if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("=" * 70)
    print(">> INICIANDO SISTEMA DE PROCESSAMENTO DIGITAL DE IMAGENS (PDI)")
    print("Backend: Python 3.14 + FastAPI + Uvicorn")
    print("Endereço da Aplicação : http://localhost:8000")
    print("Documentação Swagger   : http://localhost:8000/docs")
    print("Documentação ReDoc     : http://localhost:8000/redoc")
    print("=" * 70)

    # Inicia o servidor HTTP ASGI na porta 8000 escutando em todas as interfaces de rede (0.0.0.0)
    # reload=True reinicia o servidor automaticamente caso qualquer arquivo Python seja alterado
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)


"""
===============================================================================
ENTRYPOINT SERVERLESS - VERCEL (FastAPI Python Runtime)
===============================================================================
Este arquivo expõe a instância do FastAPI para o runtime Serverless da Vercel.
Todas as requisições direcionadas para /api/* são roteadas para esta função.
"""

import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH para importar o pacote 'backend'
diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)

from backend.app import app

# Exporta explicitamente para o runtime Vercel
app = app

"""
===============================================================================
SERVIDOR FASTAPI - API RESTFUL DE PROCESSAMENTO DIGITAL DE IMAGENS (PDI)
===============================================================================
Este servidor expõe os endpoints HTTP consumidos pelo front-end SPA (Vue 3 / Vite).

Arquitetura do Sistema:
    [ Front-end Vue 3 / Vuetify ]
                 ↕ (JSON / HTTP REST - Base64 ou Matriz 2D)
    [ FastAPI (backend/app.py) ]
                 ↕
    [ Motor de PDI em Python Puro (backend/pdi/) ]
        ├── pontuais.py      -> Operações s = T(r) (Negativo, Log, Gamma, Expansão/Compressão, Soma)
        ├── espaciais.py     -> Filtros espaciais (Média, Mediana, Moda, Mín, Máx, Laplaciano, High Boost, Prewitt, Sobel)
        ├── geometricos.py   -> Transformações geométricas (Replicação 512/1024, Bilinear 512/1024, Flip H/V, Rotações)
        ├── histograma.py    -> Análise estatística de frequências e Equalização via CDF/LUT
        └── ponta_de_prova.py-> Consulta interativa de coordenadas (x, y) e nível de cinza (NC)
"""

import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.pdi import (
    obter_ponta_de_prova,
    calcular_histograma,
    equalizar_histograma,
    rotacao_90_horario,
    rotacao_90_antihorario,
    rotacao_180,
    executar_pipeline,
    aplicar_filtro_individual,
    base64_to_matrix,
    matrix_to_base64,
)

# Instância principal da aplicação FastAPI
app = FastAPI(
    title="PDI Python Backend",
    description="Backend em Python puro para Processamento Digital de Imagens (Sem OpenCV / Sem SciPy)",
    version="2.0.0",
)

# Configuração do Middleware de CORS (Cross-Origin Resource Sharing):
# Permite que o servidor de desenvolvimento do Vite (http://localhost:5173 ou similar)
# faça requisições HTTP seguras para o servidor FastAPI (porta 8000) sem bloqueios do navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# MODELOS PYDANTIC (VALIDAÇÃO E TIPAGEM ESTÁTICA DOS PAYLOADS JSON)
# =============================================================================

class ItemFiltro(BaseModel):
    """Representa um item individual na fila de processamento do pipeline."""
    tipo: int                             # Código numérico do enum do filtro (1 a 28)
    params: Optional[Dict[str, Any]] = None # Parâmetros específicos (ex: gamma, a, b, mascara, etc.)


class RequisicaoProcessar(BaseModel):
    """Payload para a rota /api/processar."""
    imagem: Any                           # Imagem de entrada: string Base64 ou Matriz 2D List[List[int]]
    filtros: List[ItemFiltro]             # Fila sequencial ordenada de filtros a serem aplicados


class RequisicaoRotacao(BaseModel):
    """Payload para rota /api/rotacao."""
    imagem: Any
    tipo: str                             # '90_horario', '90_antihorario' ou '180'


class RequisicaoHistograma(BaseModel):
    """Payload para rotas /api/histograma e /api/equalizacao."""
    imagem: Any


class RequisicaoPontaDeProva(BaseModel):
    """Payload para consulta pontual via ferramenta Ponta de Prova."""
    imagem: Any
    x: int                                # Coordenada horizontal (coluna)
    y: int                                # Coordenada vertical (linha)


def _obter_matriz(entrada_imagem: Any) -> List[List[int]]:
    """
    Função Auxiliar de Conversão Polimórfica:
    Normaliza a imagem recebida na requisição (seja string codificada em Base64
    ou matriz 2D já descompactada) em uma matriz bidimensional de inteiros [0, 255].
    """
    if isinstance(entrada_imagem, str):
        if not entrada_imagem.strip():
            raise HTTPException(status_code=400, detail="Imagem Base64 vazia.")
        return base64_to_matrix(entrada_imagem)
    elif isinstance(entrada_imagem, list):
        return entrada_imagem
    else:
        raise HTTPException(
            status_code=400,
            detail="Formato de imagem inválido. Deve ser matriz 2D ou string Base64."
        )


# =============================================================================
# ROTAS / ENDPOINTS DA API RESTFUL
# =============================================================================

@app.get("/api/status")
def status():
    """Endpoint de checagem de saúde (health check) e diagnóstico do backend."""
    return {
        "status": "online",
        "linguagem": "Python 3.14",
        "versao": "2.0.0",
        "pdi_engine": "Implementação pura (sem bibliotecas de terceiros de PDI)",
    }


@app.post("/api/processar")
def processar_imagem(req: RequisicaoProcessar):
    """
    Endpoint Principal de Processamento:
    Aplica a fila de filtros em sequência sobre a imagem de entrada e retorna:
        - imagem_base64: Imagem resultante codificada em Base64 para exibição rápida
        - matriz: Matriz bidimensional completa dos pixels
        - histograma: Dados estatísticos recalculados após a filtragem
        - extras: Dados específicos retornados por operações especiais (ex: CDF na equalização)
    """
    try:
        matriz_inicial = _obter_matriz(req.imagem)
        if len(matriz_inicial) == 0:
            raise HTTPException(status_code=400, detail="Imagem sem dados ou vazia.")

        # Converte os modelos Pydantic da fila em dicionários puros do Python
        filtros_dict = [f.model_dump() for f in req.filtros]

        # Executa o pipeline de funções encadeadas no motor de PDI
        matriz_final, extras = executar_pipeline(matriz_inicial, filtros_dict)

        # Gera a representação Base64 para a interface web
        img_b64 = matrix_to_base64(matriz_final)
        altura = len(matriz_final)
        largura = len(matriz_final[0]) if altura > 0 else 0

        # Computa o histograma resultante da imagem final
        hist = calcular_histograma(matriz_final)

        return {
            "sucesso": True,
            "imagem_base64": img_b64,
            "matriz": matriz_final,
            "largura": largura,
            "altura": altura,
            "histograma": hist,
            "extras": extras,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rotacao")
def rotacionar_imagem(req: RequisicaoRotacao):
    """
    Endpoint Especializado para Rotações Geométricas:
    Suporta 90° horário, 90° anti-horário e 180°.
    """
    try:
        matriz = _obter_matriz(req.imagem)
        tipo = req.tipo.lower()

        if tipo in ("90_horario", "90_cw", "horario"):
            matriz_rot = rotacao_90_horario(matriz)
        elif tipo in ("90_antihorario", "90_ccw", "antihorario"):
            matriz_rot = rotacao_90_antihorario(matriz)
        elif tipo in ("180", "180_graus"):
            matriz_rot = rotacao_180(matriz)
        else:
            raise HTTPException(status_code=400, detail=f"Tipo de rotação inválido: {req.tipo}")

        img_b64 = matrix_to_base64(matriz_rot)
        altura = len(matriz_rot)
        largura = len(matriz_rot[0]) if altura > 0 else 0
        hist = calcular_histograma(matriz_rot)

        return {
            "sucesso": True,
            "imagem_base64": img_b64,
            "matriz": matriz_rot,
            "largura": largura,
            "altura": altura,
            "histograma": hist,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/histograma")
def obter_histograma(req: RequisicaoHistograma):
    """
    Endpoint para Cálculo de Histograma:
    Retorna a contagem de frequência de cada nível de cinza [0, 255] e metadados.
    """
    try:
        matriz = _obter_matriz(req.imagem)
        dados_hist = calcular_histograma(matriz)
        return {
            "sucesso": True,
            **dados_hist,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/equalizacao")
def equalizar_imagem(req: RequisicaoHistograma):
    """
    Endpoint de Equalização de Histograma:
    Executa a equalização global baseada na Função de Distribuição Acumulada (CDF),
    retornando a imagem equalizada e o respectivo histograma resultante.
    """
    try:
        matriz = _obter_matriz(req.imagem)
        matriz_eq, hist_resultante = equalizar_histograma(matriz)
        img_b64 = matrix_to_base64(matriz_eq)

        return {
            "sucesso": True,
            "imagem_base64": img_b64,
            "matriz": matriz_eq,
            "histograma": hist_resultante,
            "largura": len(matriz_eq[0]) if len(matriz_eq) > 0 else 0,
            "altura": len(matriz_eq),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ponta-de-prova")
def ponta_de_prova(req: RequisicaoPontaDeProva):
    """
    Endpoint da Função Ponta de Prova:
    Consulta e retorna o Nível de Cinza (NC) e validade do pixel na posição (x, y).
    """
    try:
        matriz = _obter_matriz(req.imagem)
        resultado = obter_ponta_de_prova(matriz, req.x, req.y)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# SERVIÇO DE ARQUIVOS ESTÁTICOS DO FRONT-END EM PRODUÇÃO
# =============================================================================
# Se o front-end tiver sido compilado ('npm run build') e a pasta 'dist' existir,
# o próprio FastAPI servirá os arquivos estáticos compilados (HTML/CSS/JS).
caminho_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))

if os.path.isdir(caminho_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(caminho_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        arquivo = os.path.join(caminho_dist, full_path)
        if os.path.isfile(arquivo):
            return FileResponse(arquivo)
        # Fallback para SPA (Single Page Application): redireciona rotas para index.html
        return FileResponse(os.path.join(caminho_dist, "index.html"))


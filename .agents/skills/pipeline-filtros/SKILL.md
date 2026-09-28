---
name: pipeline-filtros
description: Arquitetura e gerenciamento do pipeline sequencial de filtros não-destrutivo no front-end e backend.
---

# Skill: Pipeline de Filtros Não-Destrutivo

Esta skill descreve o fluxo de gerenciamento da fila ordenada de filtros no Sistema PDI.

---

## 1. Princípios do Pipeline Não-Destrutivo
1. **Origem Imutável**: O estado `imagemOriginal` nunca é alterado por nenhum filtro.
2. **Encadeamento Sequencial**: Cada filtro recebe a saída do filtro anterior:
   $$I_0 \xrightarrow{F_1} I_1 \xrightarrow{F_2} I_2 \dots \xrightarrow{F_n} I_n$$
3. **Reversão com Custo Zero**: Para remover um filtro, basta removê-lo da lista e reprocessar $I_0$ com a lista restante.
4. **Limpeza Completa**: A ação *Limpar Filtros* redefine a fila para `[]` e exibe imediatamente a `imagemOriginal`.

---

## 2. Estrutura do Payload de Pipeline
O backend espera um array tipado de filtros em `POST /api/processar`:
```json
{
  "imagem": "<base64_ou_matriz>",
  "filtros": [
    {
      "tipo": 15,
      "params": { "mascara": 3 }
    },
    {
      "tipo": 2,
      "params": {}
    }
  ]
}
```

---

## 3. Adição de Novos Filtros no Pipeline
Ao implementar um novo tipo de filtro:
1. Adicione o código no enum `ETipoFiltroPDI.ts` do frontend.
2. Adicione o caso correspondente no `processador.py` e `app.py`.
3. Garanta que parâmetros extras (ex: $\gamma$, máscaras, fatores de ampliação) sejam serializáveis em JSON.

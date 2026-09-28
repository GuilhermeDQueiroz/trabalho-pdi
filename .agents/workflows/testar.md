---
description: Procedimento operacional para executar a suíte de testes unitários do motor matemático.
---

# Workflow: Testar Algoritmos de PDI

## Execução dos Testes Unitários

1. No terminal na raiz do projeto:
   ```bash
   python -m unittest backend/tests/test_pdi.py
   ```
   *(Ou dê duplo clique em `scripts/test.bat`).*

## Saída Esperada
```
..............
----------------------------------------------------------------------
Ran 14 tests in 0.0xxs

OK
```

## Diretrizes de Novos Testes
- Sempre que criar um novo filtro em `backend/pdi/`, adicione uma classe ou método `test_<nome_do_filtro>` em `backend/tests/test_pdi.py`.
- Teste valores limites ($0$, $255$), matrizes $1 \times 1$, $3 \times 3$ e casos com valores negativos para verificar o clamping.

# Universal Rules - Sistema PDI

> Regras sempre ativas para qualquer interação no projeto.

---

## 1. Idioma da Comunicação
- Responda no idioma do usuário (Português do Brasil).
- Variáveis, funções e comentários de código devem seguir o padrão preexistente no projeto (nomes em português ou inglês conforme os módulos já estabelecidos).

---

## 2. Clean Code & Qualidade
- Código conciso, direto e legível.
- Evitar over-engineering ou abstrações desnecessárias.
- Tipagem TypeScript estrita no frontend (`<script setup lang="ts">`).
- Tipagem de tipos no Python via Type Hints (`List[List[int]]`, `Dict[str, Any]`, `Tuple`).

---

## 3. Integridade dos Testes
- Nunca quebrar os 14 testes unitários em `backend/tests/test_pdi.py`.
- Se uma nova função de PDI for adicionada ao motor matemático, adicione o respectivo teste unitário.

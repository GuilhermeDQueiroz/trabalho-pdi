# Catálogo de Arquitetura do Sistema PDI (.agents)

Este documento centraliza todos os agentes, skills, memórias, regras e fluxos de trabalho do projeto de Processamento Digital de Imagens.

---

## 🤖 Agentes Especialistas (`.agents/agent/`)

| Agente | Arquivo | Responsabilidade |
|---|---|---|
| **@especialista-pdi** | `agent/especialista-pdi.md` | Algoritmos matemáticos de PDI em Python puro (pontuais, espaciais, geométricos, histograma) |
| **@frontend-specialist** | `agent/frontend-specialist.md` | Interface Vue 3 / Vuetify, HTML5 Canvas, ApexCharts, ponta de prova e tema monocromático |
| **@orchestrator** | `agent/orchestrator.md` | Coordenação geral, pipeline sequencial, compatibilidade e validação de ponta a ponta |

---

## 📚 Skills Especializadas (`.agents/skills/`)

| Skill | Diretório | Descrição |
|---|---|---|
| **@algoritmos-pdi** | `skills/algoritmos-pdi/SKILL.md` | Padrões de implementação matemática de filtros, convoluções 2D, máscaras e clamping |
| **@pipeline-filtros** | `skills/pipeline-filtros/SKILL.md` | Arquitetura do pipeline sequencial não-destrutivo e recálculo dinâmico |
| **@inspecao-imagem-canvas** | `skills/inspecao-imagem-canvas/SKILL.md` | Inspeção ponta de prova (x, y, NC) e conversão bidirecional Base64 <-> Matriz 2D |

---

## 🧠 Memórias Persistentes (`.agents/memory/`)

| Memória | Arquivo | Conteúdo |
|---|---|---|
| **MEMORY.md** | `memory/MEMORY.md` | Convenções, estado atual do projeto e decisões arquiteturais |
| **pdi-engine.md** | `memory/pdi-engine.md` | Fórmulas teóricas e detalhes dos 18 algoritmos implementados |
| **project-conventions.md** | `memory/project-conventions.md` | Padrões de código Python PEP8, TypeScript, Vue 3 e scripts |

---

## 📜 Regras de Governança (`.agents/rules/`)

| Regra | Arquivo | Descrição |
|---|---|---|
| **pdi-pure-algorithms.md** | `rules/pdi-pure-algorithms.md` | Proibição absoluta de OpenCV/SciPy e garantia de pureza matemática |
| **core-protocol.md** | `rules/core-protocol.md` | Protocolo modular de ativação e carregamento de skills |
| **universal-rules.md** | `rules/universal-rules.md` | Diretrizes universais de Clean Code e segurança |
| **request-routing.md** | `rules/request-routing.md` | Roteamento automático de agentes por intenção do usuário |

---

## 🔄 Workflows Operacionais (`.agents/workflows/`)

| Workflow | Arquivo | Ação |
|---|---|---|
| **executar** | `workflows/executar.md` | Instruções para iniciar backend e frontend integrados |
| **testar** | `workflows/testar.md` | Execução e expansão da suíte de testes unitários |
| **build** | `workflows/build.md` | Procedimento de compilação do frontend Vue para `dist/` |

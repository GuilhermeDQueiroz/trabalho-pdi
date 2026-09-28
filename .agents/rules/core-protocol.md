# Core Protocol - Sistema PDI

> As regras de maior prioridade para carregamento de agentes e skills neste projeto.

---

## 1. Protocolo de Carregamento Modular de Skills

Quando um agente for ativado:
1. Verifique o campo `skills:` no frontmatter do agente.
2. Leia o `SKILL.md` principal da skill selecionada.
3. Carregue apenas as seções relevantes para a tarefa solicitada.

### Anúncio Obrigatório de Skill
Sempre que uma skill for carregada e utilizada, anuncie antes da resposta:
```markdown
📚 **Using skill: `@[skill-name]`...**
```

---

## 2. Princípio "Read → Understand → Apply"

Antes de alterar qualquer código no motor matemático ou no frontend:
1. **Qual é o objetivo da alteração?**
2. **Qual formulação matemática está sendo aplicada?**
3. **Como garantir que a pureza algorítmica (sem OpenCV) e o pipeline não-destrutivo sejam mantidos?**
4. **Os testes unitários continuam passando?**

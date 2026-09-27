# Regras do Projeto — Campanha Debate RAG

Qualquer agente (Cursor, Claude Code, ou outro) deve ler este arquivo por inteiro antes de implementar qualquer mudança neste repositório. Isso vale antes da primeira linha de código também.

## Contexto rápido

- Ferramenta interna (só a equipe de estratégia, ~3 pessoas) para extrair, organizar e consultar (via RAG) conteúdo de vídeos de debates e programas eleitorais.
- Sem usuários públicos, sem cadastro externo, sem cobrança — isso muda o peso de várias regras abaixo (marcado item a item).
- Stack: Python + FastAPI, PostgreSQL + pgvector (EasyPanel), Whisper local (faster-whisper), GLiNER local, yt-dlp, deploy via Docker + GitHub → EasyPanel.
- Docs de produto: [docs/PRD.md](docs/PRD.md) e [docs/TRD.md](docs/TRD.md).

## 1. Checklist de segurança antes de qualquer deploy

Para cada item, ao aplicar: status atual, arquivo/config verificado, correção aplicada (se houver), comando/evidência de validação, riscos restantes. Não marcar como concluído sem evidência real.

1. Oculte as chaves de API — **aplica-se**: `.env` fora do git, nunca hardcode.
2. Remova segredos do histórico do Git — **aplica-se**: rodar `gitleaks` antes do primeiro push público.
3. Use uma chave pública para o banco de dados — **N/A como está**: Postgres só é acessado pelo backend, na mesma rede do EasyPanel, sem client público exposto; revisar se isso mudar.
4. Ative Row-Level Security — **adaptado**: sem múltiplos tenants; ainda assim, aplicar RLS se as 3 pessoas da equipe passarem a acessar o Postgres diretamente (não só via API).
5. Criptografe dados sensíveis — **aplica-se**: nenhuma credencial em texto puro; usar variáveis de ambiente e secrets do EasyPanel.
6. Imponha autenticação no lado do servidor — **aplica-se**: toda rota da API exige auth, mesmo com só 3 usuários.
7. Restrinja o acesso aos registros — **aplica-se**: só os 3 usuários autenticados, sem acesso anônimo.
8. Impeça a adulteração de campos — **aplica-se**: validar payloads na API, nunca confiar em IDs/permissões vindos do cliente.
9. Proteja os cookies de sessão — **aplica-se se houver login por sessão**: `httpOnly`, `secure`, `sameSite`.
10. Armazene senhas com hash — **aplica-se**: bcrypt/argon2, nunca texto puro.
11. Limite tentativas de login — **adaptado**: risco baixo com 3 usuários fixos, mas manter um rate-limit simples (ver seção 3) já cobre isso.
12. Adicione proteção contra bots — **N/A por ora**: sem cadastro/formulário público exposto; reavaliar se o RAG ganhar interface pública.
13. Use consultas parametrizadas — **aplica-se**: nunca montar SQL por concatenação de string.
14. Valide todas as entradas de dados — **aplica-se**.
15. Escape o conteúdo enviado pelos usuários — **aplica-se onde houver output em HTML/UI**.
16. Restrinja uploads de arquivos — **aplica-se**: validar tipo/tamanho, mesmo sendo só a equipe subindo vídeo/PDF.
17. Retorne apenas os dados necessários nas respostas da API — **aplica-se**.
18. Adicione cabeçalhos de segurança — **aplica-se**: HSTS, X-Content-Type-Options, etc.
19. Force o uso de HTTPS — **já coberto pelo EasyPanel** (proxy reverso com Let's Encrypt).
20. Faça varreduras de segurança nas dependências — **aplica-se**: `pip-audit` no CI.

## 2. Fluxo de trabalho (GitHub)

- Toda tarefa vira uma Issue, classificada como `correção`, `melhoria` ou `nova função`.
- Todo Pull Request:
  - referencia a Issue relacionada;
  - explica o que mudou;
  - descreve como foi validado (comando/print/log);
  - registra riscos, limitações e próximos passos.
- Nada de merge direto na branch principal sem PR.

## 3. Esteira de qualidade (adaptada para stack Python)

Verificado nos templates oficiais do EasyPanel (easypanel.io/templates): **GlitchTip** e **Uptime Kuma** existem como templates prontos — usados abaixo no lugar de ferramentas pagas.

| Categoria | Ferramenta pedida originalmente | Situação | O que usar aqui |
| --- | --- | --- | --- |
| Lint/format | Biome | N/A (Biome é JS/TS) | **Ruff** (lint + format, Python, grátis) |
| Dead code | Knip | N/A (JS/TS) | **vulture** / **deptry** (Python, grátis) |
| Mutation testing | Stryker | N/A (JS/TS) | **mutmut** (Python, grátis) — opcional, só se sobrar tempo |
| Commit lint | Commitlint | Mantém | Commitlint (Node, grátis) — funciona independente da stack do backend |
| Arquitetura/fronteiras | arch-contract | N/A direto | **import-linter** (Python, grátis) — define camadas permitidas |
| Testes unit/integração | — | Mantém | pytest + pytest-cov |
| Testes E2E | Playwright / Endtest | Playwright mantém, Endtest removido | **Playwright** (grátis, tem API Python) — Endtest é SaaS pago |
| Cobertura | Codecov | Removido (pago p/ repo privado) | `pytest --cov` + relatório no próprio CI (GitHub Actions), sem SaaS externo |
| Erros/observabilidade | Sentry / Datadog / New Relic | Trocado | **GlitchTip** (self-hosted, compatível com SDK do Sentry, template oficial do EasyPanel) para erros; **Uptime Kuma** (template oficial do EasyPanel) para uptime. Datadog/New Relic removidos — overkill para 3 usuários |
| Tracing | OpenTelemetry | Adiado | Padrão aberto e grátis, mas a complexidade não se justifica ainda nesta escala — revisar se o uso crescer |
| Rate limit | — | Aplica-se | `slowapi` (FastAPI, grátis) |
| HTTPS/reverse proxy | — | Já coberto | EasyPanel já provisiona Let's Encrypt |

## 4. Arquitetura

- Evitar overengineering — projeto de 1 desenvolvedor; preferir um monólito simples (API + worker) a microsserviços.
- Componentizar desde o início, mas sem abstrações prematuras.
- Nunca reconstruir o que já existe — antes de escrever uma função nova, checar se `yt-dlp`, `faster-whisper`, `GLiNER` ou uma lib padrão já resolve.
- Fronteiras claras entre: ingestão (download + transcrição), armazenamento (Postgres + pgvector) e consulta (RAG/API).

## 5. Produto/Interface (quando houver UI)

- Este MVP é majoritariamente backend/RAG. Se/quando uma interface for construída para a equipe consultar o RAG:
  - lazy loading quando fizer sentido;
  - skeleton screens para carregamento;
  - feedback visual para ações (ex.: "processando vídeo", "gerando resposta do RAG");
  - transições consistentes entre telas/cards/modais.
- Referência de motion (avaliar só quando houver UI): https://github.com/kylezantos/design-principles
- Termos de uso / política de privacidade / revisão jurídica: **N/A** — ferramenta interna, sem usuários externos. Reavaliar se isso mudar.

## 6. Infraestrutura (EasyPanel)

- Este projeto tem sua **própria** instância de PostgreSQL/pgvector no EasyPanel — nunca reaproveitar o banco de outro projeto.
- Padrão para todo projeto novo: um "projeto" isolado no EasyPanel por repositório (app + banco + worker), provisionado via MCP do EasyPanel (servidor oficial remoto, ou um MCP de terceiros como `easypanel-mcp-server`) acionado a partir do Cursor/Claude. Isso mantém cada projeto limpo e sem risco de um afetar o banco/serviços de outro.
- Monitoramento (GlitchTip, Uptime Kuma) fica centralizado em um projeto EasyPanel separado, chamado **infra-core**, compartilhado entre todos os projetos — este projeto se registra nele, não sobe sua própria instância de monitoramento.
- Status: GlitchTip e Uptime Kuma já instalados em `infra-core` — GlitchTip em https://infra-core-glitchtip.kxryyk.easypanel.host , Uptime Kuma em https://infra-core-uptimekuma.kxryyk.easypanel.host . Pendente: criar o primeiro usuário admin do GlitchTip (`./manage.py createsuperuser` dentro do container, via terminal do EasyPanel ou SSH na VPS).

## 7. Antes de considerar uma tarefa "pronta"

- Validação não documentada não existiu. Toda entrega cita o comando/evidência que a comprova.
- Se a validação não está automatizada no fluxo (CI), ela vira tarefa manual — e tarefa manual se perde conforme o projeto acelera. Automatizar assim que possível.

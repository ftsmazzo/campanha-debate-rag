# TRD — Campanha Debate RAG

> Technical Requirements Document — traduz o PRD em decisões técnicas.
> Depende de: [PRD](PRD.md)

**Data**: 2026-09-27

## 1. Stack tecnológica

| Camada | Tecnologia | Motivo/restrição |
| --- | --- | --- |
| Backend | Python + FastAPI | Sugestão: ecossistema maduro para Whisper/GLiNER/ML, fácil de conteinerizar no EasyPanel |
| Download de vídeo | yt-dlp | Sugestão: biblioteca open-source madura e ativamente mantida, evita reescrever lógica de download do zero |
| Transcrição | Whisper (via faster-whisper) | Decidido pelo usuário (Whisper); faster-whisper sugerido para rodar bem em CPU na VPS. Chunking de áudio em blocos ≤ 20 min via ffmpeg antes de transcrever |
| Segmentação por orador (Onda 2) | GLiNER (já rodando localmente) | Aproveita modelo já disponível do usuário; combinado a marcações estruturais do texto, evita diarização de áudio pesada numa primeira versão |
| Banco de dados / vetor | PostgreSQL + pgvector | Decidido pelo usuário — instância nova e dedicada a este projeto, provisionada no EasyPanel (não reaproveita instância existente de outro projeto) |
| Embeddings | Modelo multilíngue self-hosted (ex.: BGE-M3) | **Sugestão a confirmar**: mantém tudo rodando na própria VPS, sem dependência de API externa nem custo por token — coerente com Whisper/GLiNER/Postgres já self-hosted |
| Processamento assíncrono | Worker Python consumindo fila em tabela do próprio Postgres | Sugestão: evita depender de Redis/Celery, dado que só uma pessoa mantém o sistema |
| Deploy | Docker + GitHub → EasyPanel | Decidido pelo usuário |

## 2. Integrações externas

| Integração | Finalidade | Observações |
| --- | --- | --- |
| YouTube (via yt-dlp) | Baixar áudio/vídeo das fontes | Não é API oficial — sujeito a mudanças do YouTube; manter yt-dlp atualizado |
| Whisper (local, faster-whisper) | Transcrição de áudio | Roda na própria VPS, sem dependência de API paga |
| GLiNER (local) | NER para apoiar segmentação por orador | Já em uso na máquina do usuário |
| Provedor de embeddings | Gerar vetores para o RAG | Ver sugestão (BGE-M3 self-hosted) — a confirmar |

## 3. Requisitos não-funcionais

- Confiabilidade é a prioridade explícita do usuário — preferir bibliotecas maduras/ativas (yt-dlp, faster-whisper) e arquitetura simples (menos peças móveis) em vez de otimizar por performance bruta.
- Volume: dezenas de vídeos nas 5 bases — processamento pode ser assíncrono, não precisa ser em tempo real.
- Segurança/confidencialidade: sem exigência formal declarada, mas é material de campanha eleitoral — manter repositório privado e RAG acessível só à equipe.
- Escalabilidade: baixa exigência — uso por ~3 pessoas, sem necessidade de suportar carga concorrente pesada.
- Idioma: conteúdo 100% em português — garantir bom suporte PT-BR no Whisper e no modelo de embeddings.

## 4. Ambiente e deploy

- Onde roda: VPS própria do usuário, gerenciada via EasyPanel.
- Banco: PostgreSQL + pgvector — instância dedicada, provisionada especificamente para este projeto (não compartilhada com outros projetos).
- Padrão de infraestrutura: cada projeto novo recebe seu próprio "projeto" isolado no EasyPanel (app + banco + worker), provisionado via MCP do EasyPanel (servidor oficial remoto do EasyPanel, ou um MCP de terceiros como easypanel-mcp-server) acionado a partir do Cursor/Claude — garante um ambiente limpo por projeto, sem risco de um projeto afetar o banco de outro.
- Monitoramento (GlitchTip, Uptime Kuma): centralizado em um projeto EasyPanel separado ("infra-core"), compartilhado entre todos os projetos — cada app se registra nele em vez de subir sua própria instância de monitoramento.
- Repositório: GitHub (a criar); deploy para o EasyPanel a partir desse repositório (build via Docker).
- Desenvolvimento: localmente no Cursor e/ou em conjunto com o assistente (Claude Code).

## 5. Restrições herdadas

- GLiNER já roda localmente na máquina do usuário — aproveitar esse modelo já disponível em vez de introduzir uma ferramenta de NER nova.
- Correção: o Postgres/pgvector deste projeto NÃO reaproveita uma instância já existente no EasyPanel — é uma instância nova, dedicada só a este projeto (ver Ambiente e deploy).

## 6. Manutenção

- Só o usuário mantém o código — favorecer arquitetura simples (poucos serviços, poucas dependências externas) em vez de arquitetura distribuída, para reduzir carga operacional de uma pessoa só.

---

Documento vivo também disponível como Claude Doc: https://claude.ai/code/artifact/75910468-cba1-43a5-995f-a35b093a1571

# Campanha Debate RAG

Ferramenta interna da equipe de estratégia de campanha para extrair, organizar e consultar (via RAG) o conteúdo de debates eleitorais e programas de TV/rádio de candidatos — apoio à preparação de debates.

## Antes de começar a codar

1. Leia **`CLAUDE.md`** — regras do projeto (segurança, fluxo de PR/Issue, esteira de qualidade, arquitetura). Vale para qualquer agente (Cursor, Claude Code, etc.), não só humanos.
2. Leia **`docs/PRD.md`** (o quê e por quê) e **`docs/TRD.md`** (stack e decisões técnicas).
3. Este projeto ainda está no dia 0 — sem código ainda. O TRD já define: Python + FastAPI, PostgreSQL + pgvector (já hospedado no EasyPanel do usuário), Whisper local via faster-whisper, GLiNER local, yt-dlp para download.

## Estrutura

```
campanha-debate-rag/
├── CLAUDE.md          # regras do projeto — leitura obrigatória antes de codar
├── docs/
│   ├── PRD.md
│   └── TRD.md
├── src/               # código da aplicação (a criar)
├── .cursor/rules/     # mesmas regras, em formato Cursor
└── .github/           # templates de Issue/PR (a criar)
```

## Prioridade imediata (Onda 1 do MVP — ver PRD)

1. Localizar e confirmar links no YouTube das 5 bases de vídeos.
2. Baixar áudio (yt-dlp) e transcrever (faster-whisper, com chunking ≤ 20 min).
3. Organizar o conteúdo extraído por base/vídeo.
4. Gerar embeddings e indexar no pgvector (EasyPanel) para consulta via RAG.

## Deploy

- Repositório GitHub (a criar) → build Docker → EasyPanel (produção).
- Banco: usar a instância PostgreSQL/pgvector já existente no EasyPanel — não provisionar outra.

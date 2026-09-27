# Esquema Backend — Campanha Debate RAG

> Modelagem de dados e API.
> Depende de: [TRD](TRD.md)

**Data**: 2026-09-27

## Entidades principais

| Entidade | Campos-chave | Observação |
| --- | --- | --- |
| **Base** | nome, **papel** (`central` \| `referencia_estrategica`), marqueteiro (nullable) | Bahia é `referencia_estrategica`: não é sobre os candidatos da corrida atual, serve só pra mapear o padrão do marqueteiro (Sidônio, o mesmo estrategista do Lula) — não se mistura com o conteúdo central nas análises |
| **Video** | base_id, titulo, data, source_url, **source_type** (`youtube_video` \| `youtube_channel` \| `article_page` \| `podcast_platform`), **resolved_media_url** (nullable), **resolution_status** (`pendente` \| `resolvido` \| `nao_resolvido_manual`), participantes | Muitos `source_url` enviados pelo cliente não são o vídeo em si (matéria, canal, página de podcast) — por isso a resolução de fonte é um campo/etapa própria, não uma suposição |
| **Transcript** | video_id, texto_completo, segmentos com timestamp, idioma, duracao_segundos | Gerado pelo Whisper com chunking de áudio |
| **TranscriptSegment** (Onda 2) | transcript_id, inicio, fim, orador (nullable até Onda 2 rodar), texto | Só para bases com múltiplos candidatos (debates) |
| **Chunk/Embedding** | transcript_id (ou transcript_segment_id), texto_chunk, embedding (vector), metadata (base, video, data) | Indexado no pgvector, usado pelo RAG |

## Autenticação e autorização

- Login simples, 3 usuários, todos no mesmo nível de permissão — sem hierarquia de acesso.

## Interface principal: servidor MCP (não só REST)

Decisão: a forma primária de consumir o RAG é um **servidor MCP** exposto pelo próprio backend, com ferramentas como `buscar_trechos(pergunta, base?, marqueteiro?)`, `listar_videos(base)`, `get_transcript(video_id)`, `status_processamento(base)`. Isso permite que uma IA (Claude ou outra) monte as estratégias de debate diretamente consultando o RAG — é como o cliente já opera. Uma API REST simples pode existir por baixo como camada técnica, mas o MCP é a interface de produto real.

## Processamento assíncrono

- Cada vídeo = 1 job na fila (tabela no Postgres): **resolução de fonte** → download → transcrição (chunking ≤20min) → chunking de texto + embedding.
- Onda 2: job adicional de segmentação por orador (GLiNER + heurísticas), só para as bases de debate.

## Volume e armazenamento

- ~50 vídeos/áudios ao todo nas 5 bases (contagem aproximada da lista enviada pelo cliente).
- Muitas fontes não são o link direto do vídeo — a resolução de fonte é uma etapa própria, com risco real de precisar intervenção manual em alguns casos.

## Riscos técnicos identificados na lista real de vídeos

- yt-dlp cobre YouTube direto e canal (com filtro de data) nativamente, e boa parte de páginas com embed conhecido (Globoplay, UOL) via seu extrator genérico.
- Amazon Music e Apple Podcasts provavelmente **não** são baixáveis via yt-dlp (feed fechado/DRM) — alternativa: localizar o feed RSS público do podcast, se existir, e baixar pelo enclosure do episódio. A resolver durante a codificação, não bloqueia o início.
- Páginas de blog (ex. blogspot) podem não ter extrator direto — pode exigir localizar manualmente a URL do vídeo embutido.
- Links de canal sem vídeo específico (ex. `@ronaldocaiado55`) dependem de filtro por data no yt-dlp — risco de ambiguidade se o canal postar mais de um vídeo no mesmo dia; nesses casos, marcar `resolution_status = nao_resolvido_manual` em vez de adivinhar.

---

Documento vivo também disponível como Claude Doc: https://claude.ai/code/artifact/75910468-cba1-43a5-995f-a35b093a1571

# Plano de Implementação — Campanha Debate RAG

> Depende de: todos os documentos anteriores.

**Data**: 2026-09-27

## Onda 1 — passos concretos

1. **Resolução de fontes**: para cada vídeo da lista do cliente, determinar o `resolved_media_url` — automático pra YouTube direto e canal+data; manual/heurística pra matérias e podcasts.
2. **Pipeline de download**: yt-dlp pras fontes resolvidas como YouTube; solução à parte pra podcast (RSS/enclosure) quando aplicável.
3. **Transcrição**: faster-whisper com chunking de áudio ≤20min, remontagem do texto com timestamps.
4. **Chunking de texto + embeddings**: gerar chunks e vetores (BGE-M3 self-hosted), indexar no pgvector.
5. **Servidor MCP**: expor as ferramentas de busca/consulta sobre o índice.
6. **Validação inicial**: rodar sobre 2-3 vídeos de cenários diferentes (um YouTube direto, um de canal, um de matéria) antes de processar a lista inteira, pra confirmar que a resolução de fonte funciona nos 3 cenários.

## Onda 2

7. Segmentação por orador nos debates (bases 1 e 2) via GLiNER + heurísticas estruturais.

## Critério de pronto (Onda 1)

- Todas as 5 bases com vídeos localizados (resolvidos ou marcados como pendente manual).
- Pelo menos 80% dos vídeos com transcrição completa indexada.
- MCP respondendo consultas de teste com trechos relevantes das 5 bases.

---

Documento vivo também disponível como Claude Doc: https://claude.ai/code/artifact/75910468-cba1-43a5-995f-a35b093a1571

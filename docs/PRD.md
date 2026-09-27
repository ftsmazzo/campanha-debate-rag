# PRD — Campanha Debate RAG

> Product Requirements Document — o quê e por quê, não como.
> Fonte: Entrevista com usuário

**Data**: 2026-09-27
**Responsável**: gestao@fabricadosdados.com.br

## 1. Resumo

Ferramenta interna para a equipe de estratégia da campanha (eleição presidencial 2026, candidato Lula) extrair, organizar e permitir consulta (via RAG) sobre o conteúdo integral de debates eleitorais e programas de TV/rádio de candidatos, para apoiar a preparação de Lula para debates e a definição de estratégia de perguntas e réplicas.

## 2. Problema e contexto

- Hoje alguém assiste aos vídeos manualmente, sem processo documentado ou padronizado.
- A demanda chegou com urgência máxima (prioridade 0): há um debate na Globo se aproximando e a equipe precisa rapidamente de um banco de perguntas e réplicas de Lula para os adversários (ex.: Flávio Bolsonaro, Caiado).
- Origem: solicitação de trabalho de campanha eleitoral.

## 3. Público-alvo

- Uso diário: equipe de estratégia da campanha (cerca de 3 pessoas).
- Uso de teste/validação inicial: o solicitante.

## 4. Bases de dados para análise

| # | Base | Período/turno | Itens identificados | Observação |
| --- | --- | --- | --- | --- |
| 1 | Debates presidenciais 2022 — Lula x Bolsonaro | 1º e 2º turno | 4 debates | — |
| 2 | Debates eleitorais Governo da Bahia 2022 | 1º e 2º turno | ~10 debates/entrevistas listados | Alguns "debates" viraram entrevistas por ausência de candidato |
| 3 | Programas eleitorais de Lula 2026 | — | 12 programas listados | — |
| 4 | Programas eleitorais de Flávio (Bolsonaro) 2026 | — | ~9 programas listados | — |
| 5 | Programas eleitorais de Caiado 2026 | — | 13 programas listados | — |

Lista completa de links por base: PDF "DADOS PARA ANÁLISE" fornecido pelo usuário (não versionado neste repositório — dado de trabalho, ver com o solicitante).

> Removido do escopo: "Debates presidenciais de 2018 entre Lula e Bolsonaro" — não existiu historicamente (Lula não foi candidato em 2018; Fernando Haddad disputou pelo PT, sem debate Haddad x Bolsonaro no 2º turno).

## 5. Objetivos e métricas de sucesso

- Tempo economizado frente ao processo manual atual.
- Volume de conteúdo processado na íntegra, sem erro humano.
- Capacidade de identificar padrões (ex.: estratégia de perguntas de outros candidatos) com qualidade suficiente para embasar decisão de campanha.

## 6. Escopo (MVP)

**MVP — Onda 1 (entrega imediata, resolve a urgência do próximo debate):**
- Localizar e confirmar links no YouTube (ou fonte equivalente) para as 5 bases de dados.
- Extrair a transcrição integral do áudio de cada vídeo (com chunking para vídeos acima de 20 minutos — ver TRD).
- Organizar o conteúdo extraído por base/vídeo, de forma apresentável.
- Disponibilizar esse conteúdo para consulta via RAG (busca sobre o conteúdo bruto) — já permite montar um primeiro banco de perguntas/réplicas, já que os programas eleitorais (bases 3 a 5) são discursos de um único candidato.

**MVP — Onda 2 (logo em seguida, mesma entrega, maior valor para debate prep):**
- Segmentar as transcrições dos debates (bases 1 e 2, as únicas com múltiplos candidatos) por orador/turno de fala, permitindo perguntas como "o que X perguntou a Y" e apoiando o estudo de estratégia de perguntas (ex.: campanhas do Sidônio na Bahia).

**Fora do escopo por enquanto (podem entrar depois):**
- Gerar conteúdo pronto para redes sociais.
- Fact-checking automático.
- Análise de sentimento/emoção do candidato.

## 7. Restrições de negócio

- Equipe pequena (~3 pessoas usando o resultado).
- Sem exigência formal de confidencialidade declarada, mas trata-se de material de campanha eleitoral.
- Prazo: urgência máxima / prioridade 0 (gatilho: próximo debate na Globo).

## 8. Riscos e premissas

- Decisão: base de debates 2018 removida — não existiu debate Lula x Bolsonaro em 2018 (Lula não foi candidato; Fernando Haddad disputou pelo PT, sem debate Haddad x Bolsonaro no 2º turno).
- Decisão: segmentação por orador dos debates entra no MVP como Onda 2 (ver Escopo), por ser o que mais agrega valor à demanda de debate prep.
- Fontes heterogêneas: debates (múltiplos candidatos, blocos/réplica) e programas eleitorais (peça única, sem interação) exigem tratamento de extração diferente.
- Uso de conteúdo de terceiros (emissoras de TV aberta) deve ficar restrito a análise interna da campanha, não redistribuição pública.
- Duração dos vídeos facilmente ultrapassa 60 minutos — implicação técnica detalhada no TRD.

---

Documento vivo também disponível como Claude Doc: https://claude.ai/code/artifact/75910468-cba1-43a5-995f-a35b093a1571

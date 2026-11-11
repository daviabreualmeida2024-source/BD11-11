# Cabeçalho:
## Alunos
    Davi Abreu de Almeida & Stefani Vitoria Teixeira Garutti
## Professor
    Neuton Melo

    Disciplina: Sistemas de Banco de Dados 2
# A12 — CampusFlow: relatório operacional

Análise da collection `campusflow_a12.solicitacoes` (12 solicitações) para testar, com dados, as quatro afirmações recebidas pela coordenação.

## Como executar

```bash
pip install pymongo
python seed.py        
python consultas.py   
python relatorio.py 
```

Requer MongoDB rodando em `mongodb://localhost:27017`.

## Organização do código

- `seed.py` — popula a collection e cria o índice `{situacao: 1, prioridade: -1}`.
- `consultas.py` — uma função por missão (`fila_critica`, `backlog_por_categoria`, `carga_por_setor`, `estudantes_recorrentes`). Os pipelines ficam em constantes para serem reutilizados.
- `relatorio.py` — importa as funções de `consultas.py`, imprime o relatório e **calcula** as três conclusões a partir dos resultados (nenhum número é escrito à mão).

---

## Missão 1 — A fila crítica

**Pergunta de negócio:** quais solicitações ainda em aberto (`ABERTA` ou `EM_ANALISE`) têm prioridade 4 ou 5?

```python
solicitacoes.find(
    {
        "situacao": {"$in": ["ABERTA", "EM_ANALISE"]},
        "prioridade": {"$gte": 4}
    },
    {
        "_id": 0, "protocolo": 1, "estudante.nome": 1,
        "categoria.nome": 1, "situacao": 1, "prioridade": 1
    }
).sort([("prioridade", -1), ("criadoEm", 1)])
```

**Resultado (4 documentos):**

| Protocolo | Estudante | Categoria | Situação | Prioridade |
|---|---|---|---|---|
| SOL-1011 | Isabela Torres | Trancamento de Disciplina | ABERTA | 5 |
| SOL-1006 | Eduarda Rocha | Trancamento de Disciplina | EM_ANALISE | 5 |
| SOL-1001 | Ana Ribeiro | Aproveitamento de Disciplina | EM_ANALISE | 5 |
| SOL-1009 | Gabriela Moraes | Aproveitamento de Disciplina | EM_ANALISE | 4 |

Observação: SOL-1005 tem prioridade 4, mas está `AGUARDANDO_DOCUMENTACAO` e, por isso, fica fora do filtro pedido. Entre as de prioridade 5, a ordem por `criadoEm` crescente coloca a mais antiga (SOL-1011, de 29/10) no topo.

Sobre a afirmação *"só temos algumas solicitações de prioridade alta"*: 4 de 12 solicitações (33%) estão abertas/em análise com prioridade ≥ 4 — não é um número desprezível.

---

## Missão 2 — Onde está o backlog?

**Pergunta de negócio:** entre as solicitações não concluídas, quantas há em cada categoria?

```python
[
    {"$match": {"situacao": {"$ne": "CONCLUIDA"}}},
    {"$group": {"_id": "$categoria.nome", "quantidade": {"$sum": 1}}},
    {"$sort": {"quantidade": -1, "_id": 1}}
]
```

`$ne: "CONCLUIDA"` foi usado (em vez de listar as situações) para que `AGUARDANDO_DOCUMENTACAO` — que também é backlog — seja contada. O `_id: 1` no `$sort` apenas desempata categorias com a mesma quantidade.

**Resultado:**

```json
{ "_id": "Aproveitamento de Disciplina", "quantidade": 3 }
{ "_id": "Emissão de Declaração",        "quantidade": 2 }
{ "_id": "Trancamento de Disciplina",    "quantidade": 2 }
{ "_id": "Segunda Via de Boleto",        "quantidade": 1 }
```

**Qual categoria possui o maior backlog?**
**Aproveitamento de Disciplina**, com 3 das 8 solicitações não concluídas (38%). Ela lidera, mas não "acumula tudo": as outras 5 pendências estão distribuídas em três categorias.

---

## Missão 3 — Quem realmente recebe mais trabalho?

**Pergunta de negócio:** considerando cada atendimento (e não cada solicitação), qual a carga de cada setor?

```python
[
    {"$unwind": "$atendimentos"},
    {"$group": {
        "_id": "$atendimentos.setor",
        "interacoes":   {"$sum": 1},
        "tempoMedio":   {"$avg": "$atendimentos.duracaoMin"},
        "maiorDuracao": {"$max": "$atendimentos.duracaoMin"}
    }},
    {"$sort": {"interacoes": -1, "_id": 1}}
]
```

**Resultado:**

```json
{ "_id": "SECRETARIA",  "interacoes": 10, "tempoMedio": 9.7,   "maiorDuracao": 14 }
{ "_id": "COORDENACAO", "interacoes": 5,  "tempoMedio": 47.0,  "maiorDuracao": 55 }
{ "_id": "FINANCEIRO",  "interacoes": 3,  "tempoMedio": 7.33,  "maiorDuracao": 9 }
```

**A afirmação "o problema é a Secretaria" é sustentada pelos dados?**
**Não.** A Secretaria tem o maior volume (10 de 18 interações), mas são atendimentos rápidos: tempo médio de 9,7 min e maior duração de 14 min. A Coordenação tem metade das interações, porém **tempo médio 4,8 vezes maior (47,0 min)** e a **maior duração observada (55 min)**. Somando as durações, a Coordenação ocupa 235 min contra 97 min da Secretaria. Além disso, todas as interações da Coordenação são do tipo `ANALISE` em categorias que estão no backlog (Aproveitamento e Trancamento). O gargalo provável é a Coordenação; a Secretaria aparece mais porque faz a triagem de quase tudo.

---

## Missão 4 — Há estudantes recorrentes?

**Pergunta de negócio:** quais estudantes abriram mais de uma solicitação, e quais foram?

```python
[
    {"$group": {
        "_id": "$estudante.id",
        "nome": {"$first": "$estudante.nome"},
        "quantidade": {"$sum": 1},
        "protocolos": {"$push": "$protocolo"}
    }},
    {"$match": {"quantidade": {"$gt": 1}}},
    {"$sort": {"quantidade": -1, "_id": 1}}
]
```

O agrupamento é por `estudante.id` (e não pelo nome), pois o id é o identificador estável; o nome vem com `$first`.

**Resultado:**

```json
{ "_id": 101, "nome": "Ana Ribeiro", "quantidade": 3, "protocolos": ["SOL-1001", "SOL-1004", "SOL-1012"] }
{ "_id": 102, "nome": "Bruno Lima",  "quantidade": 2, "protocolos": ["SOL-1002", "SOL-1008"] }
```

**Existem indícios de concentração de solicitações em poucos estudantes?**
Há recorrência, mas limitada. 2 de 9 estudantes (22%) respondem por 5 de 12 solicitações (42%); os outros 7 abriram uma cada. Olhando os protocolos, as solicitações de Ana e Bruno são de categorias diferentes entre si, e 2 das 5 já estão concluídas (SOL-1008 e SOL-1012). Os dados não sustentam que *"poucos alunos abrindo várias solicitações"* seja a causa do aumento de volume.

---

## Missão 5 — Relatório (`python relatorio.py`)

```
========================================
CAMPUSFLOW — RELATÓRIO OPERACIONAL
========================================

BACKLOG POR CATEGORIA
Aproveitamento de Disciplina: 3
Emissão de Declaração: 2
Trancamento de Disciplina: 2
Segunda Via de Boleto: 1

CARGA POR SETOR
SECRETARIA
  Interações: 10
  Tempo médio: 9.7 min
  Maior duração: 14 min

COORDENACAO
  Interações: 5
  Tempo médio: 47.0 min
  Maior duração: 55 min

FINANCEIRO
  Interações: 3
  Tempo médio: 7.3 min
  Maior duração: 9 min

ESTUDANTES RECORRENTES
Ana Ribeiro: 3 (SOL-1001, SOL-1004, SOL-1012)
Bruno Lima: 2 (SOL-1002, SOL-1008)

CASOS CRÍTICOS
SOL-1011 | P5 | ABERTA | Trancamento de Disciplina | Isabela Torres
SOL-1006 | P5 | EM_ANALISE | Trancamento de Disciplina | Eduarda Rocha
SOL-1001 | P5 | EM_ANALISE | Aproveitamento de Disciplina | Ana Ribeiro
SOL-1009 | P4 | EM_ANALISE | Aproveitamento de Disciplina | Gabriela Moraes
========================================
```

### Três conclusões técnicas

1. **A categoria Aproveitamento de Disciplina concentra o maior backlog:** 3 de 8 solicitações não concluídas (38%). *(Missão 2)*
2. **O setor SECRETARIA tem mais interações (10 de 18), mas o setor COORDENACAO tem o maior tempo médio** (47,0 min contra 9,7 min) e a maior duração observada (55 min). *(Missão 3)*
3. **Os estudantes Ana Ribeiro e Bruno Lima (2 de 9) respondem por 5 de 12 solicitações (42%);** há recorrência, mas restrita a dois alunos — os demais abriram uma solicitação cada. *(Missão 4)*

---

## Requisito adicional — índice `{situacao: 1, prioridade: -1}`

A **Missão 1** é a que mais se beneficia: ela filtra por igualdade em `situacao` (`$in`) e por intervalo em `prioridade` (`$gte: 4`), exatamente o prefixo do índice nessa ordem.
Assim o MongoDB percorre só as entradas de `ABERTA`/`EM_ANALISE` com prioridade ≥ 4, sem varrer a collection, e já as obtém ordenadas por `prioridade` decrescente.
O desempate por `criadoEm` ainda é feito em memória, pois esse campo não faz parte do índice.

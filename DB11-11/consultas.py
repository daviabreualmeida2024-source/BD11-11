from pprint import pprint

from pymongo import MongoClient


client = MongoClient(
    "mongodb://localhost:27017"
)

db = client["campusflow_a12"]

solicitacoes = db["solicitacoes"]


def fila_critica():
    filtro = {
        "situacao": {"$in": ["ABERTA", "EM_ANALISE"]},
        "prioridade": {"$gte": 4}
    }

    projecao = {
        "_id": 0,
        "protocolo": 1,
        "estudante.nome": 1,
        "categoria.nome": 1,
        "situacao": 1,
        "prioridade": 1
    }

    ordenacao = [
        ("prioridade", -1),
        ("criadoEm", 1)
    ]

    return list(
        solicitacoes.find(filtro, projecao).sort(ordenacao)
    )


PIPELINE_BACKLOG = [
    {
        "$match": {
            "situacao": {"$ne": "CONCLUIDA"}
        }
    },
    {
        "$group": {
            "_id": "$categoria.nome",
            "quantidade": {"$sum": 1}
        }
    },
    {
        
        "$sort": {
            "quantidade": -1,
            "_id": 1
        }
    }
]


def backlog_por_categoria():
    return list(solicitacoes.aggregate(PIPELINE_BACKLOG))



PIPELINE_SETORES = [
    {
        "$unwind": "$atendimentos"
    },
    {
        "$group": {
            "_id": "$atendimentos.setor",
            "interacoes": {"$sum": 1},
            "tempoMedio": {"$avg": "$atendimentos.duracaoMin"},
            "maiorDuracao": {"$max": "$atendimentos.duracaoMin"}
        }
    },
    {
        "$sort": {
            "interacoes": -1,
            "_id": 1
        }
    }
]


def carga_por_setor():
    return list(solicitacoes.aggregate(PIPELINE_SETORES))



PIPELINE_RECORRENTES = [
    {
        "$group": {
            "_id": "$estudante.id",
            "nome": {"$first": "$estudante.nome"},
            "quantidade": {"$sum": 1},
            "protocolos": {"$push": "$protocolo"}
        }
    },
    {
        "$match": {
            "quantidade": {"$gt": 1}
        }
    },
    {
        "$sort": {
            "quantidade": -1,
            "_id": 1
        }
    }
]


def estudantes_recorrentes():
    return list(solicitacoes.aggregate(PIPELINE_RECORRENTES))


if __name__ == "__main__":
    print("\n=== MISSÃO 1 — FILA CRÍTICA ===")
    for doc in fila_critica():
        pprint(doc, sort_dicts=False)

    print("\n=== MISSÃO 2 — BACKLOG POR CATEGORIA ===")
    for doc in backlog_por_categoria():
        pprint(doc, sort_dicts=False)

    print("\n=== MISSÃO 3 — CARGA POR SETOR ===")
    for doc in carga_por_setor():
        pprint(doc, sort_dicts=False)

    print("\n=== MISSÃO 4 — ESTUDANTES RECORRENTES ===")
    for doc in estudantes_recorrentes():
        pprint(doc, sort_dicts=False)

from datetime import datetime

from pymongo import MongoClient


client = MongoClient(
    "mongodb://localhost:27017"
)

db = client["campusflow_a12"]

solicitacoes = db["solicitacoes"]

solicitacoes.delete_many({})


dados = [
    {
        "protocolo": "SOL-1001",
        "estudante": {
            "id": 101,
            "nome": "Ana Ribeiro",
            "curso": "Engenharia de Software"
        },
        "categoria": {
            "codigo": "APROV",
            "nome": "Aproveitamento de Disciplina"
        },
        "situacao": "EM_ANALISE",
        "prioridade": 5,
        "criadoEm": datetime(2026, 11, 2, 8, 30),
        "tags": [
            "DOCUMENTACAO",
            "URGENTE"
        ],
        "atendimentos": [
            {
                "setor": "SECRETARIA",
                "tipo": "TRIAGEM",
                "duracaoMin": 12
            },
            {
                "setor": "COORDENACAO",
                "tipo": "ANALISE",
                "duracaoMin": 48
            }
        ]
    },

    {
        "protocolo": "SOL-1002",
        "estudante": {
            "id": 102,
            "nome": "Bruno Lima",
            "curso": "Engenharia de Software"
        },
        "categoria": {
            "codigo": "DECL",
            "nome": "Emissão de Declaração"
        },
        "situacao": "ABERTA",
        "prioridade": 2,
        "criadoEm": datetime(2026, 11, 8, 10, 15),
        "tags": [
            "DECLARACAO"
        ],
        "atendimentos": [
            {
                "setor": "SECRETARIA",
                "tipo": "TRIAGEM",
                "duracaoMin": 6
            }
        ]
    },

    {
        "protocolo": "SOL-1003",
        "estudante": {
            "id": 103,
            "nome": "Carla Nunes",
            "curso": "Sistemas de Informação"
        },
        "categoria": {
            "codigo": "BOL",
            "nome": "Segunda Via de Boleto"
        },
        "situacao": "CONCLUIDA",
        "prioridade": 1,
        "criadoEm": datetime(2026, 11, 3, 14, 0),
        "tags": [
            "FINANCEIRO"
        ],
        "atendimentos": [
            {
                "setor": "FINANCEIRO",
                "tipo": "ANALISE",
                "duracaoMin": 9
            }
        ]
    },

    {
        "protocolo": "SOL-1004",
        "estudante": {
            "id": 101,
            "nome": "Ana Ribeiro",
            "curso": "Engenharia de Software"
        },
        "categoria": {
            "codigo": "DECL",
            "nome": "Emissão de Declaração"
        },
        "situacao": "ABERTA",
        "prioridade": 3,
        "criadoEm": datetime(2026, 11, 7, 9, 0),
        "tags": [
            "DECLARACAO",
            "URGENTE"
        ],
        "atendimentos": [
            {
                "setor": "SECRETARIA",
                "tipo": "TRIAGEM",
                "duracaoMin": 8
            }
        ]
    },

    {
        "protocolo": "SOL-1005",
        "estudante": {
            "id": 104,
            "nome": "Diego Alves",
            "curso": "Engenharia de Software"
        },
        "categoria": {
            "codigo": "APROV",
            "nome": "Aproveitamento de Disciplina"
        },
        "situacao": "AGUARDANDO_DOCUMENTACAO",
        "prioridade": 4,
        "criadoEm": datetime(2026, 10, 28, 16, 40),
        "tags": [
            "DOCUMENTACAO"
        ],
        "atendimentos": [
            {
                "setor": "SECRETARIA",
                "tipo": "TRIAGEM",
                "duracaoMin": 11
            },
            {
                "setor": "COORDENACAO",
                "tipo": "ANALISE",
                "duracaoMin": 42
            },
            {
                "setor": "SECRETARIA",
                "tipo": "PENDENCIA",
                "duracaoMin": 7
            }
        ]
    },

    {
        "protocolo": "SOL-1006",
        "estudante": {
            "id": 105,
            "nome": "Eduarda Rocha",
            "curso": "Sistemas de Informação"
        },
        "categoria": {
            "codigo": "TRANC",
            "nome": "Trancamento de Disciplina"
        },
        "situacao": "EM_ANALISE",
        "prioridade": 5,
        "criadoEm": datetime(2026, 11, 1, 11, 20),
        "tags": [
            "COORDENACAO",
            "URGENTE"
        ],
        "atendimentos": [
            {
                "setor": "SECRETARIA",
                "tipo": "TRIAGEM",
                "duracaoMin": 10
            },
            {
                "setor": "COORDENACAO",
                "tipo": "ANALISE",
                "duracaoMin": 55
            }
        ]
    },

    {
        "protocolo": "SOL-1007",
        "estudante": {
            "id": 106,
            "nome": "Felipe Souza",
            "curso": "Engenharia de Software"
        },
        "categoria": {
            "codigo": "BOL",
            "nome": "Segunda Via de Boleto"
        },
        "situacao": "ABERTA",
        "prioridade": 2,
        "criadoEm": datetime(2026, 11, 9, 13, 0),
        "tags": [
            "FINANCEIRO"
        ],
        "atendimentos": [
            {
                "setor": "FINANCEIRO",
                "tipo": "TRIAGEM",
                "duracaoMin": 5
            }
        ]
    },

    {
        "protocolo": "SOL-1008",
        "estudante": {
            "id": 102,
            "nome": "Bruno Lima",
            "curso": "Engenharia de Software"
        },
        "categoria": {
            "codigo": "APROV",
            "nome": "Aproveitamento de Disciplina"
        },
        "situacao": "CONCLUIDA",
        "prioridade": 3,
        "criadoEm": datetime(2026, 10, 20, 8, 0),
        "tags": [
            "DOCUMENTACAO"
        ],
        "atendimentos": [
            {
                "setor": "SECRETARIA",
                "tipo": "TRIAGEM",
                "duracaoMin": 9
            },
            {
                "setor": "COORDENACAO",
                "tipo": "ANALISE",
                "duracaoMin": 39
            }
        ]
    },

    {
        "protocolo": "SOL-1009",
        "estudante": {
            "id": 107,
            "nome": "Gabriela Moraes",
            "curso": "Sistemas de Informação"
        },
        "categoria": {
            "codigo": "APROV",
            "nome": "Aproveitamento de Disciplina"
        },
        "situacao": "EM_ANALISE",
        "prioridade": 4,
        "criadoEm": datetime(2026, 10, 30, 15, 20),
        "tags": [
            "DOCUMENTACAO",
            "COORDENACAO"
        ],
        "atendimentos": [
            {
                "setor": "SECRETARIA",
                "tipo": "TRIAGEM",
                "duracaoMin": 14
            },
            {
                "setor": "COORDENACAO",
                "tipo": "ANALISE",
                "duracaoMin": 51
            }
        ]
    },

    {
        "protocolo": "SOL-1010",
        "estudante": {
            "id": 108,
            "nome": "Henrique Dias",
            "curso": "Engenharia de Software"
        },
        "categoria": {
            "codigo": "ALT",
            "nome": "Alteração Cadastral"
        },
        "situacao": "CONCLUIDA",
        "prioridade": 1,
        "criadoEm": datetime(2026, 11, 5, 10, 30),
        "tags": [
            "CADASTRO"
        ],
        "atendimentos": [
            {
                "setor": "SECRETARIA",
                "tipo": "ANALISE",
                "duracaoMin": 7
            }
        ]
    },

    {
        "protocolo": "SOL-1011",
        "estudante": {
            "id": 109,
            "nome": "Isabela Torres",
            "curso": "Engenharia de Software"
        },
        "categoria": {
            "codigo": "TRANC",
            "nome": "Trancamento de Disciplina"
        },
        "situacao": "ABERTA",
        "prioridade": 5,
        "criadoEm": datetime(2026, 10, 29, 17, 0),
        "tags": [
            "COORDENACAO",
            "URGENTE"
        ],
        "atendimentos": [
            {
                "setor": "SECRETARIA",
                "tipo": "TRIAGEM",
                "duracaoMin": 13
            }
        ]
    },

    {
        "protocolo": "SOL-1012",
        "estudante": {
            "id": 101,
            "nome": "Ana Ribeiro",
            "curso": "Engenharia de Software"
        },
        "categoria": {
            "codigo": "BOL",
            "nome": "Segunda Via de Boleto"
        },
        "situacao": "CONCLUIDA",
        "prioridade": 1,
        "criadoEm": datetime(2026, 10, 18, 9, 30),
        "tags": [
            "FINANCEIRO"
        ],
        "atendimentos": [
            {
                "setor": "FINANCEIRO",
                "tipo": "ANALISE",
                "duracaoMin": 8
            }
        ]
    }
]


resultado = solicitacoes.insert_many(
    dados
)

print(
    f"{len(resultado.inserted_ids)} "
    "documentos inseridos."
)


solicitacoes.create_index([
    ("situacao", 1),
    ("prioridade", -1)
])

print("Índice (situacao, prioridade) criado.")

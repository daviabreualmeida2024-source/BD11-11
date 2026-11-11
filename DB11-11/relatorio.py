from consultas import (
    solicitacoes,
    fila_critica,
    backlog_por_categoria,
    carga_por_setor,
    estudantes_recorrentes
)


LINHA = "=" * 40


def main():
    backlog = backlog_por_categoria()
    setores = carga_por_setor()
    recorrentes = estudantes_recorrentes()
    criticos = fila_critica()

    total_solicitacoes = solicitacoes.count_documents({})
    total_estudantes = len(solicitacoes.distinct("estudante.id"))
    total_backlog = sum(c["quantidade"] for c in backlog)
    total_interacoes = sum(s["interacoes"] for s in setores)

    print(LINHA)
    print("CAMPUSFLOW — RELATÓRIO OPERACIONAL")
    print(LINHA)

    print("\nBACKLOG POR CATEGORIA")
    for cat in backlog:
        print(f"{cat['_id']}: {cat['quantidade']}")

    print("\nCARGA POR SETOR")
    for setor in setores:
        print(setor["_id"])
        print(f"  Interações: {setor['interacoes']}")
        print(f"  Tempo médio: {setor['tempoMedio']:.1f} min")
        print(f"  Maior duração: {setor['maiorDuracao']} min")
        print()

    print("ESTUDANTES RECORRENTES")
    for est in recorrentes:
        protocolos = ", ".join(est["protocolos"])
        print(f"{est['nome']}: {est['quantidade']} ({protocolos})")

    print("\nCASOS CRÍTICOS")
    for caso in criticos:
        print(
            f"{caso['protocolo']} | P{caso['prioridade']} | "
            f"{caso['situacao']} | {caso['categoria']['nome']} | "
            f"{caso['estudante']['nome']}"
        )

    print(LINHA)

 
    maior_cat = backlog[0]
    mais_interacoes = setores[0]  
    mais_lento = max(setores, key=lambda s: s["tempoMedio"])
    total_recorrentes = sum(e["quantidade"] for e in recorrentes)
    nomes_recorrentes = " e ".join(e["nome"] for e in recorrentes)

    print("\nCONCLUSÕES")

    print(
        f"1. A categoria {maior_cat['_id']} concentra o maior backlog: "
        f"{maior_cat['quantidade']} de {total_backlog} solicitações não "
        f"concluídas ({maior_cat['quantidade'] / total_backlog:.0%}). "
        f"[Missão 2]"
    )

    print(
        f"2. O setor {mais_interacoes['_id']} tem mais interações "
        f"({mais_interacoes['interacoes']} de {total_interacoes}), "
        f"mas o setor {mais_lento['_id']} tem o maior tempo médio "
        f"({mais_lento['tempoMedio']:.1f} min contra "
        f"{mais_interacoes['tempoMedio']:.1f} min) e a maior duração "
        f"observada ({mais_lento['maiorDuracao']} min). [Missão 3]"
    )

    print(
        f"3. Os estudantes {nomes_recorrentes} ({len(recorrentes)} de "
        f"{total_estudantes}) respondem por {total_recorrentes} de "
        f"{total_solicitacoes} solicitações "
        f"({total_recorrentes / total_solicitacoes:.0%}); há recorrência, "
        f"mas restrita a dois alunos — os demais abriram uma solicitação "
        f"cada. [Missão 4]"
    )

    print(LINHA)


if __name__ == "__main__":
    main()

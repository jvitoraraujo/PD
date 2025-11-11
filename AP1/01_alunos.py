with open("./dados_alunos.txt", "r", encoding="utf-8") as file:
    notas = []
    maior_nota = None
    menor_nota = None
    aluno_maior = ""
    aluno_menor = ""

    for linha in file:
        linha = linha.strip()
        if not linha:
            continue

        partes = linha.split('#')
        if len(partes) >= 2:
            nome = partes[0].strip()
            try:
                nota = float(partes[1].strip())
            except ValueError:
                continue
            notas.append(nota)

            if maior_nota is None or nota > maior_nota:
                maior_nota = nota
                aluno_maior = nome

            if menor_nota is None or nota < menor_nota:
                menor_nota = nota
                aluno_menor = nome


    if notas:
        media = sum(notas) / len(notas)
        print()
        print(f"Média da turma: {media:.2f}")
        print(f"Maior nota: {maior_nota:.2f} (Aluno: {aluno_maior})")
        print(f"Menor nota: {menor_nota:.2f} (Aluno: {aluno_menor})")




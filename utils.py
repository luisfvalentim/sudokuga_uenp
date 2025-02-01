import csv

def formatar_grade(grade):
    resultado = []
    for i, linha in enumerate(grade):
        if i % 3 == 0 and i != 0:
            resultado.append("------+-------+------")
        linha_str = " | ".join(" ".join(map(str, linha[j:j+3])) for j in range(0, 9, 3))
        resultado.append(f" {linha_str} ")
    return "\n".join(resultado)

def ler_csv(nome_arquivo):
    quebracabecas = []
    with open(nome_arquivo, 'r') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            puzzle = linha.get('puzzle', '').strip()
            solucao = linha.get('solution', '').strip()
            if puzzle and solucao and len(puzzle) >= 81 and len(solucao) >= 81:
                quebracabecas.append((
                    puzzle[:81].ljust(81, '0'),
                    solucao[:81].ljust(81, '0')
                ))
    return quebracabecas

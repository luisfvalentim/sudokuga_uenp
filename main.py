from sudoku_ga import SudokuGA
from utils import ler_csv, formatar_grade

def main():
    dados = ler_csv('data/sudoku.csv')
    
    max_jogos = 6  
    resultados = []  

    for idx, (puzzle, solucao_real) in enumerate(dados):
        if idx + 1 > max_jogos:
            break
        print(f"\n{'='*50}")
        print(f" Resolvendo Quebra-Cabeça {idx + 1} ".center(50, '='))
        print(f"{'='*50}\n")
        
        solver = SudokuGA(puzzle, solucao_real)
        print("Quebra-Cabeça Original:")
        print(formatar_grade(solver.puzzle))
        print("\n" + "-"*50 + "\n")
        
        melhor_global = None
        melhor_semelhanca = 0
        melhor_aptidao = None

        tentativa = 1

        while True:
            print(f"Tentativa {tentativa}".center(50, '-'))
            melhor_ind, aptidao = solver.executar(
                tamanho_populacao=400,
                geracoes=250,
                taxa_mutacao=0.15
            )
            semelhanca = solver.calcular_semelhanca(melhor_ind)
    
            print(f"\nSemelhança Atual: {semelhanca:.2f}%")
            print(f"Melhor Aptidão: {aptidao}")

            if semelhanca > melhor_semelhanca:
                melhor_semelhanca = semelhanca
                melhor_global = melhor_ind
                melhor_aptidao = aptidao

            if semelhanca >= 100 or tentativa >= 100:
                break
            
            tentativa += 1

        print("\nSolução Proposta:")
        print(formatar_grade(solver.obter_grade(melhor_global)))

        print("\nSolução Real:")
        print(formatar_grade(solver.solucao_real))

        print(f"\nSemelhança Final: {melhor_semelhanca:.2f}%")
        print(f"Melhor Aptidão Final: {melhor_aptidao}")
        print(f"Total de Tentativas: {tentativa}")
        print("\n" + "="*50 + "\n")

        resultados.append({
            "id": idx + 1,
            "melhor_grade": solver.obter_grade(melhor_global),
            "solucao_real": solver.solucao_real,
            "semelhanca_final": melhor_semelhanca,
            "melhor_aptidao": melhor_aptidao,
            "tentativas": tentativa
        })
    
    print("\nResumo Final de Todos os Quebra-Cabeças:")
    for res in resultados:
        print(f"\n{'='*50}")
        print(f" Quebra-Cabeça {res['id']} ".center(50, '='))
        print(f"{'='*50}\n")
        print("Solução Proposta:")
        print(formatar_grade(res["melhor_grade"]))
        print("\nSolução Real:")
        print(formatar_grade(res["solucao_real"]))
        print(f"\nSemelhança Final: {res['semelhanca_final']:.2f}%")
        print(f"Melhor Aptidão Final: {res['melhor_aptidao']}")
        print(f"Total de Tentativas: {res['tentativas']}")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()

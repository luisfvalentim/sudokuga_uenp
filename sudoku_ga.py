import random
import numpy as np

class SudokuGA:
    def __init__(self, str_puzzle, str_solucao=None):
        self.puzzle = self.interpretar_puzzle(str_puzzle)
        self.solucao_real = self.interpretar_puzzle(str_solucao) if str_solucao else None
        self.posicoes_variaveis = self.obter_posicoes_variaveis()
        self.posicoes_fixas = {(i, j): self.puzzle[i][j] 
                              for i in range(9) for j in range(9) 
                              if self.puzzle[i][j] != 0}
        
    def interpretar_puzzle(self, str_puzzle):
        return [[int(str_puzzle[i * 9 + j]) for j in range(9)] for i in range(9)]
    
    def obter_posicoes_variaveis(self):
        return [(i, j) for i in range(9) for j in range(9) if self.puzzle[i][j] == 0]
    
    def criar_individuo(self):
        return [random.randint(1, 9) for _ in self.posicoes_variaveis]
    
    def inicializar_populacao(self, tamanho_populacao):
        return [self.criar_individuo() for _ in range(tamanho_populacao)]
    
    def obter_grade(self, individuo):
        grade = [linha.copy() for linha in self.puzzle]
        for idx, (i, j) in enumerate(self.posicoes_variaveis):
            grade[i][j] = individuo[idx]
        return grade
    
    def calcular_aptidao(self, individuo):
        grade = self.obter_grade(individuo)
        aptidao = 0
    
        for linha in grade:
            aptidao += len(set(linha))
            aptidao -= (9 - len(set(linha))) * 2
    
        for j in range(9):
            coluna = [grade[i][j] for i in range(9)]
            aptidao += len(set(coluna))
            aptidao -= (9 - len(set(coluna))) * 2
    
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subgrade = [grade[x][y] for x in range(i, i+3) for y in range(j, j+3)]
                aptidao += len(set(subgrade))
                aptidao -= (9 - len(set(subgrade))) * 2
    
        if self.solucao_real:
            aptidao += sum(1 for (i, j) in self.posicoes_variaveis 
                           if grade[i][j] == self.solucao_real[i][j])
    
        return aptidao

    def selecionar_pais(self, populacao, aptidoes, tamanho_torneio):
        selecionados = []
        for _ in range(2):
            competidores = random.sample(list(zip(populacao, aptidoes)), tamanho_torneio)
            selecionados.append(max(competidores, key=lambda x: x[1])[0])
        return selecionados
    
    def cruzar(self, pai_a, pai_b):
        return [pai_a[idx] if idx % 2 == 0 else pai_b[idx] for idx in range(len(pai_a))]
    
    def mutar(self, individuo, taxa_mutacao, geracao_atual, geracoes_totais):
        taxa_mutacao_adaptativa = taxa_mutacao * (1 - (geracao_atual / geracoes_totais))
        return [gene if random.random() > taxa_mutacao_adaptativa else random.randint(1, 9) 
                for gene in individuo]
    
    def executar(self, tamanho_populacao=500, geracoes=200, 
                tamanho_torneio=3, taxa_cruzamento=0.8, 
                taxa_mutacao=0.1, numero_elitismo=2):
        populacao = self.inicializar_populacao(tamanho_populacao)
        melhor_aptidao = 0
        melhor_individuo = None
        
        for geracao in range(geracoes):
            aptidoes = [self.calcular_aptidao(ind) for ind in populacao]
            aptidao_atual = max(aptidoes)
            
            if aptidao_atual > melhor_aptidao:
                melhor_aptidao = aptidao_atual
                melhor_individuo = populacao[aptidoes.index(aptidao_atual)]
                if aptidao_atual == 243:
                    break
            
            indices_elite = np.argsort(aptidoes)[-numero_elitismo:]
            nova_populacao = [populacao[i] for i in indices_elite]
            
            while len(nova_populacao) < tamanho_populacao:
                pais = self.selecionar_pais(populacao, aptidoes, tamanho_torneio)
                if random.random() < taxa_cruzamento:
                    filho = self.cruzar(pais[0], pais[1])
                else:
                    filho = pais[0].copy()
                filho = self.mutar(filho, taxa_mutacao, geracao_atual=geracao, geracoes_totais=geracoes)
                nova_populacao.append(filho)
            
            populacao = nova_populacao[:tamanho_populacao]
        
        return melhor_individuo, melhor_aptidao

    def calcular_semelhanca(self, solucao_proposta):
        if not self.solucao_real:
            return 0.0
        
        corretos = sum(1 for (i, j) in self.posicoes_variaveis 
                       if self.obter_grade(solucao_proposta)[i][j] == self.solucao_real[i][j])
                
        return (corretos / len(self.posicoes_variaveis)) * 100 if self.posicoes_variaveis else 0.0

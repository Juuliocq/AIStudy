import random
from collections import deque

from problema_mochila.otimizador.CromossomoOtimizador import CromossomoOtimizador
from problema_mochila.problema.Algoritmo import Algoritmo


class AlgoritmoOtimizador:

    def __init__(self, limite_massa, populacao_maxima,
                 convergencia_maxima,
                 massa_item1, valor_item1, qtd_item1,
                 massa_item2, valor_item2, qtd_item2,
                 massa_item3, valor_item3, qtd_item3):

        self.TAXA_MUTACAO = 0.1
        self.QUANTIDADE_POPULACAO = 4
        self.FITNESS_TOTAL = 50
        self.PERCENTUAL_MELHORES = 0.5

        self.CONVERGENCIA_MAXIMA = int(convergencia_maxima)
        self.POPULACAO_MAXIMA = int(populacao_maxima)
        self.LIMITE_MASSA = int(limite_massa)

        self.massa_item1 = float(massa_item1)
        self.valor_item1 = float(valor_item1)
        self.qtd_item1 = int(qtd_item1)

        self.massa_item2 = float(massa_item2)
        self.valor_item2 = float(valor_item2)
        self.qtd_item2 = int(qtd_item2)

        self.massa_item3 = float(massa_item3)
        self.valor_item3 = float(valor_item3)
        self.qtd_item3 = int(qtd_item3)

    def getPopulacao(self):
        populacao = []
        individuos_adicionados = 0

        while individuos_adicionados < self.QUANTIDADE_POPULACAO:

            cromossomo = CromossomoOtimizador(self.LIMITE_MASSA, self.POPULACAO_MAXIMA,
                                              self.CONVERGENCIA_MAXIMA, self.PERCENTUAL_MELHORES,
                self.massa_item1, self.valor_item1, self.qtd_item1,
                self.massa_item2, self.valor_item2, self.qtd_item2,
                self.massa_item3, self.valor_item3, self.qtd_item3)

            populacao.append(cromossomo)
            individuos_adicionados += 1

        return populacao

    def get_melhor(self, populacao):
        melhor: CromossomoOtimizador = None

        for individuo in populacao:
            if melhor is None:
                melhor = individuo
            else:
                if individuo.f_objetivo() > melhor.f_objetivo():
                    melhor = individuo

        return melhor

    def cross_over(self, populacao):
        #Define qual o % de melhores/piores
        percentual_por_individuo = 1 / len(populacao)
        percentual_acumulado = 0

        qtd_melhores = 0
        qtd_piores = 0

        #Conta a quantidade de melhores e piores.
        for i in range(0, len(populacao)):
            if percentual_acumulado <= self.PERCENTUAL_MELHORES:
                qtd_melhores += 1
            else:
                qtd_piores += 1

            percentual_acumulado += percentual_por_individuo

        melhores = []
        piores = []

        #Ordena em ordem reversa por valor total (função objetivo.)
        populacao_ordenada = sorted(populacao, key=lambda individuo: individuo.f_objetivo())
        populacao_ordenada.reverse()

        #Adiciona na lista de melhores ou piores.
        for individuo in populacao_ordenada:
            if len(melhores) < qtd_melhores:
                melhores.append(individuo)
            else:
                piores.append(individuo)

        total_melhores = sum(individuo.f_objetivo() for individuo in melhores)
        total_piores = sum(individuo.f_objetivo() for individuo in piores)

        probabilidade_acumulada = 0

        #Calcula as probabilidades acumuladas dos melhores e piores.
        for individuo in melhores:
            probabilidade = (individuo.f_objetivo() / total_melhores)
            probabilidade_acumulada = probabilidade + probabilidade_acumulada
            individuo.set_probabilidade_acumulada(probabilidade_acumulada)

        probabilidade_acumulada = 0

        for individuo in piores:
            probabilidade = (individuo.f_objetivo() / total_piores)
            probabilidade_acumulada = probabilidade + probabilidade_acumulada
            individuo.set_probabilidade_acumulada(probabilidade_acumulada)

        rnd = random.random()
        pai_melhor = None
        pai_pior = None

        #Decide qual será o pai melhor escolhido para sofrer crossover.
        for i, individuo in enumerate(melhores):
            if i == len(melhores) - 1:
                pai_melhor = individuo
                break
            elif melhores[i + 1].get_probabilidade_acumulada() > rnd > individuo.get_probabilidade_acumulada(): #número randomico entre individuo[i] e individuo[i+1]
                pai_melhor = individuo
                break

        rnd = random.random()

        #Decide qual será o pai pior escolhido para sofrer crossover.
        for i, individuo in enumerate(piores):
            if i == len(piores) - 1:
                pai_pior = individuo
                break

            if piores[i + 1].get_probabilidade_acumulada() > rnd > individuo.get_probabilidade_acumulada(): #número randomico entre individuo[i] e individuo[i+1]
                pai_pior = individuo
                break

        rnd = random.random()

        #Decide qual gene sofrerá crossover
        if rnd < 0.3333:
            pai_melhor.taxa_mutacao, pai_pior.taxa_mutacao = pai_pior.taxa_mutacao, pai_melhor.taxa_mutacao

        elif rnd < 0.6666:
            pai_melhor.qtd_populacao, pai_pior.qtd_populacao = pai_pior.qtd_populacao, pai_melhor.qtd_populacao

        else:
            pai_melhor.ponto_convergencia, pai_pior.ponto_convergencia = pai_pior.ponto_convergencia, pai_melhor.ponto_convergencia

        self.mutacao(pai_melhor, pai_pior)

        return populacao_ordenada

    def mutacao(self, individuo1, individuo2):
        rnd = random.random()

        #chance de 10% so sofrer mutação
        if rnd <= self.TAXA_MUTACAO:
            rnd = random.random()

            if rnd <= 0.5:
                individuo1.mutar()
            else:
                individuo2.mutar()

    def iniciar(self):
        melhores = []
        populacao = self.getPopulacao()

        for individuo in populacao:
            individuo.iniciar()

        for _ in range(self.FITNESS_TOTAL):
            populacao = self.cross_over(populacao)

            for individuo in populacao:
                individuo.iniciar()

            melhor = self.get_melhor(populacao)
            melhores.append(melhor)

            print("FUNCAO")
            print(melhor.f_objetivo())

            print("VALOR")
            print(melhor.algoritmoProblema.melhor.get_valor_total())

            print("PESO")
            print(melhor.algoritmoProblema.melhor.get_peso_total())
            print()
            print()

        melhor = self.get_melhor(melhores)

        print("Os melhores valores possíveis para o problema são:")
        print("Convergência: ", melhor.ponto_convergencia)
        print("Taxa de mutação: ", melhor.taxa_mutacao)
        print("População: ", melhor.qtd_populacao)


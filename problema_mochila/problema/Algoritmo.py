import time

import numpy as np
import random
from collections import deque

from problema_mochila.problema.Cromossomo import Cromossomo


class Algoritmo:

    melhor: Cromossomo
    tempo_execucao = 0

    def __init__(self, limite_massa,
                 taxa_mutacao, quantidade_populacao,
                 ponto_convergencia, percentual_melhores,
                 massa_item1, valor_item1, qtd_item1,
                 massa_item2, valor_item2, qtd_item2,
                 massa_item3, valor_item3, qtd_item3
                 ):


        self.LIMITE_MASSA = int(limite_massa)                        #Restrição de massa total que poderá ser levada na mochila.
        self.TAXA_MUTACAO = float(taxa_mutacao)                      #Percentual de indivíduos que sofrerão mutação ao ser realizado crossover.
        self.QUANTIDADE_POPULACAO = int(quantidade_populacao)        #Quantidade de indivíduos na população.

        self.PONTO_CONVERGENCIA = int(ponto_convergencia)            #Restrição de convergência do algoritmo (se os X últimos melhores individuos tiverem o mesmo)
                                                                     #valor da função objetivo, o algoritmo para.

        self.PERCENTUAL_MELHORES = float(percentual_melhores)        #Define qual o percentual em que a população será dividida entre os melhores
                                                                     #e os piores.

                                                                    #Caso a população tenha 4 indivíduos e o percentual seja 0.5 (50%)
                                                                    #2 indivíduos serão melhores e 2 piores.
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
            cromossomo = Cromossomo(self.massa_item1, self.valor_item1, self.qtd_item1,
                 self.massa_item2, self.valor_item2, self.qtd_item2,
                 self.massa_item3, self.valor_item3, self.qtd_item3)

            if cromossomo.get_peso_total() <= self.LIMITE_MASSA:
                populacao.append(cromossomo)
                individuos_adicionados += 1

        return populacao


    def get_melhor(self, populacao):
        melhor: Cromossomo = None

        for individuo in populacao:
            if melhor is None:
                melhor = individuo
            else:
                if individuo.get_valor_total() > melhor.get_valor_total():
                    melhor = individuo

        return melhor


    def cross_over(self, populacao):
        #Define qual o % de melhores/piores
        percentual_por_individuo = 1 / len(populacao)
        percentual_acumulado = 0

        qtd_melhores = 0

        if percentual_por_individuo == self.PERCENTUAL_MELHORES:
            qtd_melhores = 1
        else:
        #Conta a quantidade de melhores e piores.
            for i in range(0, len(populacao)):
                if percentual_acumulado <= self.PERCENTUAL_MELHORES:
                    qtd_melhores += 1

                percentual_acumulado += percentual_por_individuo

        melhores = []
        piores = []

        #Ordena em ordem reversa por valor total (função objetivo.)
        populacao_ordenada = sorted(populacao, key=lambda individuo: individuo.get_valor_total())
        populacao_ordenada.reverse()

        #Adiciona na lista de melhores ou piores.
        for individuo in populacao_ordenada:
            if len(melhores) < qtd_melhores:
                melhores.append(individuo)
            else:
                piores.append(individuo)

        total_melhores = sum(individuo.get_valor_total() for individuo in melhores)
        total_piores = sum(individuo.get_valor_total() for individuo in piores)

        probabilidade_acumulada = 0

        #Calcula as probabilidades acumuladas dos melhores e piores.
        for individuo in melhores:
            probabilidade = individuo.get_valor_total() / total_melhores
            probabilidade_acumulada = probabilidade + probabilidade_acumulada
            individuo.set_probabilidade_acumulada(probabilidade_acumulada)

        probabilidade_acumulada = 0

        for individuo in piores:
            probabilidade = individuo.get_valor_total() / total_piores
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

        cross_over_valido = False

        while not cross_over_valido:
            rnd = random.random()

            #Decide qual gene sofrerá crossover
            if rnd < 0.3333:
                pai_melhor.qtd_item1, pai_pior.qtd_item1 = pai_pior.qtd_item1, pai_melhor.qtd_item1

            elif rnd < 0.6666:
                pai_melhor.qtd_item2, pai_pior.qtd_item2 = pai_pior.qtd_item2, pai_melhor.qtd_item2

            else:
                pai_melhor.qtd_item3, pai_pior.qtd_item3 = pai_pior.qtd_item3, pai_melhor.qtd_item3

            #Se o resultado do crossover for infactível, refaz o crossover.
            cross_over_valido = pai_melhor.get_peso_total() <= self.LIMITE_MASSA and pai_pior.get_peso_total() <= self.LIMITE_MASSA

        self.mutacao(pai_melhor, pai_pior)

        return populacao_ordenada


    def mutacao(self, individuo1, individuo2):
        rnd = random.random()

        #chance de 10% so sofrer mutação
        if rnd <= self.TAXA_MUTACAO:
            rnd = random.random()

            if rnd <= 0.5:
                individuo1.mutar(self.LIMITE_MASSA)
            else:
                individuo2.mutar(self.LIMITE_MASSA)

    def melhor_valor(self):
        return self.melhor.get_valor_total()

    def melhor_peso(self):
        return self.melhor.get_peso_total()

    def iniciar(self):
        fitness = 0
        ultimos = deque(maxlen=self.PONTO_CONVERGENCIA)

        start_time = time.time()
        populacao = self.getPopulacao()

        while True:
            fitness += 1
            populacao = self.cross_over(populacao)
            ultimos.append(self.get_melhor(populacao))

            lista_ultimos = list(ultimos)

            if len(lista_ultimos) < self.PONTO_CONVERGENCIA:
                continue

            if ((sum(individuo.get_valor_total() for individuo in lista_ultimos) / self.PONTO_CONVERGENCIA)
                    == lista_ultimos[0].get_valor_total()):
                break

        self.melhor = self.get_melhor(list(ultimos))
        self.tempo_execucao = (time.time() - start_time)


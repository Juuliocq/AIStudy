import time

import numpy as np
import random
from collections import deque

from problema_mochila.problema.Cromossomo import Cromossomo  # Importa a classe Cromossomo que representa um indivíduo da população


class Algoritmo:

    melhor: Cromossomo
    tempo_execucao = 0  # Armazena o tempo total de execução do algoritmo

    def __init__(self, limite_massa,
                 taxa_mutacao, quantidade_populacao,
                 ponto_convergencia, percentual_melhores,
                 massa_item1, valor_item1, qtd_item1,
                 massa_item2, valor_item2, qtd_item2,
                 massa_item3, valor_item3, qtd_item3
                 ):

        # Inicialização dos parâmetros do algoritmo genético
        self.LIMITE_MASSA = int(limite_massa)                        # Restrição de massa total da mochila
        self.TAXA_MUTACAO = float(taxa_mutacao)                      # Probabilidade de mutação
        self.QUANTIDADE_POPULACAO = int(quantidade_populacao)        # Tamanho da população

        self.PONTO_CONVERGENCIA = int(ponto_convergencia)            # Número de gerações consecutivas sem melhora para encerrar o algoritmo
        self.PERCENTUAL_MELHORES = float(percentual_melhores)        # Porcentagem da população considerada "melhores indivíduos"

        # Parâmetros dos itens disponíveis (3 tipos)
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
        # Gera a população inicial com indivíduos viáveis (peso total dentro do limite)
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
        # Retorna o indivíduo com maior valor total da população (função objetivo)
        melhor: Cromossomo = None

        for individuo in populacao:
            if melhor is None:
                melhor = individuo
            else:
                if individuo.get_valor_total() > melhor.get_valor_total():
                    melhor = individuo

        return melhor

    def cross_over(self, populacao):
        # Realiza a operação de crossover entre indivíduos da população

        percentual_por_individuo = 1 / len(populacao)
        percentual_acumulado = 0
        qtd_melhores = 0

        # Calcula a quantidade de melhores indivíduos com base no percentual definido
        if percentual_por_individuo == self.PERCENTUAL_MELHORES:
            qtd_melhores = 1
        else:
            for i in range(0, len(populacao)):
                if percentual_acumulado <= self.PERCENTUAL_MELHORES:
                    qtd_melhores += 1

                percentual_acumulado += percentual_por_individuo

        melhores = []
        piores = []

        # Ordena os indivíduos da população por valor total (decrescente)
        populacao_ordenada = sorted(populacao, key=lambda individuo: individuo.get_valor_total())
        populacao_ordenada.reverse()

        # Separa os melhores e piores indivíduos
        for individuo in populacao_ordenada:
            if len(melhores) < qtd_melhores:
                melhores.append(individuo)
            else:
                piores.append(individuo)

        # Calcula a soma dos valores para normalização das probabilidades
        total_melhores = sum(individuo.get_valor_total() for individuo in melhores)
        total_piores = sum(individuo.get_valor_total() for individuo in piores)

        probabilidade_acumulada = 0

        # Calcula probabilidade acumulada para os melhores
        for individuo in melhores:
            probabilidade = individuo.get_valor_total() / total_melhores
            probabilidade_acumulada = probabilidade + probabilidade_acumulada
            individuo.set_probabilidade_acumulada(probabilidade_acumulada)

        probabilidade_acumulada = 0

        # Calcula probabilidade acumulada para os piores
        for individuo in piores:
            probabilidade = individuo.get_valor_total() / total_piores
            probabilidade_acumulada = probabilidade + probabilidade_acumulada
            individuo.set_probabilidade_acumulada(probabilidade_acumulada)

        rnd = random.random()
        pai_melhor = None
        pai_pior = None

        # Seleciona um pai da lista de melhores com base na roleta
        for i, individuo in enumerate(melhores):
            if i == len(melhores) - 1:
                pai_melhor = individuo
                break
            elif melhores[i + 1].get_probabilidade_acumulada() > rnd > individuo.get_probabilidade_acumulada():
                pai_melhor = individuo
                break

        rnd = random.random()

        # Seleciona um pai da lista de piores com base na roleta
        for i, individuo in enumerate(piores):
            if i == len(piores) - 1:
                pai_pior = individuo
                break

            if piores[i + 1].get_probabilidade_acumulada() > rnd > individuo.get_probabilidade_acumulada():
                pai_pior = individuo
                break

        cross_over_valido = False

        # Realiza o crossover até obter indivíduos viáveis
        while not cross_over_valido:
            rnd = random.random()

            # Escolhe aleatoriamente um gene para troca (quantidade de um item)
            if rnd < 0.3333:
                pai_melhor.qtd_item1, pai_pior.qtd_item1 = pai_pior.qtd_item1, pai_melhor.qtd_item1

            elif rnd < 0.6666:
                pai_melhor.qtd_item2, pai_pior.qtd_item2 = pai_pior.qtd_item2, pai_melhor.qtd_item2

            else:
                pai_melhor.qtd_item3, pai_pior.qtd_item3 = pai_pior.qtd_item3, pai_melhor.qtd_item3

            # Verifica se os novos indivíduos ainda respeitam o limite de peso
            cross_over_valido = pai_melhor.get_peso_total() <= self.LIMITE_MASSA and pai_pior.get_peso_total() <= self.LIMITE_MASSA

        self.mutacao(pai_melhor, pai_pior)  # Aplica mutação, se necessário

        return populacao_ordenada  # Retorna a população atualizada

    def mutacao(self, individuo1, individuo2):
        rnd = random.random()

        # Aplica mutação com probabilidade definida
        if rnd <= self.TAXA_MUTACAO:
            rnd = random.random()

            if rnd <= 0.5:
                individuo1.mutar(self.LIMITE_MASSA)
            else:
                individuo2.mutar(self.LIMITE_MASSA)

    def melhor_valor(self):
        # Retorna o valor total da melhor solução encontrada
        return self.melhor.get_valor_total()

    def melhor_peso(self):
        # Retorna o peso total da melhor solução encontrada
        return self.melhor.get_peso_total()

    def iniciar(self):
        fitness = 0  # Contador de iterações (gerações)
        ultimos = deque(maxlen=self.PONTO_CONVERGENCIA)  # Armazena os últimos melhores indivíduos

        start_time = time.time()
        populacao = self.getPopulacao()  # Gera população inicial

        while True:
            fitness += 1
            populacao = self.cross_over(populacao)  # Geração de nova população por crossover
            ultimos.append(self.get_melhor(populacao))  # Armazena o melhor da geração

            lista_ultimos = list(ultimos)

            if len(lista_ultimos) < self.PONTO_CONVERGENCIA:
                continue  # Ainda não atingiu o número necessário para verificar convergência

            # Verifica se os últimos N melhores têm o mesmo valor total (convergência)
            if ((sum(individuo.get_valor_total() for individuo in lista_ultimos) / self.PONTO_CONVERGENCIA)
                    == lista_ultimos[0].get_valor_total()):
                break  # Critério de parada atendido

        self.melhor = self.get_melhor(list(ultimos))  # Armazena a melhor solução final
        self.tempo_execucao = (time.time() - start_time)  # Calcula tempo de execução total

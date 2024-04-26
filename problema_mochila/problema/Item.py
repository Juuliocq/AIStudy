import random
import numpy as np


class Item:

    def __init__(self, tipo, massa, valor, quantidade_limite):
        self.tipo = tipo
        self.massa = float(massa)
        self.valor = float(valor)
        self.quantidade_limite = int(quantidade_limite)

        self.probabilidade_inicial = np.zeros((self.quantidade_limite + 1, 3))
        self.calcula_probabilidade_inicial()

    def calcula_probabilidade_inicial(self):
        probabilidade_acumulada = 0
        probabilidade = 1 / (self.quantidade_limite + 1)

        for qtd in range(self.quantidade_limite + 1):
            probabilidade_acumulada = probabilidade + probabilidade_acumulada
            self.probabilidade_inicial[qtd] = [qtd, probabilidade, probabilidade_acumulada]

    def get_qtd_inicial(self):
        #Randomico para decidir qual será a quantidade inicial do item com base no probabilidade_inicial.
        rdn = random.random()

        probabilidades = self.probabilidade_inicial

        for i in range(0, len(probabilidades) + 1):
            if i == len(probabilidades) - 1:
                return probabilidades[i][0]

            if probabilidades[i + 1][2] > rdn > probabilidades[i][2]:
                return probabilidades[i + 1][0]
import random
import numpy as np

class Item:

    def __init__(self, tipo, massa, valor, quantidade_limite):
        self.tipo = tipo  # Identificador do tipo de item (por exemplo, 1, 2 ou 3)
        self.massa = float(massa)  # Massa de cada unidade do item
        self.valor = float(valor)  # Valor de cada unidade do item
        self.quantidade_limite = int(quantidade_limite)  # Quantidade máxima permitida deste item

        # Matriz que armazena a distribuição de probabilidade para a quantidade inicial
        # Cada linha é composta por: [quantidade, probabilidade individual, probabilidade acumulada]
        self.probabilidade_inicial = np.zeros((self.quantidade_limite + 1, 3))
        self.calcula_probabilidade_inicial()  # Inicializa a matriz de probabilidades

    def calcula_probabilidade_inicial(self):
        # Calcula as probabilidades individuais e acumuladas para a quantidade de itens
        probabilidade_acumulada = 0
        probabilidade = 1 / (self.quantidade_limite + 1)  # Distribuição uniforme

        for qtd in range(self.quantidade_limite + 1):
            probabilidade_acumulada = probabilidade + probabilidade_acumulada
            # Armazena: [quantidade possível, probabilidade individual, probabilidade acumulada]
            self.probabilidade_inicial[qtd] = [qtd, probabilidade, probabilidade_acumulada]

    def get_qtd_inicial(self):
        # Sorteia uma quantidade inicial de itens com base na probabilidade acumulada
        rdn = random.random()  # Gera número aleatório entre 0 e 1

        probabilidades = self.probabilidade_inicial

        # Percorre a matriz de probabilidades para encontrar o intervalo correspondente ao número aleatório
        for i in range(0, len(probabilidades) + 1):
            if i == len(probabilidades) - 1:
                return probabilidades[i][0]  # Último valor como fallback

            if probabilidades[i + 1][2] > rdn > probabilidades[i][2]:
                return probabilidades[i + 1][0]  # Retorna a quantidade associada ao intervalo sorteado

import numpy as np
import random
from collections import deque

LIMITE_MASSA = 200          #Restrição de massa total que poderá ser levada na mochila.
TAXA_MUTACAO = 0.1          #Percentual de indivíduos que sofrerão mutação ao ser realizado crossover.
QUANTIDADE_POPULACAO = 10   #Quantidade de indivíduos na população.

PONTO_CONVERGENCIA = 30     #Restrição de convergência do algoritmo (se os X últimos melhores individuos tiverem o mesmo)
                            #valor da função objetivo, o algoritmo para.

PERCENTUAL_MELHORES = 0.5   #Define qual o percentual em que a população será dividida entre os melhores
                            #e os piores.

                            #Caso a população tenha 4 indivíduos e o percentual seja 0.5 (50%)
                            #2 indivíduos serão melhores e 2 piores.


class Item:

    def __init__(self, tipo, massa, valor, quantidade_limite):
        self.tipo = tipo
        self.massa = massa
        self.valor = valor
        self.quantidade_limite = quantidade_limite

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


class Cromossomo:

    def __init__(self):
        self.item1 = Item(1, 3, 40, 30)
        self.qtd_item1 = self.item1.get_qtd_inicial()

        self.item2 = Item(2, 5, 100, 20)
        self.qtd_item2 = self.item2.get_qtd_inicial()

        self.item3 = Item(3, 2, 50, 50)
        self.qtd_item3 = self.item3.get_qtd_inicial()

        self.probabilidade_acumulada = 0

        self.qtd_item1 = self.item1.get_qtd_inicial()
        self.qtd_item2 = self.item2.get_qtd_inicial()
        self.qtd_item3 = self.item3.get_qtd_inicial()

    def set_probabilidade_acumulada(self, probabilidade_acumulada):
        self.probabilidade_acumulada = probabilidade_acumulada

    def get_probabilidade_acumulada(self):
        return self.probabilidade_acumulada

    def get_peso_total(self):
        return (self.item1.massa * self.qtd_item1) + (self.item2.massa * self.qtd_item2) + (
                    self.item3.massa * self.qtd_item3)

    def get_valor_total(self):
        return (self.item1.valor * self.qtd_item1) + (self.item2.valor * self.qtd_item2) + (
                self.item3.valor * self.qtd_item3)

    def get_quantidade_item1(self):
        return self.qtd_item1

    def get_quantidade_item2(self):
        return self.qtd_item2

    def get_quantidade_item3(self):
        return self.qtd_item3

    def set_quantidade_item1(self, quantidade):
        self.qtd_item1 = quantidade

    def set_quantidade_item2(self, quantidade):
        self.qtd_item2 = quantidade

    def set_quantidade_item3(self, quantidade):
        self.qtd_item3 = quantidade

    #Realiza a mutação de algum gene aleatóriamente
    def mutar(self):
        rnd = random.random()
        valido = False

        while not valido:
            if rnd <= 0.3333: #Decide qual gene sofrerá mutação
                self.qtd_item1 = self.item1.get_qtd_inicial()
            elif rnd <= 0.6666: #Decide qual gene sofrerá mutação
                self.qtd_item2 = self.item2.get_qtd_inicial()
            else: #Decide qual gene sofrerá mutação
                self.qtd_item3 = self.item3.get_qtd_inicial()

            #Caso o resultado da mutação for infactível, refaz.
            valido = self.get_peso_total() <= LIMITE_MASSA


def getPopulacao(qtd_individuos):
    populacao = []
    individuos_adicionados = 0

    while individuos_adicionados < qtd_individuos:
        cromossomo = Cromossomo()

        if cromossomo.get_peso_total() <= LIMITE_MASSA:
            populacao.append(cromossomo)
            individuos_adicionados += 1

    return populacao


def get_melhor(populacao):
    melhor: Cromossomo = None

    for individuo in populacao:
        if melhor is None:
            melhor = individuo
        else:
            if individuo.get_valor_total() > melhor.get_valor_total():
                melhor = individuo

    return melhor


def cross_over(populacao):
    #Define qual o % de melhores/piores
    percentual_melhores = PERCENTUAL_MELHORES / 100

    percentual_por_individuo = 1 / len(populacao)
    percentual_acumulado = 0

    qtd_melhores = 0
    qtd_piores = 0

    #Conta a quantidade de melhores e piores.
    for i in range(0, len(populacao)):
        if percentual_acumulado <= PERCENTUAL_MELHORES:
            qtd_melhores += 1
        else:
            qtd_piores += 1

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

    #copia os pais para sofrer crossover
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
        cross_over_valido = pai_melhor.get_peso_total() <= LIMITE_MASSA and pai_pior.get_peso_total() <= LIMITE_MASSA

    mutacao(pai_melhor, pai_pior)

    return populacao_ordenada


def mutacao(individuo1, individuo2):
    rnd = random.random()

    #chance de 50% so sofrer mutação
    if rnd <= TAXA_MUTACAO:
        rnd = random.random()

        if rnd <= 0.5:
            individuo1.mutar()
        else:
            individuo2.mutar()


def main():
    fitness = 0
    ultimos = deque(maxlen=PONTO_CONVERGENCIA)
    populacao = getPopulacao(QUANTIDADE_POPULACAO)

    while True:
        fitness += 1
        populacao = cross_over(populacao)
        ultimos.append(get_melhor(populacao))

        lista_ultimos = list(ultimos)

        if len(lista_ultimos) < PONTO_CONVERGENCIA:
            continue

        if (sum(individuo.get_valor_total() for individuo in lista_ultimos) / PONTO_CONVERGENCIA) == lista_ultimos[0].get_valor_total():
            break

    melhor = get_melhor(list(ultimos))

    print("ACHEI EM: ", fitness, "PASSOS")
    print(melhor.get_valor_total())
    print(melhor.get_peso_total())

if __name__ == '__main__':
    main()

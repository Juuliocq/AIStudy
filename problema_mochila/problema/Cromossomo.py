import random

from problema_mochila.problema.Item import Item


class Cromossomo:

    def __init__(self, massa_item1, valor_item1, qtd_item1,
                 massa_item2, valor_item2, qtd_item2,
                 massa_item3, valor_item3, qtd_item3):
        self.item1 = Item(1, massa_item1, valor_item1, qtd_item1)
        self.qtd_item1 = self.item1.get_qtd_inicial()

        self.item2 = Item(2, massa_item2, valor_item2, qtd_item2)
        self.qtd_item2 = self.item2.get_qtd_inicial()

        self.item3 = Item(3, massa_item3, valor_item3, qtd_item3)
        self.qtd_item3 = self.item3.get_qtd_inicial()

        self.probabilidade_acumulada = 0

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
    def mutar(self, limite_massa):
        valido = False

        qtd_item1 = self.qtd_item1
        qtd_item2 = self.qtd_item2
        qtd_item3 = self.qtd_item3

        while not valido:

            self.qtd_item1 = qtd_item1
            self.qtd_item2 = qtd_item2
            self.qtd_item3 = qtd_item3

            rnd = random.random()

            if rnd <= 0.3333: #Decide qual gene sofrerá mutação
                self.qtd_item1 = self.item1.get_qtd_inicial()
            elif rnd <= 0.6666: #Decide qual gene sofrerá mutação
                self.qtd_item2 = self.item2.get_qtd_inicial()
            else: #Decide qual gene sofrerá mutação
                self.qtd_item3 = self.item3.get_qtd_inicial()

            #Caso o resultado da mutação for infactível, refaz.
            valido = self.get_peso_total() <= limite_massa
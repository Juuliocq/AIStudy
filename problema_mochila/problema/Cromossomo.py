import random

from problema_mochila.problema.Item import Item  # Importa a classe Item, que representa um tipo de item disponível

class Cromossomo:

    def __init__(self, massa_item1, valor_item1, qtd_item1,
                 massa_item2, valor_item2, qtd_item2,
                 massa_item3, valor_item3, qtd_item3):
        # Cria objetos Item para cada tipo de item e inicializa a quantidade de forma aleatória (via get_qtd_inicial)
        self.item1 = Item(1, massa_item1, valor_item1, qtd_item1)
        self.qtd_item1 = self.item1.get_qtd_inicial()

        self.item2 = Item(2, massa_item2, valor_item2, qtd_item2)
        self.qtd_item2 = self.item2.get_qtd_inicial()

        self.item3 = Item(3, massa_item3, valor_item3, qtd_item3)
        self.qtd_item3 = self.item3.get_qtd_inicial()

        self.probabilidade_acumulada = 0  # Usada para roleta na seleção

    def set_probabilidade_acumulada(self, probabilidade_acumulada):
        self.probabilidade_acumulada = probabilidade_acumulada

    def get_probabilidade_acumulada(self):
        return self.probabilidade_acumulada

    def get_peso_total(self):
        # Calcula o peso total do cromossomo com base nas quantidades e massas dos itens
        return (self.item1.massa * self.qtd_item1) + (self.item2.massa * self.qtd_item2) + (
                    self.item3.massa * self.qtd_item3)

    def get_valor_total(self):
        # Calcula o valor total do cromossomo com base nas quantidades e valores dos itens
        return (self.item1.valor * self.qtd_item1) + (self.item2.valor * self.qtd_item2) + (
                self.item3.valor * self.qtd_item3)

    # Métodos getters e setters para as quantidades de cada item
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

    # Realiza a mutação de algum gene aleatoriamente
    def mutar(self, limite_massa):
        valido = False

        # Guarda os valores atuais das quantidades
        qtd_item1 = self.qtd_item1
        qtd_item2 = self.qtd_item2
        qtd_item3 = self.qtd_item3

        while not valido:
            # Restaura os valores anteriores antes da tentativa de mutação
            self.qtd_item1 = qtd_item1
            self.qtd_item2 = qtd_item2
            self.qtd_item3 = qtd_item3

            rnd = random.random()

            # Decide aleatoriamente qual gene (item) será mutado
            if rnd <= 0.3333:
                self.qtd_item1 = self.item1.get_qtd_inicial()
            elif rnd <= 0.6666:
                self.qtd_item2 = self.item2.get_qtd_inicial()
            else:
                self.qtd_item3 = self.item3.get_qtd_inicial()

            # Verifica se o novo cromossomo continua viável (dentro do limite de massa)
            valido = self.get_peso_total() <= limite_massa
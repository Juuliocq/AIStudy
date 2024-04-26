import random

from problema_mochila.problema.Algoritmo import Algoritmo


class CromossomoOtimizador:

    probabilidade_acumulada = 0

    def __init__(self, limite_massa, populacao_maxima,
                 convergencia_maxima, percentual_melhores,
                 massa_item1, valor_item1, qtd_item1,
                 massa_item2, valor_item2, qtd_item2,
                 massa_item3, valor_item3, qtd_item3):

        self.LIMITE_MASSA = int(limite_massa)                        #Restrição de massa total que poderá ser levada na mochila.

        self.PERCENTUAL_MELHORES = float(percentual_melhores)        #Define qual o percentual em que a população será dividida entre os melhores
                                                                     #e os piores.

                                                                    #Caso a população tenha 4 indivíduos e o percentual seja 0.5 (50%)
                                                                    #2 indivíduos serão melhores e 2 piores.

        self.CONVERGENCIA_MAXIMA = int(convergencia_maxima)
        self.POPULACAO_MAXIMA = int(populacao_maxima)

        self.massa_item1 = float(massa_item1)
        self.valor_item1 = float(valor_item1)
        self.qtd_item1 = int(qtd_item1)

        self.massa_item2 = float(massa_item2)
        self.valor_item2 = float(valor_item2)
        self.qtd_item2 = int(qtd_item2)

        self.massa_item3 = float(massa_item3)
        self.valor_item3 = float(valor_item3)
        self.qtd_item3 = int(qtd_item3)

        self.taxa_mutacao = random.random()
        self.qtd_populacao = random.randint(2, self.POPULACAO_MAXIMA)
        self.ponto_convergencia = random.randint(1, self.CONVERGENCIA_MAXIMA)

        self.algoritmoProblema = self.getAlgoritmoProblema()

    def set_probabilidade_acumulada(self, probabilidade):
        self.probabilidade_acumulada = probabilidade

    def get_probabilidade_acumulada(self):
        return self.probabilidade_acumulada

    def getAlgoritmoProblema(self):
        return Algoritmo(self.LIMITE_MASSA, self.taxa_mutacao,
                                       self.qtd_populacao, self.ponto_convergencia, self.PERCENTUAL_MELHORES,
                                       self.massa_item1, self.valor_item1, self.qtd_item1,
                                       self.massa_item2, self.valor_item2, self.qtd_item2,
                                       self.massa_item3, self.valor_item3, self.qtd_item3)


    def f_objetivo(self):
        return self.algoritmoProblema.melhor_valor()

    def mutar(self):

        rnd = random.random()

        if rnd <= 0.3333:  # Decide qual gene sofrerá mutação
            self.taxa_mutacao = random.random()
        elif rnd <= 0.6666:  # Decide qual gene sofrerá mutação
            self.qtd_populacao = random.randint(2, self.POPULACAO_MAXIMA)
        else:  # Decide qual gene sofrerá mutação
            self.ponto_convergencia = random.randint(1, self.CONVERGENCIA_MAXIMA)

    def iniciar(self):
        self.algoritmoProblema.iniciar()


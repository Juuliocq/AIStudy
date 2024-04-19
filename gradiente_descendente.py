#RECEITA DE TREINAMENTO
# 1 - DESIGN DO MODELO (INPUT, OUTPUT, FORWARD PASS)
# 2 - DEFINIÇÃO DA FUNÇÃO DE CUSTO E OTIMIZADOR
# 3 - LOOP DE TREINAMENTO:
#   - FORWARD PASS: CALCULA A PREDIÇÃO E O CUSTO
#   - BACKWARDPASS: CALCULAR OS GRADIENTES
#   - ATUALIZAR OS PESOS

import torch
import time
import torch.nn as nn
import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from torch.autograd import Variable

#PREPARAÇÃO DA DATA
x_numpy, y_numpy = datasets.make_regression(n_samples=100, n_features=1, noise=20, random_state=1)

x = torch.from_numpy(x_numpy.astype(np.float32))
y = torch.from_numpy(y_numpy.astype(np.float32))
y = y.view(y.shape[0], 1)

plt.plot(x_numpy, y_numpy, 'ro')

# DEFINIÇÃO DO MODELO
input_size = 1
output_size = 1
model = nn.Linear(input_size, output_size)

# DEFINIÇÃO DA FUNÇÃO DE CUSTO E OTIMIZADOR
learning_rate = 0.05
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
print(model.parameters())

# LOOP DE TREINAMENTO
num_epochs = 2000
contador_custo = []

for epoch in range(num_epochs):
    #Gera a reta
    y_hat = model(x)

    #Calcula o custo ou perda da reta
    loss = criterion(y_hat, y)

    #Salva o custo da época
    contador_custo.append(loss)

    #Calcula o gradiente
    loss.backward()

    #Atualiza as variáveis (coeficiente angular e linear)
    optimizer.step()

    if (epoch+1)%100 == 0:
        print('-------------------------------------------------')
        print('Época ', epoch)
        print('Custo {:.20f}'.format(loss.item()))
        print('Coeficientes: ')
        print('CA: {:.20f}'.format(model.weight.data.detach().item()))
        print('CA Gradiente: {:.20f}'.format(model.weight.grad.detach().item()))
        print('CL: {:.20f}'.format(model.bias.data.detach().item()))
        print('CL Gradiente: {:.20f}'.format(model.bias.grad.detach().item()))
        previsao_final = y_hat.detach().numpy()
        plt.plot(x_numpy, y_numpy, 'ro')
        plt.plot(x_numpy, previsao_final, 'b')
        plt.show()

    optimizer.zero_grad()

    #Caso não seja mais identificado melhora no custo, para o algoritmo.
    if len(contador_custo) > 2 and contador_custo[epoch - 1].item() == loss.item():
        break

#PLOTA O GRÁFICO DA FUNÇÃO DE CUSTO
fi_los = [fl.item() for fl in contador_custo]
plt.plot(fi_los)
plt.show()


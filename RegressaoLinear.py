from matplotlib import pyplot as plt
import pandas as pd
import pylab as pl
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score, mean_squared_error,mean_absolute_error
from sklearn.model_selection import train_test_split
from math import sqrt

ds = pd.read_csv("FuelConsumptionCo2.csv")

print(ds.describe())

motores = ds[['ENGINESIZE']]
co2 = ds[['CO2EMISSIONS']]

motores_treino, motores_test, co2_treino, co2_test = train_test_split(motores, co2, test_size=0.2, random_state=42)

model = linear_model.LinearRegression()
model.fit(motores_treino, co2_treino)

print('(A) Intercepto: ', model.intercept_)
print('(B) Inclinação: ', model.coef_)

plt.scatter(motores_treino, co2_treino, color='red')
plt.plot(motores_treino, model.coef_[0][0]*motores_treino + model.intercept_[0], '-r')
plt.ylabel("Emissao de CO2")
plt.xlabel("Motores")
plt.show()

predicoesCo2 = model.predict(motores_test)

plt.scatter(motores_test, co2_test, color='blue')
plt.plot(motores_test, model.coef_[0][0]*motores_test + model.intercept_[0], '-r')
plt.ylabel("Emissão de C02")
plt.xlabel("Motores")
plt.show()

print("Soma dos Erros ao Quadrado (SSE): %.2f " % np.sum((predicoesCo2 - co2_test)**2))
print("Erro Quadrático Médio (MSE): %.2f" % mean_squared_error(co2_test, predicoesCo2))
print("Erro Médio Absoluto (MAE): %.2f" % mean_absolute_error(co2_test, predicoesCo2))
print ("Raiz do Erro Quadrático Médio (RMSE): %.2f " % sqrt(mean_squared_error(co2_test, predicoesCo2)))
print("R2-score: %.2f" % r2_score(co2_test, predicoesCo2) )
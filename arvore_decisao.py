import numpy as np
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.tree
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from six import StringIO
import pydotplus
import matplotlib.image as mpimg
from IPython.display import Image

df = pd.read_csv('dataset_einstein.csv', delimiter=';')

df = df.dropna()
print(df[df['SARS-Cov-2 exam result'] == 'negative'].shape[0])
print(df[df['SARS-Cov-2 exam result'] == 'positive'].shape[0])

Y = df['SARS-Cov-2 exam result'].values

X = df[['Hemoglobin', 'Leukocytes', 'Basophils', "Proteina C reativa mg/dL"]].values

X_treino, X_teste, Y_treino, Y_teste = train_test_split(X, Y, test_size=0.2, random_state=3)

arvore = sklearn.tree.DecisionTreeClassifier(criterion="entropy", max_depth=5)
modelo = arvore.fit(X_treino, Y_treino)

nome_features = ['Hemoglobin', 'Leukocytes', 'Basophils', 'Proteina C Reativa mg/dL']
nome_classe = modelo.classes_

dot_data = StringIO()
export_graphviz(modelo, out_file=dot_data, filled=True, feature_names=nome_features, class_names=nome_classe, rounded=True, special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png)
graph.write_png("arvore.png")
Image('arvore.png')
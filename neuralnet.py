from sklearn.neural_network import MLPClassifier
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carrega os elementos do dataset
dataset = pd.read_csv('Datasets/data_K1.csv')
x = dataset.iloc[:, [2,5]].values
y = dataset.iloc[:, 8].values

# Define a RNA com solver, numero de neuronios, ...
clf = MLPClassifier(activation='tanh', alpha=1e-05, batch_size='auto',
              beta_1=0.9, beta_2=0.999, early_stopping=False,
              epsilon=1e-08, hidden_layer_sizes=100,
              learning_rate='constant', learning_rate_init=0.01,
              max_iter=200, momentum=0.9, n_iter_no_change=10,
              nesterovs_momentum=True, power_t=0.5, random_state=1,
              shuffle=True, solver='adam', tol=0.0001,
              validation_fraction=0.1, verbose=False, warm_start=False)

# 80% do dataset é usado para treinar a RNA
x_fit = x[0:int(0.8*len(x))]
y_fit = y[0:int(0.8*len(y))]

# 20% do dataset é usado para testar a RNA
x_test = x[int(0.8*len(x)+1):len(x)]
y_test = y[int(0.8*len(y)+1):len(y)]

# Treina a RNA
clf.fit(x_fit, y_fit)

# Valores da saida preditos
y_predicted = clf.predict(x_test)

# Errro RMS entre os dados reais e os preditos
err_rms = sqrt(mean_squared_error(y_test, y_predicted))

print('Erro RMS:{0}'.format(err_rms))

plt.plot(y_test, label='Largura de Pulso Real')
plt.plot(y_predicted, label='Largura de Pulso Predita pela RNA')
plt.xlabel('Sequência de Pulsos')
plt.ylabel('Largura de Pulso [$\mu$S]')
plt.title('Comparação entre as Larguras de Pulso Reais e as Preditas pela Rede Neural Artificial')
plt.legend(loc=4)
plt.grid(True)
plt.savefig("position.png")
plt.show()

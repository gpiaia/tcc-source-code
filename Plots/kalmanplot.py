import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('../data.csv')

plt.plot(data['Posicaox'], label='x')
plt.plot(data['Posicaoy'], label='y')
plt.plot(data['Posicaoz'], label='z')
plt.plot(data['kPosicaox'], label='KVx')
plt.plot(data['kPosicaoy'], label='KVy')
plt.plot(data['kPosicaoz'], label='KVz')
plt.xlabel('Número de Amostras')
plt.ylabel('Posição Angular')
plt.title('Posição Angular com e sem Filtro de Kalman')
plt.legend(loc=3)
plt.grid(True)
plt.savefig("offset.png")
plt.show()
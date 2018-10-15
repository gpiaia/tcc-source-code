import pandas as pd
import numpy as np
# Carrega os elementos do dataset
dataset = pd.read_csv('data_r.csv')
x = dataset.iloc[:, 9].values
y = dataset.iloc[:, 2].values

print(len(x))
print(len(y))
z = np.column_stack((x,y))

np.savetxt("data.csv", z, delimiter=",")
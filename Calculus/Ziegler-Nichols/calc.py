import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import least_squares


data = pd.read_csv('../../Datasets/data_K1.csv')
sp = 45
zpos = data['kPosicaoz']

t = data['Tempo'].sub(dataset['Tempo'][0])

# 80% do dataset é usado para treinar a RNA
lenz = int(len(zpos)/6)
fitlen = int(0.8*lenz)
trainlen = int(0.2*lenz)

def fun(x, t, y):
    return x[0] * t + x[1] - y

def generate_data(t, k, tau):
	return k * t + tau

x0 = np.ones(2)

z_train = zpos[5:fitlen]
t_train = t[5:fitlen]

z_test = zpos[fitlen + 1:lenz]
t_test = t[fitlen + 1:lenz]

res_robust = least_squares(fun, x0, loss='soft_l1', f_scale=0.1, args=(t_train, z_train))

y_robust = generate_data(t_train, *res_robust.x)

def funL(a , b):
	return -b/a

def funA2(a , b):
	return (sp-b)/a

def funA(a , b):
	return -b


A = funA(*res_robust.x)
L = funL(*res_robust.x)
A2 = funA(*res_robust.x)

K = 1.2/A
Ti = 2*L
Td = L/2
Tp = 3.4*L

P = K*Tp
I = K*(1/Ti) 
D = K*(1/Td) 

P2 = 1.2*(L/A2)
I2 = 2*L
D2 = 0.5*L

print('P: {0}, P2: {1}'.format(P, P2))
print('I: {0}, I2: {1}'.format(I, I2))
print('D: {0}, D2: {1}'.format(D, D2))

plt.plot(t,zpos, label='test')
#plt.plot(y_robust, label='y_robust')
plt.xlabel('Tempo [s]')
plt.ylabel('Posição [°]')
plt.title('Posição Angular em Malha Fechada com Controlador PID Sintonizado via Ziegler-Nichols')
plt.legend(loc=1)
plt.grid(True)
plt.savefig("position.png")
plt.show()
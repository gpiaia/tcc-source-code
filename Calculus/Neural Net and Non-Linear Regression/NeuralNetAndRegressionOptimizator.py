from math import sqrt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import mean_squared_error
from scipy.optimize import least_squares

# Carrega os elementos do dataset
dataset = pd.read_csv('../../Datasets/data_k1_ensaio.csv')
z = dataset['kPosicaoz']
sp = dataset['SetPointz']

t = dataset['Tempo'].sub(dataset['Tempo'][0])

x = pd.concat([z, sp], axis=1, sort=False)
y = dataset['Largura de Pulso z']


################################## Neural Net ################################
# Define a RNA com solver, numero de neuronios, ...
clf = MLPClassifier(activation='tanh', alpha=1e-05, batch_size='auto',
              beta_1=0.9, beta_2=0.999, early_stopping=False,
              epsilon=1e-08, hidden_layer_sizes=70,
              learning_rate='constant', learning_rate_init=0.01,
              max_iter=400, momentum=0.9, n_iter_no_change=10,
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
y_predicted = clf.predict(x_fit)

# Errro RMS entre os dados reais e os preditos
err_rms = sqrt(mean_squared_error(y_fit, y_predicted))

print('Erro RMS:{0}'.format(err_rms))


################################## Plot Neural Net Comparison ################################
# plt.plot(y_fit, label='Largura de Pulso Real')
# plt.plot(y_predicted, label='Largura de Pulso Predita pela RNA')
# plt.xlabel('Sequência de Pulsos')
# plt.ylabel('Largura de Pulso [$\mu$S]')
# plt.title('Comparação entre as Larguras de Pulso Reais e as Preditas pela Rede Neural Artificial')
# plt.legend(loc=1)
# plt.grid(True)
# plt.savefig("position.png")
# plt.show()

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18,10))

# Set the font dictionaries (for plot title and axis titles)
title_font = {'fontname':'Times', 'size':'24', 'color':'black', 'weight':'normal',
  'verticalalignment':'bottom', 'usetex': 'true'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Times', 'size':'24', 'usetex': 'true'}

ax[1].plot(y_fit, label='Real', color='k', ls='solid')
ax[1].plot(y_predicted, label='Predita pela RNA', color='0.75', ls='solid')
ax[1].set_xlabel('Sequência de Pulsos', **axis_font)
ax[1].set_ylabel('Largura de Pulso [$\mu$S]', **axis_font)
ax[1].set_title('(b) Larguras de Pulso Reais e as Preditas pela RNA', **title_font)
ax[1].tick_params(axis='both', which='major', labelsize=18)
ax[1].set_xlim(0, 3500)
ax[1].legend(loc=0, borderpad=1.5, fontsize=18)
ax[1].grid(True)

# Neural Result
data_rna = pd.read_csv('../../Datasets/data_neural_ensaio.csv')
t_rna = data_rna['Tempo'].sub(data_rna['Tempo'][0])
sp = data_rna['SetPointz']
sp[0] = 0

# Anti Wind
data_pidaw = pd.read_csv('../../Datasets/data_antiwind_ensaio.csv')
t1 = data_pidaw['Tempo'].sub(data_pidaw['Tempo'][0])

# Simulação
data_obj = pd.read_csv('data.csv')
data_tmp = pd.read_csv('tempo.csv')

#ax[1].plot(t_rna, data_rna['kPosicaoz'], label=r'$\theta_x$z RNA', color='k', ls='solid')
ax[0].plot(t, dataset['kPosicaoz'], label=r'$\theta_z$ Treinamento', color='0.75', ls='solid')
ax[0].plot(data_tmp['Tempo'], data_obj['Posicaoz'], label=r'$\theta_z$ Objetivo', color='0.25', ls='solid')
ax[0].plot(t_rna, sp, label='Referência', color='k', linestyle='--')
ax[0].set_xlabel('Tempo [s]', **axis_font)
ax[0].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
ax[0].set_title('(a) Resposta ao Degrau com Sintonia Clássica e via RNA', **title_font)
ax[0].tick_params(axis='both', which='major', labelsize=18)
ax[0].set_xlim(0, 75)
ax[0].legend(loc=0, borderpad=1.5, fontsize=18)
ax[0].grid(True)


plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
plt.rc('axes', labelsize=18)
plt.subplots_adjust(left=0.06, right=0.98, top=0.95, bottom=0.07)
plt.savefig("../../../Monografia/resultados/img/neural_output.pdf")


################################## Optimization ################################

# # data = pd.read_csv('../../Datasets/data_neural_ensaio.csv')
# # z = data['kPosicaoz']
# data = pd.read_csv('data.csv')
# z = data['Posicaoz']

# sp = dataset['SetPointz']
# t = dataset['Tempo'].sub(dataset['Tempo'][0])

# dt = t[5]-t[400]
# x = pd.concat([z, sp], axis=1, sort=False)

# # 80% do dataset é usado para treinar a RNA
# lenz = int(len(z)/6)
# fitlen = int(0.8*lenz)
# trainlen = int(0.2*lenz)

# sp = dataset['SetPointz']

# err_sum = 0
# spn = sp[100] 
# n = 0

# z_train = z[0:fitlen]
# x_train = x[0:fitlen]
# n_train = pd.DataFrame(np.linspace(0, len(z_train), len(z_train)+1))

# y_pred = clf.predict(x_train)
# y_pred = np.array(y_pred[:], dtype=np.float)

# def fun(x, n_t, y) :
# 	global n, err_sum, dt, spn
# 	err = spn - z_train[int(n_t[0][n])]
# 	if(n>0) :
# 		err_sum += err
# 		err_int =  (z_train[int(n_t[0][n])] -  z_train[int(n_t[0][n-1])])/(dt)
# 		u = x[0] * err + (x[0]/x[1])*err_sum*dt - x[0]*x[2]*err_int
# 	else : 
# 		u = 0
# 	n += 1
# 	return u - y


# kp = 29.192682465627243
# ki = 20.70403011746613
# kd = 10.290420569133603

# x0 = [kp, kp/ki,kd/kp]

# res_robust = least_squares(fun, x0, loss='arctan', f_scale=0.1, args=(n_train, y_pred))


# def funK(a, b, c):
# 	return (a, b, c)

# K = funK(*res_robust.x)
# Kp = K[0]
# Ki =Kp/K[1]
# Kd = Kp*K[2]

# print('Kp ={0}, Ki ={1}, Kd = {2}'.format(Kp, Ki, Kd))
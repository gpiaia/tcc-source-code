import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares


A = 2
sigma = 0.1
omega = 0.1 * 2 * np.pi
x_true = np.array([A, sigma, omega])

noise = 0.1

t_min = 0
t_max = 30


def generate_data(t, A, sigma, omega, noise=0, n_outliers=0, random_state=0):
    y = A * np.exp(-sigma * t) * np.sin(omega * t)
    rnd = np.random.RandomState(random_state)
    error = noise * rnd.randn(t.size)
    outliers = rnd.randint(0, t.size, n_outliers)
    error[outliers] *= 35
    return y + error	

t_train = np.linspace(t_min, t_max, 30)
y_train = generate_data(t_train, A, sigma, omega, noise=noise, n_outliers=4)

def fun(x, t, y):
    return x[0] * np.exp(-x[1] * t) * np.sin(x[2] * t) - y

x0 = np.ones(3)

res_lsq = least_squares(fun, x0, args=(t_train, y_train))


res_robust = least_squares(fun, x0, loss='soft_l1', f_scale=0.1, args=(t_train, y_train))

t_test = np.linspace(t_min, t_max, 300)
y_test = generate_data(t_test, A, sigma, omega)


y_lsq = generate_data(t_test, *res_lsq.x)
y_robust = generate_data(t_test, *res_robust.x)


########################## Regressão Não-Linear ##############################


# Set the font dictionaries (for plot title and axis titles)
title_font = {'fontname':'Times', 'size':'20', 'color':'black', 'weight':'normal',
  'verticalalignment':'bottom', 'usetex': 'true'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Times', 'size':'20', 'usetex': 'true'}

plt.plot(t_train, y_train,'o', label='Dados', color='k')
plt.plot(t_test, y_test, label='Analítico', color='k', ls='solid')
plt.plot(t_test, y_lsq, label='MMQ', color='0.5', ls='solid')
plt.plot(t_test, y_robust, label='MMQ Robusto', color='k', linestyle='--')
plt.xlabel('Tempo [s] ', **axis_font)
plt.ylabel('Amplitude', **axis_font)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.legend(loc=1, borderpad=1.5, fontsize=16)
plt.grid(True)


plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
plt.rc('axes', labelsize=18)
plt.subplots_adjust(left=0.1, right=0.99, top=0.97, bottom=0.15)
plt.savefig("../../Monografia/referencial/img/robust_regression.pdf")
#scp pi@10.0.0.100:/home/pi/Code/data.csv '/c/Users/Gpiaia/Google Drive/Eng. de Controle e Automacao/TCC/Code/data.csv'
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv('../Datasets/data_k1.csv')
data_comp = pd.read_csv('../Datasets/data_neural.csv')

t = data['Tempo'].sub(data['Tempo'][0])

zn = data_comp['kPosicaoz']

sp = data['SetPointz']
sp[0] = 0

####################### Posição #################################

# fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15,13))

# # Set the font dictionaries (for plot title and axis titles)
# title_font = {'fontname':'Times', 'size':'16', 'color':'black', 'weight':'normal',
#   'verticalalignment':'bottom', 'usetex': 'true'} # Bottom vertical alignment for more space
# axis_font = {'fontname':'Times', 'size':'14', 'usetex': 'true'}

# ax[0][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[0][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[0][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[0][0].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[0][0].set_xlabel('Tempo [s]', **axis_font)
# ax[0][0].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[0][0].set_title('(a) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[0][0].legend(loc=2)
# ax[0][0].grid(True)

# ax[0][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[0][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[0][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[0][1].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[0][1].set_xlabel('Tempo [s]', **axis_font)
# ax[0][1].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[0][1].set_title('(b) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[0][1].legend(loc=2)
# ax[0][1].grid(True)

# ax[1][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[1][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[1][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[1][0].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[1][0].set_xlabel('Tempo [s]', **axis_font)
# ax[1][0].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[1][0].set_title('(c) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[1][0].legend(loc=2)
# ax[1][0].grid(True)

# ax[1][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[1][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[1][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[1][1].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[1][1].set_xlabel('Tempo [s]', **axis_font)
# ax[1][1].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[1][1].set_title('(d) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[1][1].legend(loc=2)
# ax[1][1].grid(True)

# plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
# plt.rc('xtick', labelsize=18)
# plt.rc('ytick', labelsize=18)
# plt.rc('axes', labelsize=18)
# plt.subplots_adjust(left=0.04, right=0.99, top=0.97, bottom=0.04)
# plt.savefig("../../Monografia/resultados/img/pid_result.pdf")

####################### Rede Neural #################################

# fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15,13))

# # Set the font dictionaries (for plot title and axis titles)
# title_font = {'fontname':'Times', 'size':'20', 'color':'black', 'weight':'normal',
#   'verticalalignment':'bottom', 'usetex': 'true'} # Bottom vertical alignment for more space
# axis_font = {'fontname':'Times', 'size':'20', 'usetex': 'true'}

# ax[0][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[0][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[0][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[0][0].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[0][0].set_xlabel('Tempo [s]', **axis_font)
# ax[0][0].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[0][0].set_title('(a) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[0][0].tick_params(axis='both', which='major', labelsize=16)
# ax[0][0].legend(loc=2, borderpad=1.5, fontsize=16)
# ax[0][0].grid(True)

# ax[0][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[0][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[0][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[0][1].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[0][1].set_xlabel('Tempo [s]', **axis_font)
# ax[0][1].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[0][1].set_title('(b) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[0][1].tick_params(axis='both', which='major', labelsize=16)
# ax[0][1].legend(loc=2, borderpad=1.5, fontsize=16)
# ax[0][1].grid(True)

# ax[1][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[1][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[1][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[1][0].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[1][0].set_xlabel('Tempo [s]', **axis_font)
# ax[1][0].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[1][0].set_title('(c) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[1][0].tick_params(axis='both', which='major', labelsize=16)
# ax[1][0].legend(loc=2, borderpad=1.5, fontsize=16)
# ax[1][0].grid(True)

# ax[1][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[1][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[1][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[1][1].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[1][1].set_xlabel('Tempo [s]', **axis_font)
# ax[1][1].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[1][1].set_title('(d) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[1][1].legend(loc=2, borderpad=1.5, fontsize=16)
# ax[1][1].set_title('(d) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[1][1].tick_params(axis='both', which='major', labelsize=16)
# ax[1][1].grid(True)

# plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
# plt.rc('xtick', labelsize=18)
# plt.rc('ytick', labelsize=18)
# plt.rc('axes', labelsize=18)
# plt.subplots_adjust(left=0.07, right=0.99, top=0.97, bottom=0.06)
# plt.savefig("../../Monografia/resultados/img/pid_result.pdf")



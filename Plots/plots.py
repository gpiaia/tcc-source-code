#scp pi@192.168.0.100:/home/pi/Code/data.csv '/c/Users/Gpiaia/Google Drive/Eng. de Controle e Automacao/TCC/Code/Datasets/data.csv'
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv('../Datasets/data_rele_h1_k100.csv')
data_comp = pd.read_csv('../Datasets/data_neural.csv')

t = data['Tempo'].sub(data['Tempo'][0])

zn = data_comp['kPosicaoz']

sp = data['SetPointz']
sp[0] = 0


####### Simple Plot ##########################
# plt.plot(t, data['kPosicaoz'], label='x')
# plt.plot(t, data['Largura de Pulso z'].sub(data['Largura de Pulso z'][0]-145), label='z')
# plt.plot(t, sp, label='Referência')
# plt.xlabel('Tempo [s]')
# plt.ylabel('Posição [°]')
# plt.annotate('100',xy=(55,50))
# plt.xlim(50, 60)
# plt.ylim(0, 105)
# plt.title('Posição Angular em Malha Fechada com Controlador PID Sintonizado via Ziegler-Nichols')
# plt.legend(loc=0)
# plt.grid(True)
# plt.show()

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
# ax[0][0].legend(loc=0)
# ax[0][0].grid(True)

# ax[0][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[0][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[0][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[0][1].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[0][1].set_xlabel('Tempo [s]', **axis_font)
# ax[0][1].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[0][1].set_title('(b) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[0][1].legend(loc=0)
# ax[0][1].grid(True)

# ax[1][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[1][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[1][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[1][0].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[1][0].set_xlabel('Tempo [s]', **axis_font)
# ax[1][0].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[1][0].set_title('(c) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[1][0].legend(loc=0)
# ax[1][0].grid(True)

# ax[1][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaox'], label=r'$\theta_x$', color='k', ls='solid')
# ax[1][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoy'], label=r'$\theta_x$y', color='0.75', ls='solid')
# ax[1][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['kPosicaoz'], label=r'$\theta_x$z', color='0.5', ls='solid')
# ax[1][1].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[1][1].set_xlabel('Tempo [s]', **axis_font)
# ax[1][1].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[1][1].set_title('(d) Velocidade Angular Instantânea nos Três Eixos', **title_font)
# ax[1][1].legend(loc=0)
# ax[1][1].grid(True)

# plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
# plt.rc('xtick', labelsize=18)
# plt.rc('ytick', labelsize=18)
# plt.rc('axes', labelsize=18)
# plt.subplots_adjust(left=0.04, right=0.99, top=0.97, bottom=0.04)
# plt.savefig("../../Monografia/resultados/img/pid_result.pdf")

####################### Simulacao x real #################################

# ##### Simulacao
# data_simu = pd.read_csv('../Calculus/Matlab/simu_data_anti.csv')
# data_t = pd.read_csv('../Calculus/Matlab/simu_data_tempo_anti.csv')
# t1 = data_t['t']

# # Anti Wind
# data_pidaw = pd.read_csv('../Datasets/data_antiwind_ensaio.csv')
# t = data_pidaw['Tempo'].sub(data_pidaw['Tempo'][0])
# sp = data_pidaw['SetPointz']
# sp[0] = 0

# # Neural Result
# data_rna = pd.read_csv('../Datasets/data_neural_ensaio.csv')
# t_rna = data_rna['Tempo'].sub(data_rna['Tempo'][0])

# fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15,13))

# # Set the font dictionaries (for plot title and axis titles)
# title_font = {'fontname':'Times', 'size':'20', 'color':'black', 'weight':'normal',
#   'verticalalignment':'bottom', 'usetex': 'true'} # Bottom vertical alignment for more space
# axis_font = {'fontname':'Times', 'size':'20', 'usetex': 'true'}

# ax[0][1].plot(t1, data_simu['z'], label=r'$\theta_z$ com Anti-Windup Simulado', color='k', ls='solid')
# ax[0][1].plot(t, data_pidaw['kPosicaoz'], label=r'$\theta_z$ Real', color='0.75', ls='solid')
# ax[0][1].plot(t_rna, data_rna['kPosicaoz'], label=r'$\theta_z$ Real RNA', color='0.5', ls='solid')
# ax[0][1].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[0][1].set_xlabel('Tempo [s]', **axis_font)
# ax[0][1].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[0][1].set_title('(b) Respostas ao Degrau Simuladas e Reais', **title_font)
# ax[0][1].tick_params(axis='both', which='major', labelsize=16)
# ax[0][1].legend(loc=0, borderpad=1.5, fontsize=16)
# ax[0][1].set_xlim(0, 67)
# ax[0][1].grid(True)


# ##### Simulacao
# data_simu_pid = pd.read_csv('../Calculus/Matlab/simu_data_pid_2.csv')
# data_t = pd.read_csv('../Calculus/Matlab/simu_time_pid.csv')
# t_simu = data_t['t']
# t = data['Tempo'].sub(data['Tempo'][0])
# zn = data_comp['kPosicaoz']

# # Anti Wind sumulacao
# data_pidaw_simu = pd.read_csv('../Calculus/Matlab/simu_data_anti.csv')
# data_pidaw_t = pd.read_csv('../Calculus/Matlab/simu_data_tempo_anti.csv')

# t_anti = data_pidaw_t['t']
# sp = data_pidaw_simu['sp']
# sp[0] = 0

# ax[0][0].plot(t_simu, data_simu_pid['z'], label=r'$\theta_z$ com Anti-Windup', color='k', ls='solid')
# ax[0][0].plot(t_anti, data_pidaw_simu['z'], label=r'$\theta_z$', color='0.5', ls='solid')
# ax[0][0].plot(t_anti, sp, label='Referência', color='k', linestyle='--')
# ax[0][0].set_xlabel('Tempo [s]', **axis_font)
# ax[0][0].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[0][0].set_title('(a) Respostas ao Degrau Simuladas ', **title_font)
# ax[0][0].tick_params(axis='both', which='major', labelsize=16)
# ax[0][0].legend(loc=0, borderpad=1.5, fontsize=16)
# ax[0][0].grid(True)


# ax[1][0].plot(data['Tempo'].sub(data['Tempo'][0]), data['Gyroz'], label=r'$\omega_z$', color='0.25', ls='solid')
# ax[1][0].set_xlabel('Tempo [s]', **axis_font)
# ax[1][0].set_ylabel('Velocidade Angular Instantânea [°]', **axis_font)
# ax[1][0].set_title('(c) Velocidade Angular Instantânea no Eixo z', **title_font)
# ax[1][0].tick_params(axis='both', which='major', labelsize=16)
# ax[1][0].legend(loc=0, borderpad=1.5, fontsize=16)
# ax[1][0].grid(True)

# ax[1][1].plot(data['Tempo'].sub(data['Tempo'][0]), data['Largura de Pulso z'], label=r'$u_z$', color='0.5', ls='solid')
# ax[1][1].set_xlabel('Tempo [s]', **axis_font)
# ax[1][1].set_ylabel('Amplitude', **axis_font)
# ax[1][1].legend(loc=0, borderpad=1.5, fontsize=16)
# ax[1][1].set_title('(d) Sinal de Controle Real com Anti-Windup', **title_font)
# ax[1][1].tick_params(axis='both', which='major', labelsize=16)
# ax[1][1].grid(True)

# plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
# plt.rc('xtick', labelsize=18)
# plt.rc('ytick', labelsize=18)
# plt.rc('axes', labelsize=18)
# plt.subplots_adjust(left=0.05, right=0.99, top=0.97, bottom=0.05)
# plt.savefig("../../Monografia/resultados/img/pid_result_simu.pdf")


####### Rele ##########################

data = pd.read_csv('../Datasets/data_rele_h1_k100.csv')

t = data['Tempo'].sub(data['Tempo'][0])

sp = data['SetPointz']
sp[0] = 0

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18,10))

# Set the font dictionaries (for plot title and axis titles)
title_font = {'fontname':'Times', 'size':'24', 'color':'black', 'weight':'normal',
  'verticalalignment':'bottom', 'usetex': 'true'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Times', 'size':'24', 'usetex': 'true'}

data_pidaw = pd.read_csv('../Datasets/data_antiwind_ensaio.csv')
t_sp = data_pidaw['Tempo'].sub(data_pidaw['Tempo'][0])
sp = data_pidaw['SetPointz']
sp[0] = 0
# Simulação

ax[1].plot(t, data['kPosicaoz'], label=r'$\theta_z$ [°]', color='k', ls='solid')
ax[1].plot(t, data['Largura de Pulso z'].sub(data['Largura de Pulso z'][0]-145), label='Sinal de Controle [$\mu$S]', color='0.5', ls='solid')
ax[1].plot(t_sp, sp, label='Referência [°]', color='k', linestyle='--')
ax[1].set_xlabel('Tempo [s]', **axis_font)
ax[1].set_ylabel('Amplitude', **axis_font)
ax[1].set_title('(b) Resultado Método do Relé em Regime Permanente', **title_font)
ax[1].tick_params(axis='both', which='major', labelsize=18)
ax[1].set_xlim(50, 56)
ax[1].set_ylim(0, 105)
ax[1].legend(loc=0, borderpad=1.5, fontsize=18)
ax[1].grid(True)


ax[0].plot(t, data['kPosicaoz'], label=r'$\theta_z$  [°]', color='k', ls='solid')
ax[0].plot(t, data['Largura de Pulso z'].sub(data['Largura de Pulso z'][0]-145), label='Sinal de Controle [$\mu$S]', color='0.5', ls='solid')
ax[0].set_xlabel('Tempo [s]', **axis_font)
ax[0].set_ylabel('Amplitude', **axis_font)
ax[0].plot(t_sp, sp, label='Referência [°]', color='k', linestyle='--')
ax[0].set_title('(a) Resultado Método do Relé', **title_font)
ax[0].tick_params(axis='both', which='major', labelsize=18)
ax[0].set_xlim(0, 60)
ax[0].legend(loc=0, borderpad=1.5, fontsize=18)
ax[0].grid(True)

plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
plt.rc('axes', labelsize=18)
plt.subplots_adjust(left=0.05, right=0.99, top=0.95, bottom=0.07)
plt.savefig("../../Monografia/resultados/img/relay.pdf")

####################### Simulacao x real #################################

##### Simulacao
# data_simu = pd.read_csv('../Calculus/Matlab/simu_data_anti.csv')
# data_t = pd.read_csv('../Calculus/Matlab/simu_data_tempo_anti.csv')
# t1 = data_t['t']

# # Anti Wind
# data_pidaw = pd.read_csv('../Datasets/data_antiwind_ensaio.csv')
# t = data_pidaw['Tempo'].sub(data_pidaw['Tempo'][0])
# sp = data_pidaw['SetPointz']
# sp[0] = 0

# # Neural Result
# data_rna = pd.read_csv('../Datasets/data_neural_ensaio.csv')
# t_rna = data_rna['Tempo'].sub(data_rna['Tempo'][0])

# fig, ax = plt.subplots(nrows=1, ncols=2,  figsize=(24,12))

# # Set the font dictionaries (for plot title and axis titles)
# title_font = {'fontname':'Times', 'size':'32', 'color':'black', 'weight':'normal',
#   'verticalalignment':'bottom', 'usetex': 'true'} # Bottom vertical alignment for more space
# axis_font = {'fontname':'Times', 'size':'32', 'usetex': 'true'}

# ax[1].plot(t1, data_simu['z'], label=r'$\theta_z$ Simulado', color='k', ls='solid')
# ax[1].plot(t, data_pidaw['kPosicaoz'], label=r'$\theta_z$ Real', color='0.75', ls='solid')
# ax[1].plot(t_rna, data_rna['kPosicaoz'], label=r'$\theta_z$ RNA', color='0.5', ls='solid')
# ax[1].plot(t, sp, label='Referência', color='k', linestyle='--')
# ax[1].set_xlabel('Tempo [s]', **axis_font)
# ax[1].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[1].set_title('(b) Respostas ao Degrau Simuladas e Reais', **title_font)
# ax[1].tick_params(axis='both', which='major', labelsize=28)
# ax[1].legend(loc=0, borderpad=1.5, fontsize=28)
# ax[1].set_xlim(0, 67)
# ax[1].grid(True)


# # # ##### Simulacao
# data_simu_pid = pd.read_csv('../Calculus/Matlab/simu_data_pid_2.csv')
# data_t = pd.read_csv('../Calculus/Matlab/simu_time_pid.csv')
# t_simu = data_t['t']
# t = data['Tempo'].sub(data['Tempo'][0])
# zn = data_comp['kPosicaoz']

# # Anti Wind sumulacao
# data_pidaw_simu = pd.read_csv('../Calculus/Matlab/simu_data_anti.csv')
# data_pidaw_t = pd.read_csv('../Calculus/Matlab/simu_data_tempo_anti.csv')

# t_anti = data_pidaw_t['t']
# sp = data_pidaw_simu['sp']
# sp[0] = 0

# ax[0].plot(t_simu, data_simu_pid['z'], label=r'$\theta_z$ com Anti-Windup', color='k', ls='solid')
# ax[0].plot(t_anti, data_pidaw_simu['z'], label=r'$\theta_z$', color='0.5', ls='solid')
# ax[0].plot(t_anti, sp, label='Referência', color='k', linestyle='--')
# ax[0].set_xlabel('Tempo [s]', **axis_font)
# ax[0].set_ylabel('Posição Angular Instantânea [°]', **axis_font)
# ax[0].set_title('(a) Respostas ao Degrau Simuladas ', **title_font)
# ax[0].tick_params(axis='both', which='major', labelsize=28)
# ax[0].legend(loc=0, borderpad=1.5, fontsize=28)
# ax[0].grid(True)

# plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
# plt.rc('xtick', labelsize=28)
# plt.rc('ytick', labelsize=28)
# plt.rc('axes', labelsize=28)
# plt.subplots_adjust(left=0.06, right=0.99, top=0.95, bottom=0.08)
# plt.savefig("../../Monografia/resultados/img/pid_result.pdf")

# fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24,12))

# ax[0].plot(data_pidaw['Tempo'].sub(data_pidaw['Tempo'][0]), data_pidaw['Gyroz'], label=r'$\omega_z$', color='0.25', ls='solid')
# ax[0].set_xlabel('Tempo [s]', **axis_font)
# ax[0].set_ylabel('Velocidade Angular Instantânea [°/s]', **axis_font)
# ax[0].set_title('(a) Velocidade Angular Instantânea no Eixo z', **title_font)
# ax[0].tick_params(axis='both', which='major', labelsize=28)
# ax[0].legend(loc=0, borderpad=1.5, fontsize=28)
# ax[0].set_xlim(0, 80)
# ax[0].grid(True)

# ax[1].plot(data_pidaw['Tempo'].sub(data_pidaw['Tempo'][0]), data_pidaw['Largura de Pulso z'], label=r'$u_z$', color='0.5', ls='solid')
# ax[1].set_xlabel('Tempo [s]', **axis_font)
# ax[1].set_ylabel('Largura de Pulso [$\mu$S]', **axis_font)
# ax[1].legend(loc=0, borderpad=1.5, fontsize=28)
# ax[1].set_title('(b) Sinal de Controle Real com Anti-Windup', **title_font)
# ax[1].tick_params(axis='both', which='major', labelsize=28)
# ax[1].set_xlim(0, 80)
# ax[1].grid(True)

# plt.rc('font', family='serif', serif='Times')
# plt.rc('text', usetex=True)
# plt.rc('xtick', labelsize=28)
# plt.rc('ytick', labelsize=28)
# plt.rc('axes', labelsize=28)
# plt.subplots_adjust(left=0.07, right=0.99, top=0.95, bottom=0.08)
# plt.savefig("../../Monografia/resultados/img/pid_result_controller.pdf")
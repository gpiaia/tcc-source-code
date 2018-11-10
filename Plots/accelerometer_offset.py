import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd
import numpy as np

data = pd.read_csv('../Datasets/data.csv')


#%%%%%%%%%%%%%%%%%%%%%% Data %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

medianx = data['Gyrox'].median()
mediany = data['Gyroy'].median()
medianz = data['Gyroz'].median()

meanx = data['Gyrox'].mean()
meany = data['Gyroy'].mean()
meanz = data['Gyroz'].mean()

print('Mediana: {0}, {1}, {2}'.format(medianx, mediany, medianz))
print('Media: {0}, {1}, {2}'.format(meanx, meany, meanz))

# xx = np.full(len(data), medianx)
# yy = np.full(len(data), mediany)
# zz = np.full(len(data), medianz)

# xm = np.full(len(data), meanx)
# ym = np.full(len(data), meany)
# zm = np.full(len(data), meanz)


#%%%%%%%%%%%%%%%%%%%%%% Histograma %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15,13))

# Set the font dictionaries (for plot title and axis titles)
title_font = {'fontname':'Times', 'size':'20', 'color':'black', 'weight':'normal',
  'verticalalignment':'bottom', 'usetex': 'true'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Times', 'size':'20', 'usetex': 'true'}

ax[0][0].plot(data['Gyrox'], label='$\omega_x$', color='k', ls='solid')
ax[0][0].plot(data['Gyroy'], label='$\omega_y$', color='0.75', ls='solid')
ax[0][0].plot(data['Gyroz'], label='$\omega_z$', color='0.5', ls='solid')
ax[0][0].set_xlabel('Número de Amostras', **axis_font)
ax[0][0].set_ylabel('Velocidade Angular Instantânea [°/s]', **axis_font)
ax[0][0].set_title('(a) Velocidade Angular Instantânea nos Três Eixos', **title_font)
ax[0][0].tick_params(axis='both', which='major', labelsize=16)
#ax[0][0].set_xlim(0, 110000)
ax[0][0].legend(loc=1, fontsize=16)
ax[0][0].grid(True)

ax[0][1].hist(data['Gyrox'], bins='auto', color='k', ls='solid')
ax[0][1].set_xlabel('Velocidade Angular Instantânea [°/s]', **axis_font)
ax[0][1].set_ylabel('Número de Amostras', **axis_font)
ax[0][1].set_title('(b) Histograma da Velocidade Angular no Eixo x', **title_font)
ax[0][1].tick_params(axis='both', which='major', labelsize=16)
ax[0][1].grid(True)
ax[0][1].text(60, .025, r'$\mu=100,\ \sigma=15$')

ax[1][0].hist(data['Gyroy'], bins='auto', color='k', ls='solid')
ax[1][0].set_xlabel('Velocidade Angular Instantânea [°/s]', **axis_font)
ax[1][0].set_ylabel('Número de Amostras', **axis_font)
ax[1][0].set_title('(c) Histograma da Velocidade Angular no Eixo y', **title_font)
ax[1][0].tick_params(axis='both', which='major', labelsize=16)
ax[1][0].grid(True)

ax[1][1].hist(data['Gyroz'], bins='auto', color='k', ls='solid')
ax[1][1].set_xlabel('Velocidade Angular Instantânea[°/s]', **axis_font)
ax[1][1].set_ylabel('Número de Amostras', **axis_font)
ax[1][1].set_title('(d) Histograma da Velocidade Angular no Eixo z', **title_font)
ax[1][1].tick_params(axis='both', which='major', labelsize=16)
#ax[1][1].set_xlim(0, 0.6)
ax[1][1].grid(True)

plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
plt.rc('axes', labelsize=18)
plt.subplots_adjust(left=0.06, right=0.99, top=0.97, bottom=0.055)
#plt.savefig("../../Monografia/metodologia/img/bias_correction.pdf")
plt.show()

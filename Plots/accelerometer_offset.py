import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('../Datasets/GyroData.csv')

medianx = data['Gyrox'].median()
mediany = data['Gyroy'].median()
medianz = data['Gyroz'].median()

meanx = data['Gyrox'].mean()
meany = data['Gyroy'].mean()
meanz = data['Gyroz'].mean()


print('Mediana: {0}, {1}, {2}'.format(medianx, mediany, medianz))
print('Media: {0}, {1}, {2}'.format(meanx, meany, meanz))

xx = np.full(len(data), medianx)
yy = np.full(len(data), mediany)
zz = np.full(len(data), medianz)

xm = np.full(len(data), meanx)
ym = np.full(len(data), meany)
zm = np.full(len(data), meanz)

plt.plot(data['Gyrox'], label='Vx')
plt.plot(data['Gyroy'], label='Vy')
plt.plot(data['Gyroz'], label='Vz')
plt.plot(xx, label='Mediana Vx') 
plt.plot(yy, label='Mediana Vy') 
plt.plot(zz, label='Mediana Vz') 
plt.plot(xm, label='Media Vx') 
plt.plot(ym, label='Media Vy') 
plt.plot(zm, label='Media Vz') 
plt.xlabel('Número de Amostras')
plt.ylabel('Velocidade Angular Instantânea[°/s]')
plt.title('Velocidade Angular com o Satélite parado')
plt.legend(loc=3)
plt.grid(True)
plt.savefig("offset.png")
plt.show()
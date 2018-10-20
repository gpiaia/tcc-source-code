import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

train_df = pd.read_csv('../Datasets/AccelData.csv')

median = train_df.median()
mean = train_df.mean()

print('Mediana: {0}'.format(median))
print('Media: {0}'.format(mean))

xx = np.full(len(train_df), median[0])
yy = np.full(len(train_df), median[1])
zz = np.full(len(train_df), median[2])

xm = np.full(len(train_df), mean[0])
ym = np.full(len(train_df), mean[1])
zm = np.full(len(train_df), mean[2])

plt.plot(train_df['x'], label='Vx')
plt.plot(train_df['y'], label='Vy')
plt.plot(train_df['z'], label='Vz')
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
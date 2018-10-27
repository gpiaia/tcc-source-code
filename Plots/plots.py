#scp pi@10.0.0.100:/home/pi/Code/data.csv '/c/Users/Gpiaia/Google Drive/Eng. de Controle e Automacao/TCC/Code/data.csv'
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv('../data.csv')

x = data['kPosicaox']
y = data['kPosicaoy']
z = data['kPosicaoz']
t = data['Tempo'].sub(data['Tempo'][0])

sp = data['SetPointz']
sp[0] = 0

plt.plot(t, x, label='x')
plt.plot(t, y, label='y')
plt.plot(t, z, label='z')
plt.plot(t, sp, label='Referência')
plt.xlabel('Tempo [s]')
plt.ylabel('Posição [°]')
plt.title('Posição Angular em Malha Fechada com Controlador PID Sintonizado via Ziegler-Nichols')
plt.legend(loc=1)
plt.grid(True)
plt.savefig("position.png")
plt.show()

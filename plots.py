# scp pi@10.0.0.102:/home/pi/Code/logs.csv '/c/Users/Gpiaia/Google Drive/Eng. de Controle e Automacao/TCC/Code/logs.csv'
import matplotlib.pyplot as plt
import numpy as np
import csv
# float(row['Tempo'][0])
t = []
x = []
y = []
z = []
sp = []
i = 0

with open('data_PID.csv', 'r') as csvfile:
    plots = csv.DictReader(csvfile, delimiter=',')
    for row in plots:
        y.append(float(row['Posicaoy']))
        x.append(float(row['Posicaox']))
        z.append(float(row['Posicaoz']))
        t.append(float(row['Tempo']) -1539540499.0584)
        if i == 0:
            sp.append(float(0))
        else:
            sp.append(float(45))
        i = i + 1

#plt.plot(t, x, label='x') #t, y, t, z, t, sp)
#plt.plot(t, y, label='y')
plt.plot(t, z, label='z')
plt.plot(t, sp, label='Referência')
plt.xlabel('Tempo [s]')
plt.ylabel('Posição [°]')
plt.title('Posição Angular em Malha Fechada com Controlador PID Sintonizado via Ziegler-Nichols')
plt.legend(loc=3)
plt.grid(True)
plt.savefig("position.png")
plt.show()

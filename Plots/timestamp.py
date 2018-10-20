import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('../Datasets/timestamp_original.csv')


plt.plot(data['gyro'], label='Gyro')
plt.plot(data['quat']-data['gyro'], label='Quaternions')
plt.plot(data['kalm']-data['quat'], label='Kalman Filter')
plt.plot(data['pid']-data['kalm'], label='PID')
plt.plot(data['motor']-data['pid'], label='Motores')
plt.xlabel('Número de Amostras')
plt.ylabel('Tempo [ms]')
plt.title('Tempo de Execução de Cada Tarefa')
plt.legend(loc=3)
plt.grid(True)
plt.savefig("offset.png")
plt.show()
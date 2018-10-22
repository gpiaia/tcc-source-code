#!/usr/bin/python3
#
# Main file for control a Satellite model
# This file use a repo IvPID.
# This file use arepo MPU-6050Python.
# Copyright (C) 2018 Guilherme Piaia . <piaiag@live.com>
#==============================================================================

import time, threading
import numpy as np
from scipy import integrate
from scipy import signal
import pigpio
import csv
import sys
import RPi.GPIO as GPIO
from ivPID import PID
from MPU6050Python.MPU6050 import MPU6050
from kalman import *

#  Rasp Pins
ESC_GPIOz = 12
ESC_GPIOy = 16
ESC_GPIOx = 20

# Pulses Widths
dPW = 30
sPW = 1000
lPW = 90
zG = 4 # Z actuator gain

# Pulses Widths arrays
StopPW = {'x': sPW,               'y': sPW,               'z': sPW} 
HPW    = {'x': sPW + lPW + 2*dPW, 'y': sPW + lPW + 2*dPW, 'z': sPW + lPW + zG*dPW} # Hight Pulse Width
MPW    = {'x': sPW + lPW + dPW,   'y': sPW + lPW + dPW,   'z': sPW + lPW + (zG/2)*dPW} # Average  Pulse Width
LPW    = {'x': sPW + lPW,         'y': sPW + lPW,         'z': sPW + lPW} # low Pulse Width

pidoutput = MPW
pidx = 0
pidy = 0
pidz = 0

loop_init = time.time()

update_pid = 0
SampleTime = 0.04

xdisplacement = 0
ydisplacement = 0
zdisplacement = 0
SetPoint = {'x': 0, 'y': 0, 'z': 0}

# Set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Connect to pigpio
pi = pigpio.pi()

# Create a new instance of the MPU6050 class
sensor = MPU6050(0x68)

kx = Kalman(state_dim=9, obs_dim=3)
ky = Kalman(state_dim=9, obs_dim=3)
kz = Kalman(state_dim=9, obs_dim=3)

# determined by calibration: offset of the gyro; take away to reduce drift.
offset_GYRO = [((-1.5190839694656488 - 1.5155436229394403)/2), 
               (( 0.7938931297709924 + 0.7937952924312573)/2),
               (( 0.2137404580152672 + 0.21279166334853986)/2)]

def RiemannSun(velocity, STime):
    global xdisplacement, ydisplacement, zdisplacement
    xdisplacement += (velocity['x'] - offset_GYRO[0]) * STime
    ydisplacement += (velocity['y'] - offset_GYRO[1]) * STime
    zdisplacement += (velocity['z'] - offset_GYRO[2]) * STime

    return (xdisplacement, ydisplacement, zdisplacement)

def Motors(Pulse, state):
    pi.set_servo_pulsewidth(ESC_GPIOx, int(Pulse['x']))
    if (state == 0) :
        time.sleep(5/1000)
    pi.set_servo_pulsewidth(ESC_GPIOy, int(Pulse['y']))
    if (state == 0) :
        time.sleep(5/1000)
    pi.set_servo_pulsewidth(ESC_GPIOz, int(Pulse['z']))  
    if (state == 0) :
        time.sleep(40/1000)


def PIDController(P, I, D, SetPoint):
    global pidx, pidy, pidz
    pidx = PID.PID(P['x'], I['x'], D['x'])
    pidy = PID.PID(P['y'], I['y'], D['y'])
    pidz = PID.PID(P['z'], I['z'], D['z'])

    pidx.SetPoint = SetPoint['x']
    pidx.setSampleTime(SampleTime)
    pidy.SetPoint = SetPoint['y']
    pidy.setSampleTime(SampleTime)
    pidz.SetPoint = SetPoint['z']
    pidz.setSampleTime(SampleTime)


def mainTask():
    global pidoutput, pidx, pidy, pidz, SetPoint, loop_init
    
    rec_interval = time.time() - loop_init
    loop_init = time.time()

    print(rec_interval*1000)

    Motors(pidoutput, 1)

    gyro_data = sensor.get_gyro_data()
    accel_data = sensor.get_accel_data()

    displacement = RiemannSun(gyro_data, rec_interval)
    
    girox = np.r_[displacement[0], (gyro_data['x']-offset_GYRO[0]), accel_data['x']]
    giroy = np.r_[displacement[1], (gyro_data['y']-offset_GYRO[1]), accel_data['y']]
    giroz = np.r_[displacement[2], (gyro_data['z']-offset_GYRO[2]), accel_data['z']]

    kx.update(girox)
    ky.update(giroy)
    kz.update(giroz)

    kgirox = kx.predict()
    kgiroy = ky.predict()
    kgiroz = kz.predict()

    pidx.update(kgirox[0])
    pidy.update(kgiroy[0])
    pidz.update(kgiroz[0])

    if (pidx.output >= dPW):
        outputx = HPW['x']
    elif (pidz.output < -dPW):
        outputx = LPW['x']
    else:
        outputx = MPW['x'] + pidx.output

    if (pidy.output >= dPW):
        outputy = HPW['x']
    elif (pidy.output < -dPW):
        outputy = LPW['x']
    else:
        outputy = MPW['x'] + pidy.output

    if (pidz.output >= zG*dPW):
        outputz = HPW['x']
    elif (pidz.output < -zG*dPW):
        outputz = LPW['x']
    else:
        outputz = MPW['x'] + pidz.output

    pidoutput = {'x': outputx, 'y': outputy, 'z': outputz}

    with open(r'data.csv', 'a') as csvfile:
        fieldnames = ['Posicaox', 'Posicaoy', 'Posicaoz',
                      'kPosicaox', 'kPosicaoy', 'kPosicaoz',
                      'SetPointx', 'SetPointy', 'SetPointz', 
                      'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                      'Gyrox', 'Gyroy', 'Gyroz',
                      'Tempo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Posicaox': float(displacement[0]),
                         'Posicaoy': float(displacement[1]),
                         'Posicaoz': float(displacement[2]),
                         'kPosicaox': float(kgirox[0]),
                         'kPosicaoy': float(kgiroy[0]),
                         'kPosicaoz': float(kgiroz[0]),
                         'SetPointx': float(SetPoint['x']),
                         'SetPointy': float(SetPoint['y']),
                         'SetPointz': float(SetPoint['z']),
                         'Largura de Pulso x': int(outputx),
                         'Largura de Pulso y': int(outputy),
                         'Largura de Pulso z': int(outputz),
                         'Gyrox' : float(gyro_data['x']),
                         'Gyroy' : float(gyro_data['y']), 
                         'Gyroz' : float(gyro_data['z']),
                         'Tempo': time.time()})

    threading.Timer(0.0001, mainTask).start()

def main():
    argList = sys.argv

    Motors(StopPW, 1)
    if int(argList[5])== 1:  
        time.sleep(1)
        Motors(MPW, 0)

    with open(r'data.csv', 'a') as csvfile:
        fieldnames = ['Posicaox', 'Posicaoy', 'Posicaoz',
                      'kPosicaox', 'kPosicaoy', 'kPosicaoz',
                      'SetPointx', 'SetPointy', 'SetPointz', 
                      'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                      'Gyrox', 'Gyroy', 'Gyroz',
                      'Tempo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    P = {'x': 1, 'y': 1, 'z': float(argList[1])}
    I = {'x': 0, 'y': 0, 'z': float(argList[2])}
    D = {'x': 0, 'y': 0, 'z': float(argList[3])}
    SetPoint = {'x': 0, 'y': 0, 'z': float(argList[4])}
    SetPointInit = {'x': 0, 'y': 0, 'z': 0}

    print('Controle Iniciando em 5s')
    time.sleep(5)

    PIDController(P, I, D, SetPoint)

    mainTask()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Controle Interrompido pelo Usuario')
        Motors(StopPW, 1)
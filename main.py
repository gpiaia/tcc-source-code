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
from Kalman import KalmanAngle

#  Rasp Pins
ESC_GPIOz = 12
ESC_GPIOy = 16
ESC_GPIOx = 20

# Pulses Widths
zG = 2
dPW = 100
sPW = 1000
lPW = 90

# Pulses Widths arrays
StopPW = {'x': sPW,                  'y': sPW,                    'z': sPW} 
HPW    = {'x': sPW + lPW + zG*dPW,   'y': sPW + lPW + zG*dPW,     'z': sPW + lPW + zG*dPW} # Hight Pulse Width
MPW    = {'x': sPW + lPW + 0.45*dPW, 'y': sPW + lPW +  0.45*dPW,  'z': sPW + lPW + dPW} # Average  Pulse Width
LPW    = {'x': sPW + lPW ,           'y': sPW + lPW,              'z': sPW + lPW} # low Pulse Width

pidoutput = MPW
pidx = 0
pidy = 0
pidz = 0

SampleTime = 0.015
loop_init = 0
th = 0

SetPoint = {'x': 0, 'y': 0, 'z': 0}

# Set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Connect to pigpio
pi = pigpio.pi()

# Create a new instance of the MPU6050 class
sensor = MPU6050(0x68)

kalmanX = KalmanAngle()
kalmanY = KalmanAngle()
kalmanZ = KalmanAngle()

kalAngleX = 0
kalAngleY = 0
kalAngleZ = 0

kalmanX.setAngle(kalAngleX)
kalmanY.setAngle(kalAngleY)
kalmanZ.setAngle(kalAngleZ)

# determined by calibration: offset of the gyro; take away to reduce drift.
offset_GYRO = [((-1.5038167938931295-1.499391320990328)/2), 
               ((0.9618320610687024 + 0.9609864992485626)/2),
               ((-0.8702290076335878 -0.8714008716032413)/2)]


def Motors(Pulse, state):
    #pi.set_servo_pulsewidth(ESC_GPIOx, int(Pulse['x']))
    if (state == 0) :
        time.sleep(5)
    #pi.set_servo_pulsewidth(ESC_GPIOy, int(Pulse['y']))
    if (state == 0) :
        time.sleep(5)
    pi.set_servo_pulsewidth(ESC_GPIOz, int(Pulse['z']))  
    if (state == 0) :
        time.sleep(40)


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

    #pidx.setWindup(10)
    #pidy.setWindup(10)
    pidz.setWindup(10)


def mainTask():
    global pidoutput, SetPoint, pidx, pidy, pidz, kalAngleX, kalAngleY, kalAngleZ, loop_init, th

    if(loop_init == 0) :
      dt = SampleTime
    else :
      dt = time.time() - loop_init

    loop_init = time.time()

    Motors(pidoutput, 1)

    gyro_data = sensor.get_gyro_data()

    kalAngleX = kalmanX.getAngle(kalAngleX, (gyro_data['x']-offset_GYRO[0]), dt)
    kalAngleY = kalmanY.getAngle(kalAngleY, (gyro_data['y']-offset_GYRO[1]), dt)
    kalAngleZ = kalmanZ.getAngle(kalAngleZ, (gyro_data['z']-offset_GYRO[2]), dt)

    pidx.update(kalAngleX)
    pidy.update(kalAngleY)
    pidz.update(kalAngleZ)

    outputx = MPW['x'] + pidx.output
    outputy = MPW['y'] + pidy.output
    outputz = MPW['z'] + pidz.output

    if (outputx >= HPW['x']):
        outputx = HPW['x']
    elif (outputx < LPW['x']):
        outputx = LPW['x']

    if (outputy >= HPW['y']):
        outputy = HPW['y']
    elif (outputy < LPW['y']):
        outputy = LPW['y']

    if (outputz >= HPW['z']):
        outputz = HPW['z']
    elif (outputz < LPW['z']):
        outputz = LPW['z']

    pidoutput = {'x': outputx, 'y': outputy, 'z': outputz}

    with open(r'data.csv' , 'a') as csvfile:
        fieldnames = ['kPosicaox', 'kPosicaoy', 'kPosicaoz',
                      'SetPointx', 'SetPointy', 'SetPointz', 
                      'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                      'Gyrox', 'Gyroy', 'Gyroz',
                      'Tempo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'kPosicaox': float(kalAngleX),
                         'kPosicaoy': float(kalAngleY),
                         'kPosicaoz': float(kalAngleZ),
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
    
    #print('PW:' + str(outputx) + ',' + str(outputy) + ',' + str(outputz))
    print('PID:' + str(pidz.output))
    print('Pos z:' + str(kalAngleZ))
    threading.Timer(0.0015, mainTask).start()

def main():
    global SetPoint

    argList = sys.argv

    if int(argList[1])== 1:  
        Motors(StopPW, 1)
        time.sleep(1)
        Motors(MPW, 0)

    with open('data.csv' , 'w') as csvfile:
        fieldnames = ['kPosicaox', 'kPosicaoy', 'kPosicaoz',
                      'SetPointx', 'SetPointy', 'SetPointz', 
                      'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                      'Gyrox', 'Gyroy', 'Gyroz',
                      'Tempo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    # P =            {'x': 4.05, 'y': 1.3,   'z': 2}
    # I =            {'x': 0,    'y': 6.54,  'z': 10.16}
    # D =            {'x': 0,    'y': 0.065, 'z': 0.134}
    # SetPoint =     {'x': 0,    'y': 0,     'z': 45}

    #Classico
    # P =            {'x': 0,  'y': 0,   'z':1.2}
    # I =            {'x': 0,  'y': 0,   'z':10}
    # D =            {'x': 0,  'y': 0,   'z':2.5}
    # SetPoint =     {'x': 0,  'y': 0,   'z': 45}

    #Neural
    # P =            {'x': 0,  'y': 0,   'z':1.2}
    # I =            {'x': 0,  'y': 0,   'z':2}
    # D =            {'x': 0,  'y': 0,   'z':0.25}
    # SetPoint =     {'x': 0,  'y': 0,   'z': 45}

    # P =            {'x': 10,  'y': 10,   'z': 29.19268246562724/10}
    # I =            {'x': 5,  'y': 5,  'z':20.7/10}
    # D =            {'x': 2,  'y': 2,   'z':10.29/10}
    # SetPoint =     {'x': 0,  'y': 0,   'z': 0}


    P =            {'x': 0,  'y': 0,   'z':1.2}
    I =            {'x': 0,  'y': 0,   'z':10}
    D =            {'x': 0,  'y': 0,   'z':2.5}
    SetPoint =     {'x': 0,  'y': 0,   'z': 45}

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
        print(str(pidoutput))

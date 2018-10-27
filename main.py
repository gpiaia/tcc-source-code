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
dPW = 30
sPW = 1000
lPW = 90
zG = 2 # Z actuator gain

# Pulses Widths arrays
StopPW = {'x': sPW,               'y': sPW,               'z': sPW} 
HPW    = {'x': sPW + lPW + 2*dPW, 'y': sPW + lPW + 2*dPW, 'z': sPW + lPW + 2*zG*dPW} # Hight Pulse Width
MPW    = {'x': sPW + lPW + dPW,   'y': sPW + lPW + dPW,   'z': sPW + lPW + zG*dPW} # Average  Pulse Width
LPW    = {'x': sPW + lPW,         'y': sPW + lPW,         'z': sPW + lPW} # low Pulse Width

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
offset_GYRO = [((-1.29007633588 - 1.286599576676129)/2), 
               (( 0.7709923664120001 + 0.7709923664120001)/2),
               (( 0.320610687023 + 0.32110736690888425)/2)]


def Motors(Pulse, state):
    pi.set_servo_pulsewidth(ESC_GPIOx, int(Pulse['x']))
    if (state == 0) :
        time.sleep(5)
    pi.set_servo_pulsewidth(ESC_GPIOy, int(Pulse['y']))
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
    #print('PID:' + str(pidx.output) + ',' + str(pidy.output) + ',' + str(pidz.output))
    #print('Pos:' + str(kalAngleX) + ',' + str(kalAngleY) + ',' + str(kalAngleZ))
    threading.Timer(0.0015, mainTask).start()

def main():
    global SetPoint

    argList = sys.argv

    Motors(StopPW, 1)
    if int(argList[5])== 1:  
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
        print(str(pidoutput))

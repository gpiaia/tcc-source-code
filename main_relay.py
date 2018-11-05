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
zG = 1.75
dPW = 70
sPW = 1000
lPW = 90

# Pulses Widths arrays
StopPW = {'x': sPW,               'y': sPW,                'z': sPW} 
HPW    = {'x': sPW + lPW + zG*dPW,   'y': sPW + lPW + zG*dPW,    'z': sPW + lPW + zG*dPW} # Hight Pulse Width
MPW    = {'x': sPW + lPW + 0.45*dPW,    'y': sPW + lPW + 0.45*dPW,   'z': sPW + lPW + 0.45*dPW} # Average  Pulse Width
LPW    = {'x': sPW + lPW ,              'y': sPW + lPW,               'z': sPW + lPW} # low Pulse Width

pidoutput = MPW
pidx = 0
pidy = 0
pidz = 0

SampleTime = 0.015
loop_init = 0
hys = 5
gain = 10

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
offset_GYRO = [(( -1.4961832061068705 - 1.49196158901234)/2), 
               (( 1.015267175572519 + 1.0198711686928483)/2),
               (( -1.236641221374046 - 1.2385469091787231)/2)]


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

def Relay(kalmanX, kalmanY, kalmanZ):
    global hys, gain
    errx = 45 - kalmanX
    erry = 45 - kalmanY
    errz = 45 - kalmanZ

    if(errx >= hys):
        outputx = gain
    elif(errx < -hys):
        outputx = -gain
    else:
        outputx = errx

    if(erry >= hys):
        outputy = gain
    if(erry < -hys):
        outputy = -gain
    else:
        outputy = erry

    if(errz >= hys):
        outputz = gain
    if(errz < -hys):
        outputz = -gain
    else:
        outputz = errz

    if (outputx >= dPW):
        outputx = HPW['x']
    elif (outputx < -dPW):
        outputx = LPW['x']
    else:
        outputx = MPW['x'] + outputx    

    if (outputy >= dPW):
        outputy = HPW['x']
    elif (outputy < -dPW):
        outputy = LPW['x']
    else:
        outputy = MPW['x'] + outputy

    if (outputz >= zG*dPW):
        outputz = HPW['x']
    elif (outputz < -zG*dPW):
        outputz = LPW['x']
    else:
        outputz = MPW['x'] + outputz

    return {'x': outputx, 'y': outputy, 'z': outputz}


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

    pidoutput = Relay(kalAngleX, kalAngleY, kalAngleZ)

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
                         'Largura de Pulso x': int(pidoutput['x']),
                         'Largura de Pulso y': int(pidoutput['y']),
                         'Largura de Pulso z': int(pidoutput['z']),
                         'Gyrox' : float(gyro_data['x']),
                         'Gyroy' : float(gyro_data['y']), 
                         'Gyroz' : float(gyro_data['z']),
                         'Tempo': time.time()})
    
    print('PID:' + str(pidoutput['x']) + ',' + str(pidoutput['y']) + ',' + str(pidoutput['z']))
    print('Pos:' + str(kalAngleX) + ',' + str(kalAngleY) + ',' + str(kalAngleZ))
    threading.Timer(0.0015, mainTask).start()

def main():
    global SetPoint, hys, gain

    argList = sys.argv

    if int(argList[3])== 1:  
        Motors(StopPW, 1)
        time.sleep(1)
        Motors(MPW, 0)

    hys = float(argList[1])
    gain = float(argList[2])

    with open('data.csv' , 'w') as csvfile:
        fieldnames = ['kPosicaox', 'kPosicaoy', 'kPosicaoz',
                      'SetPointx', 'SetPointy', 'SetPointz', 
                      'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                      'Gyrox', 'Gyroy', 'Gyroz',
                      'Tempo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    Motors(MPW, 1)
    print('Controle Iniciando em 5s')
    time.sleep(5/1000)

    mainTask()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Controle Interrompido pelo Usuario')
        Motors(StopPW, 1)
        print(str(pidoutput))

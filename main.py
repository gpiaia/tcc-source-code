#!/usr/bin/python3
#
# Main file for control a Satellite model
# This file use a repo IvPID.
# This file use arepo MPU-6050Python.
# Copyright (C) 2018 Guilherme Piaia . <piaiag@live.com>
#==============================================================================

import time
import numpy as np
from scipy import integrate
from scipy import signal
import pigpio
import csv
import sys
import RPi.GPIO as GPIO
from ivPID import PID
from MPU6050Python.MPU6050 import MPU6050
from QuaternionIntregration import *
from  Quaternion import *
from kalman import *

#  Rasp Pins
ESC_GPIOz = 12
ESC_GPIOy = 16
ESC_GPIOx = 20

# Pulses Widths
StopPW = {'x': 1000, 'y': 1000, 'z':1000} 
StopPWSD = {'x': 1001, 'y': 1001, 'z':1001} 
HPW    = {'x': 1400, 'y': 1400, 'z':1400} # Hight Pulse Width
LPW    = {'x': 1090, 'y': 1090, 'z':1090} # low Pulse Width

update_pid = 0
SampleTime = 0.01

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
offset_GYRO = [-1.610687, 0.908397, 0.305344]

GYR_Integration_Instance = GYR_Integration(dt=SampleTime, offset_GYRO=offset_GYRO, verbose=3)

def Motors(Pulse):
    pi.set_servo_pulsewidth(ESC_GPIOx, int(Pulse['x']))
    if (Pulse['x']==1000 and Pulse['y']==1000 and Pulse['z']==1000) :
        time.sleep(5)
    pi.set_servo_pulsewidth(ESC_GPIOy, int(Pulse['y']))
    if (Pulse['x']==1000 and Pulse['y']==1000 and Pulse['z']==1000):  
        time.sleep(5)
    pi.set_servo_pulsewidth(ESC_GPIOz, int(Pulse['z']))
    if (Pulse['x']==1000 and Pulse['y']==1000 and Pulse['z']==1000) :   
        time.sleep(40)


def PIDController(P, I, D, SetPoint):

    pidx = PID.PID(P['x'], I['x'], D['x'])
    pidy = PID.PID(P['y'], I['y'], D['y'])
    pidz = PID.PID(P['z'], I['z'], D['z'])

    pidx.SetPoint = SetPoint['x']
    pidx.setSampleTime(SampleTime)
    pidy.SetPoint = SetPoint['y']
    pidy.setSampleTime(SampleTime)
    pidz.SetPoint = SetPoint['z']
    pidz.setSampleTime(SampleTime)

    while update_pid == 0:

        gyro_data = sensor.get_gyro_data()
        accel_data = sensor.get_accel_data()

        #perform one gyro integration: read, update quaternion
        displacement = GYR_Integration_Instance.perform_one_iteration()
        print('Posicao Angular (x, y, z): {0}'.format(displacement))
        
        girox = np.r_[displacement[0], gyro_data['x'], accel_data['x']]
        giroy = np.r_[displacement[1] ,gyro_data['y'], accel_data['x']]
        giroz = np.r_[displacement[2] ,gyro_data['z'], accel_data['x']]

        kx.update(girox)
        ky.update(giroy)
        kz.update(giroz)

        kgirox = kx.predict()
        kgiroy = ky.predict()
        kgiroz = kz.predict()
        
        pidx.update(kgirox[0])
        pidy.update(kgiroy[0])
        pidz.update(kgiroz[0])

        if (pidx.output >= 360):
            outputx = HPW['x']
        elif (pidz.output < 0):
            outputx = StopPWSD['x']
        else:
            outputx = LPW['x'] + pidx.output

        if (pidy.output >= 360):
            outputy = HPW['x']
        elif (pidy.output < 0):
            outputy = StopPWSD['x']
        else:
            outputy = LPW['x'] + pidy.output

        if (pidz.output >= 360):
            outputz = HPW['x']
        elif (pidz.output < 0):
            outputz = StopPWSD['x']
        else:
            outputz = LPW['x'] + pidz.output

        pidoutput = {'x': outputx, 'y': outputy, 'z':outputz} 

        Motors(pidoutput)

        with open(r'data.csv', 'a') as csvfile:
            fieldnames = ['Posicaox', 'Posicaoy', 'Posicaoz',
                          'SetPointx', 'SetPointy', 'SetPointz', 
                          'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                          'Tempo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Posicaox': float(displacement[0]),
                             'Posicaoy': float(displacement[1]),
                             'Posicaoz': float(displacement[2]),
                             'SetPointx': float(SetPoint['x']),
                             'SetPointy': float(SetPoint['y']),
                             'SetPointz': float(SetPoint['z']),
                             'Largura de Pulso x': int(outputx),
                             'Largura de Pulso y': int(outputy),
                             'Largura de Pulso z': int(outputz),
                             'Tempo': time.time()}) 
        time.sleep(SampleTime)

def main():
    argList = sys.argv

    Motors(StopPW)
    if int(argList[5])== 1:  
        time.sleep(2)
        Motors(LPW)

    with open(r'data.csv', 'a') as csvfile:
        fieldnames = ['Posicaox', 'Posicaoy', 'Posicaoz',
                      'SetPointx', 'SetPointy', 'SetPointz', 
                      'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                      'Tempo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    P = {'x': 0.1275, 'y': 0.1275, 'z': float(argList[1])}
    I = {'x': 0.048, 'y': 0.048, 'z': float(argList[2])}
    D = {'x': 0.192, 'y': 0.192, 'z': float(argList[3])}
    SetPoint = {'x': 0, 'y': 0, 'z': float(argList[4])}

    print('Controle Iniciando em 5s')
    time.sleep(5)

    PIDController(P, I, D, SetPoint)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Controle Interrompido pelo Usuario')
        Motors(StopPW)

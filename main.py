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
from QuaternionIntregration import *
from  Quaternion import *
from kalman import *

#  Rasp Pins
ESC_GPIOz = 12
ESC_GPIOy = 16
ESC_GPIOx = 20

# Pulses Widths
StopPW = {'x': 1000, 'y': 1000, 'z':1000} 
LPWP   = {'x': 1090, 'y': 1090, 'z':1090} # low Pulse Width 
HPW    = {'x': 1390, 'y': 1390, 'z':1390} # Hight Pulse Width
MPW    = {'x': 1190, 'y': 1190, 'z':1190} # Mean Pulse Width

update_pid = 0
SampleTime = 0.037

# Set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Connect to pigpio
pi = pigpio.pi()

kx = Kalman(state_dim=9, obs_dim=3)
ky = Kalman(state_dim=9, obs_dim=3)
kz = Kalman(state_dim=9, obs_dim=3)

# determined by calibration: offset of the gyro; take away to reduce drift.
#offset_GYRO = [((-1.601500-1.603053)/2), ((0.884710+0.885496)/2), ((0.328244+0.332608)/2)]
offset_GYRO = [((-1.681646-1.687023)/2), ((0.854962+0.858823)/2), ((0.259542+0.264288)/2)]
GYR_Integration_Instance = GYR_Integration(dt=SampleTime, offset_GYRO=offset_GYRO, verbose=3)

def Motors(Pulse, state):
    #pi.set_servo_pulsewidth(ESC_GPIOx, int(Pulse['x']))
    if (state == 0) :
        time.sleep(5/1000)
    #pi.set_servo_pulsewidth(ESC_GPIOy, int(Pulse['y']))
    if (state == 0) :
        time.sleep(5/1000)
    pi.set_servo_pulsewidth(ESC_GPIOz, int(Pulse['z']))  
    if (state == 0) :
        time.sleep(25/1000)


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

        loop_init = time.time()

        #perform one gyro integration: read, update quaternion
        quat_data = GYR_Integration_Instance.perform_one_iteration()
        
        quattime = int(time.time()*1000.0)- int(loop_init*1000.0)

        girox = np.r_[quat_data[0], quat_data[3], quat_data[6]]
        giroy = np.r_[quat_data[1], quat_data[4], quat_data[7]]
        giroz = np.r_[quat_data[2], quat_data[5], quat_data[8]]

        kx.update(girox)
        ky.update(giroy)
        kz.update(giroz)

        kgirox = kx.predict()
        kgiroy = ky.predict()
        kgiroz = kz.predict()

        kalmanttime = int(time.time()*1000.0)- int(loop_init*1000.0)

        print('Posicao:{0},{1},{2}'.format(quat_data[0], quat_data[1], quat_data[2]))

        pidx.update(kgirox[0])
        pidy.update(kgiroy[0])
        pidz.update(kgiroz[0])

        if (pidx.output >= 180):
            outputx = HPW['x']
        elif (pidz.output < -180):
            outputx = LPWP['x']
        else:
            outputx = MPW['x'] + pidx.output

        if (pidy.output >= 180):
            outputy = HPW['x']
        elif (pidy.output < -180):
            outputy = LPWP['x']
        else:
            outputy = MPW['x'] + pidy.output

        if (pidz.output >= 180):
            outputz = HPW['x']
        elif (pidz.output < -180):
            outputz = LPWP['x']
        else:
            outputz = MPW['x'] + pidz.output

        #print('PID:{0},{1},{2}'.format(pidx.output, pidy.output, pidz.output))

        pidoutput = {'x': outputx, 'y': outputy, 'z':outputz} 

        pidtime = int(time.time()*1000.0)- int(loop_init*1000.0)

        Motors(pidoutput, 1)

        motortime = int(time.time()*1000.0)- int(loop_init*1000.0)
        
        with open(r'data.csv', 'a') as csvfile:
            fieldnames = ['Posicaox', 'Posicaoy', 'Posicaoz',
                          'kPosicaox', 'kPosicaoy', 'kPosicaoz',
                          'SetPointx', 'SetPointy', 'SetPointz', 
                          'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                          'Tempo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Posicaox': float(quat_data[0]),
                             'Posicaoy': float(quat_data[1]),
                             'Posicaoz': float(quat_data[2]),
                             'kPosicaox': float(kgirox[0]),
                             'kPosicaoy': float(kgiroy[0]),
                             'kPosicaoz': float(kgiroz[0]),
                             'SetPointx': float(SetPoint['x']),
                             'SetPointy': float(SetPoint['y']),
                             'SetPointz': float(SetPoint['z']),
                             'Largura de Pulso x': int(outputx),
                             'Largura de Pulso y': int(outputy),
                             'Largura de Pulso z': int(outputz),
                             'Tempo': time.time()})
        writetime = int(time.time()*1000.0)- int(loop_init*1000.0)
        #print('{0},{1},{2},{3}'.format(quattime, kalmanttime, pidtime, motortime, writetime))
        #time.sleep(SampleTime)

def main():
    argList = sys.argv

    Motors(StopPW, 1)
    if int(argList[5])== 1:  
        time.sleep(2/1000)
        Motors(LPWP, 0)

    with open(r'data.csv', 'a') as csvfile:
        fieldnames = ['Posicaox', 'Posicaoy', 'Posicaoz',
                      'kPosicaox', 'kPosicaoy', 'kPosicaoz',
                      'SetPointx', 'SetPointy', 'SetPointz', 
                      'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                      'Tempo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    P = {'x': 1, 'y': 1, 'z': float(argList[1])}
    I = {'x': 0, 'y': 0, 'z': float(argList[2])}
    D = {'x': 0, 'y': 0, 'z': float(argList[3])}
    SetPoint = {'x': 0, 'y': 0, 'z': float(argList[4])}

    print('Controle Iniciando em 10s')
    Motors(MPW, 0)
    time.sleep(10/1000)

    PIDController(P, I, D, SetPoint)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Controle Interrompido pelo Usuario')
        Motors(StopPW, 1)

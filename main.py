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
import RPi.GPIO as GPIO
from ivPID import PID
from MPU6050Python.MPU6050 import MPU6050
from kalman import *
import sys

#  Rasp Pins
ESC_GPIOz = 12
ESC_GPIOy = 16
ESC_GPIOx = 20

# Pulses Widths
StopPW = 1000  # Stop Pulse Width
HPW = 1400  # Hight Pulse Width
LPW = 1090  # low Pulse Width

update_pid = 0
SampleTime = 0.01
PIDUpdateTime = 0.01

xdisplacement = 0
ydisplacement = 0
zdisplacement = 0

# Set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Connect to pigpio
pi = pigpio.pi()

# Create a new instance of the MPU6050 class
sensor = MPU6050(0x68)

kx = Kalman(state_dim=6, obs_dim=2)
ky = Kalman(state_dim=6, obs_dim=2)
kz = Kalman(state_dim=6, obs_dim=2)


def StartMotors():
    pi.set_servo_pulsewidth(ESC_GPIOx, LPW)
    time.sleep(5)
    pi.set_servo_pulsewidth(ESC_GPIOy, LPW)
    time.sleep(5)
    pi.set_servo_pulsewidth(ESC_GPIOz, LPW)
    time.sleep(40)


def StopMotors():
    pi.set_servo_pulsewidth(ESC_GPIOx, StopPW)
    pi.set_servo_pulsewidth(ESC_GPIOy, StopPW)
    pi.set_servo_pulsewidth(ESC_GPIOz, StopPW)


def RiemannSun(velocity, STime):

    global xdisplacement, ydisplacement, zdisplacement

    if ((velocity['x'] >= 1.75) or (velocity['x'] <= -1.75)):
        ydisplacement = ydisplacement + 6 * velocity['x'] * STime

    if ((velocity['y'] >= 1.75) or (velocity['y'] <= -1.75)):
        xdisplacement = xdisplacement + 6 * velocity['y'] * STime

    if ((velocity['z'] >= 0.5) or (velocity['z'] <= -0.5)):
        zdisplacement = zdisplacement + 6 * velocity['z'] * STime

    return {'x': xdisplacement, 'y': ydisplacement, 'z': zdisplacement}


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

        girox = np.r_[gyro_data['x'], time.time()]
        giroy = np.r_[gyro_data['y'], time.time()]
        giroz = np.r_[gyro_data['z'], time.time()]

        kx.update(girox)
        ky.update(giroy)
        kz.update(giroz)

        kgirox = kx.predict()
        kgiroy = ky.predict()
        kgiroz = kz.predict()

        gyro_data_filtred = {'x': kgirox[0], 'y': kgiroy[0], 'z': kgiroz[0]}

        displacement = RiemannSun(gyro_data_filtred, SampleTime)
        pidx.update(displacement['x'])
        pidy.update(displacement['y'])
        pidz.update(displacement['z'])

        if (pidx.output >= 360):
            outputx = HPW
        elif (pidz.output < 0):
            outputx = LPW
        else:
            outputx = LPW + pidx.output

        if (pidy.output >= 360):
            outputy = HPW
        elif (pidy.output < 0):
            outputy = LPW
        else:
            outputy = LPW + pidy.output

        if (pidz.output >= 360):
            outputz = HPW
        elif (pidz.output < 0):
            outputz = StopPW
        else:
            outputz = LPW + pidz.output

        pi.set_servo_pulsewidth(ESC_GPIOx, int(outputx))
        pi.set_servo_pulsewidth(ESC_GPIOy, int(outputy))
        pi.set_servo_pulsewidth(ESC_GPIOz, int(outputz))

        with open(r'data.csv', 'a') as csvfile:
            fieldnames = ['Posicaox', 'Posicaoy', 'Posicaoz',
                          'SetPointx', 'SetPointy', 'SetPointz', 
                          'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                          'Tempo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Posicaox': float(displacement['x']),
                             'Posicaoy': float(displacement['y']),
                             'Posicaoz': float(displacement['z']),
                             'SetPointx': float(SetPoint['x']),
                             'SetPointy': float(SetPoint['y']),
                             'SetPointz': float(SetPoint['z']),
                             'Largura de Pulso x': int(outputx),
                             'Largura de Pulso y': int(outputy),
                             'Largura de Pulso z': int(outputz),
                             'Tempo': time.time()})

        time.sleep(PIDUpdateTime)


def RelayAutoTune():
    t = np.linspace(0, 1, 500, endpoint=False)
    Square = signal.square(2*np.pi*5*t)


def main():
    argList = sys.argv

    StopMotors()
    if int(argList[5])== 1:  
        time.sleep(2)
        StartMotors()

    with open(r'data.csv', 'a') as csvfile:
        fieldnames = ['Posicaox', 'Posicaoy', 'Posicaoz',
                      'SetPointx', 'SetPointy', 'SetPointz', 
                      'Largura de Pulso x', 'Largura de Pulso y', 'Largura de Pulso z',
                      'Tempo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    P = {'x': 1, 'y': 1, 'z': float(argList[1])}
    I = {'x': 0, 'y': 0, 'z': float(argList[2])}
    D = {'x': 0, 'y': 0, 'z': float(argList[3])}
    SetPoint = {'x': 0, 'y': 0, 'z': float(argList[4])}

    print('Controle Iniciando em 5s')
    time.sleep(2)

    PIDController(P, I, D, SetPoint)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Controle Interrompido pelo Usuario')
        StopMotors()

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
import signal
import RPi.GPIO as GPIO
from ivPID import PID
from MPU6050Python.MPU6050 import MPU6050
from kalman import *
import os
#os.system('sudo pigpiod')

#  Rasp Pins
ESC_GPIOz = 12
ESC_GPIOy = 16
ESC_GPIOx = 20

# Pulses Widths
StopPW = 1000 # Stop Pulse Width 
HPW = 1400 # Hight Pulse Width
LPW = 1090 # low Pulse Width

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

kx = Kalman(state_dim = 6, obs_dim = 2)
ky = Kalman(state_dim = 6, obs_dim = 2)
kz = Kalman(state_dim = 6, obs_dim = 2)

def StartMotors() :
    #pi.set_servo_pulsewidth(ESC_GPIOx, LPW) 
    #time.sleep(5)
    #pi.set_servo_pulsewidth(ESC_GPIOy, LPW) 
    #time.sleep(5)
    pi.set_servo_pulsewidth(ESC_GPIOz, LPW) 
    time.sleep(20)

def StopMotors() :
    pi.set_servo_pulsewidth(ESC_GPIOx, StopPW)  
    pi.set_servo_pulsewidth(ESC_GPIOy, StopPW)  
    pi.set_servo_pulsewidth(ESC_GPIOz, StopPW)  

def RiemannSun(velocity, STime):
    
    global xdisplacement, ydisplacement, zdisplacement 

    if ((velocity['x'] >= 0.5) or (velocity['x'] <= -0.5)) :
        xdisplacement = xdisplacement + 6*velocity['x'] * STime

    if ((velocity['y'] >= 0.5) or (velocity['y'] <= -0.5)) :
        ydisplacement = ydisplacement + 6*velocity['y'] * STime
    
    if ((velocity['z'] >= 0.5) or (velocity['z'] <= -0.5)) :
        zdisplacement = zdisplacement + 6*velocity['z'] * STime
        print(velocity['z'])
        print(zdisplacement)
    return {'x': xdisplacement, 'y': ydisplacement, 'z': zdisplacement}


def PIDController(P,  I , D, SetPoint):

    pidz = PID.PID(P, I, D)

    pidz.SetPoint=SetPoint
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
        
        pidz.update(displacement['z'])

        print('Z position: {0} and PID action: {1}'.format(displacement['z'], pidz.output))

        if (pidz.output >= 90):
            output = HPW
        elif (pidz.output < 0):
            output = StopPW
        else :
            output = LPW + 2*pidz.output
        print('Z PulseWidth: {0}'.format(output))
        pi.set_servo_pulsewidth(ESC_GPIOz, int(output))
        time.sleep(PIDUpdateTime)

def RelayAutoTune() :
    t = np.linspace(0, 1, 500, endpoint=False)
    Square = signal.square(2 * np.pi * 5 * t)

def main() :
    StopMotors()
    time.sleep(2)
    StartMotors()
    PIDController(3, 0.01, 0, -90)

if __name__ == "__main__":
       
    try:
        main()
    except KeyboardInterrupt:
        print('Controle Interrompido pelo Usuario')
        StopMotors()
        



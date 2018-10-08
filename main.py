#!/usr/bin/python3
#
# Main file for control a Satellite model
# This file use arepo IvPID.
# Copyright (C) 2018 Guilherme Piaia . <piaiag@live.com>
#==============================================================================

import time
import numpy as np
from scipy import integrate
from scipy import signal
import pigpio
import RPi.GPIO as GPIO
from ivPID import PID
from MPU6050Python.MPU6050 import MPU6050
# Set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Connect to pigpio
pi = pigpio.pi() 

# Create a new instance of the MPU6050 class
sensor = MPU6050(0x68)

#  Rasp Pins
ESC_GPIOz = 12
ESC_GPIOy = 16
ESC_GPIOx = 20

HPulseWidth = 1400
LPulseWidth = 1100
RATPulseWidth = 1200

update_pid = 0
SampleTime = 0.01
PIDUpdateTime = 0.01

xdisplacement = 0
ydisplacement = 0
zdisplacement = 0

pi.set_servo_pulsewidth(ESC_GPIOx, 1000)
pi.set_servo_pulsewidth(ESC_GPIOy, 1000)
pi.set_servo_pulsewidth(ESC_GPIOz, 1000)

def RiemannSun(velocity, STime):
    global xdisplacement, ydisplacement, zdisplacement 
    xdisplacement += xdisplacement + velocity['x'] * STime
    ydisplacement += ydisplacement + velocity['y'] * STime
    zdisplacement += zdisplacement + velocity['z'] * STime

    return {'x': xdisplacement, 'y': ydisplacement, 'z': zdisplacement}

def PIDController(P = 0.2,  I = 0.0, D= 0.0, SetPoint = 30):

    pi.set_servo_pulsewidth(ESC_GPIOx, LPulseWidth)
    pi.set_servo_pulsewidth(ESC_GPIOy, LPulseWidth)
    pi.set_servo_pulsewidth(ESC_GPIOz, LPulseWidth)

    pid = PID.PID(P, I, D)

    pid.SetPoint=SetPoint
    pid.setSampleTime(SampleTime)

    while update_pid == 0:
        
        gyro_data = sensor.get_gyro_data()

        displacement = RiemannSun(gyro_data, SampleTime)
        
        pid.update(displacement['z'])

        print(displacement['z'])

        if (pid.output >= 30):
            output = HPulseWidth
        elif (pid.output < 0):
            output = LPulseWidth
        else :
            output = LPulseWidth + pid.output*10

        pi.set_servo_pulsewidth(ESC_GPIOz, int(output))
        time.sleep(PIDUpdateTime)

def RelayAutoTune() :
    t = np.linspace(0, 1, 500, endpoint=False)
    Square = signal.square(2 * np.pi * 5 * t)


PIDController(1, 0, 0, 35)




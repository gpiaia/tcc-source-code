#!/usr/bin/python3
import time
import pigpio
import RPi.GPIO as GPIO

# Set up BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Connect to pigpio
pi = pigpio.pi() 

# Calibrate ESC
ESC_GPIOz = 12
ESC_GPIOy = 16
ESC_GPIOx = 20

pi.set_servo_pulsewidth(ESC_GPIOx, 2000)
pi.set_servo_pulsewidth(ESC_GPIOy, 2000)
pi.set_servo_pulsewidth(ESC_GPIOz, 2000)

time.sleep(4)

pi.set_servo_pulsewidth(ESC_GPIOx, 1000)
pi.set_servo_pulsewidth(ESC_GPIOy, 1000)
pi.set_servo_pulsewidth(ESC_GPIOz, 1000)


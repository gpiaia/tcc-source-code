#!/usr/bin/python3
import smbus
import math
import time

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def get_z_rotation(x,y,z):
    radians = math.atan2(z, dist(x,y))
    return math.degrees(radians)
 
 
def angular_position():
    bus.write_byte_data(address, 0x3b, 1)

    accelerometer_xout = read_word_2c(0x43)
    accelerometer_yout = read_word_2c(0x45)
    accelerometer_zout = read_word_2c(0x47)

    return (accelerometer_xout, accelerometer_yout,accelerometer_zout)

while 1:
    (a, b, c) = angular_position()
    print('x = {0}'.format(a))
    print('y = {0}'.format(b))
    print('z = {0}'.format(c))
    time.sleep(1)



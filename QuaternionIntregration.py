import numpy as np
import math
from MPU6050Python.MPU6050 import MPU6050
import time

sensor = MPU6050(0x68)

class Quaternion(object):
    """A class for describing a quaternion."""
    def __init__(self, q0=0, q1=0, q2=0, q3=0):
        self.q0 = q0
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3


class Vector(object):
    """A class for describing a vector"""
    def __init__(self, vx=0, vy=0, vz=0):
        self.vx = vx
        self.vy = vy
        self.vz = vz

class GYR_Integration(object):
    def __init__(self, dt, offset_GYRO, verbose=0):
        # Create a new instance of the MPU6050 class
        self.dt = dt
        self.verbose = verbose
        self.Gyro_Data = []
        self.list_measurements = []
        self.offset_GYRO = offset_GYRO

        # initial state: assume resting, Z downwards, still --------------------
        # no rotation to Earth referential
        self.o = normalise_quaternion(Quaternion(1, 0.0001, 0.0001, 0.0001))
        # reference vectors; can be used to print assumed orientation ----------
        self.X_IMU_ref_IMU = Vector(1, 0, 0)
        self.Y_IMU_ref_IMU = Vector(0, 1, 0)
        self.Z_IMU_ref_IMU = Vector(0, 0, 1)
        self.read_and_update_measurement()
        self.cycle = 0

    def predict_state(self):
        """predict quaternion orientation. Use a First order finite difference
        for integration of sensor motion. The integration input is the
        gyroscope signal"""

        qDelta = angular_rate_to_quaternion_rotation(self.wm, self.dt)
        self.o = quaternion_product(self.o, qDelta)

    def read_and_update_measurement(self):
        """Read and update measurement from MPU6050."""

        self.latest_measurement = [sensor.get_gyro_data()['x'], sensor.get_gyro_data()['y'],sensor.get_gyro_data()['z']]
        self.wm = Vector(self.latest_measurement[0] - self.offset_GYRO[0],
                            self.latest_measurement[1] - self.offset_GYRO[1],
                            self.latest_measurement[2] - self.offset_GYRO[2])

        self.list_measurements.append(self.latest_measurement)

    def perform_one_iteration(self):
        """Perform one integration iteration: read, integrate to compute update,
        and print if necessary."""
        loop_init = time.time()
        self.predict_state()
        predtime = int(time.time()*1000.0)- int(loop_init*1000.0)
        self.read_and_update_measurement()
        updatetime = int(time.time()*1000.0)- int(loop_init*1000.0)
        # normalise orientation quaternion: this can be necessary if some noise
        # due to for exemple nearly singular matrix that get inverted
        self.o = normalise_quaternion(self.o)
        normatime = int(time.time()*1000.0)- int(loop_init*1000.0)
        # if self.verbose > 0:
        #     print("PRINT STATE AT END INTEGRATION CYCLE ###")
        pos = self.print_state(self.o)
        printtime = int(time.time()*1000.0)- int(loop_init*1000.0)
        self.cycle += 1
        #print('{0},{1},{2},{3}'.format(predtime, updatetime, normatime, printtime))
        return pos

    def print_state(self, o):
        """Print information about state of the quaternion"""
        rpy = roll_pitch_yaw(o)

        return((180/np.pi)*rpy[0], (180/np.pi)*rpy[1], (180/np.pi)*rpy[2])


def quaternion_product(p, q):
    """p, q are two quaternions; quaternion product."""

    p0 = p.q0
    p1 = p.q1
    p2 = p.q2
    p3 = p.q3

    q0 = q.q0
    q1 = q.q1
    q2 = q.q2
    q3 = q.q3

    r0 = p0 * q0 - p1 * q1 - p2 * q2 - p3 * q3
    r1 = p0 * q1 + p1 * q0 + p2 * q3 - p3 * q2
    r2 = p0 * q2 - p1 * q3 + p2 * q0 + p3 * q1
    r3 = p0 * q3 + p1 * q2 - p2 * q1 + p3 * q0

    r = Quaternion(r0, r1, r2, r3)

    return(r)


def angular_rate_to_quaternion_rotation(w, dt):
    """w is the vector indicating angular rate in the reference frame of the
    IMU, all coords in rad/s
    dt is the time interval during which the angular rate is valid"""

    wx = w.vx
    wy = w.vy
    wz = w.vz

    l = (wx**2 + wy**2 + wz**2)**0.5

    dtlo2 = dt * l / 2

    q0 = np.cos(dtlo2)
    q1 = np.sin(dtlo2) * wx / l
    q2 = np.sin(dtlo2) * wy / l
    q3 = np.sin(dtlo2) * wz / l

    r = Quaternion(q0, q1, q2, q3)

    return(r)


def compute_quaternion_norm(q):
    """q is a quaternion"""

    return((q.q0**2 + q.q1**2 + q.q2**2 + q.q3**2)**0.5)


def normalise_quaternion(q):
    """q is a quaternion"""

    l = compute_quaternion_norm(q)

    return(Quaternion(q.q0 / l, q.q1 / l, q.q2 / l, q.q3 / l))


def roll_pitch_yaw(q):
    """q is a quaternion"""

    x, y, z, w = q.q1, q.q2, q.q3, q.q0
    pitch = math.atan2(2 * y * w - 2 * x * z, 1 - 2 * y * y - 2 * z * z)
    roll = math.atan2(2 * x * w - 2 * y * z, 1 - 2 * x * x - 2 * z * z)
    yaw = math.asin(2 * x * y + 2 * z * w)

    return (roll, pitch, yaw)
from  Quaternion import *
import numpy as np;
from MPU6050Python.MPU6050 import MPU6050

sensor = MPU6050(0x68)

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

        #if self.verbose > 2:
            #print("PRINT NEW STATE ###")
            #self.print_state(self.o)

    def read_and_update_measurement(self):
        """Read and update measurement from MPU6050."""

        self.latest_measurement = [sensor.get_gyro_data()['x'], sensor.get_gyro_data()['y'],sensor.get_gyro_data()['z']]
        self.wm = Vector(self.latest_measurement[0] - self.offset_GYRO[0],
                            self.latest_measurement[1] - self.offset_GYRO[1],
                            self.latest_measurement[2] - self.offset_GYRO[2])

        #if self.verbose > 2:
            #print("Obtained measurements in SI:")
            #print("{0}, {1}, {2}".format((self.latest_measurement[0] - self.offset_GYRO[0]), 
            #                             (self.latest_measurement[1] - self.offset_GYRO[1]), 
            #                             (self.latest_measurement[2] - self.offset_GYRO[2])))

        self.list_measurements.append(self.latest_measurement)

    def perform_one_iteration(self):
        """Perform one integration iteration: read, integrate to compute update,
        and print if necessary."""

        # if self.verbose > 0:
        #     print("\n### NEW CYCLE " + str(self.cycle) + " ###\n")

        self.predict_state()
        self.read_and_update_measurement()

        # normalise orientation quaternion: this can be necessary if some noise
        # due to for exemple nearly singular matrix that get inverted
        self.o = normalise_quaternion(self.o)

        # if self.verbose > 0:
        #     print("PRINT STATE AT END INTEGRATION CYCLE ###")
        pos = self.print_state(self.o)

        self.cycle += 1
        return pos

    def print_state(self, o):
        """Print information about state of the quaternion"""

        current_X_IMU = apply_rotation_on_vector(o, self.X_IMU_ref_IMU)
        current_Y_IMU = apply_rotation_on_vector(o, self.Y_IMU_ref_IMU)
        current_Z_IMU = apply_rotation_on_vector(o, self.Z_IMU_ref_IMU)

        #print("Print state of quaternion --------------------------------------------")

        #print("state orientation: current X, Y, Z of the IMU, in referential Earth:")
        
        xpos = (180/np.pi)*np.arctan2(float(current_Z_IMU.vy), float(current_Y_IMU.vz))
        ypos = (180/np.pi)*np.arctan2(float(current_X_IMU.vy), float(current_Z_IMU.vx)) 
        zpos = (180/np.pi)*np.arctan2(-float(current_Y_IMU.vx), -float(current_X_IMU.vz)) 

        #print("Z angle: {0}".format((180/np.pi)*np.arctan(float(current_X_IMU.vx/current_Z_IMU.vz))))
        #print_vector(current_X_IMU)
        #print_vector(current_Y_IMU)
        #print_vector(current_Z_IMU)

        return(xpos, ypos, zpos)
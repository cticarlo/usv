from machine import Pin, I2C #type: ignore
from bno08x import *
from i2c import BNO08X_I2C


class IMU(object):
    '''
    Define uma classe para gerenciar o uso da IMU BNO08X usando I2C
    '''
    def __init__(self, tl, i2c, r_pin, i_pin, addr=0x4b):
        self.imu = BNO08X_I2C(i2c, address=addr,
                              reset_pin=Pin(r_pin, Pin.OUT),  # BNO sensor (RST)
                              int_pin=Pin(i_pin, Pin.IN))     # BNO sensor (INT)
        self.tl = tl


    def iniciar(self):
        self.imu.linear_acceleration.enable(20) # Atualizações a 20Hz
        self.imu.geomagnetic_quaternion.enable(20)
        self.imu.quaternion.enable(20)


    def atualizar(self):
        try:
            self.imu.update_sensors()
            if self.imu.linear_acceleration.updated:
                self.tl['values']['imu_lacl'][0],\
                self.tl['values']['imu_lacl'][1],\
                self.tl['values']['imu_lacl'][2] = self.imu.linear_acceleration
            if self.imu.geomagnetic_quaternion.updated:
                self.tl['values']['imu_bus'][0],\
                self.tl['values']['imu_bus'][1],\
                self.tl['values']['imu_bus'][2] = self.imu.geomagnetic_quaternion.euler
            if self.imu.quaternion.updated:
                self.tl['values']['imu_orient'][2],\
                self.tl['values']['imu_orient'][1],\
                self.tl['values']['imu_orient'][0] = self.imu.quaternion.euler           
        except Exception as e:
            print ('Falha na leitura da IMU')
            print (e)

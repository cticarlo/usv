from machine import I2C, Pin, Timer # type: ignore
from time import sleep_ms, time #, localtime
# OLED
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB # type: ignore


class displayOLED(object):
    '''
    Gerencia o uso do display OLED
    '''
    def __init__(self, i2c, tl):
        '''
        i2c: barramento i2c a usar com o display
        tl: dicionário padrão com dados de telemetria
        '''
        self.d = SSD1306_I2C(128, 64, i2c)
        self.tl = tl

    def atualizarDisplay(self, q='gps'):
        '''
        Força a atualização do display OLED com os dados disponíveis na telemetria
        q: qual é a atualização ('gps' ou 'imu')
        '''
        self.d.fill(0)
        if q == 'gps':
            if self.tl['values']['gps_sat'] is not None:
                self.d.text(f"{self.tl['values']['gps_sat']:2d}", 1, 1)
            else:        
                self.d.text("--", 1, 1)
            if self.tl['values']['gps_lat'] is not None:
                self.d.text(f"lat:{self.tl['values']['gps_lat']:+10.5f}", 1, 11)
            else:        
                self.d.text("lat:----.-----", 1, 11)
            if self.tl['values']['gps_lon'] is not None:
                self.d.text(f"lon:{self.tl['values']['gps_lon']:+10.5f}", 1, 21)
            else:        
                self.d.text("lon:----.-----", 1, 21)
            if self.tl['values']['gps_vel'] is not None:
                self.d.text(f"v:{self.tl['values']['gps_vel']:5.2f}", 1, 32)
            else:        
                self.d.text("v:--.--", 1, 32)
            if self.tl['values']['gps_cur'] is not None:
                self.d.text(f"v:{self.tl['values']['gps_cur']:6.2f}", 52, 32)
            else:        
                self.d.text(":---.--", 52, 32)
            if self.tl['values']['gps_alt'] is not None:
                self.d.text(f"{self.tl['values']['gps_alt']:6.2f}m", 60,1)
            else:        
                self.d.text("---.--m", 52, 32)
            self.d.text(f"{self.tl['ts']}", 1, 52)
            
        elif q == 'acl':
            self.d.text("IMU - Aceleracao", 1, 1)
            if self.tl['values']['imu_lacl'][0] is not None:
                self.d.text(f"x: {self.tl['values']['imu_lacl'][0]:7.3f}", 1, 10)
            else:
                self.d.text(f"x: ---.---", 1, 10)
            if self.tl['values']['imu_lacl'][1] is not None:
                self.d.text(f"y: {self.tl['values']['imu_lacl'][1]:7.3f}", 1, 20)
            else:
                self.d.text(f"y: ---.---", 1, 20)
            if self.tl['values']['imu_lacl'][2] is not None:
                self.d.text(f"z: {self.tl['values']['imu_lacl'][2]:7.3f}", 1, 30)
            else:
                self.d.text(f"z: ---.---", 1, 30)
        
        elif q == 'bus':
            self.d.text("IMU - Magnetometro", 1, 1)
            if self.tl['values']['imu_bus'][0] is not None:
                self.d.text(f"x: {self.tl['values']['imu_bus'][0]:7.3f}", 1, 10)
            else:
                self.d.text(f"x: ---.---", 1, 10)
            if self.tl['values']['imu_bus'][1] is not None:
                self.d.text(f"y: {self.tl['values']['imu_bus'][1]:7.3f}", 1, 20)
            else:
                self.d.text(f"y: ---.---", 1, 20)
            if self.tl['values']['imu_bus'][2] is not None:
                self.d.text(f"z: {self.tl['values']['imu_bus'][2]:7.3f}", 1, 30)
            else:
                self.d.text(f"z: ---.---", 1, 30)
        
        else:
            self.d.text("IMU - Orientacao", 1, 1)
            if self.tl['values']['imu_orient'][0] is not None:
                self.d.text(f"x: {self.tl['values']['imu_orient'][0]:7.3f}", 1, 10)
            else:
                self.d.text(f"x: ---.---", 1, 10)
            if self.tl['values']['imu_orient'][1] is not None:
                self.d.text(f"y: {self.tl['values']['imu_orient'][1]:7.3f}", 1, 20)
            else:
                self.d.text(f"y: ---.---", 1, 20)
            if self.tl['values']['imu_orient'][2] is not None:
                self.d.text(f"z: {self.tl['values']['imu_orient'][2]:7.3f}", 1, 30)
            else:
                self.d.text(f"z: ---.---", 1, 30)
            
        self.d.show()
   

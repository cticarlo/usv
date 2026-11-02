from machine import I2C, Pin, UART
from time import sleep_ms
# IMU
from bno08x import *
from i2c import BNO08X_I2C
# OLED
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB
#GPS
from micropyGPS import MicropyGPS

i2c0 = I2C(0, scl=Pin(10), sda=Pin(11), freq=400_000)

bno = BNO08X_I2C(i2c0, address=0x4b,
                 reset_pin=Pin(5, Pin.OUT),  # BNO sensor (RST)
                 int_pin=Pin(4, Pin.IN))     # BNO sensor (INT)

oled = SSD1306_I2C(128, 64, i2c0)

# GPS utiliza UART
uart1 = UART(1, baudrate=9600, tx=17, rx=18)
gps = MicropyGPS()

print("Dispositivos encontrados:", [hex(d) for d in i2c0.scan()])

bno.acceleration.enable(100)
bno.print_report_period()

while True:

    oled.fill(0)
    try:
        bno.update_sensors()
        if bno.acceleration.updated:
            accel_x, accel_y, accel_z = bno.acceleration
            #print(f"Ax:{accel_x:+.3f};Ay:{accel_y:+.3f};Az:{accel_z:+.3f}")
            oled.text(f"Ax:{accel_x:+.3f}", 1, 1)
            oled.text(f"Ay:{accel_y:+.3f}", 1, 10)
            oled.text(f"Az:{accel_z:+.3f}", 1, 20)
    except:
        print ('Falha na leitura do BNO080')
        
    try:
        if uart1.any():
            dtGPS = uart1.readline()
            for c in dtGPS:
                gps.update(chr(c)) # Alimenta a biblioteca caractere por caractere
            #print(dtGPS)
            oled.text(f"Lat: {gps.latitude_string()}", 1, 30)
            oled.text(f"Lon: {gps.longitude_string()}", 1, 40)
    except:
        print ('Falha na leitura do GPS')
        
    oled.show()
    sleep_ms(500)
    
    

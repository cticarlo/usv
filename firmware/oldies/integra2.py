import gc
from machine import I2C, Pin, UART, RTC
from time import sleep_ms, localtime
# OLED
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB
# IMU
from bno08x import *
from i2c import BNO08X_I2C
#GPS
from light_nmea import LightNMEA, CST_MASK_GPS


# barramento i2c para display OLED e IMU
i2c0 = I2C(0, scl=Pin(10), sda=Pin(11), freq=400_000)

# configura displayu oled
oled = SSD1306_I2C(128, 64, i2c0)

# Cria o IMU
bno = BNO08X_I2C(i2c0, address=0x4b,
                 reset_pin=Pin(5, Pin.OUT),  # BNO sensor (RST)
                 int_pin=Pin(4, Pin.IN))     # BNO sensor (INT)

# GPS utiliza UART
uart1 = UART(1, baudrate=9600, tx=17, rx=18)
gps = LightNMEA(trust_gga_fix=True) # Confia no fix de msgs GGA
gps.set_cst_filter(CST_MASK_GPS) # Apenas mensagens GPS

# RTC, para manter timestamp da aquisição
rtc = RTC()
sincRTC = False # Assume que o rtc não está sincronizado com o sinal de GPS

gc.threshold(8192)  # Limpa a memória quando ela está baixa
contaGC = 0         # Depois de contaGC operações, força a limpeza de memória


print("Dispositivos encontrados:", [hex(d) for d in i2c0.scan()])

bno.acceleration.enable(100)
bno.print_report_period()

tele = {"satelites": None,
        "latitude": None,
        "longitude": None,
        "velocidade": None,
        "curso": None,
        "altitude": None}

while True:
#     try:
#         bno.update_sensors()
#         if bno.acceleration.updated:
#             accel_x, accel_y, accel_z = bno.acceleration
#             #print(f"Ax:{accel_x:+.3f};Ay:{accel_y:+.3f};Az:{accel_z:+.3f}")
#             oled.text(f"Ax:{accel_x:+.3f}", 1, 1)
#             oled.text(f"Ay:{accel_y:+.3f}", 1, 10)
#             oled.text(f"Az:{accel_z:+.3f}", 1, 20)
#     except:
#         print ('Falha na leitura do BNO080')
        
    try:
        if uart1.any(): # Se há bytes no buffer de entrada
            strGPS = uart1.readline()
            if strGPS and len(strGPS) > 10:
                if gps.parse_line(strGPS) and gps.valid:
                    if gps.has_coordinates():
                        if not sincRTC:
                            # Sincroniza o RTC na primeira aquisição válida
                            try:
                                if gps.date and gps.time:
                                    d = gps.date.decode()
                                    t = gps.time.decode()
                                    rtc.datetime((2000 + int(d[4:6], 10),
                                                  int(d[2:4], 10),
                                                  int(d[0:2], 10), 0,
                                                  int(t[0:2], 10),
                                                  int(t[2:4], 10),
                                                  int(t[4:6], 10), 0))
                                    sincRTC = True
                            except ValueError as e:
                                print ('Problemas ao decodificar timestamp')
                                
                        tele['satelites'] = gps.satellites
                        tele['latitude'] = gps.latitude
                        tele['longitude'] = gps.longitude
                                
                    if gps.has_navigation():
                        tele['velocidade'] = gps.speed
                        tele['curso'] = gps.course
                        
                    if gps.has_3d_fix():
                        tele['altitude'] = gps.altitude
                
                # A cada 500 pacotes, força a limpeza da memória
                contaGC += 1
                if contaGC >= 500:
                    gc.collect()
                    contaGC = 0
    except Exception as e:
        print (e)
        print('Problemas com GPS')
    
    oled.fill(0)
    oled.text(f"{tele['satelites'] if tele['satelites'] is not None else '--'}", 1, 1)
    oled.text(f"{tele['latitude'] if tele['latitude'] is not None else '-----.-----'}", 1, 11)
    oled.text(f"{tele['longitude'] if tele['longitude'] is not None else '-----.-----'}", 1, 21)
    oled.text(f"{tele['velocidade'] if tele['velocidade'] is not None else '---.--'};{tele['curso'] if tele['curso'] is not None else '---.--'}", 1, 32)
    oled.text(f"{tele['altitude'] if tele['altitude'] is not None else '---.--'}", 80, 1)    
    oled.show()
    sleep_ms(1500)
    
    

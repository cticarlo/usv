import gc
from machine import Pin, UART, RTC
from time import sleep_ms, localtime
from light_nmea import LightNMEA, CST_MASK_GPS

# GPS utiliza UART
uart1 = UART(1, baudrate=9600, tx=17, rx=18, rxbuf=512)

# RTC, para manter timestamp da aquisição
rtc = RTC()
sincRTC = False # Assume que o rtc não está sincronizado com o sinal de GPS

gc.threshold(8192)  # Limpa a memória quando ela está baixa
contaGC = 0         # Depois de contaGC operações, força a limpeza de memória

parserNMEA = LightNMEA(trust_gga_fix=True) # Confia no fix de msgs GGA
parserNMEA.set_cst_filter(CST_MASK_GPS) # Apenas mensagens GPS


while True:
    if uart1.any(): # Se há bytes no buffer de entrada
        strGPS = uart1.readline()
        if strGPS and len(strGPS) > 10:
            if parserNMEA.parse_line(strGPS):
                if parserNMEA.valid:
                    if parserNMEA.has_coordinates():
                        if not sincRTC:
                            # Sincroniza o RTC na primeira aquisição válida
                            try:                            
                                d = parserNMEA.date.decode()
                                t = parserNMEA.time.decode()
                                print (d)
                                print (t)
                                rtc.datetime((2000 + int(d[4:6], 10),
                                              int(d[2:4], 10),
                                              int(d[0:2], 10), 0,
                                              int(t[0:2], 10),
                                              int(t[2:4], 10),
                                              int(t[4:6], 10), 0))
                                sincRTC = True
                            except ValueError as e:
                                print ('Problemas ao decodificar timestamp')
                                
                        print(f"Latitude: {parserNMEA.latitude:+9.4f}")
                        print(f"Longitude: {parserNMEA.longitude:+9.4f}")
                        print(f"Satélites: {parserNMEA.satellites:.2d}")
                        
                    if parserNMEA.has_navigation():                        
                        print(f"Orientação: {parserNMEA.course:6.2f}deg")
                        print(f"Velocidade: {parserNMEA.speed:6.2f}km/h")
                        
                    if parserNMEA.has_3d_fix():
                        print(f"Altitude: {parserNMEA.altitude:.4f}m")
                        
                    print(f"ts: {localtime()}")
                
                # A cada 500 pacotes, força a limpeza da memória
                contaGC += 1
                if contaGC >= 500:
                    gc.collect()
                    contaGC = 0
    
    sleep_ms(500)


        

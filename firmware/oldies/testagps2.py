from machine import UART
from micropyGPS import MicropyGPS
from time import sleep_ms

# Configuração UART com pinos do ESP32
uart = UART(1, baudrate=9600, tx=17, rx=18)

gps = MicropyGPS()

while True:
    if uart.any():
        dados = uart.readline()
        for caractere in dados:
            gps.update(chr(caractere)) # Alimenta a biblioteca caractere por caractere
            
        # Lendo os dados já convertidos:
        print(dados)
        print(f"Latitude: {gps.latitude_string()}")
        print(f"Longitude: {gps.longitude_string()}")
        print(f"Velocidade: {gps.speed[2]} km/h")
    sleep_ms(1000)

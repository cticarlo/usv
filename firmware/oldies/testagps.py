from machine import UART
from time import sleep_ms

# Configura a UART2 no ESP32: baudrate padrão do NEO-6M é 9600 bps
gps_serial = UART(1, baudrate=9600, tx=17, rx=18)

print("Aguardando dados do GPS NEO-6M...")

while True:
    if gps_serial.any():
        # Lê a linha de dados vinda do GPS
        dados = gps_serial.readline()
        # Decodifica os bytes para texto (string)
        sentenca = dados.decode('utf-8')
        print(sentenca.strip())
    sleep_ms(100)
    

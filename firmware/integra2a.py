import gc
from machine import I2C, Pin, Timer # type: ignore
from time import sleep_ms, time #, localtime

# Definição dos dados de telemetria
from usvteledata import tl

# Display OLED
from usvdisplay import displayOLED

# GPS
from usvgps import GPS

# IMU
from usvimu import IMU

# barramento i2c para display OLED e IMU
i2c0 = I2C(0, scl=Pin(10), sda=Pin(11), freq=400_000)

# Cria o display OLED
oled = displayOLED(i2c0, tl)

# IMU -> classe que automatiza o processamento dos dados da IMU
imu = IMU(tl, i2c0, Pin(5, Pin.OUT), Pin(4, Pin.IN))

# GPS -> classe que automatiza o processamento do sensor GPS
gps = GPS(tl, uart=1, bps=9600, tx=17, rx=18)

# Timers para usos diversos
tim = Timer(0)
tdsp = Timer(1)

# Sobre o RTC
sincRTC = False # Assume que o rtc não está sincronizado com o sinal de GPS

def atualizarRTC(t):
    '''
    Força a atualização do RTC em um intervalo padrão (1h, no momento)
    '''
    global sincRTC
    sincRTC = False

# Sobre a limpeza de memória
gc.threshold(8192)  # Limpa a memória quando ela está baixa

#print("Dispositivos encontrados:", [hex(d) for d in i2c0.scan()])

# Display circular
tela = 0
telaopts = ['gps', 'acl', 'bus', 'euler']


def atualizarTela(t):
    global tela
    
    tela = (tela+1)%4


tdsp.init(mode=Timer.PERIODIC, period=3000, callback=atualizarTela)

imu.iniciar()

while True:    
    # Utilização do GPS
    if not sincRTC:
        sincRTC = gps.atualizarRTC()
        if sincRTC:
            tim.init(mode=Timer.ONE_SHOT, period=3_600_000, callback=atualizarRTC)
    else:
        gps.atualizar()                    

    # Utilização da IMU
    imu.atualizar()

    # Atualização do timestamp
    tl['ts'] = (time() + 946_684_800)*1000 # Compensa 30 anos de offset entre epochs

    oled.atualizarDisplay(q=telaopts[tela])
    sleep_ms(1000)
    
    

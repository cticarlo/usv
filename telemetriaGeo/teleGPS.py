from machine import I2C, Pin, Timer # type: ignore
from time import sleep_ms
from network import WLAN
from espnow import ESPNow

# Definição dos dados de telemetria
from usvteledata import tl
# GPS
from usvgps import GPS
gps = GPS(tl, uart=1, bps=9600, tx=1, rx=0)

rede = WLAN(WLAN.IF_STA)
rede.active(True)
rede.config(txpower=5)

# Inicialização do ESPNow
sens = ESPNow()
sens.active(True)

helm = b'\x34\x85\x18\x42\xed\x58'
sens.add_peer(helm)      # Must add_peer() before send()


# Timers para usos diversos
tim = Timer(0)

def atualizarRTC(t):
    '''
    Força a atualização do RTC em um intervalo padrão (1h, no momento)
    '''
    global sincRTC
    sincRTC = False


# Sobre o RTC
sincRTC = False # Assume que o rtc não está sincronizado com o sinal de GPS


while True:
    # Utilização do GPS
    if not sincRTC:
        valido = sincRTC = gps.atualizarRTC()
        if sincRTC:
            tim.init(mode=Timer.ONE_SHOT, period=3_600_000, callback=atualizarRTC)
    else:
        valido = gps.atualizar()

    if valido:
        sens.send(helm, gps.nmea)
        print (gps.nmea)
    sleep_ms(100)

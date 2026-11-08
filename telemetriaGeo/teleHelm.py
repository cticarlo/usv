from machine import Pin
from network import WLAN
from espnow import ESPNow

from time import sleep_ms

rede = WLAN(WLAN.IF_STA)
rede.active(True)


nav = ESPNow()
nav.active(True)

while True:
    for mac, msg in nav:
        try:
            print (msg)
        except OSError as err:
            print("")
            sleep_ms(100)
        except AttributeError as err:
            print(f"{mac}:{msg}")
            sleep_ms(100)

from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

cores = ((255, 0, 0),
         (0, 255, 0),
         (0, 0, 255),
         (255, 255, 0),
         (255, 0, 255),
         (0, 255, 255),
         (255, 128, 0),
         (128, 255, 0),
         (255, 0, 128),
         (128, 0, 255),
         (0, 255, 128),
         (0, 128, 255),
         (255, 255, 255))


pin = Pin(48, Pin.OUT)
np = NeoPixel(pin, 1)   # create NeoPixel driver on GPIO0 for 8 pixels

for c in cores:
    np[0] = c
    np.write()
    sleep_ms(750)
    
np[0]=(0,0,0)
np.write()
print ('foi')
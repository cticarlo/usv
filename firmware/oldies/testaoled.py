from machine import I2C, Pin
from time import sleep_ms
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB


i2c0 = I2C(0, scl=Pin(10), sda=Pin(11), freq=400_000)

oled = SSD1306_I2C(128, 64, i2c0)



vez = 0

while True:
    vez += 1
    oled.fill(0)
    oled.text(f'{vez:3d}', 10, 10)
    oled.show()
    sleep_ms(1000)
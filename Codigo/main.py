from library.hx711 import HX711
from library.ssd1306 import SSD1306_I2C
from library.dht11 import DHT11, InvalidChecksum
from machine import Pin, I2C
import utime as time

# GPIO 8	i2c0_sda_pin
# GPIO 9	i2c0_slc_pin
# GPIO 18	clock_pin
# GPIO 19	data_pin
# GPIO 28	DHT11

led1 = Pin(2, Pin.OUT)
led2 = Pin(3, Pin.OUT)
led3 = Pin(4, Pin.OUT)

i2c0_slc_pin = 7
i2c0_sda_pin = 6
i2c0 = I2C(1, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=400000)
display = SSD1306_I2C(128, 32, i2c0)

sensor = DHT11(Pin(22, Pin.OUT, Pin.PULL_DOWN))

data_pin = Pin(19, Pin.IN, pull=Pin.PULL_DOWN)
clock_pin = Pin(18, Pin.OUT)
hx711 = HX711(clock_pin, data_pin)
hx711.tare()


while True:
    t  = (sensor.temperature)
    
    raw_wt = hx711.read()
    sf = 3880/350000 * 1.3
    weight = raw_wt*sf
    if (weight > 400):
        led1.on()
        led2.off()
        led3.off()
    elif (weight > 250):
        led1.off()
        led2.on()
        led3.off()
    else:
        led1.off()
        led2.off()
        led3.on()
    if (weight < 0):
        weight = 0    
    display.fill(0)
    display.text("Temp.: {:.1f}C".format(sensor.temperature), 0, 0, 1)
    display.text("Peso: {:.0f} g".format(weight), 0, 20, 1)
    display.show()
    
    time.sleep(2)

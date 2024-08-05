import adafruit_bh1750
import board
from gpiozero import LED

# Get LED
led = LED(26)  # pin 37 (GPIO26)
funnel = LED(12)  # pin 32 (GPIO12)

LIGHT_THRESHOLD = 20  # lux


def LEDon_chamber():
    led.on()


def LEDoff_chamber():
    led.off()


def LEDon_funnel():
    funnel.on()


def LEDoff_funnel():
    funnel.off()


def getLight():
    i2c = board.I2C()
    sensor = adafruit_bh1750.BH1750(i2c)
    return round(sensor.lux, 2)


def manageLight():
    if getLight() < LIGHT_THRESHOLD:
        LEDon_chamber()
        LEDon_funnel()
    else:
        LEDoff_chamber()
        LEDoff_funnel()


def exit():
    LEDoff_chamber()
    LEDoff_funnel()

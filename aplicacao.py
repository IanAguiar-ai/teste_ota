#Código teste OTA

version = [0, 1, 0]
def main_principal():
    from machine import Pin, UART
    from time import sleep

    led = Pin(2, Pin.OUT)
    led.on()

    n = 0
    while n < 10:
        n += 1
        sleep(3)
        led.on()
        sleep(3)
        led.off()

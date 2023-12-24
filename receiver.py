import network
import espnow
from machine import Pin
from time import sleep

#b'\xe4e\xb8\x13Kx'

def pisca(led, v:int = 3):
    for _ in range(v):
        led.on()
        sleep(0.3)
        led.off()
        sleep(0.3)
    sleep(1)

if __name__ == "__main__":
    led = Pin(2, Pin.OUT)
    
    pisca(led, v = 15)
    
    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    print(f"MAC: {sta.config('mac')}")

    e = espnow.ESPNow()
    e.active(True)

    while True:
        host, msg = e.recv()
        if msg:             # msg == None if timeout in recv()
            print(host, msg)
            if msg == b'end':
                break

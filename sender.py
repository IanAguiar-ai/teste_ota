import network
import espnow
from machine import Pin
from time import sleep

#b'\xe4e\xb8\x13Kx' <- connect

#b'\xd4\x8a\xfc\x9d\xdbl'

def pisca(led, v:int = 3):
    for _ in range(v):
        led.on()
        sleep(0.3)
        led.off()
        sleep(0.3)
    sleep(1)

if __name__ == "__main__":
    led = Pin(2, Pin.OUT)
    
    pisca(led)   
    
    sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
    sta.active(True)
    print(f"MAC: {sta.config('mac')}")
    
    pisca(led,2)

    e = espnow.ESPNow()
    e.active(True)
    peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'
    e.add_peer(peer)

    pisca(led,3)

    e.send(peer, "Starting...")
    for i in range(100):
        e.send(peer, str(i)*20, True)
    e.send(peer, b'end')

#Código teste OTA

from OTA_esp32 import ota
from time import sleep
from wifi_esp32 import Wifi

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    
    sta_if.active(True)
    if sta_if.isconnected():
        sta_if.disconnect()
        print (f'started in the connected state, but now disconnected')
        sleep(1)
    else:
        print (f'started in the disconnected state')
    
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ota', 'otateste')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

if __name__ == "__main__":
    print("Ligando")
    wifi = Wifi("ota", "otateste")
    wifi.connect_continuos()
    print(" (OK)")
    print("OTA", end = "")
    ota("https://github.com/IanAguiar-ai/teste_ota/blob/main/aplicacao.py")
    print(" (OK)")
    print("import", end = "")
    from aplicacao import main_principal as mp
    print(" (OK)")
    print("Executando programa", end = "")
    mp()
    print(" (OK)")
        

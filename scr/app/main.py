#Código teste OTA

#Código teste OTA

from ota_updater import OTAUpdater
from time import sleep
import network

def download_and_install_update_if_available():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('ota', 'otateste')
    while not sta_if.isconnected():
        pass

    sleep(1)
    o = OTAUpdater('https://github.com/rdehuyss/chicken-shed-mgr', github_src_dir='scr', main_dir='app')
    o.install_update_if_available_after_boot('ota', 'otateste')


def start():
    from aplicacao import main_principal
    main_principal()


def boot():
    download_and_install_update_if_available()
    start()

print("Ligando")
sleep(0.5)
boot()
print("Feito")
        
        

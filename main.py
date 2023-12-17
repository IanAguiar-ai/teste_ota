#Código teste OTA

from ota_updater import OTAUpdater
from time import sleep

def download_and_install_update_if_available():
    o = OTAUpdater('https://github.com/IanAguiar-ai/teste_ota')
    o.install_update_if_available_after_boot('ota', 'otateste')


def start():
    from aplicacao import main_principal
    main_principal()


def boot():
    download_and_install_update_if_available()
    start()

print("Ligando")
sleep(1)
boot()
print("Feito")

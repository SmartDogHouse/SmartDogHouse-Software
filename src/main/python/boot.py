import sys
import machine
import gc
import esp
import webrepl
import secret
import time
import network

WIFI_SSID = secret.WIFI_SSID
WIFI_PW = secret.WIFI_PW


# This file is executed on every boot (including wake-boot from deepsleep)
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PW)
        while not sta_if.isconnected():
            time.sleep(1)
            print(".", end='')
    print('Network config:', sta_if.ifconfig())


network.WLAN(network.AP_IF).active(False)
sys.path.reverse()
machine.freq(240000000)
gc.enable()
esp.osdebug(None)
webrepl.start()
gc.collect()
do_connect()

### NOTES MICROPYTHON
 - Connect ESP32

if using VirtualBox:
 - VirtualBox -> Settings -> Usb -> Add "SiliconLabs ..." (or the Usb of the ESP)
 - in Ubuntu (or the OS emulated), on the top: Devices -> Usb -> Select it

 - check if you can see it with command ```ls /dev/ttyU*```

#### install esptool
sudo pip3 install esptool
#### esptool is used to flash the ESP's memory (press "BOOT" on ESP if stuck on "connecting..--....--..")
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
#### micropython is a python firmware for microcontrollers, download it 
wget https://micropython.org/resources/firmware/esp32-20210618-v1.16.bin
#### use esp tool to flash it on the ESP
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20210618-v1.16.bin 

#### install ampy, it's used to move files in the ESP
pip3 install adafruit-ampy
#### take the files you need, modify main.py with your WiFi's SSID & password, add cerficates and secrets
#### move them inside with ampy, es
ampy -d 1 --port /dev/ttyUSB0 put src/main/python/boot.py
ampy -d 1 --port /dev/ttyUSB0 put src/main/python/main.py
ampy -d 1 --port /dev/ttyUSB0 put src/main/python/water_sensor.py
#### __please don't upload file "machine.py" it's a stub to make the files work with normal python__

#### picocom is used to get python REPL of the  ESP 
#### ctrl+c to access the REPL
#### (esc with ctrl+a+x) (/!\ when open blaocks ampy) 
picocom /dev/ttyUSB0 -b 115200

#### test working 
from water_sensor import WaterSensor

ws=WaterSensor(33)

ws.measure()

ws.get_last_measure()

#### press RST, wait "Connecting Wifi" and check the IP

#### clone webrepl, it's used to move files like ampy, but it doesn't get stuck by picocom
git clone https://github.com/micropython/webrepl
#### to push file main.py, substitute also the IP
./webrepl_cli.py -p cam ../main.py 192.168.1.208:/main.py

### BASH SCRIPTS
#### to fast forward flashing memory and upload firmware on your ESP you can use
bash upload_firmware.sh
#### to fast forward moving files to your ESP you can use
bash upload_folder_files.sh 
#### it doesn't upload file "machine.py", the stub to make the files work with normal python

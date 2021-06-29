# SmartDogHouse-Software

CodeFactor: [![CodeFactor](https://www.codefactor.io/repository/github/smartdoghouse/smartdoghouse-software/badge)](https://www.codefactor.io/repository/github/smartdoghouse/smartdoghouse-software)

Codacy: [![Codacy Badge](https://app.codacy.com/project/badge/Grade/2b0b479212d047058a885b6f4ee8602e)](https://www.codacy.com/gh/SmartDogHouse/SmartDogHouse-Software/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SmartDogHouse/SmartDogHouse-Software&amp;utm_campaign=Badge_Grade)

SonarCloud: [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=SmartDogHouse_SmartDogHouse-Software&metric=alert_status)](https://sonarcloud.io/dashboard?id=SmartDogHouse_SmartDogHouse-Software)

## Run Tests
inside project folder <br> 
### without coverage
```bash
python -m src.test.python.test_water_sensor #single test
```
```bash
python -m unittest discover -s ./src/test/ #all tests
```
### with coverage
```bash
pip install coverage
```
all tests:
```bash
coverage run -m unittest discover -s ./src/test/
```
create report:
```bash
coverage report	        #report in shell
coverage html		#report website, open index.html in htmlcov folder
```


## INSTALLATION
### MICROPYTHON
 - Connect ESP32 (you need a device)
 - check if you can see it with command ```ls /dev/ttyU*```

if using VirtualBox:
 - VirtualBox -> Settings -> Usb -> Add "Usb name of the ESP"
 - in Ubuntu (or the OS emulated), on the top: Devices -> Usb -> Select it


#### install esptool
```bash
sudo pip3 install esptool
```

#### esptool is used to flash the ESP's memory (press "BOOT" on ESP if stuck on "connecting..--....--..")
```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
```

#### micropython is a python firmware for microcontrollers, download it 
```bash
wget https://micropython.org/resources/firmware/esp32-20210618-v1.16.bin
```

#### use esptool to flash it on the ESP
```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20210618-v1.16.bin
``` 
### Ampy, Moving files to ESP
#### install ampy, it's used to move files in the ESP
```bash
pip3 install adafruit-ampy
```

#### take the files you need, modify main.py with your WiFi's SSID & password, add cerficates and secrets
#### move them inside with ampy, es
```bash
ampy -d 1 --port /dev/ttyUSB0 put src/main/python/boot.py
ampy -d 1 --port /dev/ttyUSB0 put src/main/python/main.py
ampy -d 1 --port /dev/ttyUSB0 put src/main/python/water_sensor.py
```
 _Careful! in the code folder there are some stubs that shouldn't be uploaded to your esp, 
 use the [bash script](bash-scripts) in the folder if you want to upload the files of this project.
 Stubs are used to make the tests work with normal python installation_

### Picocom (reach the REPL of MicroPython in the ESP)
#### picocom is used to use micropython REPL running the ESP 
#### ctrl+c to access the REPL
#### (esc with ctrl+a+x) (/!\ when it's open, it blocks ampy) 
```bash
picocom /dev/ttyUSB0 -b 115200
```

#### test working with python REPL
```
from water_sensor import WaterSensor

ws=WaterSensor(33)

ws.measure()

ws.get_last_measure()
```
#### IP of the ESP: press RST, wait "Connecting WiFi" and check the IP,

### WebREPL
#### (optional) if you want to upload files using the REPL meanwhile you can use this instead of ampy
#### clone webrepl, it's used to move files like ampy, but it doesn't get stuck by picocom
```bash
git clone https://github.com/micropython/webrepl
```
#### to push file main.py, substitute also the IP
```bash
./webrepl_cli.py -p cam ../main.py 192.168.1.208:/main.py
```

## BASH SCRIPTS
#### To fast forward flashing memory and upload firmware on your ESP you can use
```bash
bash upload_firmware.sh
```

#### To fast forward moving files in python folder to your ESP you can use
```bash
bash src/main/python/upload_folder_files.sh 
```
it is safe, it doesn't upload stub files like "machine.py", the stub to make the files work with normal python

#### To fast forward moving key and cert to your ESP you can use
```bash
bash src/main/python/flash/upload_key_cert.sh 
```


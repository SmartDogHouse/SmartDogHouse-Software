#!/bin/bash
DEVICE=$(ls /dev/ttyU*) #find devices usb
if [[ $DEVICE ]]
then
	echo "found device: $DEVICE"
	read -p "Wanna Upload files to $DEVICE [y/n]?" -n 1 -r
	echo    # (optional) moves to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then

		echo --Downloading Firmware
		wget https://micropython.org/resources/firmware/esp32-20210623-v1.16.bin
		echo --Erasing Flash, --Press boot on ESP if stuck on connecting--
		esptool.py --chip esp32 --port "$DEVICE" erase_flash
		echo --Writing Firmware
		esptool.py --chip esp32 --port "$DEVICE" write_flash -z 0x1000 esp32-20210623-v1.16.bin
		echo --Removing Download
		rm esp32-20210618-v1.16.bin
		echo --Done!
	fi
else 
	echo device not found
fi

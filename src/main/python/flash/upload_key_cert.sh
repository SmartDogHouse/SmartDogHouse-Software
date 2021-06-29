#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" #directory script is located
DEVICE=$(ls /dev/ttyU*) #find devices usb
if [[ $DEVICE ]]
then
	echo "found device: $DEVICE"
	read -p "Wanna Upload files to $DEVICE [y/n]?" -n 1 -r
	echo    #moves to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
		ampy -d 1 --port /dev/ttyUSB0 mkdir flash
		ampy -d 1 --port /dev/ttyUSB0 put "$SCRIPT_DIR"/key /flash/key
		ampy -d 1 --port /dev/ttyUSB0 put "$SCRIPT_DIR"/cert /flash/cert
	fi
else 
	echo device not found
fi

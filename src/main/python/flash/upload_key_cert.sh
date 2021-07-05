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
	  #check existing directory
	  DIR_EXISTS=$(ampy -d 1 --port "$DEVICE" ls | grep /flash )
	  if [[ -n "$DIR_EXISTS" ]]
    then
        echo "The folder exists, will be deleted before."
        ampy -d 1 --port "$DEVICE" rmdir /flash
        echo "Deleted."
    fi
		ampy -d 1 --port "$DEVICE" mkdir flash
    echo "Putting key."
		ampy -d 1 --port "$DEVICE" put "$SCRIPT_DIR"/key /flash/key
    echo "Putting cert."
		ampy -d 1 --port "$DEVICE" put "$SCRIPT_DIR"/cert /flash/cert
	fi
else 
	echo device not found
fi

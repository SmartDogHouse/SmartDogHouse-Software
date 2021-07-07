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
		#find files in path (if you change path remember to change all paths of the stubs ignored)
		for f in "$SCRIPT_DIR"/*.py; do #for all files python, in script directory
			test "$f" = "$SCRIPT_DIR"/machine.py && continue #exept stub
			test "$f" = "$SCRIPT_DIR"/micropython.py && continue #exept stub
			test "$f" = "$SCRIPT_DIR"/utime.py && continue #exept stub
			test "$f" = "$SCRIPT_DIR"/uasyncio.py && continue #exept stub
			echo "Delivering file: $f"
			ampy -d 1 --port "$DEVICE" put "$f" #deliver file with ampy in the device fond
		done
		#fast alternative to ignore only one file
		#find .  -maxdepth 1 -type f ! -name machine.py -exec echo {} \;
	fi
else 
	echo device not found
fi

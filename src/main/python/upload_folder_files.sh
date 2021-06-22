#!/bin/bash
DEVICE=$(ls /dev/ttyU*) #find devices usb
if [[ $DEVICE ]]
then
	echo found device: $DEVICE
	read -p "Wanna Upload files to $DEVICE [y/n]?" -n 1 -r
	echo    # (optional) moves to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
		#find files in path (remember to change also path of machine.py)
		for f in ./*.py; do #for all files python
			test "$f" = ./machine.py && continue #exept machine.py
			echo "Delivering file: $f"
			ampy -d 1 --port $DEVICE put $f #deliver file with ampy in the device fond
		done
		#fast alternative
		#find .  -maxdepth 1 -type f ! -name machine.py -exec echo {} \;
	fi
else 
	echo device not found
fi

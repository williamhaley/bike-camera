#!/usr/bin/env bash

# Disable HDMI to save power
# This could be in /etc/rc.local, but it is in this script as a convenience.
/usr/bin/tvservice -o

# Run record script at boot
python3 /home/pi/bike-camera/record.py &

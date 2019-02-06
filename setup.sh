#!/usr/bin/env bash

[[ $(id -u) = 0 ]] || { echo "must be root"; exit 1; }

# Install essential software
apt-get install python3-picamera python3-numpy

#  Set the timezone to Chicago
ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime
dpkg-reconfigure -f noninteractive tzdata

# Prepare a directory for storing videos
mkdir -p /videos && chown pi:pi /videos

# Disable non-essential services
systemctl disable hciuart
systemctl disable bluetooth
systemctl disable cron

# Enable the camera
raspi-config nonint do_camera 0

# Disable the LEDs to save power

# Disable the ACT LED on the Pi Zero
## Delete any existing configs for the LED first
sed -i '/dtparam=act_led_trigger=/d' /boot/config.txt
sed -i '/dtparam=act_led_activelow=/d' /boot/config.txt
## Set the LED config lines like we want them
echo "dtparam=act_led_trigger=none" >> /boot/config.txt
echo "dtparam=act_led_activelow=on" >> /boot/config.txt

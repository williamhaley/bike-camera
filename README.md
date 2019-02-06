# Bike Camera

Code for a Raspberry Pi camera on a bike. The camera detects motion and then records until motion has ceased for 10 seconds. Motion is determined by visual input, not GPS or Gyro readings.

# Install

Clone this repo to your `pi` user's `$HOME` dir.

Run the `./setup.sh` script to get required packages and update some easily scripted configurations.

Add this to `/etc/rc.local` before the "exit 0" line.

```
/home/pi/bike-camera/run.sh &
```

_Thanks to [Jeff Geerling](https://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-zero-conserve-energy) for the power saving tips._

# Sync/Download Videos From Pi

```
./download.sh the.pi.ip.address
```

# Delete Videos From Pi

```
./purge.sh the.pi.ip.address
```

# TODO / Wish List

* Button to turn camera on and off
* Configurable options for video
* Audio recording
* Sensors for motion detection
* GPS info
* Battery info
* Nice enclosure solution
* Only run `nginx` as needed to save battery, or get a better file delivery mechanism
* System for deleting/expiring old videos

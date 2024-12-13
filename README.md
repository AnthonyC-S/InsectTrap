# Insect Trap Information
Anthony Nicolaides (ajn68),
Anthony Coffin-Schmitt (awc93),
Professor Sunghwan Jung

Last Edited: Decemeber 2024

Insect trap with iNaturalist intergration to monitor insect populations or selectively capture/kill insect pests. Ran on Raspberry Pi  4B.

# Equipment
- Raspberry Pi
- Raspberry Pi Camera
- Two SG90 micro servos
- adafruit BH1750 Light Sensor
- 12 small LED lights

# Wiring
- Raspberry Pi: 
	- Powered via solar panel manager (which is connected to a solar panel)
- Camera: 
	- Raspberry Pi camera module via ribbon cable
- Servo in main chamber: 
	- 3.3V
	- GND
	- GPIO4
- Servo in kill chamber: 
	- 3.3V
	- GND
	- GPIO18
- Light sensor: 
	- Vin: 3.3V (achieved by using a voltage divider connected to a 5V pin)
	- GND
	- SCL: GPIO3
	- SDA: GPIO2
- 3 LEDs for main chamber:
	- Connected all in parallel
	- Positive end connected to GPIO26
	- GND
- 9 LEDs for funnel:
	- Connected all in parallel
	- Positive end connected to GPIO12
	- GND

# Note about wiring

Check `lightControl.py` to see which pins are assigned to the LEDs.

Check `servoControl.py` to see which pins are assigned to the servos.  

# Before Starting Program

See [INSTALL.md](INSTALL.md) for setting up Python envrionment on device. 

This code utilizes pigpio, please run `sudo pigpiod` to allow pigpio to work.

# Recommendations
If using a Raspberry Pi Zero model, consider changing the Pi to auto boot to console instead of desktop to converse power. Having the program running while using the desktop can cause lag.

# Cron jobs
Cron jobs are ran at regular intervals and are useful for when the insect trap is operating for long periods of time as if updates troubleshooting logs and auto runs the python script if it ever stops during its operation in the field.

Enter `crontab -e` in the terminal and all the follow:

To have the raspberry pi automatically run the python script at reboot add:
`@reboot /path/to/InsectTrap/bin/python3 /path/to/InsectTrap/InsectTrapProject/main.py >> /path/to/InsectTrap/Logs/heartbeat.log 2>$1`

To have a log of when the raspberry pi boots up and how long it is on (useful for knowing if the device lost power / shutdown at any point when operating the trap) add:

`@reboot /path/to/InsectTrap/scripts/system_status.sh startup`
`*/10 * * * * /path/to/InsectTrap/scripts/system_status.sh`

To have the pi auto reboot if the python script is not running, add:
`*/1 * * * * /path/to/InsectTrap/scripts/monitor_log.sh`

If using cron jobs, make sure to go into `path/to/InsectTrap/scripts/` and modify the `LOG_FILE` variable in both `system_status.sh` and `monitor_log.sh` to `/path/to/InsectTrap/Logs/system_status.log` and `/path/to/InsectTrap/Logs/heartbeat.log`, respectively

# Running program
If using cron jobs, reboot the device and the python script will begin running in the background.

If manually starting the python script, make sure to activate the environment first (see Before Starting Program). Then run:
`python3 /path/to/InsectTrap/InsectTrapProject/main.py`

By default, the camera will not show on the screen. This is to avoid lagging the device when running the program at the same time you are using it.
If you want to see the camera on screen and see some print outputs, run:
`python3 /path/to/InsectTrap/InsectTrapProject/main.py --autoOFF`

Running the program with `--autoOFF` while using the device can cause lag on Raspberry Pi Zero models. No lag should be present with bigger models like Raspberry Pi 4. 
Raspberry Pi Zero 2W is used for is low energy consumption.

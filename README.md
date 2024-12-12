# Insect Trap Information
Anthony Nicolaides (ajn68)
Anthony Coffin-Schmitt (awc93)
Professor Sunghwan Jung
Last Edited: Decemeber 2024

Insect trap with iNaturalist intergration to selectively kill insects. Ran on Raspberry Pi  4B.

# Equipment
- Raspberry pi
- Raspberry pi Camera
- Two SG90 micro servos
- adafruit BH1750 Light Sensor
- 12 small LED lights

# Wiring
- Raspberry pi: 
	- Powered via solar panel manager (which is connected to a solar panel)
- Camera: 
	- Raspberry pi camera module via ribbon cable
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
	- connected all in parallel
	- positive end connected to GPIO26
	- GND
- 9 LEDs for funnel:
	- connected all in parallel
	- positive end connected to GPIO12
	- GND

# Note about wiring

Check `lightControl.py` to see which pins are assigned to the LEDs.

Check `servoControl.py` to see which pins are assigned to the servos.  

# Before Starting Program

See setup_notes.txt for python environment details. 

This code utilizes pigpio, please run `sudo pigpiod` to allow pigpio to work.

## If using Raspberry Pi Zero
InsectTrap contains an environment with all necessary packages installed. Run `source path/to/InsectTrap/bin/activate` to start environment (`deactivate` to close environment).
Python3 should already be in the virtual environment.

Run `pip3 install -r path/to/InsectTrap/requirements.txt` to make sure all necessary packages are installed.

If running on a Raspberry Pi Zero model, make sure to modify your config.txt file.
Open your config file with `sudo nano /boot/firmware/config.txt` or `sudo nano /boot/config.txt` for older OS versions.

Make the following modifications to the `config.txt` file:
  If present, comment or delete `camera__auto_detect=1`
  Ensure the following lines are present, if not, add them in:

  `start_x=1`
  `gpu_mem=128`

Ensure I2C is enabled in `sudo raspi-config`


# Recommendations
If using a Raspberry Pi Zero model, consider changing the pi to auto boot to console instead of desktop to converse power. Having the program running while using the desktop can cause lag.

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

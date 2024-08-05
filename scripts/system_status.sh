#!/bin/bash

LOG_FILE="/home/pi/InsectTrap/Logs/system_status.log"

# Log startup time
if [ "$1" == "startup" ]; then
	echo -e "\nRaspberry Pi booted at $(date)" >> "$LOG_FILE"
fi

# Log uptime
echo "Uptime at $(date): $(uptime -p)" >> "$LOG_FILE"

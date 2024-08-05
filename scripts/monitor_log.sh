#!/bin/bash

LOG_FILE="/home/pi/InsectTrap/Logs/heartbeat.log"

# Seconds the log file can not be updated before a reboot
THRESHOLD=120

CURRENT_TIME=$(date +%s)
MOD_TIME=$(stat -c %Y "$LOG_FILE")

TIME_DIFF=$((CURRENT_TIME - MOD_TIME))

if [ "$TIME_DIFF" -gt "$THRESHOLD" ]; then
	echo -e "\n\nLog file has not been updated within the last $THRESHOLD seconds ($TIME_DIFF seconds).\nRebooting...\n" >> "$LOG_FILE"
	sudo reboot
fi

from time import sleep

import RPi.GPIO as GPIO

# Set up servos
servo_pin = 4  # pin 7 (GPIO4)
servo_pin_2 = 18  # pin 12 (GPIO18)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(servo_pin_2, GPIO.OUT)
servoX = GPIO.PWM(servo_pin, 50)  # 50 Hz
servoKill = GPIO.PWM(servo_pin_2, 50)  # 50 Hz


def initializeServos():
    servoX.ChangeDutyCycle(0)
    servoKill.ChangeDutyCycle(0)
    servoX.start(0)
    servoKill.start(0)


def moveInsect(good, found):
    if not found:
        return
    if good:
        saveBug()
    else:
        killBug()


def openRight():
    # when camera is facing you
    servoX.ChangeDutyCycle(3)
    sleep(1)
    servoX.ChangeDutyCycle(0)
    sleep(2)


def openMiddle():
    # when camera is facing you
    servoX.ChangeDutyCycle(6.2)
    sleep(1)
    servoX.ChangeDutyCycle(0)
    sleep(2)


def openLeft():
    # when camera is facing you
    servoX.ChangeDutyCycle(10)
    sleep(1)
    servoX.ChangeDutyCycle(0)
    sleep(2)


def openKillChamber():
    servoKill.ChangeDutyCycle(14)
    sleep(1)
    servoKill.ChangeDutyCycle(0)
    sleep(2)


def closeKillChamber():
    servoKill.ChangeDutyCycle(1)
    sleep(1)
    servoKill.ChangeDutyCycle(0)
    sleep(2)
    servoKill.ChangeDutyCycle(3)
    sleep(1)
    servoKill.ChangeDutyCycle(1)
    sleep(2)


def saveBug():
    openRight()
    sleep(5)
    openMiddle()


def killBug():
    openKillChamber()
    openLeft()
    sleep(1)
    closeKillChamber()
    openMiddle()
    sleep(2)
    openKillChamber()


def exit():
    openMiddle()
    openKillChamber()
    GPIO.cleanup()

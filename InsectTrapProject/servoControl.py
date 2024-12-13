from time import sleep

import RPi.GPIO as GPIO
import pigpio

# Set up servos
servo_pin = 25  # pin 22 (GPIO25)
servo_pin_2 = 24  # pin 18 (GPIO24)
servoX = pigpio.pi()
servoKill = pigpio.pi()

servoX.set_mode(servo_pin, pigpio.OUTPUT)
servoKill.set_mode(servo_pin_2, pigpio.OUTPUT)

servoX.set_PWM_frequency(servo_pin, 50)
servoKill.set_PWM_frequency(servo_pin_2, 50)

def initializeServos():
    servoX.set_servo_pulsewidth(servo_pin, 1600)
    servoKill.set_servo_pulsewidth(servo_pin_2, 1550)
    servoKill.set_PWM_dutycycle(servo_pin_2, 0)
    servoX.set_PWM_dutycycle(servo_pin, 0)

def moveInsect(good, found):
    if not found:
        return
    if good:
        saveBug()
    else:
        killBug()


def openRight():
    # when camera is facing you
    servoX.set_servo_pulsewidth(servo_pin, 500)
    sleep(2)
    servoX.set_servo_pulsewidth(servo_pin, 1600)
    sleep(2)


def openMiddle():
    # when camera is facing you
    servoX.set_servo_pulsewidth(servo_pin, 1600)
    sleep(2)
    servoKill.set_PWM_dutycycle(servo_pin_2, 0)


def openLeft():
    servoX.set_servo_pulsewidth(servo_pin, 2500)
    sleep(1)
    servoX.set_servo_pulsewidth(servo_pin, 1600)
    sleep(2)
    

def openKillChamber():
    servoKill.set_servo_pulsewidth(servo_pin_2, 1500)
    sleep(1)
    servoKill.set_PWM_dutycycle(servo_pin_2, 0)


def closeKillChamber():
    servoKill.set_servo_pulsewidth(servo_pin_2, 500)
    sleep(1)
    servoKill.set_servo_pulsewidth(servo_pin_2, 1000)
    sleep(1)
    servoKill.set_servo_pulsewidth(servo_pin_2, 500)
    sleep(1)
    servoKill.set_PWM_dutycycle(servo_pin_2, 0)


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
    servoX.set_PWM_dutycycle(servo_pin, 0)
    servoX.set_PWM_frequency(servo_pin, 0)
    servoKill.set_PWM_dutycycle(servo_pin_2, 0)
    servoKill.set_PWM_frequency(servo_pin_2, 0)
    
def test():
    servoX.start(0)
    sleep(3)
    servoX.ChangeDutyCycle(8)
    sleep(2)
    servoX.ChangeDutyCycle(5)
    sleep(2)
    servoX.ChangeDutyCycle(12)
    sleep(2)
    servoX.stop()
    GPIO.cleanup()

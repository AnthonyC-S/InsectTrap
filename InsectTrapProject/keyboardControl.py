import lightControl as lC
import servoControl as sC


# check to see if any key has been pressed
def keyboard_press(pressed, auto):
    if pressed == 27:  # ESC key
        return False  # stop running program
    if not auto:
        if pressed == ord("1"):  # turn on LED only
            lC.LEDon_chamber()
        elif pressed == ord("2"):  # turn off LED only
            lC.LEDoff_chamber()
        elif pressed == ord("l"):  # open left
            sC.openLeft()
        elif pressed == ord("r"):  # open right
            sC.openRight()
        elif pressed == ord("m"):  # open middle
            sC.openMiddle()
        elif pressed == ord("k"):
            sC.closeKillChamber()
        elif pressed == ord("o"):
            sC.openKillChamber()
    return True

import argparse
from time import time

import cv2

import keyboardControl as kC
import lightControl as lC
import MLprocessing as ML
import servoControl as sC
import videoProcessing as vP


def start_heartbeat():
    namestamp = vP.getNamestamp(vP.getTimestamp()) + " EDT 2024\n"
    with open("/home/pi/InsectTrap/Logs/heartbeat.log", "a") as f:
        f.write("\nInsectTrapProject/main.py started at " + namestamp)
    return


def update_heartbeat():
    namestamp = vP.getNamestamp(vP.getTimestamp()) + " EDT 2024\n"
    with open("/home/pi/InsectTrap/Logs/heartbeat.log", "a") as f:
        f.write("	main.py running at " + namestamp)
    return


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--autoOFF',
        help='Turns off auto mode. Auto mode does not show camera and ML outputs. Auto mode is on by default.',
        action='store_true')
    args = parser.parse_args()
    auto = not args.autoOFF
    if not auto:
        print("Auto mode disabled.")
    start_heartbeat()
    running = True
    cap = vP.initialize()
    sC.initializeServos()
    sC.openMiddle()
    lC.LEDon_chamber()
    lC.LEDon_funnel()
    last_heartbeat = time()
    last_ML = time()
    start_time = time()
    counter = 0
    fps = 0.0
    while vP.cameraOpen(cap) and running:
        lC.manageLight()
        running = kC.keyboard_press(cv2.waitKey(1), auto)
        running, image = vP.checkCamera(cap)
        if time() - last_ML > 5: # seconds
            found, augmented_image, bug, insect, others, good = ML.insectModel(
                auto, image)
            last_ML = time()
            vP.save_ML_image(image, found, insect, bug, good)
            vP.showBug(image, found, insect, bug, auto)
            sC.moveInsect(good, found)
        if time() - last_heartbeat > 60: # seconds
            update_heartbeat()
            last_heartbeat = time()
        if not auto:
            end_time = time()
            vP.FPS(image, counter, start_time, end_time, fps)
            start_time = time()
            vP.showTimestamp(image, vP.getTimestamp())
            title = "(ESC to exit)"
            vP.showFrame(image, title)
            counter = 0
        counter += 1

    sC.exit()
    lC.exit()
    vP.exit(cap)


if __name__ == "__main__":
    main()

import argparse
from time import time, sleep

import cv2

#import keyboardControl as kC
import lightControl as lC
import MLprocessing as ML
import servoControl as sC
import videoProcessing as vP
import Get_Classification as gC

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
    #start_heartbeat()
    #vP.initializePicamera()
    cap = vP.initialize()
    #cap = cv2.VideoCapture(0)
    print(cap)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    driver = gC.initialize_driver(True)
    sC.initializeServos()
    sC.openMiddle()
    sleep(2)
    #sC.openMiddle()
    lC.LEDon_chamber()
    lC.LEDon_funnel()
    last_heartbeat = time()
    last_read = time()
    start_time = time()
    counter = 0
    fps = 0.0
    while vP.cameraOpen(cap):
        sC.openMiddle()
        cv2.destroyAllWindows()
        lC.manageLight()

        image_path = '/home/pi/InsectTrap/picture.jpg'
        last_read = time()
        frame = vP.saveImage(cap, image_path)
        driver, results = gC.get_ID(image_path, driver, auto)
        #print(results)
        found = True
        if results['taxon_most_likely_scientific_name'] == 'Not Found':
            found = False
        # check if good or bad
        good = False
        
        # kill or release
        sC.moveInsect(good, found)
        
        # move image to correct folder, rename
        vP.move_rename_image(image_path, results, good)
        #vP.showBug(image, found, insect, bug, auto)
        #sC.moveInsect(good, found)
        if not auto:
            #end_time = time()
            #vP.FPS(image, counter, start_time, end_time, fps)
            #start_time = time()
            #vP.showTimestamp(image, vP.getTimestamp())
            title = results['taxon_most_likely_scientific_name']
            vP.showFrame(frame, title)
            sleep(1)
            counter = 0
        if time() - last_heartbeat > 60: # seconds
            #update_heartbeat()
            last_heartbeat = time()
        
        counter += 1
        sleep(10)

    sC.exit()
    lC.exit()
    vP.exit(cap)
    gC.quit_driver(driver)


if __name__ == "__main__":
    main()

import datetime
from picamera2 import Picamera2, Preview
from time import time, sleep

import cv2
import pytz
import os
import shutil
import numpy as np
from PIL import Image, ImageFont, ImageDraw

# wait 100 frames before taking picture to let camera adjust to light
waitFrames = 100
takepicture = (waitFrames * -1) - 1


# Variables to calculate FPS
counter, fps = 0, 0
start_time = time()

# Visualization parameters
row_size = 20  # pixels
left_margin = 24  # pixels
text_color = (0, 0, 255)  # red
font_size = 1
font_thickness = 1


def initializePicamera():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start()
    time.sleep(2)
    picam2.capture_file("test.jpg")

def initialize():
    cap = Picamera2()
    cap.start()
    sleep(1)
    
    return cap


def adjust_contrast_brightness(
        img,
        contrast: float = 1.0,
        brightness: int = 0):
    """
    Adjusts contrast and brightness of an uint8 image.
    contrast:   (0.0,  inf) with 1.0 leaving the contrast as is
    brightness: [-255, 255] with 0 leaving the brightness as is
    """
    brightness += int(round(255 * (1 - contrast) / 2))
    return cv2.addWeighted(img, contrast, img, 0, brightness)


def cameraOpen(cap):
    return cap.started #True #cap.isOpened()


def saveImage(cap, image_path):
    frame = cap.capture_image()
    img = Image.fromarray(np.array(frame))
    img = img.convert("RGB")
    img.save(image_path, "JPEG")
    return frame



def calculateFPS(counter, start_time, end_time, fps):
    fps_avg_frame_count = 10
    if counter % fps_avg_frame_count == 0:
        fps = fps_avg_frame_count / (end_time - start_time)
    return fps


def showFPS(image, fps):
    fps_text = "FPS = {:.1f}".format(fps)
    text_location = (left_margin, row_size + 20)
    cv2.putText(
        image,
        fps_text,
        text_location,
        cv2.FONT_HERSHEY_PLAIN,
        font_size,
        text_color,
        font_thickness,
    )


def FPS(image, counter, start_time, end_time, fps=0.0):
    fps = calculateFPS(counter, start_time, end_time, fps)
    showFPS(image, fps)


def showTimestamp(image, timestamp):
    # Show timestamp
    text_location = (left_margin, row_size)
    cv2.putText(
        image,
        timestamp,
        text_location,
        cv2.FONT_HERSHEY_PLAIN,
        font_size,
        text_color,
        font_thickness,
    )


def getTimestamp():
    return str(datetime.datetime.now(pytz.timezone("US/Eastern")))


def getNamestamp(timestamp):
    return timestamp[0:10] + "_" + timestamp[11:19]


def showFrame(frame, title):
    draw = ImageDraw.Draw(frame)
    font = ImageFont.truetype("/home/pi/InsectTrap/InsectTrapProject/OpenSans-Regular.ttf", 32)
    draw.text((0,0), title, (255, 0, 0), font=font)
    frame.show(title=title)


def showBug(image, found, insect, bug, auto):
    if found and not auto:
        showFrame(
            image,
            f"{bug['tagName']} | {round(bug['probability'] * 100, 2)}%")


def save_ML_image(image, found, insect, bug, good):
    timestamp = getTimestamp()
    namestamp = getNamestamp(timestamp)
    image_directory = "/home/pi/InsectTrap/images/"
    if found:
        print(
            f"^Found {bug['tagName']} | {round(bug['probability'] * 100, 2)}%")
        if good:
            directory = image_directory + "save/"
            print("-> save")
        else:
            directory = image_directory + "kill/"
            print("-> kill")
        name = (
            bug["tagName"]
            + "_"
            + str(round(bug["probability"] * 100, 2))
            + "_"
            + namestamp
            + ".PNG"
        )
        showTimestamp(image, timestamp)
        cv2.imwrite(directory + name, image)
    if insect:
        directory = image_directory + "other/"
        name = namestamp + ".PNG"
        showTimestamp(image, timestamp)
        cv2.imwrite(directory + name, image)
    return directory + name

def move_rename_image(image_path, results, good):
    not_found_dir = '/home/pi/InsectTrap/images/NotFound'
    found_dir = '/home/pi/InsectTrap/images/Found'
    timestamp = getTimestamp()
    namestamp = getNamestamp(timestamp)
    taxon_name = results['taxon_most_likely_scientific_name']
    taxon_name_formatted = ''.join(word.capitalize() for word in taxon_name.split())
    if taxon_name == 'Not Found':
        new_filename = f"{namestamp}_{taxon_name_formatted}.jpg"
        os.makedirs(not_found_dir, exist_ok=True)
        shutil.move(image_path, os.path.join(not_found_dir, new_filename))
    else:
        if good:
            gb = "good"
        else:
            gb = "bad"
        new_filename = f"{namestamp}_{taxon_name_formatted}_{gb}.jpg"
        os.makedirs(found_dir, exist_ok=True)
        shutil.move(image_path, os.path.join(found_dir, new_filename))
        
def exit(cap):
    cap.close()
    cv2.destroyAllWindows()
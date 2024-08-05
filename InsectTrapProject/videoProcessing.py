import datetime
#from picamera import PiCamera
from time import time

import cv2
import pytz

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


def initialize():
    # Start capturing video input from the camera
    camera_id = -1
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # cv2.resizeWindow('cap', 480, 640)
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
    return cap.isOpened()


def checkCamera(cap):
    success, image = cap.read()
    image = adjust_contrast_brightness(image, contrast=2, brightness=80)
    # image = cv2.flip(image, 1)
    if not success:
        raise Exception("ERROR: Unable to read from camera.")
    return success, image


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


def showFrame(image, title):
    cv2.imshow(title, image)
    cv2.namedWindow(title)


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


def exit(cap):
    cap.release()
    cv2.destroyAllWindows()

import cv2
import numpy as np
import tflite_runtime.interpreter as tf
from PIL import Image

import helper
from object_detection import ObjectDetection

MODEL_FILENAME = "/home/pi/InsectTrap/InsectTrapProject/model.tflite"
LABELS_FILENAME = "/home/pi/InsectTrap/InsectTrapProject/labels.txt"


class TFLiteObjectDetection(ObjectDetection):
    """Object Detection class for TensorFlow Lite"""

    def __init__(self, model_filename, labels):
        super(TFLiteObjectDetection, self).__init__(labels)
        self.interpreter = tf.Interpreter(model_path=model_filename)
        self.interpreter.allocate_tensors()
        self.input_index = self.interpreter.get_input_details()[0]["index"]
        self.output_index = self.interpreter.get_output_details()[0]["index"]

    def predict(self, preprocessed_image):
        inputs = np.array(preprocessed_image, dtype=np.float32)[
            np.newaxis, :, :, (2, 1, 0)
        ]  # RGB -> BGR and add 1 dimension.

        # Resize input tensor and re-allocate the tensors.
        self.interpreter.resize_tensor_input(self.input_index, inputs.shape)
        self.interpreter.allocate_tensors()

        self.interpreter.set_tensor(self.input_index, inputs)
        self.interpreter.invoke()
        return self.interpreter.get_tensor(self.output_index)[0]


def insectModel(auto, frame, image_filename=""):
    # Load labels
    with open(LABELS_FILENAME, "r") as f:
        labels = [line.strip() for line in f.readlines()]

    od_model = TFLiteObjectDetection(MODEL_FILENAME, labels)

    found = False

    # Update orientation based on EXIF tags, if the file has orientation info.
    image = helper.update_orientation(frame)

    # If the image has either w or h greater than 1600 we resize it down
    # respecting aspect ratio such that the largest dimension is 1600
    image = helper.resize_down_to_1600_max_dim(image)

    # We next get the largest center square
    h, w = image.shape[:2]
    min_dim = min(w, h)
    max_square_image = helper.crop_center(image, min_dim, min_dim)

    # Resize that square down to 512x512
    augmented_image = helper.resize_to_512_square(max_square_image)
    # Predict image using PIL Image
    predictions = od_model.predict_image(Image.fromarray(augmented_image))
    found, bug, augmented_image, insect, others = lookAtPredictions(
        augmented_image, predictions, auto
    )
    good = goodBadBug(bug["tagName"])
    return found, augmented_image, bug, insect, others, good


def lookAtPredictions(augmented_image, predictions, auto):
    font = cv2.FONT_HERSHEY_SIMPLEX
    found = False
    bug = {
        "probability": 0.0,
        "tagId": 0,
        "tagName": "",
        "boundingBox": {"left": 0.0, "top": 0.0, "width": 0.0, "height": 0.0},
    }
    others = []
    bug_text = ""
    insect = False
    # Looping through number of predictions
    if not auto:
        print(">***********")
    for pred in predictions:
        insect = True
        text = f"{pred['tagName']} | {round(pred['probability'] * 100, 2)}%"
        if not auto:
            print(text)
        if pred["probability"] >= 0.50:
            found = True
            # only choose best predicition
            if pred["probability"] > bug["probability"]:
                bug = pred
                bug_text = text
        else:
            others.append(pred)
        # Draw rectangle for each bounding box based on left, top pixel + width
        # and height
        topleft = (
            int(pred["boundingBox"]["left"] * augmented_image.shape[0]),
            int(pred["boundingBox"]["top"] * augmented_image.shape[1]),
        )
        bottomright = (int(topleft[0] +
                           pred["boundingBox"]["width"] *
                           augmented_image.shape[0]),
                       int(topleft[1] +
                           pred["boundingBox"]["height"] *
                           augmented_image.shape[0]), )
        # draw rectangle and text on img
        cv2.rectangle(augmented_image, topleft, bottomright, (255, 0, 0), 2)
        cv2.putText(augmented_image, text, topleft, font,
                    0.5, (255, 0, 0), 1, cv2.LINE_AA)
    topleft = (
        int(bug["boundingBox"]["left"] * augmented_image.shape[0]),
        int(bug["boundingBox"]["top"] * augmented_image.shape[1]),
    )
    bottomright = (int(topleft[0] +
                       bug["boundingBox"]["width"] *
                       augmented_image.shape[0]),
                   int(topleft[1] +
                       bug["boundingBox"]["height"] *
                       augmented_image.shape[0]), )

    cv2.rectangle(augmented_image, topleft, bottomright, (0, 0, 255), 2)
    cv2.putText(augmented_image, bug_text, topleft,
                font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    # print(topleft)
    # print(bottomright)
    if not auto:
        print("***********<")
    return found, bug, augmented_image, insect, others


def goodBadBug(name):
    good_bugs = [
        "housefly",
        "ant",
        "bumble bee",
        "butterfly",
        "grasshopper",
        "common house spider",
    ]
    return name in good_bugs

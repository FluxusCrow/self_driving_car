import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import mss
import mss.tools
import cv2

model = keras.applications.mobilenet_v2.MobileNetV2(
    weights= "imagenet",   
    alpha = 0.35,
    include_top=True,  # we only want to have the base, not the final dense layers 
    input_shape=(224, 224, 3)
)

K.clear_session()
box = np.array([0, 0, 1, 1])
boxes = box.reshape([1, 1, 4])
colors = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])

with mss.mss() as sct:
    mon1 = sct.monitors[1]
    monitor = {"top": mon1["top"] + 65, "left": mon1["left"] + 75, "width": 800, "height": 600}
    while True:
        screen = np.array(sct.grab(monitor))
        cv2.imshow("window", screen)
        screen = cv2.resize(screen, (224,224))
        cv2.imshow("window2", screen)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2RGB)
        #image_batch = np.reshape(screen, [1, 244, 244, 3])
        image_array = image.img_to_array(screen)
        
        image_batch = np.expand_dims(image_array, axis=0)
        processed_image = keras.applications.mobilenet_v2.preprocess_input(image_batch)
        prediction = model.predict(processed_image)
        tf.image.draw_bounding_boxes(image_batch, boxes, colors, name=None)

        print(keras.applications.mobilenet_v2.decode_predictions(prediction, top=5))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


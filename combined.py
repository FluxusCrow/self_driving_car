# coding: utf-8
# # Object Detection Demo
# License: Apache License 2.0 (https://github.com/tensorflow/models/blob/master/LICENSE)
# source: https://github.com/tensorflow/models
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf

import mss
import mss.tools
import cv2
from pynput import keyboard
from pyKey import pressKey, releaseKey
import time
from alexnet import alexnet

# This is needed since the notebook is stored in the object_detection folder.
#sys.path.append("..")


# ## Object detection imports
# Here are the imports from the object detection module.

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# set up key logging. F1 = start, ESC = end
def on_press_start(key):
    if key == keyboard.Key.f1:
        return False

def on_press_loop(key):
    if key == keyboard.Key.esc:
        return False
        
t_time = 0.09

# # Model preparation 
# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = '/home/pascal/Dokumente/self_driving_car/data/mscoco_label_map.pbtxt'

NUM_CLASSES = 90

# ## Download Model
opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
  file_name = os.path.basename(file.name)
  if 'frozen_inference_graph.pb' in file_name:
    tar_file.extract(file, os.getcwd())


# ## Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.compat.v1.GraphDef()
  with tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# ## Helper code
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
MODEL_NAME_1 = 'model/pygta5-car-fast-{}-{}-{}-epochs-300K-data.model'.format(LR, 'alexnetv2',EPOCHS)

t_time = 0.09

def straight():
##    if random.randrange(4) == 2:
##        ReleaseKey(W)
##    else:
    pressKey("w")
    releaseKey("a")
    releaseKey("d")

def left():
    pressKey("w")
    pressKey("a")
    #ReleaseKey(W)
    releaseKey("d")
    #ReleaseKey(A)
    time.sleep(t_time)
    releaseKey("a")

def right():
    pressKey("w")
    pressKey("d")
    releaseKey("a")
    #ReleaseKey(W)
    #ReleaseKey(D)
    time.sleep(t_time)
    releaseKey("d")
    
model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME_1)

def main():
    last_time = time.time()
    with detection_graph.as_default():
      with tf.compat.v1.Session(graph=detection_graph) as sess:
        with mss.mss() as sct:
            mon1 = sct.monitors[1]
            monitor = {"top": mon1["top"] + 65, "left": mon1["left"] + 75, "width": 800, "height": 600}
            with keyboard.Listener(on_press=on_press_loop) as listener:
                while listener.running:
                    #screen = cv2.resize(grab_screen(region=(0,40,1280,745)), (WIDTH,HEIGHT))
                    screen = np.array(sct.grab(monitor))
                    ## Controlling part
                    print('loop took {} seconds'.format(time.time()-last_time))
                    last_time = time.time()
                    screen_contr = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
                    screen_contr = cv2.resize(screen_contr, (160,120))
        
                    prediction = model.predict([screen_contr.reshape(160,120,1)])[0]
                    print(prediction)
        
                    turn_thresh = .75
                    fwd_thresh = 0.70
        
                    if prediction[1] > fwd_thresh:
                        straight()
                    elif prediction[0] > turn_thresh:
                        left()
                    elif prediction[2] > turn_thresh:
                        right()
                    else:
                        straight()
    
                    ## Object detection part
                    screen_obj_det = cv2.resize(screen, (800,450))
                    image_np = cv2.cvtColor(screen_obj_det, cv2.COLOR_BGRA2BGR)
                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    # Each box represents a part of the image where a particular object was detected.
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    # Each score represent how level of confidence for each of the objects.
                    # Score is shown on the result image, together with the class label.
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                    # Actual detection.
                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})
                    # Visualization of the results of a detection.
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8)
            
                    cv2.imshow('window',image_np)
                    cv2.waitKey(1)

if __name__ == "__main__":
    print("The machine is ready. Press F1 to start!")
    with keyboard.Listener(on_press=on_press_start) as listener:
        listener.join()
    
    main()

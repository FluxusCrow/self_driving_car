"""
Script that takes constantly screenshots of the upper left corner
of the screen. Screenshots are processed to extract the most dominant
lines of the image. The two most dominant lines are considered as
the lanes and are shown in extra window. The script gives then a
keyboard input (w, a or d) depending on if the middle of the image
is between these two lines.
Adapted from Sentdex: https://pythonprogramming.net/finding-lanes-self-driving-car-python-plays-gta-v/?completed=/hough-lines-python-plays-gta-v/
"""

import numpy as np
import cv2
import mss
import mss.tools
from key_inputs import straight, left, right, release_keys
from grab_screen import process_img
from pynput import keyboard

# set up key logging. F1 = start, ESC = end
def on_press_start(key):
    """
    Monitors the keyboard inputs and executes if F1 is pressed.
    """
    if key == keyboard.Key.f1:
        return False

def on_press_stop(key):
    """
    Monitors the keyboard inputs and executes if ESC is pressed.
    """
    if key == keyboard.Key.esc:
        return False



def main():
    """
    Defines which monitor and which part of the monitor is grabbed.
    Defines at which position the two new windows are positioned.
    """
    paused = False
    with mss.mss() as sct:
    # If only one screen is connected:
        #monitor = {"top": 65, "left": 75, "width": 800, "height": 600}
    # If multiple screens are connected:
        monitor_1 = sct.monitors[1]
        monitor = {"top": monitor_1["top"] + 65, "left": monitor_1["left"] + 75, "width": 800, "height": 600}
        image = np.array(sct.grab(monitor))
        new_image,original_image, lane_1, lane_2 = process_img(image)
        cv2.imshow('line extraction', new_image)
        cv2.imshow('detected lanes', original_image)
        cv2.moveWindow("line extraction", 3080,20)
        cv2.moveWindow("detected lanes", 3080,450)
    
    with keyboard.Listener(on_press=on_press_stop) as listener:
        while listener.running:
            """
            As long as ESC is not pressed, executes the while loop.
            Screenshots are taken and processed. Generates keyboard
            inputs (w, a or d).
            """
            image = np.array(sct.grab(monitor))
            new_image,original_image, lane_1, lane_2 = process_img(image)
            cv2.imshow('line extraction', new_image)
            cv2.imshow('detected lanes', original_image)
            if lane_1 < 0 and lane_2 < 0:
                right()
            elif lane_1 > 0  and lane_2 > 0:
                left()
            else:
                straight()
            cv2.waitKey(1)

if __name__ == "__main__":
    print("The machine is ready. Press F1 to start!")
    with keyboard.Listener(on_press=on_press_start) as listener:
        listener.join()
    
    main()

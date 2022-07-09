import numpy as np
import cv2
import time
import mss
import mss.tools
from key_inputs import straight, left, right, release_keys
from grab_screen import process_img
from pynput import keyboard

# set up key logging. F1 = start, ESC = end
def on_press_start(key):
    if key == keyboard.Key.f1:
        return False

def on_press_loop(key):
    if key == keyboard.Key.esc:
        return False

def main():
    
    for i in list(range(0))[::-1]:
        print(i+1)
        time.sleep(1)

    #last_time = time.time()
    with mss.mss() as sct:
    # The screen part to capture
    ## If only one screen is connected
        #monitor = {"top": 65, "left": 75, "width": 800, "height": 600}
    ## If multiple screens are connected
        mon1 = sct.monitors[1]
        monitor = {"top": mon1["top"] + 65, "left": mon1["left"] + 75, "width": 800, "height": 600}
    with keyboard.Listener(on_press=on_press_loop) as listener:
        while listener.running:
            screen =  np.array(sct.grab(monitor))
            #print('Frame took {} seconds'.format(time.time()-last_time))
            #last_time = time.time()
            new_screen,original_image, m1, m2 = process_img(screen)
            cv2.imshow('window', new_screen)
            cv2.imshow('window2', original_image)
    
            if m1 < 0 and m2 < 0:
                right()
            elif m1 > 0  and m2 > 0:
                left()
            else:
                straight()
    
            ##cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                release_keys()
                break

print("The machine is ready. Press F1 to start!")
with keyboard.Listener(on_press=on_press_start) as listener:
    listener.join()

main()

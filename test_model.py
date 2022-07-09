import mss
import mss.tools
import cv2
import time
from pyKey import pressKey, releaseKey
from key_inputs import straight, left, right, release_keys
from alexnet import alexnet
import numpy as np
from pynput import keyboard

# set up key logging. F1 = start, ESC = end
def on_press_start(key):
    if key == keyboard.Key.f1:
        return False

def on_press_loop(key):
    if key == keyboard.Key.esc:
        return False


WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'model/pygta5-car-fast-{}-{}-{}-epochs-300K-data.model'.format(LR, 'alexnetv2',EPOCHS)

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
model.load(MODEL_NAME)

def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    with mss.mss() as sct:
        mon1 = sct.monitors[1]
        monitor = {"top": mon1["top"] + 65, "left": mon1["left"] + 75, "width": 800, "height": 600}
    
    with keyboard.Listener(on_press=on_press_loop) as listener:
        while listener.running:
        #while(True):
            
            if not paused:
                # 800x600 windowed mode
                #screen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
                screen = np.array(sct.grab(monitor))
                print('loop took {} seconds'.format(time.time()-last_time))
                last_time = time.time()
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
                screen = cv2.resize(screen, (160,120))
    
                prediction = model.predict([screen.reshape(160,120,1)])[0]
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
    
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    release_keys()
                    break

print("The machine is ready. Press F1 to start!")
with keyboard.Listener(on_press=on_press_start) as listener:
    listener.join()

main()

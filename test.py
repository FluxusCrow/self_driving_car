from evdev import UInput, ecodes as e
import time

ui = UInput()

for i in list(range(2))[::-1]:
    print(i+1)
    time.sleep(1)

for i in range(50):
     ui.write(e.EV_KEY, e.KEY_W,1)
     ui.write(e.EV_KEY, e.KEY_W,0)
     ui.syn()

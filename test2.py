from pyKey import pressKey, releaseKey, press, sendSequence, showKeys
import time

for i in list(range(2))[::-1]:
    print(i+1)
    time.sleep(1)

pressKey("W")

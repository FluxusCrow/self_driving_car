from pyKey import pressKey, releaseKey, press, sendSequence, showKeys

def straight():
    pressKey("w")
    releaseKey("a")
    releaseKey("d")

def left():
    pressKey("a")
    releaseKey("w")
    releaseKey("d")
    releaseKey("a")

def right():
    pressKey("d")
    releaseKey("a")
    releaseKey("w")
    releaseKey("d")

def release_keys():
    releaseKey("w")
    releaseKey("a")
    releaseKey("d")

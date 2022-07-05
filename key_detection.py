from pynput import keyboard

keys=[]
def on_press(key):
    try:
        format(key.char)
    except AttributeError:
        format(key)
    keys.append(key)
    print(keys)

def on_release(key):
    format(key)
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


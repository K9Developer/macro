from pynput import keyboard
from time import sleep as wait
import json
import pyautogui
import multiprocessing
from pynput.keyboard import Key, Controller

# SETUP
active = False
started = True
proc = None

k = Controller()

print("\n"*50)

print("""
███╗░░░███╗░█████╗░░█████╗░██████╗░░█████╗░
████╗░████║██╔══██╗██╔══██╗██╔══██╗██╔══██╗
██╔████╔██║███████║██║░░╚═╝██████╔╝██║░░██║
██║╚██╔╝██║██╔══██║██║░░██╗██╔══██╗██║░░██║
██║░╚═╝░██║██║░░██║╚█████╔╝██║░░██║╚█████╔╝
╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░╚════╝░\n\n\n""")


def press():
    global active

    with open("./config.json", "r") as f:
        data = json.load(f)

    while True:
        k.press(data["key1"])
        k.release(data["key1"])
        wait((1/data["clicks_per_sec"])/2)
        k.press(data["key2"])
        k.release(data["key2"])
        wait((1/data["clicks_per_sec"])/2)


if __name__ == '__main__':

    proc = multiprocessing.Process(target=press, args=())

    def on_press(key):
        global active
        global started
        global proc

        if key == keyboard.Key.caps_lock:
            if not active:
                active = True
                started = True
            if active and started:
                proc.start()
            started = False

    def on_release(key):
        global started
        global active
        global proc

        if key == keyboard.Key.caps_lock:
            proc.terminate()
            proc = None
            proc = multiprocessing.Process(target=press, args=())
            active = False
            started = False

    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

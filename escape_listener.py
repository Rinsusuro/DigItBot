# escape_listener.py

import os
from pynput import keyboard

def start_global_escape_listener():
    """Starts a global listener that exits the process on ESC key press."""
    def on_press(key):
        if key == keyboard.Key.esc:
            print("[Main] ESC pressed globally. Forcing termination.")
            os._exit(0)  # Immediately kills the entire process

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()

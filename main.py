import queue
import threading
import os
from pynput import keyboard
from screen_capture import LiveScreenCapture
from debugger_gui import DebuggerGUI
from controller import Controller

def global_escape_listener():
    """Listen for ESC globally and terminate the script."""
    def on_press(key):
        if key == keyboard.Key.esc:
            print("[Main] ESC pressed globally. Forcing termination.")
            os._exit(0)  # Immediately kills the entire process

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()

if __name__ == "__main__":
    frame_queue = queue.Queue(maxsize=1)
    centers_queue = queue.Queue(maxsize=1)

    global_escape_listener()

    capture_tool = LiveScreenCapture(frame_queue)
    capture_tool.start_mouse_listener()

    if capture_tool.region:
        # Run the debugger GUI in a separate thread
        debugger = DebuggerGUI(frame_queue, centers_queue)
        debug_thread = threading.Thread(target=debugger.run)
        debug_thread.start()

        # Run the Controller in a separate thread
        controller = Controller(centers_queue)
        controller_thread = threading.Thread(target=controller.process_centers)
        controller_thread.start()

        # Start streaming screenshots
        capture_tool.stream_screenshots()


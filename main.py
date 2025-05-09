import queue
import threading
from screen_capture import LiveScreenCapture
from debugger_gui import DebuggerGUI
from controller import Controller
from escape_listener import start_global_escape_listener
from start_GUI import show_start_gui

if __name__ == "__main__":
    # Show GUI and wait for user to click "Start"
    did_user_start = show_start_gui()

    if not did_user_start:
        print("[Main] GUI was closed before starting. Exiting.")
        exit()

    # Start your actual program
    frame_queue = queue.Queue(maxsize=1)
    centers_queue = queue.Queue(maxsize=1)

    start_global_escape_listener()

    capture_tool = LiveScreenCapture(frame_queue)
    capture_tool.start_mouse_listener()

    if capture_tool.region:
        debugger = DebuggerGUI(frame_queue, centers_queue)
        debug_thread = threading.Thread(target=debugger.run)
        debug_thread.start()

        controller = Controller(centers_queue)
        controller_thread = threading.Thread(target=controller.process_centers)
        controller_thread.start()

        capture_tool.stream_screenshots()

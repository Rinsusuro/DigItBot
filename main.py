import queue
import threading
from screen_capture import LiveScreenCapture
from debugger_gui import DebuggerGUI
from controller import Controller

if __name__ == "__main__":
    frame_queue = queue.Queue(maxsize=1)
    centers_queue = queue.Queue(maxsize=1)

    capture_tool = LiveScreenCapture(frame_queue)
    capture_tool.start_mouse_listener()

    if capture_tool.region:
        # Run the debugger GUI in a separate thread
        debug_thread = threading.Thread(target=DebuggerGUI, args=(frame_queue, centers_queue))
        debug_thread.start()

        # Run the Controller in a separate thread
        controller = Controller(centers_queue)
        controller_thread = threading.Thread(target=controller.process_centers)
        controller_thread.start()

        # Start streaming screenshots
        capture_tool.stream_screenshots()

import cv2
import numpy as np
import mss
from pynput import mouse


class LiveScreenCapture:
    def __init__(self, frame_queue):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.region = None
        self.frame_queue = frame_queue
        self.running = True

    def on_click(self, x, y, button, pressed):
        """Track mouse press and release to determine the region."""
        if pressed:
            self.start_x, self.start_y = x, y
        else:
            self.end_x, self.end_y = x, y
            return False  # Stop listener

    def get_region(self):
        """Calculate (x, y, width, height) from mouse drag."""
        if None in (self.start_x, self.start_y, self.end_x, self.end_y):
            print("No region selected.")
            return None

        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)

        return {"top": y, "left": x, "width": width, "height": height}

    def start_mouse_listener(self):
        """Start a listener for selecting the screen capture region."""
        print("Click and drag to select a region...")
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()

        self.region = self.get_region()

    def stream_screenshots(self):
        """Continuously capture the selected screen region and send frames to the queue."""
        if not self.region:
            print("Invalid region. Exiting...")
            return

        with mss.mss() as sct:
            while self.running:
                # Capture the screen region
                screenshot = sct.grab(self.region)

                # Convert the image to a NumPy array
                img = np.array(screenshot)

                # Convert from BGR (mss default) to RGB for OpenCV
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                # Send frame to the queue for processing
                if not self.frame_queue.full():
                    self.frame_queue.put(img)

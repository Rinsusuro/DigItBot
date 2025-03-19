import pyautogui
import mss
from pynput import mouse
import time


class ScreenCapture:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.capture_ready = False

    def on_click(self, x, y, button, pressed):
        """Track mouse press and release."""
        if pressed:
            self.start_x, self.start_y = x, y
        else:
            self.end_x, self.end_y = x, y
            self.capture_ready = True
            return False  # Stop listener

    def get_region(self):
        """Calculate (x, y, width, height) from mouse drag."""
        if self.start_x is None or self.start_y is None or self.end_x is None or self.end_y is None:
            print("No region selected.")
            return None

        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)

        return (x, y, width, height)

    def capture_screen(self, region):
        """Capture screenshot using mss."""
        if not region:
            print("Invalid region. Screenshot not taken.")
            return

        x, y, width, height = region
        print(f"Capturing region: {region}")

        time.sleep(1)  # Short delay to allow repositioning

        with mss.mss() as sct:
            screenshot = sct.grab({"top": y, "left": x, "width": width, "height": height})
            filename = "screenshot.png"
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)
            print(f"Screenshot saved as {filename}")


if __name__ == "__main__":
    capture_tool = ScreenCapture()

    print("Click and drag to select a region...")
    with mouse.Listener(on_click=capture_tool.on_click) as listener:
        listener.join()

    selected_region = capture_tool.get_region()
    if selected_region:
        capture_tool.capture_screen(selected_region)

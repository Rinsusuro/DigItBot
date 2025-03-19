import queue
import threading
import time
import keyboard  # For hotkey detection
from pynput.mouse import Controller as MouseController, Button

class Controller:
    def __init__(self, centers_queue):
        self.centers_queue = centers_queue
        self.mouse = MouseController()
        self.running = True
        self.last_click_time = time.time()  # Track last click time

        # Set up hotkey for termination
        keyboard.add_hotkey("esc", self.stop)
        print("[INFO] Press 'ESC' to terminate the controller.")

    def process_centers(self):
        """Continuously checks center values and controls left-clicking."""
        while self.running:
            latest_centers = None

            # Keep removing old entries until only the latest one remains
            while not self.centers_queue.empty():
                latest_centers = self.centers_queue.get()

            if latest_centers:  # Process only the latest available entry
                bar_center = latest_centers.get("bar", None)
                indicator_center = latest_centers.get("indicator", None)

                if bar_center is not None and indicator_center is not None:
                    if bar_center > indicator_center:
                        self.mouse.press(Button.left)  # Hold left click
                    else:
                        self.mouse.release(Button.left)  # Release left click

            # Perform a quick click every 3 seconds
            if time.time() - self.last_click_time >= 3:
                self.mouse.click(Button.left, 1)  # Quick click
                print("Quick Click Triggered")
                self.last_click_time = time.time()  # Reset timer

            time.sleep(0.01)  # Small delay to prevent excessive CPU usage

    def stop(self):
        """Stops the controller thread and exits the program."""
        print("\n[INFO] Terminating Controller...")
        self.running = False
        self.mouse.release(Button.left)  # Ensure left click is released before exiting
        print("[INFO] Controller Stopped. Exiting program.")
        exit(0)  # Force exit

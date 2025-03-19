import cv2
import queue


class DebuggerGUI:
    def __init__(self, frame_queue):
        self.frame_queue = frame_queue
        self.running = True
        self.show_debugger()

    def show_debugger(self):
        """Display the live screen capture feed."""
        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()

                # Show the frame in a debug window
                cv2.imshow("Debugger - Live Screen Capture", frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

        cv2.destroyAllWindows()

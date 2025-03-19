import cv2
import numpy as np
import queue

class DebuggerGUI:
    def __init__(self, frame_queue):
        self.frame_queue = frame_queue
        self.running = True
        self.show_debugger()

    def process_frame(self, frame):
        """Detects and highlights the bar in the given frame."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
        edges = cv2.Canny(blurred, 50, 150)  # Edge detection

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:  # Assuming the bar is a rectangle
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)

                # Filter based on expected aspect ratio and area
                if 2.0 < aspect_ratio < 10.0 and w * h > 500:
                    rect = cv2.minAreaRect(cnt)  # Get rotated bounding box
                    box = cv2.boxPoints(rect)
                    box = np.intp(box)

                    angle = rect[-1]  # Get tilt angle
                    if angle < -45:
                        angle += 90  # Normalize angle

                    cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)  # Draw rectangle
                    cv2.putText(frame, f"Angle: {angle:.2f}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame

    def show_debugger(self):
        """Display the live screen capture feed with bar detection."""
        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                frame = self.process_frame(frame)  # Process frame for bar detection
                cv2.imshow("Debugger - Bar Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

        cv2.destroyAllWindows()

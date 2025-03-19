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

        # Adaptive thresholding for better edge detection
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)

        # Dilate to thicken edges
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)

        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detected = False
        for cnt in contours:
            # Get convex hull (fixes rounded edges)
            hull = cv2.convexHull(cnt)
            rect = cv2.minAreaRect(hull)  # Get rotated bounding box
            box = cv2.boxPoints(rect)
            box = np.intp(box)

            x, y, w, h = cv2.boundingRect(hull)
            aspect_ratio = w / float(h)

            # Filter shapes that resemble a bar
            if 2.0 < aspect_ratio < 10.0 and w * h > 500:
                angle = rect[-1]
                if angle < -45:
                    angle += 90  # Normalize angle

                cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)  # Draw bounding box
                cv2.putText(frame, f"Angle: {angle:.2f}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                detected = True

        # Fallback: Hough Line Transform if bar wasn't detected
        if not detected:
            edges = cv2.Canny(blurred, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=10)

            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

        return frame

    def show_debugger(self):
        """Display the live screen capture feed with bar detection."""
        window_name = "Debugger - Bar Detection"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Allow resizing
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)  # Keep on top

        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                frame = self.process_frame(frame)  # Process frame for bar detection
                cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

        cv2.destroyAllWindows()

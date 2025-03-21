import cv2
import numpy as np
import queue

class DebuggerGUI:
    def __init__(self, frame_queue, centers_queue):
        self.frame_queue = frame_queue
        self.centers_queue = centers_queue  # Store the queue reference
        self.running = True
        self.show_debugger()

    def detect_vertical_edges(self, gray_image):
        """Detects vertical edges using Sobel edge detection."""
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)  # Detect vertical edges
        abs_sobel_x = np.absolute(sobel_x)  # Get absolute values
        sobel_x = np.uint8(255 * abs_sobel_x / np.max(abs_sobel_x))  # Normalize to 0-255

        return sobel_x

    def detect_edge_based_bar(self, edge_image):
        """Finds the leftmost and rightmost vertical contour edges to define the bar."""
        height, width = edge_image.shape

        # Scan left to right for the first strong vertical edge
        left_x = 0
        while left_x < width - 1 and np.mean(edge_image[:, left_x]) < 50:  # Edge threshold
            left_x += 1

        # Scan right to left for the first strong vertical edge
        right_x = width - 1
        while right_x > 0 and np.mean(edge_image[:, right_x]) < 50:
            right_x -= 1

        # Ensure valid detection
        if left_x < right_x:
            bar_x = left_x
            bar_width = right_x - left_x
            bar_y = 0  # Full height
            bar_height = height

            return (bar_x, bar_y, bar_width, bar_height)

        return None

    def detect_lightest_vertical_bar(self, frame):
        """Finds the vertical bar based on its expected color (#989898 in RGB) with a precision threshold."""

        # Convert frame to RGB (OpenCV loads as BGR by default)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Target color (152, 152, 152) in RGB
        target_color = np.array([152, 152, 152])

        # Compute absolute difference from target color for each pixel
        diff = np.abs(rgb_frame - target_color)  # Shape: (height, width, 3)

        # Sum the differences across RGB channels (lower sum = closer match)
        color_distance = np.sum(diff, axis=2)

        # Threshold: Columns where most pixels are within ±3 of target color
        precision_threshold = 3
        matched_pixels = np.sum(color_distance <= precision_threshold * 3, axis=0)  # Sum along height

        # Find the column index with the highest match count
        bar_x = np.argmax(matched_pixels)

        # Define the vertical range of this column
        y_start = 0
        y_end = frame.shape[0]

        return (bar_x, y_start, 5, y_end)  # Width set to 5 for visibility

    def process_frame(self, frame):
        """Detects and highlights the horizontal bar and vertical indicator."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect vertical edges using Sobel
        edge_image = self.detect_vertical_edges(blurred)

        # Detect the bar using vertical edge contours
        bar = self.detect_edge_based_bar(edge_image)

        # Detect the vertical indicator
        indicator = self.detect_lightest_vertical_bar(frame)

        # Store center-x values
        bar_center_x = (bar[0] + bar[2] // 2) if bar else None  # bar[0] is x, bar[2] is width
        indicator_center_x = (indicator[0] + indicator[2] // 2) if indicator else None  # indicator[0] is x, indicator[2] is width

        # Send centers to queue with overflow handling
        if bar_center_x is not None and indicator_center_x is not None:
            if self.centers_queue.full():  # If the queue is full, remove the oldest entry
                self.centers_queue.get()
            self.centers_queue.put({"bar": bar_center_x, "indicator": indicator_center_x})

        # Draw the detected bar
        if bar:
            x, y, w, h = bar
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Bar", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw the detected indicator (lightest vertical bar)
        if indicator:
            x, y, w, h = indicator
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Indicator", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        return frame

    def show_debugger(self):
        """Display the live screen capture feed with bar detection and match its size to the stream."""
        window_name = "Debugger - Bar Detection"
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)  # Auto-resize based on frame dimensions
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)  # Keep on top

        first_frame = True  # Track if it's the first frame to set window size

        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                frame = self.process_frame(frame)  # Process frame for bar detection

                # Set window size to match frame size on the first frame
                if first_frame:
                    height, width, _ = frame.shape
                    cv2.resizeWindow(window_name, width, height)
                    first_frame = False  # Only set size once

                cv2.imshow(window_name, frame)
                cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)  # Reinforce on top

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

        cv2.destroyAllWindows()

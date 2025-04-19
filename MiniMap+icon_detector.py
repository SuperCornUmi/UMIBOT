import cv2
import numpy as np
import time

class MinimapDetector:
    def __init__(self, cam_index=0, width=1920, height=1080):
        # Initialize HDMI camera input
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Define the top-left region to search for the minimap initially
        self.search_x1 = 0
        self.search_y1 = 0
        self.search_width = 280
        self.search_height = 225

        # Store the detected minimap bounding box (x, y, width, height)
        self.detected_box = None

        # Threshold for detecting black screen (e.g., during map transition)
        self.black_screen_threshold = 85
        self.was_black = False  # Tracks if the previous frame was black

    def detect_minimap_box(self, search_region):
        # Convert region to grayscale and detect edges
        gray = cv2.cvtColor(search_region, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find a rectangle that likely represents the minimap
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 130 and h > 40 and w / h > 1.5:
                return (x + self.search_x1, y + self.search_y1, w, h)
        return None

    def is_black_screen(self, frame):
        # Calculate average brightness to determine if screen is black
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        return mean_brightness < self.black_screen_threshold

    def detect_player_position(self, minimap_region):
        # Convert the minimap region to HSV color space
        hsv = cv2.cvtColor(minimap_region, cv2.COLOR_BGR2HSV)

        # Define the HSV range for the player's icon (yellow/orange)
        lower = np.array([26, 100, 200])
        upper = np.array([31, 255, 255])

        # Create a mask for matching colors
        mask = cv2.inRange(hsv, lower, upper)

        # If no pixels match, return None
        if np.all(mask == 0):
            return None

        # Compute the average location of the matching pixels
        coords = np.argwhere(mask > 0)
        mean = np.mean(coords, axis=0).astype(int)
        y, x = mean[0], mean[1]  # row = y, col = x

    ####print(f"[INFO] Player position: x={x}, y={y}")

        # Draw a marker on the player's location
        cv2.drawMarker(minimap_region, (x, y), (0, 255, 255), cv2.MARKER_CROSS, 10, 2)
        return (x, y)
    
    def detect_runn_position(self, minimap_region):
        # Convert the minimap region to HSV color space
        hsv = cv2.cvtColor(minimap_region, cv2.COLOR_BGR2HSV)

        # Define the HSV range for the runn's icon (yellow/orange)
        lower = np.array([135, 100, 170])
        upper = np.array([149, 160, 255])

        # Create a mask for matching colors
        mask = cv2.inRange(hsv, lower, upper)

        # If no pixels match, return None
        if np.all(mask == 0):
            return None

        # Compute the average location of the matching pixels
        coords = np.argwhere(mask > 0)
        mean = np.mean(coords, axis=0).astype(int)
        y, x = mean[0], mean[1]  # row = y, col = x

    ####print(f"[INFO] Runn position: x={x}, y={y}")

        # Draw a marker on the runn's location
        cv2.drawMarker(minimap_region, (x, y), (255, 0, 255), cv2.MARKER_CROSS, 10, 2)
        return (x, y)

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return False

        # Check for black screen and handle accordingly
        if self.is_black_screen(frame):
            if not self.was_black:
                print("[INFO] Black screen detected. Resetting minimap detection...")
            print("[INFO] Black screen detected. Exiting program...")
            return False
        else:
            if self.was_black:
                print("[INFO] Screen recovered. Resuming minimap detection.")
            self.was_black = False

        # Detect the minimap box once, then reuse its position
        if self.detected_box is None:
            search_region = frame[
                self.search_y1:self.search_y1 + self.search_height,
                self.search_x1:self.search_x1 + self.search_width
            ]
            result = self.detect_minimap_box(search_region)
            if result:
                self.detected_box = result
                print(f"[INFO] Detected minimap box at: {self.detected_box}")

        # Once the minimap is found, extract and analyze it
        if self.detected_box:
            x, y, w, h = self.detected_box
            minimap_region = frame[y:y + h, x:x + w]

            # Detect and mark the player's position
            self.detect_player_position(minimap_region)

            # Show the minimap window with annotations
            cv2.imshow("Minimap with Player", minimap_region)

        return True

    def run(self):
        print("[INFO] Waiting 5 seconds before starting detection...")
        time.sleep(5)
        while True:
            if not self.process_frame():
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Clean up on exit
        self.cap.release()
        cv2.destroyAllWindows()

# --- Entry Point ---
if __name__ == '__main__':
    detector = MinimapDetector()
    detector.run()

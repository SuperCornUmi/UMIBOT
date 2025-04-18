import cv2
import numpy as np

class MinimapDetector:
    def __init__(self, cam_index=0, width=1920, height=1080):
        # Initialize HDMI camera
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Define fixed region for initial minimap detection (top-left corner)
        self.search_x1 = 0
        self.search_y1 = 0
        self.search_width = 280
        self.search_height = 220

        # Store detected minimap bounding box (x, y, w, h)
        self.detected_box = None

    def detect_minimap_box(self, search_region):
        # Convert to grayscale and detect edges
        gray = cv2.cvtColor(search_region, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Apply shape and size filter to identify potential minimap box
            if w > 130 and h > 40 and w / h > 1.5:
                # Return position with offset from search region to full frame
                return (x + self.search_x1, y + self.search_y1, w, h)
        return None

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return False

        # Detect minimap only once and save its position
        if self.detected_box is None:
            search_region = frame[
                self.search_y1:self.search_y1 + self.search_height,
                self.search_x1:self.search_x1 + self.search_width
            ]
            result = self.detect_minimap_box(search_region)
            if result:
                self.detected_box = result
                print(f"[INFO] Detected minimap box at: {self.detected_box}")

        # Once detected, always crop from the saved minimap box
        if self.detected_box:
            x, y, w, h = self.detected_box
            minimap_region = frame[y:y + h, x:x + w]
            cv2.imshow("White Frame Content", minimap_region)

        return True

    def run(self):
        while True:
            if not self.process_frame():
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

# --- Entry point ---
if __name__ == '__main__':
    detector = MinimapDetector()
    detector.run()

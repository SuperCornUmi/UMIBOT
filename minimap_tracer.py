import cv2
import numpy as np

# Load minimap template in grayscale
minimap_template = cv2.imread("minimap_template.png", cv2.IMREAD_GRAYSCALE)
template_h, template_w = minimap_template.shape[:2]

# Open HDMI camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Search area defined in top-left corner
search_x1 = 0
search_y1 = 0
search_width = 400
search_height = 300

# Extension distances from minimap
extend_left = 150
extend_down = 140
extend_right = 20

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Crop search region
    search_region = frame[search_y1:search_y1+search_height, search_x1:search_x1+search_width]
    gray_search = cv2.cvtColor(search_region, cv2.COLOR_BGR2GRAY)

    # Template matching within search region
    result = cv2.matchTemplate(gray_search, minimap_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Calculate minimap coordinates in full frame
    top_left = (max_loc[0] + search_x1, max_loc[1] + search_y1)
    bottom_right = (top_left[0] + template_w, top_left[1] + template_h)

    # Expand the region from minimap position
    ext_x1 = max(0, top_left[0] - extend_left)
    ext_y1 = top_left[1]
    ext_x2 = bottom_right[0] + extend_right
    ext_y2 = bottom_right[1] + extend_down

    # Crop extended region
    extended_region = frame[ext_y1:ext_y2, ext_x1:ext_x2]

    if extended_region.size > 0:
        cv2.imshow("Minimap Tracked", extended_region)

        # --- White rectangle detection within extended minimap region ---
        gray_ext = cv2.cvtColor(extended_region, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_ext, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            # Filter: wide horizontal white box (e.g. the inner white map frame)
            if w > 200 and h > 50 and w / h > 2.5:
                # Crop the content inside the white border
                white_frame_content = extended_region[y:y + h, x:x + w]
                cv2.imshow("White Frame Content", white_frame_content)

                # Optional: Draw detection result (for debug)
                cv2.rectangle(extended_region, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break  # Assume only one match needed
    
  
    display = frame.copy()
    cv2.rectangle(display, (search_x1, search_y1), (search_x1+search_width, search_y1+search_height), (255, 0, 0), 2)
    cv2.rectangle(display, top_left, bottom_right, (0, 255, 0), 2)
    cv2.imshow("HDMI View", cv2.resize(display, (1280, 720)))
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

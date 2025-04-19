import cv2
import numpy as np

# Callback for trackbar updates
def nothing(x):
    pass

# Create a window
cv2.namedWindow('HSV Color Picker')

# Create trackbars for H, S, and V
cv2.createTrackbar('H', 'HSV Color Picker', 0, 179, nothing)
cv2.createTrackbar('S', 'HSV Color Picker', 0, 255, nothing)
cv2.createTrackbar('V', 'HSV Color Picker', 0, 255, nothing)

# Create an image that will show the color
color_img = np.zeros((200, 400, 3), dtype=np.uint8)

while True:
    # Get current positions of trackbars
    h = cv2.getTrackbarPos('H', 'HSV Color Picker')
    s = cv2.getTrackbarPos('S', 'HSV Color Picker')
    v = cv2.getTrackbarPos('V', 'HSV Color Picker')

    # Convert HSV to BGR for display
    hsv_color = np.uint8([[[h, s, v]]])
    bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)

    # Update the color image
    color_img[:] = bgr_color

    # Show the color and values
    cv2.putText(color_img, f'H: {h}  S: {s}  V: {v}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255) if v < 128 else (0, 0, 0), 2)

    cv2.imshow('HSV Color Picker', color_img)

    if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to exit
        break

cv2.destroyAllWindows()

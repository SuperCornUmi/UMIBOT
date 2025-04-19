import cv2
import numpy as np

def show_HSV_on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv[y, x]
        print(f"HSV at ({x},{y}) = {pixel}")  # print H, S, V values

# Load image
img = cv2.imread('01.png')  # §ï¦¨§Aªº¹Ï¤ù¸ô®|
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.namedWindow("HSV Picker")
cv2.setMouseCallback("HSV Picker", show_HSV_on_click)

while True:
    cv2.imshow("HSV Picker", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

cv2.destroyAllWindows()

import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


ref_point = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    global ref_point, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cropping = False

        cv2.rectangle(param, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("HDMI Preview", param)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    display = cv2.resize(frame, (1280, 720))
    clone = display.copy()
    cv2.imshow("HDMI Preview", display)
    cv2.setMouseCallback("HDMI Preview", click_and_crop, clone)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        if len(ref_point) == 2:
           
            scale_x = frame.shape[1] / display.shape[1]
            scale_y = frame.shape[0] / display.shape[0]
            x1 = int(ref_point[0][0] * scale_x)
            y1 = int(ref_point[0][1] * scale_y)
            x2 = int(ref_point[1][0] * scale_x)
            y2 = int(ref_point[1][1] * scale_y)

            cropped = frame[y1:y2, x1:x2]
            filename = "WhiteLine.png"
            cv2.imwrite(filename, cropped)
            print(f"?? Saved cropped region as {filename}")

            
            cap.release()
            cv2.destroyAllWindows()

            cv2.imshow("Cropped Screenshot", cropped)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            break
        else:
            print("?? Please select a region with the mouse first.")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

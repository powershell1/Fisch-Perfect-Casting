import cv2
import numpy as np
from mss import mss
import pygetwindow as gw
import pyautogui
import time

# Get the window by title
window_title = "Roblox"
window = gw.getWindowsWithTitle(window_title)[0]

CONFIG_BOUNDING_TOP = 85
CONFIG_WINDOWS_LEAP = 10

CONFIG_DEBUG = True

# Define the bounding box for screen capture
bbox = {'top': window.top + CONFIG_BOUNDING_TOP, 'left': window.left+CONFIG_WINDOWS_LEAP, 'width': window.width - CONFIG_WINDOWS_LEAP*2, 'height': window.height - CONFIG_BOUNDING_TOP - CONFIG_WINDOWS_LEAP}

# Create an instance of mss for screen capture
sct = mss()

while True:
    # Capture the screen within the bounding box
    screenshot = sct.grab(bbox)

    # Convert the screenshot to a numpy array
    screenshot_np = np.array(screenshot)

    # Convert BGRA to BGR (OpenCV format)
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_BGRA2BGR)

    # Dummy Screen
    dummy_cv = np.zeros((screenshot_cv.shape[0], screenshot_cv.shape[1], 3), dtype=np.uint8)

    # Create a mask for green pixels
    lower_green = np.array([35, 100, 100], dtype=np.uint8)
    upper_green = np.array([85, 255, 255], dtype=np.uint8)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2HSV)

    # Create a mask for green pixels in the HSV color space
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours of the green regions
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around the contours
    for contour in green_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(dummy_cv if CONFIG_DEBUG else screenshot_cv, (x, y), (x + w, y + h), (0, 255, 255), 2)

    # Create a mask for white pixels
    lower_white = np.array([240, 240, 240], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)
    white_mask = cv2.inRange(screenshot_cv, lower_white, upper_white)

    # Apply the mask to get only white pixels
    white_pixels = cv2.bitwise_and(screenshot_cv, screenshot_cv, mask=white_mask)

    # Find contours of the white regions
    white_contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    biggest_white_contour = None

    # Draw bounding boxes around the contours
    for contour in white_contours:
        x, y, w, h = cv2.boundingRect(contour)
        if biggest_white_contour is None or w * h > cv2.contourArea(biggest_white_contour):
            biggest_white_contour = contour
        cv2.rectangle(dummy_cv if CONFIG_DEBUG else screenshot_cv, (x, y), (x + w, y + h), (255, 255, 0), 2)

    if biggest_white_contour is not None:
        if len(green_contours) == 1:
            white_contours_top = sorted(white_contours, key=lambda x: cv2.boundingRect(x)[1])
            # check if white is touching green
            x, y, w, h = cv2.boundingRect(white_contours_top[0])
            x2, y2, w2, h2 = cv2.boundingRect(green_contours[0])
            fullsize = (h+y)-y2
            progress = h/fullsize
            if progress > 0.93:
                print("Simulating mouse Up.")
                # Simulate mouse up
                pyautogui.mouseUp()

    # Display the captured image
    if CONFIG_DEBUG:
        if len(green_contours) > 1:
            cv2.putText(dummy_cv, "Green contours detected more than 1!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif len(green_contours) == 0:
            cv2.putText(dummy_cv, "Green contours not detected!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Detected", dummy_cv)

    # Display the image with bounding boxes
    cv2.imshow("App Windows", screenshot_cv)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Close all windows
cv2.destroyAllWindows()
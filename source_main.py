import cv2
import numpy as np

# Video Capture
cap = cv2.VideoCapture('a11.mp4')

# Constants/Parameters
count_line_pos = 500
min_rect_size = (50, 50)
offset = 5
car_count = 0

# Background Subtractor
algo = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

# Function for counting incoming vehicles
def center_count(x, y, w, h):
    cx = x + w // 2
    cy = y + h // 2
    return cx, cy

# Main loop to analyze frames
while True:
    ret, frame_1 = cap.read()

    # Break the loop if video capture is complete
    if not ret or frame_1 is None:
        break

    # Preprocess the frame
    gray = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply background subtraction
    img_sub = algo.apply(blur)
    dil = cv2.dilate(img_sub, np.ones((5, 5)), iterations=2)
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dila = cv2.morphologyEx(dil, cv2.MORPH_CLOSE, ker, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(dila, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw counter line
    cv2.line(frame_1, (150, count_line_pos), (1090, count_line_pos), (0, 0, 255), 4)

    # Process each contour
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        valid_counter = (w >= min_rect_size[0]) and (h >= min_rect_size[1])

        if not valid_counter:
            continue

        # Draw rectangle around cars
        cv2.rectangle(frame_1, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Get center coordinates
        center = center_count(x, y, w, h)

        # Update car count and change color of line line for counting
        if count_line_pos - offset < center[1] < count_line_pos + offset:
            car_count += 1
            cv2.line(frame_1, (125, count_line_pos), (1100, count_line_pos), (0, 127, 255), 4)
        # Display car count
        cv2.putText(frame_1, "Car Counter: " + str(int(car_count/2)), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    

    # Display the frame
    cv2.imshow('Video', frame_1)

    # Break the loop if 'Enter' key is pressed
    if cv2.waitKey(1) == 13:
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()

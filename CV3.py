import cv2
import numpy as np
import mediapipe as mp
from collections import deque
from pyfirmata import Arduino, util
import time

# Set up Arduino connection
board = Arduino('COM4')  # Update this with your Arduino port
pin = board.get_pin('d:13:o')  # Configuring pin 13 for output (LED)

# MediaPipe hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Window for drawing setup
paintWindow = np.zeros((471, 636, 3)) + 255
draw_color = (0, 0, 255)  # Color for drawing (blue)

# Store points for drawing
drawing_points = deque(maxlen=512)

# Initialize video capture with webcam
cap = cv2.VideoCapture(0)

def check_fingers_touching(finger1_tip, finger2_tip):
    """Check if the index finger and thumb are close enough to be considered as touching."""
    return np.linalg.norm(np.array(finger1_tip) - np.array(finger2_tip)) < 20

def classify_shape(pts):
    """Classify the shape of the contour formed by the points."""
    contour = np.array(pts, dtype=np.int32).reshape((-1, 1, 2))
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    if len(approx) == 3:
        return "Triangle"
    elif len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        return "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
    elif len(approx) > 4:
        return "Circle"
    return "Unknown"

drawing_active = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Draw the "CLEAR" button
    frame = cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            landmarks = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for lm in handLms.landmark]
            index_tip = landmarks[8]
            thumb_tip = landmarks[4]

            if check_fingers_touching(index_tip, thumb_tip):
                drawing_active = False
            else:
                if not drawing_active and len(drawing_points) > 10:  # Shape detection on finger release
                    shape_name = classify_shape(list(drawing_points))
                    print(f"Detected shape: {shape_name}")
                    pin.write(1 if shape_name == "Circle" else 0)
                    drawing_points.clear()

                drawing_active = True
                if 40 <= index_tip[0] <= 140 and index_tip[1] <= 65:  # Check for clear button press
                    drawing_points.clear()
                    paintWindow[:, :, :] = 255
                elif drawing_active:
                    drawing_points.append(index_tip)

    # Draw points
    for i in range(1, len(drawing_points)):
        if drawing_points[i - 1] is None or drawing_points[i] is None:
            continue
        cv2.line(frame, drawing_points[i - 1], drawing_points[i], draw_color, 2)
        cv2.line(paintWindow, drawing_points[i - 1], drawing_points[i], draw_color, 2)

    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
board.exit()  # Properly close the board connection

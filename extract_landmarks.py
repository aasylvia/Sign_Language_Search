import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
from utilities import full_normalization

# Initialize MediaPipe components
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Create a DataFrame to store landmarks
data = []

# Start video capture
cap = cv2.VideoCapture(0)

symbol = input("Enter the symbol you want to capture (a-z and numbers): ").lower()
print("Press 'c' to capture landmarks, 'q' to quit.")


while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    cv2.imshow('ASL Data Collection', frame)

    # Capture landmarks on 'c' key press
    if cv2.waitKey(5) & 0xFF == ord('c'):
        # Optionally, you can save the current frame with landmarks drawn
        print("Capturing landmarks...")

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                # Extract landmark coordinates
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

                # Normalize landmarks
                landmarks = full_normalization(landmarks)
                data.append(landmarks)

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

new_data = []
for row in data:
    current_row = []
    for column in row:
        current_row.append(f"{float(column[0])},{float(column[1])},{float(column[2])}")
    
    new_data.append(current_row)


data_df = pd.DataFrame(new_data)
data_df.to_csv(f'landmarks/{symbol}_asl_landmarks.csv', index=False)
print(f"Data saved to landmarks/{symbol}_asl_landmarks.csv")
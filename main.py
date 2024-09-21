import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os
from utilities import full_normalization

# load csv data so that we can use it to choose the best match
current_landmarks = os.listdir("landmarks")
refrence_landmarks_list = []
for landmark_file_name in current_landmarks:
    refrence_landmarks_list.append([landmark_file_name, pd.read_csv(f"landmarks/{landmark_file_name}")])

print(refrence_landmarks_list)

# refrence_landmarks = pd.read_csv("asl_landmarks.csv")
# refrence_landmarks_data = []
# for row in refrence_landmarks.values:
#     current_refrence = []
#     for point in row:
#         points = point.split(",")
#         current_refrence.append([float(i) for i in points])
    
#     refrence_landmarks_data.append(current_refrence)


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open a connection to the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # frame = cv2.flip(frame, 1)

    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and find hand landmarks
    result = hands.process(rgb_frame)

    # Draw hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = np.array([(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark])
            
            # Normalize landmarks
            landmarks = full_normalization(landmarks)

            # Compare the landmarks with the reference landmarks
            for _, refrence_landmarks in refrence_landmarks_list:
                refrence_landmarks_data = [] 
                for row in refrence_landmarks.values:
                    current_refrence = []
                    for point in row:
                        current_refrence.append([float(i) for i in point.split(",")])

                refrence_landmarks_data.append(current_refrence)

                for refrence_landmark in refrence_landmarks_data:
                    refrence_landmark = full_normalization(refrence_landmark)
                    
                    # Calculate the Euclidean distance between landmarks and reference landmarks

                    distances = np.linalg.norm(landmarks - refrence_landmark, axis=1)
                    current_match_accuracy = np.sum(distances)
                    
                    if current_match_accuracy < 4:
                        print("yess that is a four", current_match_accuracy)


    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
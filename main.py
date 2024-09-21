import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os
from time import time
from utilities import full_normalization

# load csv data so that we can use it to choose the best match
current_landmarks = os.listdir("landmarks")
refrence_landmarks_list = []
for landmark_file_name in current_landmarks:
    refrence_landmarks_list.append([landmark_file_name, pd.read_csv(f"landmarks/{landmark_file_name}")])

print(refrence_landmarks_list)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open a connection to the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

start, prev_symbol = time(), ""
word_so_far = ""
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

            # Find the best match
            best_match, best_match_score = "", 0 

            # Compare the landmarks with the reference landmarks
            for landmark_file_name, refrence_landmarks in refrence_landmarks_list:
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

                    if current_match_accuracy < 7:
                        if current_match_accuracy > best_match_score:
                            best_match = landmark_file_name.split("_")[0]
                            best_match_score = current_match_accuracy
                    

            print(best_match, best_match_score)
            
            if best_match != prev_symbol:
                start = time()
                prev_symbol = best_match
            
            if time() - start > 1:
                start = time()
                prev_symbol = best_match
                word_so_far += best_match

            frame = cv2.putText(frame, best_match, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            frame = cv2.putText(frame, word_so_far, (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os
import time
from googleapiclient.discovery import build
from utilities import full_normalization

# Initialize the Google Custom Search API
# Initialize the Google Custom Search API
def search_google(query):
    api_key = "AIzaSyDPNZC7JFRk_30vsugiHTxy--ZeiXnyOI8"  # Replace with your actual API key
    cse_id = "f71bdbf3a61d74d4f"  # Replace with your search engine ID
    service = build("customsearch", "v1", developerKey=api_key)
    
    # Perform the search
    result = service.cse().list(q=query, cx=cse_id).execute()
    return result

# Load CSV reference data for landmarks (letters)
current_landmarks = os.listdir("landmarks")
reference_landmarks_list = []
for landmark_file_name in current_landmarks:
    reference_landmarks_list.append([landmark_file_name, pd.read_csv(f"landmarks/{landmark_file_name}")])

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open a connection to the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

word_so_far = ""  # Variable to store recognized hand gestures as a search query
start = time.time()  # To track time for search trigger
prev_symbol = ""

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

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
            
            # Extract the landmarks from the hand and normalize them
            landmarks = np.array([(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark])
            landmarks = full_normalization(landmarks)

            # Match the current landmarks to the reference landmarks (letters)
            best_match, best_match_score = "", float("inf")

            for landmark_file_name, reference_landmarks in reference_landmarks_list:
                reference_landmarks_data = []
                for row in reference_landmarks.values:
                    current_reference = []
                    for point in row:
                        current_reference.append([float(i) for i in point.split(",")])
                    reference_landmarks_data.append(current_reference)
                
                for reference_landmark in reference_landmarks_data:
                    reference_landmark = full_normalization(reference_landmark)
                    
                    # Calculate Euclidean distance between the current and reference landmarks
                    distances = np.linalg.norm(landmarks - reference_landmark, axis=1)
                    current_match_accuracy = np.sum(distances)

                    # Find the closest match
                    if current_match_accuracy < best_match_score:
                        best_match = landmark_file_name.split("_")[0]  # Extract the letter/gesture
                        best_match_score = current_match_accuracy

            # If the best match is different from the previous symbol and it's reliable, update word_so_far
            if best_match != prev_symbol and best_match_score < 5:  # Adjust threshold as needed
                word_so_far += best_match
                prev_symbol = best_match
                start = time.time()

            # Display the word being constructed on the screen
            frame = cv2.putText(frame, word_so_far, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # After 3 seconds of inactivity or when the word reaches a certain length, trigger the search
    if time.time() - start > 3 and len(word_so_far) > 0:
        print(f"Searching Google for: {word_so_far}")
        
        # Perform the Google search with the word_so_far as the query
        search_results = search_google(word_so_far)
        
        # Display the search results
        if 'items' in search_results:
            for index, item in enumerate(search_results['items']):
                print(f"{index+1}. {item['title']}")
                print(f"Link: {item['link']}\n")
        
        # Reset word_so_far and timer after search
        word_so_far = ""
        start = time.time()  # Reset the start time after the search is performed

    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()


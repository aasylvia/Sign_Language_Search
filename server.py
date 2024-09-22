from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2, os
import numpy as np
from PIL import Image
import io
import mediapipe as mp
import pandas as pd
from utilities import full_normalization
from time import time

app = Flask(__name__)
CORS(app)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Load csv data so that we can use it to choose the best match
current_landmarks = os.listdir("landmarks")
refrence_landmarks_list = []
for landmark_file_name in current_landmarks:
    refrence_landmarks_list.append([landmark_file_name, pd.read_csv(f"landmarks/{landmark_file_name}")])

start, prev_symbol = time(), ""
word_so_far = ""

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/upload', methods=['POST'])
def upload_frame():
    global prev_symbol, start, word_so_far
    if 'frame' not in request.files:
        return 'No frame part', 400

    frame = request.files['frame']

    # Read the image in memory
    image_stream = io.BytesIO(frame.read())
    image = Image.open(image_stream)
    image = np.array(image)

    # Convert RGB to BGR (OpenCV uses BGR format)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Process the frame and find hand landmarks
    result = hands.process(image)
    frame = image

    # Draw hand landmarks
    if result.multi_hand_landmarks:
        print("Hand detected")
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = np.array([(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark])
            
            # Normalize landmarks
            landmarks = full_normalization(landmarks)

            # Find the best match
            best_match, best_match_score = "", float("inf") 

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

                    if current_match_accuracy < 5:
                        if current_match_accuracy < best_match_score:
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
    
    
    # cv2.imwrite('uploaded_framehasdfasdf.png', frame)
    # cv2.waitKey(1)
    
    # frame.save('uploaded_frame.png')  # Save the frame to a file
    if prev_symbol:
        return jsonify({"symbol": prev_symbol}), 200
    
    return jsonify({"status": 'Frame received'}), 200

if __name__ == '__main__':
    app.run(debug=False, port=8081)
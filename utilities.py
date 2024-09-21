import numpy as np

# Function to normalize the landmarks relative to the wrist
def normalize_landmarks(landmarks):
    # Get the wrist coordinates (landmark 0)
    wrist = landmarks[0]
    
    # Subtract the wrist coordinates from all landmarks to make the wrist the origin
    normalized_landmarks = [(lm[0] - wrist[0], lm[1] - wrist[1], lm[2] - wrist[2]) for lm in landmarks]
    
    return normalized_landmarks


# Function to scale landmarks based on the distance between wrist and middle fingertip (landmark 12)
def scale_landmarks(landmarks):
    wrist = np.array(landmarks[0])
    middle_finger_tip = np.array(landmarks[12])
    
    # Calculate the distance between the wrist and the middle fingertip
    hand_size = np.linalg.norm(wrist - middle_finger_tip)
    
    # Scale landmarks by the hand size
    scaled_landmarks = [(lm[0] / hand_size, lm[1] / hand_size, lm[2] / hand_size) for lm in landmarks]
    
    return scaled_landmarks


# Full normalization: relative positioning and scaling
def full_normalization(landmarks):
    # Step 1: Normalize relative to the wrist
    normalized_landmarks = normalize_landmarks(landmarks)
    
    # Step 2: Scale based on hand size (wrist to middle fingertip distance)
    scaled_landmarks = scale_landmarks(normalized_landmarks)
    
    return scaled_landmarks


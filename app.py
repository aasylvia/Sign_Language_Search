from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mediapipe as mp
import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
from utilities import full_normalization

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React

@app.route('/')
def home():
    return "Welcome to the Home Page"


# Google Custom Search API settings
GOOGLE_SEARCH_API = 'https://www.googleapis.com/customsearch/v1'
API_KEY = os.getenv('GOOGLE_API_KEY')  # Fetch API key from .env
CX = os.getenv('GOOGLE_CX')  # Fetch search engine ID from .env

# Load pre-recorded landmarks
def load_landmarks():
    reference_landmarks_list = []
    current_landmarks = os.listdir("landmarks")
    for landmark_file_name in current_landmarks:
        reference_landmarks_list.append([landmark_file_name, pd.read_csv(f"landmarks/{landmark_file_name}")])
    return reference_landmarks_list

reference_landmarks_list = load_landmarks()

# Perform search with Google Custom Search API
def perform_search(query):
    params = {
        'key': API_KEY,
        'cx': CX,
        'q': query
    }
    response = requests.get(GOOGLE_SEARCH_API, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Normalize landmarks and compare with reference landmarks
def recognize_sign(landmarks):
    landmarks = full_normalization(np.array(landmarks))
    best_match, best_match_score = "", float("inf")

    for landmark_file_name, reference_landmarks in reference_landmarks_list:
        reference_landmarks_data = []
        for row in reference_landmarks.values:
            current_reference = [float(i) for i in row[0].split(",")]
            reference_landmarks_data.append(current_reference)

        distances = np.linalg.norm(landmarks - np.array(reference_landmarks_data), axis=1)
        current_match_accuracy = np.sum(distances)

        if current_match_accuracy < best_match_score:
            best_match = landmark_file_name.split("_")[0]
            best_match_score = current_match_accuracy

    return best_match

# Route for recognition and search
@app.route('/recognize_and_search', methods=['POST'])
def recognize_and_search():
    data = request.json
    landmarks = data.get('landmarks')

    if not landmarks:
        return jsonify({'error': 'No landmarks provided'}), 400

    recognized_symbol = recognize_sign(landmarks)
    
    if recognized_symbol:
        search_results = perform_search(recognized_symbol)
        if search_results:
            formatted_results = [
                {'title': item['title'], 'link': item['link'], 'snippet': item['snippet']}
                for item in search_results.get('items', [])
            ]
            return jsonify({'recognized_symbol': recognized_symbol, 'search_results': formatted_results})
        return jsonify({'recognized_symbol': recognized_symbol, 'search_results': []})
    return jsonify({'error': 'No matching sign found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

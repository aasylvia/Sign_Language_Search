from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/upload', methods=['POST'])
def upload_frame():
    if 'frame' not in request.files:
        return 'No frame part', 400

    frame = request.files['frame']
    frame.save('uploaded_frame.png')  # Save the frame to a file
    return 'Frame received', 200

if __name__ == '__main__':
    app.run(debug=True, port=8081)
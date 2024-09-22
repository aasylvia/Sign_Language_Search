// import React, { useState, useRef } from 'react';
// import '@fortawesome/fontawesome-free/css/all.min.css'; // Font Awesome for icons
// import './App.css'; // Import your CSS
// import { Hands } from '@mediapipe/hands'; // MediaPipe Hands
// import { Camera } from '@mediapipe/camera_utils'; // MediaPipe Camera Utils

// function App() {
//   const [query, setQuery] = useState(''); // Search query state (to be filled with recognized signs)
//   const [isCameraActive, setCameraActive] = useState(false); // Camera state
//   const videoRef = useRef(null); // Reference to the video element
//   const [recognizedWord, setRecognizedWord] = useState(""); // Holds the recognized word so far

//   // Start the webcam when the sign language button is clicked
//   const startCamera = () => {
//     setCameraActive(true);

//     navigator.mediaDevices.getUserMedia({ video: true })
//       .then(stream => {
//         const video = videoRef.current;
//         video.srcObject = stream;

//         // Wait for the video stream to be fully loaded before playing
//         video.onloadedmetadata = () => {
//           video.play(); // Play video once metadata is loaded
//         };

//         // Initialize MediaPipe Hands
//         const hands = new Hands({
//           locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
//         });

//         hands.setOptions({
//           maxNumHands: 1,
//           minDetectionConfidence: 0.7,
//           minTrackingConfidence: 0.5,
//         });

//         // Handle results and detect hand landmarks
//         hands.onResults(handleHandLandmarks);

//         // Set up the camera for MediaPipe to process frames
//         const camera = new Camera(videoRef.current, {
//           onFrame: async () => {
//             try {
//               await hands.send({ image: videoRef.current });
//             } catch (error) {
//               console.error("Error in sending frame to MediaPipe:", error);
//             }
//           },
//           width: 640,
//           height: 480,
//         });
//         camera.start(); // Ensure this is inside the then block
//       })
//       .catch(err => {
//         console.error("Error accessing webcam:", err);
//       });
//   };

//   // Function to process the hand landmarks and fill the search bar
//   const handleHandLandmarks = (results) => {
//     if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
//       const handLandmarks = results.multiHandLandmarks[0];
      
//       // Here we can process hand landmarks and recognize a sign
//       // For demonstration, let's assume the landmarks give us a letter (you can replace this logic with actual sign recognition)
//       const recognizedLetter = "A"; // You would replace this with actual recognition logic
//       updateRecognizedWord(recognizedLetter);
//     }
//   };

//   // Function to update the recognized word based on hand gestures
//   const updateRecognizedWord = (letter) => {
//     setRecognizedWord((prevWord) => prevWord + letter);
//     setQuery((prevQuery) => prevQuery + letter); // This updates the search bar
//   };

//   // Handle input changes manually for text entry
//   const handleInputChange = (e) => {
//     setQuery(e.target.value);
//   };

//   return (
//     <div className="App">
//       <div className="search-bar-container">
//         {/* Search Input Field (filled by hand recognition or user input) */}
//         <input 
//           type="text" 
//           value={query} 
//           onChange={handleInputChange} 
//           placeholder="Search the web" 
//         />
        
//         {/* Button for Voice Search */}
//         <button onClick={() => console.log('Voice search triggered')}>
//           <i className="fa fa-microphone"></i>
//         </button>
        
//         {/* Button for Image Search */}
//         <button onClick={() => console.log('Image search triggered')}>
//           <i className="fa fa-camera"></i>
//         </button>
        
//         {/* Button for Sign Language Search (Starts the webcam) */}
//         <button onClick={startCamera}>
//           <i className="fa fa-hand-paper"></i>
//         </button>

//         {/* Button to Trigger Search */}
//         <button onClick={() => console.log("Searching for:", query)}>Search</button>
//       </div>

//       {/* Display Webcam Feed When Camera Is Active */}
//       {isCameraActive && (
//         <div className="camera-container">
//           <video ref={videoRef} style={{ width: "400px", height: "400px", transform: "scaleX(-1)" }}></video> 
//         </div>
//       )}

//       {/* Display the recognized word */}
//       <div className="recognized-word">
//         <h3>Recognized Word: {recognizedWord}</h3>
//       </div>
//     </div>
//   );
// }

// export default App;


import React, { useRef, useEffect, useState } from 'react';
import { Hands } from '@mediapipe/hands';
import { Camera } from '@mediapipe/camera_utils';
import './App.css'; // Your custom styles

function App() {
  const videoRef = useRef(null); // Reference to the video element
  const canvasRef = useRef(null); // Reference to the canvas element for drawing
  const [isCameraActive, setCameraActive] = useState(false); // Camera state
  const [detectedHand, setDetectedHand] = useState(null); // State to hold detected hand landmarks
  
  // Start the webcam and hand detection
  const startCamera = () => {
    setCameraActive(true);

    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        const video = videoRef.current;
        video.srcObject = stream;

        video.onloadedmetadata = () => {
          video.play(); // Start video once metadata is loaded
        };

        // Initialize MediaPipe Hands for hand tracking
        const hands = new Hands({
          locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
        });

        hands.setOptions({
          maxNumHands: 2,
          minDetectionConfidence: 0.7,
          minTrackingConfidence: 0.5,
        });

        hands.onResults(onHandResults); // Set up callback for hand detection results

        // Initialize camera feed for MediaPipe processing
        const camera = new Camera(videoRef.current, {
          onFrame: async () => {
            await hands.send({ image: videoRef.current });
          },
          width: 640,
          height: 480,
        });
        camera.start(); // Start the camera feed
      })
      .catch((err) => {
        console.error("Error accessing webcam:", err);
      });
  };

  // Callback for processing hand detection results
  const onHandResults = (results) => {
    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
      const handLandmarks = results.multiHandLandmarks[0];
      setDetectedHand(handLandmarks); // Set detected hand landmarks in state
      drawHandLandmarks(handLandmarks); // Draw landmarks on the canvas
    }
  };

  // Draw hand landmarks on the canvas
  const drawHandLandmarks = (landmarks) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

    ctx.strokeStyle = '#00FF00'; // Green color for hand landmarks
    ctx.lineWidth = 5;

    landmarks.forEach((landmark) => {
      const x = landmark.x * canvas.width;
      const y = landmark.y * canvas.height;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, 2 * Math.PI);
      ctx.fill();
    });
  };

  return (
    <div className="App">
      <h1>Hand Detection</h1>

      {/* Video feed from webcam */}
      <div className="video-container">
        <video ref={videoRef} style={{ display: isCameraActive ? 'block' : 'none' }} />
        <canvas ref={canvasRef} width="640" height="480" />
      </div>

      <button onClick={startCamera}>Start Camera</button>

      {/* Display detected hand landmarks in text format */}
      {detectedHand && (
        <div className="hand-data">
          <h2>Detected Hand Landmarks:</h2>
          <pre>{JSON.stringify(detectedHand, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

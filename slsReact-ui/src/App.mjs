
import React, { useState, useRef, useEffect } from 'react';
import '@fortawesome/fontawesome-free/css/all.min.css'; // Font Awesome for icons
import './App.css'; // Import your CSS
import '@mediapipe/hands';
import '@mediapipe/camera_utils';

function App() {
  const [query, setQuery] = useState(''); // Search query state
  const [isCameraActive, setCameraActive] = useState(false); // Camera state
  const videoRef = useRef(null); // Reference to the video element
  const canvasRef = useRef(null); // Reference to the canvas element

  // Function to handle input changes in the search bar
  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  // Simulate search query submission (replace with API call later)
  const handleSearch = () => {
    console.log("Searching for:", query);
    // Integrate search functionality or API here
  };

  // Start the webcam when the sign language button is clicked
  const startCamera = () => {
    setCameraActive(true);

    // Accessing the user's webcam feed
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        let video = videoRef.current;
        video.srcObject = stream;
        video.play();
      })
      .catch(err => {
        console.error("Error accessing webcam: ", err);
      });
  };

  // Function to capture frame from video and send to backend
  const captureFrameAndSend = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    // Set canvas dimensions to match video dimensions
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the current video frame onto the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas content to a Blob
    canvas.toBlob(async (blob) => {
      if (blob) {
        // Send the Blob to the backend
        const formData = new FormData();
        formData.append('frame', blob, 'frame.png');

        try {
            const response = await fetch('http://localhost:8081/upload', {
            method: 'POST',
            body: formData,
          });

          if (response.ok) {
            console.log('Frame sent successfully');
          } else {
            console.error('Error sending frame:', response.statusText);
          }
        } catch (error) {
          console.error('Error sending frame:', error);
        }
      }
    }, 'image/png');
  };

  // Use effect to start capturing frames when the camera is active
  useEffect(() => {
    if (isCameraActive) {
      alert("camera activate");
      const intervalId = setInterval(captureFrameAndSend, 50); // Capture frame every second
      captureFrameAndSend(); // Capture frame immediately
      return () => clearInterval(intervalId); // Cleanup interval on component unmount or camera deactivation
    }
  }, [isCameraActive]);

  return (
    <div className="App">
      <div className="search-bar-container">
        {/* Search Input Field */}
        <input 
          type="text" 
          value={query} 
          onChange={handleInputChange} 
          placeholder="Search the web" 
        />
        
        {/* Button for Voice Search */}
        <button onClick={() => console.log('Voice search triggered')}>
          <i className="fa fa-microphone"></i>
        </button>
        
        {/* Button for Image Search */}
        <button onClick={() => console.log('Image search triggered')}>
          <i className="fa fa-camera"></i>
        </button>
        
        {/* Button for Sign Language Search (Starts the webcam) */}
        <button onClick={startCamera}>
          <i className="fa fa-hand-paper"></i>
        </button>

        {/* Button to Trigger Search */}
        <button onClick={handleSearch}>Search</button>
      </div>

      {/* Display Webcam Feed When Camera Is Active */}
      {isCameraActive && (
        <div className="camera-container">
          <video ref={videoRef} style={{ width: "400px", height: "400px", transform: "scaleX(-1)" }}></video> 
          <canvas ref={canvasRef} style={{ display: 'none' }}></canvas> {/* Assign canvasRef to canvas element */}
        </div>
      )}
    </div>
  );
}

export default App;

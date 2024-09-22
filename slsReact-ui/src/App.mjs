
import React, { useState, useRef } from 'react';
import '@fortawesome/fontawesome-free/css/all.min.css'; // Font Awesome for icons
import './App.css'; // Import your CSS
import '@mediapipe/hands';
import '@mediapipe/camera_utils';

function App() {
  const [query, setQuery] = useState(''); // Search query state
  const [isCameraActive, setCameraActive] = useState(false); // Camera state
  const videoRef = useRef(null); // Reference to the video element

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
        </div>
      )}
    </div>
  );
}

export default App;

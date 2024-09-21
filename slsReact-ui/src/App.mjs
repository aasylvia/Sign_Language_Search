import React, { useState } from 'react';
import './App.css';

function App() {
  // State to store the search query entered by the user
  const [query, setQuery] = useState('');

  // Function to handle input changes in the search bar
  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  // Function to simulate the search query submission (replace this with actual search API call)
  const handleSearch = () => {
    console.log("Searching for:", query);
    // Here you would integrate the Google Custom Search API or handle gesture recognition
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
        
        {/* Button for Sign Language Search */}
        <button onClick={() => console.log('Sign language search triggered')}>
          <i className="fa fa-hand-paper"></i>
        </button>

        {/* Button to Trigger Search */}
        <button onClick={handleSearch}>Search</button>
      </div>
    </div>
  );
}

export default App;

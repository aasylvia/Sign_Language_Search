/* global cv */ // Declare cv as a global variable for ESLint

import React, { useRef, useEffect } from "react";

function OpenCVComponent() {
    const canvasRef = useRef(null);
    const videoRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");
        const video = videoRef.current;

        // Initialize OpenCV
        cv.onRuntimeInitialized = () => {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((stream) => {
                    video.srcObject = stream;
                    video.play();
                });

            // Process video frames
            const processVideo = () => {
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                let src = cv.imread(canvas); // Read the image from the canvas
                let dst = new cv.Mat();
                
                // Example: Convert to grayscale
                cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
                
                // Write the result back to the canvas
                cv.imshow(canvas, dst);
                src.delete(); // Free memory
                dst.delete(); // Free memory
                requestAnimationFrame(processVideo); // Call the next frame
            };
            requestAnimationFrame(processVideo); // Start processing
        };
    }, []);

    return (
        <div>
            <h2>OpenCV in React</h2>
            <video ref={videoRef} style={{ display: "none" }}></video>
            <canvas ref={canvasRef} width="640" height="480"></canvas>
        </div>
    );
}

export default OpenCVComponent;

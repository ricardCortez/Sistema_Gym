import React, { useState, useEffect, useRef } from 'react';

function CameraCapture() {
    const [capturing, setCapturing] = useState(false);
    const [imagesCaptured, setImagesCaptured] = useState(0);
    const videoRef = useRef(null);

    useEffect(() => {
        // Setup media stream
        async function setupCamera() {
            try {
                const constraints = { video: true };
                const stream = await navigator.mediaDevices.getUserMedia(constraints);
                if (videoRef.current) videoRef.current.srcObject = stream;
            } catch (error) {
                console.error('Error accessing the camera:', error);
            }
        }

        setupCamera();

        return () => {
            if (videoRef.current && videoRef.current.srcObject) {
                const tracks = videoRef.current.srcObject.getTracks();
                tracks.forEach(track => track.stop());
            }
        };
    }, []);

    useEffect(() => {
        if (capturing && imagesCaptured < 300) {
            const interval = setInterval(() => {
                if (imagesCaptured >= 300) {
                    clearInterval(interval);
                    setCapturing(false);
                    console.log('Capture complete');
                } else {
                    captureAndSendImage();
                }
            }, 50); // Adjust interval as needed for performance
            return () => clearInterval(interval);
        }
    }, [capturing, imagesCaptured]);

    const startCapture = () => {
        const video = videoRef.current;
        if (video && video.readyState === 4) {
            console.log('Starting capture...');
            setImagesCaptured(0);
            setCapturing(true);
        } else {
            console.log('Video is not ready or not playing.');
        }
    };

    const stopCapture = () => {
        setCapturing(false);
        console.log('Capturing stopped manually.');
    };

    const captureAndSendImage = () => {
        const video = videoRef.current;
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth / 2; // Make the canvas width half of the video width
        canvas.height = video.videoHeight / 2; // Make the canvas height half of the video height
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => {
            if (blob) {
                const formData = new FormData();
                formData.append('file', blob, 'capture.jpg');
                formData.append('face_id', 'default_id');  // Asegúrate de añadir el face_id
                fetch('/api/start_capture', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    setImagesCaptured(prev => prev + 1);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            } else {
                console.error('Blob was not created successfully');
            }
        }, 'image/jpeg');
    };

    return (
        <div>
            <video ref={videoRef} autoPlay playsInline style={{ width: '320px', height: '240px' }}></video> {/* Adjust the size of the video element */}
            <button onClick={startCapture}>Start Capture</button>
            <button onClick={stopCapture}>Stop Capture</button>
        </div>
    );
}

export default CameraCapture;

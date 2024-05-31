import React, { useState, useEffect, useRef } from 'react';
import Swal from 'sweetalert2';
import './style/SystemFace.css';

function Modal({ isOpen, onClose, children }) {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <button onClick={onClose} className="close-button">X</button>
                {children}
            </div>
        </div>
    );
}

function CameraCapture() {
    const [capturing, setCapturing] = useState(false);
    const [imagesCaptured, setImagesCaptured] = useState(0);
    const [showModal, setShowModal] = useState(false);
    const [trainingProgress, setTrainingProgress] = useState(0);
    const [recognizing, setRecognizing] = useState(false);
    const videoRef = useRef(null);

    useEffect(() => {
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
                    setShowModal(true);
                    Swal.fire({
                        icon: 'success',
                        title: 'Captura Completa',
                        text: 'La captura de imágenes se ha completado con éxito.',
                    });
                    stopCamera();
                    console.log('Capture complete');
                } else {
                    captureAndSendImage();
                }
            }, 100);
            return () => clearInterval(interval);
        }
    }, [capturing, imagesCaptured]);

    const startCapture = async () => {
        const video = videoRef.current;
        if (video && video.readyState === 4) {
            console.log('Starting capture...');
            setImagesCaptured(0);
            setCapturing(true);
        } else {
            console.log('Video is not ready or not playing. Setting up camera...');
            try {
                const constraints = { video: true };
                const stream = await navigator.mediaDevices.getUserMedia(constraints);
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                    videoRef.current.onloadedmetadata = () => {
                        videoRef.current.play();
                        setImagesCaptured(0);
                        setCapturing(true);
                    };
                }
            } catch (error) {
                console.error('Error accessing the camera:', error);
            }
        }
    };

    const stopCapture = () => {
        setCapturing(false);
        console.log('Capturing stopped manually.');
        if (videoRef.current && videoRef.current.srcObject) {
            const tracks = videoRef.current.srcObject.getTracks();
            tracks.forEach(track => track.stop());
            videoRef.current.srcObject = null;
        }
    };

    const stopCamera = () => {
        if (videoRef.current && videoRef.current.srcObject) {
            const tracks = videoRef.current.srcObject.getTracks();
            tracks.forEach(track => track.stop());
            videoRef.current.srcObject = null;
        }
    };

    const closeModal = () => {
        setShowModal(false);
    };

    const captureAndSendImage = () => {
        const video = videoRef.current;
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth / 2;
        canvas.height = video.videoHeight / 2;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => {
            if (blob) {
                const formData = new FormData();
                formData.append('file', blob, 'capture.jpg');
                formData.append('face_id', 'default_id');
                formData.append('current_count', imagesCaptured);
                fetch('/api/start_capture', {
                    method: 'POST',
                    body: formData,
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        if (data.status === 'success' && data.captured) {
                            setImagesCaptured(data.new_count);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            } else {
                console.error('Blob was not created successfully');
            }
        }, 'image/jpeg');
    };

    const trainModel = () => {
        console.log('Iniciando el entrenamiento del modelo...');
        fetch('/api/train_model', {
            method: 'POST',
        })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                if (data.status === 'success') {
                    setTrainingProgress(100);
                    alert('Entrenamiento iniciado correctamente.');
                } else {
                    alert('Error al iniciar el entrenamiento: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error al conectar con el servidor:', error);
                alert('Error al conectar con el servidor: ' + error);
            });
    };

    const recognizeFaces = () => {
        console.log('Iniciando el reconocimiento de rostros...');
        fetch('/api/recognize_faces', {
            method: 'POST',
        })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                alert(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al conectar con el servidor: ' + error);
            });
    };

    return (
        <div className="main-container">
            <div className="camera-container">
                <div className="video-container">
                    <video ref={videoRef} autoPlay playsInline></video>
                    <div className="progress-bar-container">
                        <progress value={imagesCaptured} max="300"></progress>
                        <span>{imagesCaptured} / 300 imágenes capturadas</span>
                    </div>
                </div>
                <div className="controls">
                    <button onClick={startCapture} className="systemFace-button">Iniciar Captura</button>
                    <button onClick={stopCapture} className="systemFace-button">Detener Captura</button>
                </div>
                <Modal isOpen={showModal} onClose={closeModal}>
                    <p>La captura de imágenes se ha completado.</p>
                </Modal>
            </div>

            <div className="training-model">
                <button onClick={trainModel} className="train-button">Entrenar Modelo</button>
                <div className="progress-bar-container">
                    <progress value={trainingProgress} max="100"></progress>
                    <span>{trainingProgress}% de entrenamiento completado</span>
                </div>
            </div>
        </div>
    );
}

export default CameraCapture;

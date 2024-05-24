import React, { useState } from 'react';
import './style/SystemDetection.css'; // Asegúrate de crear este archivo CSS

function FaceRecognitionStarter() {
    const [status, setStatus] = useState('');

    const startRecognition = async () => {
        setStatus('Iniciando reconocimiento...');
        try {
            const response = await fetch('/api/recognize_faces', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            const data = await response.json();
            if (data.status === 'success') {
                setStatus('Reconocimiento iniciado con éxito. Esperando resultados...');
            } else {
                setStatus('Error al iniciar el reconocimiento.');
            }
        } catch (error) {
            console.error('Error al iniciar el reconocimiento:', error);
            setStatus('Error de conexión con el servidor.');
        }
    };

    return (
        <div className="recognition-container">
            <button onClick={startRecognition} className="start-button">Iniciar Reconocimiento de Rostros</button>
            <p className="status-message">{status}</p>
        </div>
    );
}

export default FaceRecognitionStarter;

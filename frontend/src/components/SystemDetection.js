import React, { useState } from 'react';

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
                setStatus('Reconocimiento en progreso...');
                checkValidation();
            } else {
                setStatus('Error al iniciar el reconocimiento.');
            }
        } catch (error) {
            console.error('Error al iniciar el reconocimiento:', error);
            setStatus('Error de conexión con el servidor.');
        }
    };

    const checkValidation = async () => {
        const interval = setInterval(async () => {
            try {
                const response = await fetch('/api/check_validation_status');
                const data = await response.json();
                if (data.status === 'validated') {
                    setStatus('Usuario validado.');
                    clearInterval(interval);
                }
            } catch (error) {
                console.error('Error al verificar el estado de validación:', error);
                setStatus('Error al validar el usuario.');
                clearInterval(interval);
            }
        }, 2000); // Polling cada 2 segundos
    };

    return (
        <div className="recognition-container">
            <button onClick={startRecognition} className="start-button">Iniciar Reconocimiento de Rostros</button>
            <p className="status-message">{status}</p>
        </div>
    );
}

export default FaceRecognitionStarter;

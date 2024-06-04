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
    const [canCapture, setCanCapture] = useState(false);  // Controla la habilidad de iniciar la captura
    const [imagesCaptured, setImagesCaptured] = useState(0);
    const [showModal, setShowModal] = useState(false);
    const [trainingProgress, setTrainingProgress] = useState(0);
    const [recognizing, setRecognizing] = useState(false);
    const [socioData, setSocioData] = useState({
        nombre: '',
        apellidos: '',
        codigo_unico: '',
        direccion: '',
        telefono: '',
        fecha_nacimiento: '',
        fecha_registro: '',
        estado_membresia: ''
    });

    const videoRef = useRef(null);

    // Verifica si todos los campos requeridos están llenos para habilitar el botón de captura
    useEffect(() => {
        const requiredFields = ['nombre', 'apellidos', 'direccion', 'telefono', 'fecha_nacimiento', 'fecha_registro', 'estado_membresia'];
        const allFieldsFilled = requiredFields.every(field => socioData[field].trim() !== '');
        setCanCapture(allFieldsFilled);
    }, [socioData]);

    const handleInputChange = (event) => {
        setSocioData(prevState => ({
            ...prevState,
            [event.target.name]: event.target.value
        }));
    };

    const saveSocioData = () => {
        fetch('/api/save_socio_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(socioData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                Swal.fire('Guardado', 'Los datos del socio han sido guardados correctamente.', 'success');
            } else {
                Swal.fire('Error', data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire('Error', 'Error al conectar con el servidor: ' + error, 'error');
        });
    };


    // // Efecto para controlar la habilidad de capturar basado en la validez de los datos
    // useEffect(() => {
    //     setCanCapture(validateData());
    // }, [socioData]);  // Dependiendo de socioData para reevaluar cuando los datos cambian

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
        fetch('/api/generate_unique_code')
            .then(response => response.json())
            .then(data => {
                setSocioData(currentData => ({ ...currentData, codigo_unico: data.codigo_unico }));
            })
            .catch(error => console.error('Error fetching unique code:', error));
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
                formData.append('codigo_unico', socioData.codigo_unico);  // Asegúrate que esto esté siendo enviado correctamente
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
                    <button onClick={startCapture} className="systemFace-button" disabled={!canCapture}>Iniciar Captura</button>
                    <button onClick={stopCapture} className="systemFace-button">Detener Captura</button>
                </div>
                <form>
                    <input type="text" name="nombre" placeholder="Nombre" value={socioData.nombre}
                           onChange={handleInputChange}/>
                    <input type="text" name="apellidos" placeholder="Apellidos" value={socioData.apellidos}
                           onChange={handleInputChange}/>
                    <input type="text" name="codigo_unico" placeholder="Código Único" value={socioData.codigo_unico}
                           disabled/>
                    <input type="text" name="direccion" placeholder="Direccion" value={socioData.direccion}
                           onChange={handleInputChange}/>
                    <input type="text" name="telefono" placeholder="Telefono" value={socioData.telefono}
                           onChange={handleInputChange}/>
                    <input type="date" name="fecha_nacimiento" placeholder="Fecha de Nacimiento"
                           value={socioData.fecha_nacimiento}
                           onChange={handleInputChange}/>
                    <input type="date" name="fecha_registro" placeholder="Fecha de Registro"
                           value={socioData.fecha_registro}
                           onChange={handleInputChange}/>
                    <select name="estado_membresia" value={socioData.estado_membresia} onChange={handleInputChange}>
                        <option value="">Seleccione el estado de membresía</option>
                        <option value="activo">Activo</option>
                        <option value="inactivo">Inactivo</option>
                        <option value="suspendido">Suspendido</option>
                    </select>
                </form>
                    <button onClick={saveSocioData} className="save-button">Guardar Datos del Socio</button>
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

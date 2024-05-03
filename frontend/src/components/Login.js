import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import './style/Login.css'; // Asegúrate de que la ruta del estilo es correcta
import imageLogo from './image/image_logo.jpeg';
import { useUser } from './UserContext'; // Asegúrate de que la ruta es correcta


function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { setUser } = useUser();
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!username || !password) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Por favor, complete todos los campos.',
            });
            return;
        }

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                const data = await response.json();
                setUser(data); // Actualiza el estado del usuario con los datos obtenidos
                console.log("Usuario logueado:", data);
                Swal.fire({
                    icon: 'success',
                    title: 'Inicio de sesión exitoso',
                    text: 'Has sido logueado correctamente.',
                });
                navigate('/Dashboard'); // Usa history.push para redirigir
            } else {
                const errorData = await response.json();
                Swal.fire({
                    icon: 'error',
                    title: 'Inicio de sesión fallido',
                    text: errorData.message,
                });
            }
        } catch (error) {
            console.error("Error en la petición:", error);
            Swal.fire({
                icon: 'error',
                title: 'Error de conexión',
                text: 'No se pudo conectar con el servidor.',
            });
        }
    };

    return (
        <div className="login-container">
            <div className="login-content">
                <div className="login-image">
                    <img src={imageLogo} alt="Logo" />
                </div>
                <div className="login-form">
                    <form onSubmit={handleSubmit}>
                        <label htmlFor="username">Usuario</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Ingresa tu usuario"
                        />
                        <label htmlFor="password">Contraseña</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Ingresa tu contraseña"
                        />
                        <button type="submit">Iniciar Sesión</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Login;

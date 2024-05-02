import React, { useState } from 'react';
import Swal from 'sweetalert2';
import './components/style/Login.css'; // Asegúrate de importar el CSS adecuadamente
import imageLogo from './components/image/image_logo.jpeg';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

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

            const data = await response.json();
            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Inicio de sesión exitoso',
                    text: 'Has sido logueado correctamente.',
                });
                // Redirigir al usuario o actualizar el estado global
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Inicio de sesión fallido',
                    text: data.message,
                });
            }
        } catch (error) {
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

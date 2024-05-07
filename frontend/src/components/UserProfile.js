import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import { useTheme } from './ThemeContext';

import './style/UserProfile.css';

const UserProfile = () => {
    const { theme } = useTheme();  // Obtiene el tema actual del contexto
    const [user, setUser] = useState({
        nombre: '',
        tipo_usuario: '',
        email: ''
    });

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('/api/get_user', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include'
            });
            const data = await response.json();
            if (response.ok) {
                setUser(data.user);
            } else {
                console.error('Failed to fetch user data:', data.message);
            }
        };

        fetchData();
    }, []);

    const handleEdit = async (field, currentValue) => {
        let inputValue = currentValue;
        let inputOptions = {};

        if (field === 'tipo_usuario') {
            inputOptions = {
                'admin': 'Admin',
                'dueño': 'Dueño',
                'counter': 'Counter'
            };

            const { value: userType } = await Swal.fire({
                title: 'Select user type',
                input: 'radio',
                inputOptions: inputOptions,
                inputValue: currentValue,
                showCancelButton: true,
                inputValidator: (value) => {
                    if (!value) {
                        return 'You need to choose something!';
                    }
                }
            });

            inputValue = userType;
        } else {
            const { value: newValue } = await Swal.fire({
                title: `Edit ${field}`,
                input: 'text',
                inputValue: currentValue,
                showCancelButton: true,
                confirmButtonText: 'Save',
                cancelButtonText: 'Cancel',
                inputValidator: (value) => {
                    if (!value) {
                        return 'You need to write something!';
                    }
                }
            });

            inputValue = newValue;
        }

        if (inputValue && inputValue !== currentValue) {
            updateUser(field, inputValue);
        }
    };

    const updateUser = async (field, newValue) => {
        const updatedInfo = { id: user.id, [field]: newValue };
        const response = await fetch('/api/update_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(updatedInfo)
        });

        const data = await response.json();
        if (response.ok) {
            setUser({ ...user, [field]: newValue });
            Swal.fire('Updated!', 'Your user information has been updated.', 'success');
        } else {
            Swal.fire('Error!', data.message, 'error');
        }
    };

    return (
        <div className={`user-profile ${theme}`}>
            <h1>User Profile</h1>
            <div className="profile-item">
                <span>Nombre: {user.nombre}</span>
                <button className="edit-btn" onClick={() => handleEdit('nombre', user.nombre)}>Edit</button>
            </div>
            <div className="profile-item">
                <span>Tipo de Usuario: {user.tipo_usuario}</span>
                <button className="edit-btn" onClick={() => handleEdit('tipo_usuario', user.tipo_usuario)}>Edit</button>
            </div>
            <div className="profile-item">
                <span>Email: {user.email}</span>
                <button className="edit-btn" onClick={() => handleEdit('email', user.email)}>Edit</button>
            </div>
        </div>
    );
}

export default UserProfile;

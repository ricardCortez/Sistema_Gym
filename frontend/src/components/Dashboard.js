import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMenu } from './Utils';
import { useTheme } from './ThemeContext';  // Verifica que la ruta a ThemeContext sea correcta
import './style/Dashboard.css';

// Importa las imágenes
import logoImage from './image/image_logo.jpeg';
import userAvatar from './image/user-avatar.png';

const Dashboard = () => {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const [user, setUser] = useState(null);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch('/api/get_user', {
          method: 'GET',
          credentials: 'include'
        });
        const data = await response.json();
        if (response.ok) {
          setUser(data.user);
        } else {
          navigate('/login');
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
        navigate('/login');
      }
    };

    fetchUserData();
  }, [navigate]);

  if (!user) {
    return <div>Loading...</div>;
  }

  const links = getMenu(user.tipo_usuario);

  const handleLinkClick = (url) => {
    navigate(url);
  };

  const handleLogout = async () => {
    try {
      const response = await fetch('/logout', {
          method: 'POST',
          credentials: 'include'
      });
      if (response.ok) {
          setUser(null);
          navigate('/login');
      } else {
          const errorData = await response.json();
          console.error("Logout failed:", errorData.message);
      }
    } catch (error) {
        console.error("Error al cerrar sesión:", error);
    }
  };

  const toggleDropdown = () => {
    setShowDropdown(!showDropdown);
  };

  const handleSettingsClick = (event) => {
  event.stopPropagation();  // Detiene la propagación del evento
  toggleTheme();  // Aquí asumo que quieres cambiar el tema con este botón, ajusta según lo que debe hacer el botón
};

  return (
    <div className={`dashboard ${theme}`}>
      <div className="sidebar">
        <div className="logo-settings">
          <img src={logoImage} alt="Logo" className="sidebar-logo" onClick={() => navigate('/dashboard')} />
        </div>
        {links.map((link, index) => (
          <button key={index} onClick={() => handleLinkClick(link.url)} className="sidebar-link">
            {link.name}
          </button>
        ))}
      </div>
      <div className="main-content">
        <header className="top-bar">
          <h1>Dashboard</h1>

          <div className="user-info" onClick={toggleDropdown}>
          <i className="fas fa-cog settings-icon" onClick={handleSettingsClick}></i>
            <img src={userAvatar} alt="User Avatar" className="user-avatar"/>
            <div className="user-text">
              <div className="user-name">{user.nombre}</div>
              <div className="user-role">{user.tipo_usuario}</div>
            </div>
            {showDropdown && (
              <div className="dropdown-menu">
                <a href="#profile">Profile</a>
                <a href="#inbox">Inbox</a>
                <button onClick={handleLogout}>Cerrar Sesión</button>
              </div>
            )}

          </div>
        </header>
        <main className="content">
          {/* Contenido dinámico aquí */}

        </main>
      </div>
    </div>
  );
};

export default Dashboard;

import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import './App.css';
import { ThemeProvider } from './components/ThemeContext';

function App() {
  return (
    <ThemeProvider> {/* Envuelve todos los componentes en ThemeProvider */}
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/" element={<Navigate replace to="/login" />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;

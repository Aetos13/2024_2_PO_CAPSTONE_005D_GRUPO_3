import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import ResetPass from './components/ResetPass';

function App() {
    return (
        <Router>
            <Routes>
                {/* Redirige al login por defecto */}
                <Route path="/" element={<Navigate to="/login" />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/reset_password" element={<ResetPass />} />
            </Routes>
        </Router>
    );
}

export default App;
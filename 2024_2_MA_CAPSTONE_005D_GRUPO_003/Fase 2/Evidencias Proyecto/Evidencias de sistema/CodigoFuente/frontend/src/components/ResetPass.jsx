import React, { useState } from 'react';
import axios from 'axios';

function ResetPassword() {
  const [email, setEmail] = useState('');

  const handleResetPassword = async () => {
    try {
      await axios.post('http://localhost:5000/reset_password', { email });
      console.log('Correo de recuperación enviado');
    } catch (error) {
      console.error('Error en restablecimiento de contraseña:', error);
    }
  };

  return (
    <div>
      <h2>Restablecer Contraseña</h2>
      <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <button onClick={handleResetPassword}>Restablecer Contraseña</button>
    </div>
  );
}

export default ResetPassword;
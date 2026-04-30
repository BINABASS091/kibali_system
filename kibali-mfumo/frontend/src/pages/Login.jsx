import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../api';
import './Login.css';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(username, password);
      const { access_token, user } = response.data;
      
      onLogin(access_token, user);
      navigate('/dashboard');
    } catch (err) {
      setError('Jina la mtumiaji au neno siri si sahihi');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>KIBALI CHA UJENZI</h1>
          <p>Serekali ya Mapinduzi ya Zanzibar</p>
        </div>
        
        <form onSubmit={handleSubmit}>
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="username">Jina la Mtumiaji</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Ingiza jina lako"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Neno Siri</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Ingiza neno siri lako"
              required
            />
          </div>

          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Inatumia...' : 'Ingia'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;

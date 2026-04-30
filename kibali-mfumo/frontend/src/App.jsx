import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import CreatePermit from './pages/CreatePermit';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('access_token');
    const userInfo = localStorage.getItem('user');
    
    if (token && userInfo) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userInfo));
    }
    setLoading(false);
  }, []);

  const handleLogin = (token, userInfo) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user', JSON.stringify(userInfo));
    setIsAuthenticated(true);
    setUser(userInfo);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
  };

  if (loading) {
    return <div className="loading">Inatumia...</div>;
  }

  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        <Route 
          path="/login" 
          element={
            isAuthenticated ? 
            <Navigate to="/dashboard" /> : 
            <Login onLogin={handleLogin} />
          } 
        />
        <Route 
          path="/dashboard" 
          element={
            isAuthenticated ? 
            <Dashboard user={user} onLogout={handleLogout} /> : 
            <Navigate to="/login" />
          } 
        />
        <Route 
          path="/create-permit" 
          element={
            isAuthenticated ? 
            <CreatePermit user={user} onLogout={handleLogout} /> : 
            <Navigate to="/login" />
          } 
        />
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Router>
  );
}

export default App;

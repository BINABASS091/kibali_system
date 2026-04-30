import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { permitAPI } from '../api';
import './Dashboard.css';

function Dashboard({ user, onLogout }) {
  const [permits, setPermits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadPermits();
  }, []);

  const loadPermits = async () => {
    try {
      setLoading(true);
      const response = await permitAPI.list();
      setPermits(response.data);
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Session imeisha. Tafadhali ingia tena.');
        onLogout();
        navigate('/login');
        return;
      }

      setError('Hitilafu katika kupakia permits');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  const downloadPDF = async (permitId, permitNumber) => {
    try {
      const response = await permitAPI.download(permitId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${permitNumber}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      alert('Hitilafu katika kudownload PDF');
      console.error('Error:', err);
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>KIBALI CHA UJENZI - DASHIBODI</h1>
          <div className="user-info">
            <span>Karibu, {user?.username}</span>
            <button onClick={handleLogout} className="btn-logout">Toka</button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-container">
          <div className="action-buttons">
            <button 
              onClick={() => navigate('/create-permit')} 
              className="btn btn-primary btn-lg"
            >
              + Unda Kibali Kipya
            </button>
            <button 
              onClick={loadPermits} 
              className="btn btn-secondary btn-lg"
            >
              Upya
            </button>
          </div>

          {error && <div className="error-message">{error}</div>}

          {loading ? (
            <div className="loading">Inatumia...</div>
          ) : permits.length === 0 ? (
            <div className="no-data">
              <p>Hakuna kibali</p>
            </div>
          ) : (
            <div className="permits-table-container">
              <table className="permits-table">
                <thead>
                  <tr>
                    <th>Namba</th>
                    <th>Jina</th>
                    <th>Aina</th>
                    <th>Mahali</th>
                    <th>Tarehe</th>
                    <th>Hatua</th>
                  </tr>
                </thead>
                <tbody>
                  {permits.map((permit) => (
                    <tr key={permit.id}>
                      <td className="permit-number">{permit.permit_number}</td>
                      <td>{permit.jina}</td>
                      <td>{permit.aina}</td>
                      <td>{permit.pahala}</td>
                      <td>{new Date(permit.tarehe_kutolewa).toLocaleDateString('sw-TZ')}</td>
                      <td className="actions">
                        <button
                          onClick={() => downloadPDF(permit.id, permit.permit_number)}
                          className="btn-small btn-download"
                          title="Download PDF"
                        >
                          ↓ PDF
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default Dashboard;

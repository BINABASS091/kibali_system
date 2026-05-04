import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { permitAPI } from '../api';
import './VerifyPermit.css';

function VerifyPermit() {
  const { permitNumber } = useParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [data, setData] = useState(null);

  useEffect(() => {
    const verify = async () => {
      setLoading(true);
      setError('');

      try {
        const response = await permitAPI.verify(permitNumber);
        setData(response.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setError('Kibali hiki hakijapatikana kwenye mfumo.');
        } else {
          setError('Imeshindikana kuhakiki kibali kwa sasa. Jaribu tena.');
        }
      } finally {
        setLoading(false);
      }
    };

    verify();
  }, [permitNumber]);

  const permit = data?.permit;
  const isValid = data?.is_valid;

  return (
    <div className="verify-page">
      <div className="verify-card">
        <h1>Uhakiki wa Kibali</h1>
        <p className="permit-ref">Namba: {permitNumber}</p>

        {loading && <p>Inahakiki kibali...</p>}

        {!loading && error && <div className="verify-error">{error}</div>}

        {!loading && !error && permit && (
          <>
            <div className={`verify-status ${isValid ? 'valid' : 'expired'}`}>
              {isValid ? 'HALALI' : 'IMEISHA MUDA'}
            </div>

            <div className="verify-grid">
              <div><strong>Mwombaji:</strong> {permit.jina}</div>
              <div><strong>Aina ya Ujenzi:</strong> {permit.aina}</div>
              <div><strong>Mahali:</strong> {permit.pahala}</div>
              <div><strong>Shehia:</strong> {permit.shehia}</div>
              <div><strong>Tarehe ya Kutolewa:</strong> {permit.tarehe_kutolewa}</div>
              <div><strong>Tarehe ya Mwisho:</strong> {permit.tarehe_mwisho}</div>
            </div>
          </>
        )}

        <div className="verify-actions">
          <Link to="/login" className="verify-link">Ingia Mfumo</Link>
        </div>
      </div>
    </div>
  );
}

export default VerifyPermit;

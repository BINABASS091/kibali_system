import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { permitAPI } from '../api';
import './CreatePermit.css';

function CreatePermit({ user, onLogout }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [createdPermit, setCreatedPermit] = useState(null);

  const [formData, setFormData] = useState({
    jina: '',
    aina: 'NYUMBA',
    pahala: '',
    shehia: '',
    kaskazini: '',
    mashariki: '',
    magharibi: '',
    kusini: '',
    upana: '',
    urefu: '',
    tarehe_mwisho: '',
  });

  const constructionTypes = [
    { value: 'UKUTA', label: 'Ukuta (Wall)' },
    { value: 'NYUMBA', label: 'Nyumba (House)' },
    { value: 'JENGO', label: 'Jengo (Building)' },
    { value: 'KIWANDA', label: 'Kiwanda (Factory)' },
    { value: 'DUKA', label: 'Duka (Shop)' },
    { value: 'OFISI', label: 'Ofisi (Office)' },
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await permitAPI.create(formData);
      setCreatedPermit(response.data);
      setSuccess(true);

      if (response.data?.id) {
        const pdfResponse = await permitAPI.download(response.data.id);
        const blob = new Blob([pdfResponse.data], { type: 'application/pdf' });
        const pdfUrl = window.URL.createObjectURL(blob);
        window.open(pdfUrl, '_blank', 'noopener,noreferrer');
      }
    } catch (err) {
      setError('Hitilafu katika kuunda kibali: ' + (err.response?.data?.detail || 'Jaribu tena'));
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!createdPermit?.id) return;

    try {
      const response = await permitAPI.download(createdPermit.id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${createdPermit.permit_number || 'kibali'}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Imeshindikana kudownload PDF. Jaribu tena.');
      console.error('Download error:', err);
    }
  };

  const handleOpenPdf = async () => {
    if (!createdPermit?.id) return;

    try {
      const response = await permitAPI.download(createdPermit.id);
      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
      window.open(url, '_blank', 'noopener,noreferrer');
    } catch (err) {
      setError('Imeshindikana kufungua PDF. Jaribu tena.');
      console.error('Open PDF error:', err);
    }
  };

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  return (
    <div className="create-permit">
      <header className="header">
        <div className="header-content">
          <h1>UNDA KIBALI KIPYA</h1>
          <div className="user-info">
            <span>Karibu, {user?.username}</span>
            <button onClick={handleLogout} className="btn-logout">Toka</button>
          </div>
        </div>
      </header>

      <main className="create-permit-main">
        <div className="form-container">
          {success && (
            <div className="success-message">
              Kibali kimeundwa kwa ufanisi.
              {createdPermit?.permit_number ? ` Namba: ${createdPermit.permit_number}` : ''}
              <div className="form-actions" style={{ marginTop: '12px' }}>
                <button type="button" className="btn btn-primary" onClick={handleOpenPdf}>
                  Fungua PDF
                </button>
                <button type="button" className="btn btn-secondary" onClick={handleDownloadPdf}>
                  Download PDF
                </button>
                <button type="button" className="btn btn-secondary" onClick={() => navigate('/dashboard')}>
                  Rudi Dashibodi
                </button>
              </div>
            </div>
          )}

          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleSubmit} className="permit-form">
            {/* Section 1: Applicant Information */}
            <fieldset className="form-section">
              <legend>HABARI ZA MGOMBEZI</legend>
              
              <div className="form-group">
                <label htmlFor="jina">Jina la Mgombezi *</label>
                <input
                  type="text"
                  id="jina"
                  name="jina"
                  value={formData.jina}
                  onChange={handleChange}
                  required
                  placeholder="Ingiza jina la mgombezi"
                />
              </div>
            </fieldset>

            {/* Section 2: Construction Details */}
            <fieldset className="form-section">
              <legend>MAELEZO YA JENGO</legend>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="aina">Aina ya Ujenzi *</label>
                  <select
                    id="aina"
                    name="aina"
                    value={formData.aina}
                    onChange={handleChange}
                    required
                  >
                    {constructionTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="pahala">Mahali (Location) *</label>
                  <input
                    type="text"
                    id="pahala"
                    name="pahala"
                    value={formData.pahala}
                    onChange={handleChange}
                    required
                    placeholder="Mahali"
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="shehia">Shehia / Kata *</label>
                <input
                  type="text"
                  id="shehia"
                  name="shehia"
                  value={formData.shehia}
                  onChange={handleChange}
                  required
                  placeholder="Shehia / Kata"
                />
              </div>
            </fieldset>

            {/* Section 3: Land Boundaries */}
            <fieldset className="form-section">
              <legend>MIPAKA YA ARDHI</legend>
              
              <div className="form-row-2col">
                <div className="form-group">
                  <label htmlFor="kaskazini">Kaskazini (North) *</label>
                  <input
                    type="text"
                    id="kaskazini"
                    name="kaskazini"
                    value={formData.kaskazini}
                    onChange={handleChange}
                    required
                    placeholder="Kaskazini"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="mashariki">Mashariki (East) *</label>
                  <input
                    type="text"
                    id="mashariki"
                    name="mashariki"
                    value={formData.mashariki}
                    onChange={handleChange}
                    required
                    placeholder="Mashariki"
                  />
                </div>
              </div>

              <div className="form-row-2col">
                <div className="form-group">
                  <label htmlFor="magharibi">Magharibi (West) *</label>
                  <input
                    type="text"
                    id="magharibi"
                    name="magharibi"
                    value={formData.magharibi}
                    onChange={handleChange}
                    required
                    placeholder="Magharibi"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="kusini">Kusini (South) *</label>
                  <input
                    type="text"
                    id="kusini"
                    name="kusini"
                    value={formData.kusini}
                    onChange={handleChange}
                    required
                    placeholder="Kusini"
                  />
                </div>
              </div>
            </fieldset>

            {/* Section 4: Measurements */}
            <fieldset className="form-section">
              <legend>VIPIMO VYA JENGO</legend>
              
              <div className="form-row-2col">
                <div className="form-group">
                  <label htmlFor="upana">Upana (Width) - Mita *</label>
                  <input
                    type="number"
                    id="upana"
                    name="upana"
                    value={formData.upana}
                    onChange={handleChange}
                    required
                    step="0.01"
                    placeholder="Upana"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="urefu">Urefu (Height) - Mita *</label>
                  <input
                    type="number"
                    id="urefu"
                    name="urefu"
                    value={formData.urefu}
                    onChange={handleChange}
                    required
                    step="0.01"
                    placeholder="Urefu"
                  />
                </div>
              </div>
            </fieldset>

            {/* Section 5: Dates */}
            <fieldset className="form-section">
              <legend>TAREHE</legend>
              
              <div className="form-group">
                <label htmlFor="tarehe_mwisho">Tarehe ya Mwisho (Expiry Date) *</label>
                <input
                  type="date"
                  id="tarehe_mwisho"
                  name="tarehe_mwisho"
                  value={formData.tarehe_mwisho}
                  onChange={handleChange}
                  required
                />
                <small>Tarehe ya kutolewa itawekwa kwa sasa</small>
              </div>
            </fieldset>

            {/* Form Actions */}
            <div className="form-actions">
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Inatumia...' : 'Unda Kibali'}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => navigate('/dashboard')}
              >
                Ghairi
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}

export default CreatePermit;

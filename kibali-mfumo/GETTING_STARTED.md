# Kibali cha Ujenzi System - Complete Setup Guide

**Building Permit Management System for Zanzibar Government**

## 🚀 Quick Start (10 minutes)

### What You're Building
A full-stack web application where government officers can:
- Log in with JWT authentication
- Create building permits with details
- Auto-generate official permit numbers (KU-0001, etc.)
- Generate professional PDF documents
- View and download their permits

### System Architecture
```
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│  React Frontend  │  ←→     │  Django Backend  │  ←→     │  PostgreSQL DB   │
│  (Vite)          │ HTTP    │  (REST API)      │ SQL     │  (kibali_db)     │
│ :5173            │         │  :8000           │         │                  │
└──────────────────┘         └──────────────────┘         └──────────────────┘
```

---

## 📋 Prerequisites

Check you have these installed:

```bash
python3 --version          # Should be 3.8+
node --version            # Should be 16+
npm --version             # Should be 8+
```

If you don't have PostgreSQL, install it:
```bash
# macOS
brew install postgresql

# Linux (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib
```

---

## 📂 Your Project Structure

Everything is already created at:
```
/Users/phantomx/Desktop/bin-abass/kibali/kibali-mfumo/
├── backend/                  # Django application
├── frontend/                 # React application  
├── README.md                # Full documentation
├── SETUP.md                 # This file (expanded)
├── ARCHITECTURE.md          # Technical details
├── QUICK_REFERENCE.md       # Commands reference
└── CHECKLIST.md             # Verification checklist
```

---

## 🔧 Step-by-Step Installation

### Phase 1: Database Setup (2 minutes)

Start PostgreSQL:
```bash
# macOS with Homebrew
brew services start postgresql

# Verify it's running
brew services list
# Should show: postgresql started
```

Create database:
```bash
# Start PostgreSQL shell
psql postgres

# In the PostgreSQL prompt, run these commands:
CREATE DATABASE kibali_db;
CREATE USER postgres WITH PASSWORD 'password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET default_transaction_deferrable TO off;
ALTER ROLE postgres SET default_timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE kibali_db TO postgres;
\q
```

✅ **Database Ready**

### Phase 2: Backend Setup (3 minutes)

```bash
# Navigate to backend
cd /Users/phantomx/Desktop/bin-abass/kibali/kibali-mfumo/backend

# Create Python virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
# Your terminal should now show (venv) at the start

# Install Python packages
pip install -r requirements.txt

# Initialize database with Django migrations
python manage.py migrate

# Create admin account (you'll be prompted)
python manage.py createsuperuser
# Follow the prompts:
# Username: admin
# Email: admin@kibali.go.tz
# Password: (choose a strong password, you'll need it)
# Password (again): (confirm)

# Create test officer user
python manage.py shell
```

In the Python shell that appears:
```python
from django.contrib.auth.models import User
from kibali_app.models import KibaliUser

# Create officer user
officer = User.objects.create_user(
    username='officer1',
    email='officer@kibali.go.tz',
    password='officer123'
)
KibaliUser.objects.create(user=officer, role='officer')

# Add admin role to admin user
admin_user = User.objects.get(username='admin')
KibaliUser.objects.create(user=admin_user, role='admin')

exit()
```

✅ **Backend Ready**

### Phase 3: Frontend Setup (2 minutes)

In a NEW terminal (keep backend running):
```bash
# Navigate to frontend
cd /Users/phantomx/Desktop/bin-abass/kibali/kibali-mfumo/frontend

# Install Node packages
npm install

# This may take 1-2 minutes...
```

✅ **Frontend Ready**

### Phase 4: Start the System (2 minutes)

Keep everything running in separate terminals:

**Terminal 1 - Backend (keep running):**
```bash
cd /Users/phantomx/Desktop/bin-abass/kibali/kibali-mfumo/backend
source venv/bin/activate
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Terminal 2 - Frontend (new terminal, keep running):**
```bash
cd /Users/phantomx/Desktop/bin-abass/kibali/kibali-mfumo/frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:5173/
```

**Terminal 3 - Optional (for database access):**
```bash
psql -U postgres -d kibali_db
```

---

## 🌐 Access the System

### Open in Browser
Go to: **http://localhost:5173**

You should see the login page with "KIBALI CHA UJENZI" title.

### Login Credentials

**Option 1 - Test Officer:**
- Username: `officer1`
- Password: `officer123`

**Option 2 - Administrator:**
- Username: `admin`
- Password: (the password you created during setup)

---

## 📝 Using the System

### Create Your First Permit

1. **Login** using officer credentials
2. Click **"+ Unda Kibali Kipya"** button
3. Fill the form:
   - **Jina** (Name): Enter applicant name
   - **Aina** (Type): Select construction type
   - **Pahala** (Location): Enter location
   - **Shehia** (Ward): Enter ward name
   - **Land Boundaries** (Kaskazini/East/West/South): Enter boundary info
   - **Measurements**: Enter width and height in meters
   - **Tarehe ya Mwisho** (Expiry): Select date
4. Click **"Unda Kibali"** button
5. Wait ~2 seconds for PDF generation
6. Redirected to dashboard

### Download the PDF

- Go to dashboard
- See your created permit in the table
- Click **"↓ PDF"** button
- PDF downloads with permit number as filename
- PDF includes official government formatting

### View All Your Permits

- Dashboard shows all permits you created
- Each row shows: Number, Name, Type, Location, Date
- Click PDF button to download any permit

### Admin Features (if logged in as admin)

- See ALL permits in system (not just own)
- Access Django admin: http://localhost:8000/admin
- Manage users and permits directly

---

## 🛠️ Common Issues & Solutions

### Issue: "Connection refused" when starting Django
**Solution:** PostgreSQL isn't running
```bash
brew services start postgresql
# Wait 5 seconds for it to start
```

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:** Virtual environment not activated
```bash
cd backend
source venv/bin/activate
# (venv) should appear at start of prompt
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution:** Run on different port
```bash
python manage.py runserver 8001
# Then update API_BASE_URL in frontend/src/api.js to 'http://localhost:8001/api'
```

### Issue: "Port 5173 already in use"
**Solution:** Vite will use next available port
```bash
npm run dev -- --port 5174
```

### Issue: PDF not generating / WeasyPrint errors
**Solution:** Install system dependencies
```bash
# macOS
brew install cairo pango gdk-pixbuf libffi
pip install --upgrade WeasyPrint

# Ubuntu/Debian
sudo apt-get install libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libffi-dev
```

### Issue: "CORS error" when creating permit
**Solution:** Make sure both servers are running on correct ports
```bash
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# Check frontend/src/api.js has correct API_BASE_URL
```

### Issue: Login page shows blank/infinite loading
**Solution:** Check backend is running
```bash
# Terminal with backend should show:
# Starting development server at http://127.0.0.1:8000/
```

---

## 📊 API Endpoints (Reference)

All endpoints require JWT token except login:

```
POST   /api/login/                    # Login
POST   /api/permits/create/           # Create permit
GET    /api/permits/                  # List permits
GET    /api/permits/{id}/             # Get permit
GET    /api/permits/{id}/download/    # Download PDF
```

---

## 🔐 Default Database Credentials

```
Database: kibali_db
Username: postgres
Password: password
Host: localhost
Port: 5432
```

To connect manually:
```bash
psql -U postgres -d kibali_db
\dt                    # List tables
SELECT * FROM kibali_app_permit;
\q                     # Exit
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/kibali_app/models.py` | Database models |
| `backend/kibali_app/views.py` | API endpoints |
| `backend/templates/permit.html` | PDF template (customize here) |
| `frontend/src/pages/CreatePermit.jsx` | Permit form |
| `frontend/src/pages/Dashboard.jsx` | Permit list |
| `frontend/src/api.js` | API client |

---

## 🎨 Customization Quick Tips

### Change PDF Styling
Edit: `backend/templates/permit.html`
- Modify colors, borders, fonts
- Change layout of sections
- Add/remove fields

### Add New Fields to Permit
1. Edit `backend/kibali_app/models.py` - add to Permit model
2. Run: `python manage.py makemigrations && python manage.py migrate`
3. Edit `backend/kibali_app/serializers.py` - add to PermitSerializer
4. Edit `frontend/src/pages/CreatePermit.jsx` - add form input
5. Edit `backend/templates/permit.html` - display in PDF

### Change API URL
Edit: `frontend/src/api.js`
```javascript
const API_BASE_URL = 'http://localhost:8000/api';  // Change this line
```

---

## ✅ Verification Checklist

After setup, verify everything works:

```bash
# 1. Database connected
psql -U postgres -d kibali_db -c "SELECT 1;"
# Should print: (1 row)

# 2. Backend running
curl http://localhost:8000/admin/
# Should show HTML admin page (not error)

# 3. Frontend running
curl http://localhost:5173
# Should show HTML

# 4. API working
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"officer1","password":"officer123"}'
# Should return JSON with access_token
```

---

## 📚 Additional Resources

- **Full README:** See `README.md` for detailed documentation
- **Quick Reference:** See `QUICK_REFERENCE.md` for commands
- **Architecture:** See `ARCHITECTURE.md` for system design
- **Django Docs:** https://docs.djangoproject.com/
- **React Docs:** https://react.dev/

---

## 🔄 Stopping the System

When done, press `Ctrl+C` in each terminal:

**Terminal 1 (Backend):**
```
^C (Ctrl+C)
Shutting down...
```

**Terminal 2 (Frontend):**
```
^C (Ctrl+C)
```

To stop PostgreSQL:
```bash
brew services stop postgresql
```

---

## 📱 Mobile/Remote Access

For other devices on your network:

1. Find your machine's IP:
```bash
ifconfig | grep "inet "
# Look for something like 192.168.1.x
```

2. Update frontend API:
Edit `frontend/src/api.js`:
```javascript
const API_BASE_URL = 'http://192.168.1.100:8000/api';  // Use your IP
```

3. Update backend CORS:
Edit `backend/kibali_project/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://192.168.1.100:5173',  # Add your IP
]
```

4. Access from other device:
```
http://192.168.1.100:5173
```

---

## 🚀 Next Steps

1. **Customize:** Modify PDF template and form fields
2. **Deploy:** Set up on production server
3. **Users:** Create actual government officer accounts
4. **Training:** Train users on the system
5. **Backup:** Configure database backups

---

## 📞 Troubleshooting Support

1. **Check logs:** Look at terminal output
2. **Check browser console:** F12 → Console tab
3. **Check database:** `psql -U postgres -d kibali_db`
4. **Verify all servers running:** Check all 3 terminals
5. **Restart everything:** Kill all processes and start fresh

---

## ✨ Success Indicators

You know everything is working when:

✅ Can login at `http://localhost:5173`  
✅ Dashboard loads with permit list  
✅ Can create new permit  
✅ PDF generates and downloads  
✅ No errors in browser console  
✅ No errors in terminal output  

---

**Congratulations! 🎉 Your Kibali cha Ujenzi system is ready to use!**

For questions, refer to the detailed documentation files or check the Django/React/PostgreSQL official documentation.

**Happy Building! 🏗️**

# Setup Guide for Kibali cha Ujenzi System

## Quick Start (5 minutes)

### Prerequisites Check
```bash
python3 --version        # Should be 3.8+
node --version          # Should be 16+
npm --version           # Should be 8+
brew services list      # Check if PostgreSQL is available
```

### Step 1: Setup PostgreSQL Database

```bash
# Start PostgreSQL
brew services start postgresql

# Create database and user
psql postgres

# In PostgreSQL shell, run:
CREATE DATABASE kibali_db;
CREATE USER postgres WITH PASSWORD 'password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET default_transaction_deferrable TO off;
ALTER ROLE postgres SET default_timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE kibali_db TO postgres;
\q
```

### Step 2: Setup Backend

**Terminal 1:**
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Create test users
python manage.py shell
```

**In Python shell:**
```python
from django.contrib.auth.models import User
from kibali_app.models import KibaliUser

# Create officer
officer = User.objects.create_user('officer1', 'officer@kibali.go.tz', 'officer123')
KibaliUser.objects.create(user=officer, role='officer')

# Create admin role
admin_user = User.objects.get(username='admin')
KibaliUser.objects.create(user=admin_user, role='admin')

exit()
```

**Start backend server:**
```bash
python manage.py runserver
```

### Step 3: Setup Frontend

**Terminal 2:**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Step 4: Access the Application

Open browser: `http://localhost:5173`

**Login with:**
- Username: `officer1`
- Password: `officer123`

Or:
- Username: `admin`
- Password: (your superuser password)

## Common Issues & Solutions

### PostgreSQL Connection Error
```bash
# Check if PostgreSQL is running
brew services list

# Start PostgreSQL if not running
brew services start postgresql

# Verify connection
psql -U postgres -d kibali_db
```

### Port Already in Use (8000)
```bash
# Use different port
python manage.py runserver 8001

# Then update in frontend/src/api.js:
# API_BASE_URL = 'http://localhost:8001/api'
```

### npm install errors
```bash
# Clear npm cache
npm cache clean --force

# Try again
npm install
```

### WeasyPrint/PDF errors
```bash
# Install system dependencies (macOS)
brew install cairo pango gdk-pixbuf libffi

# Reinstall WeasyPrint
pip install --upgrade WeasyPrint
```

## Directory Structure Created

```
backend/
├── kibali_project/     # Django config
├── kibali_app/         # App code
├── templates/          # PDF template
├── media/              # Generated PDFs
├── venv/               # Virtual environment
├── manage.py
└── requirements.txt

frontend/
├── src/                # React components
│   ├── pages/
│   ├── api.js
│   └── App.jsx
├── index.html
├── package.json
└── vite.config.js
```

## Next Steps

1. **Customize** the PDF template at `backend/templates/permit.html`
2. **Add fields** to the permit form as needed
3. **Configure** database credentials if not using defaults
4. **Deploy** to production when ready

## Useful Commands

```bash
# Backend
python manage.py migrate              # Apply migrations
python manage.py createsuperuser      # Create admin
python manage.py shell                # Django shell
python manage.py collectstatic        # Collect static files

# Frontend
npm install                           # Install dependencies
npm run dev                          # Start dev server
npm run build                        # Build for production
npm run preview                      # Preview production build

# PostgreSQL
psql -U postgres -d kibali_db        # Connect to database
\dt                                  # List tables
\q                                   # Quit
```

## Verification

After setup, verify everything works:

1. **Backend:** Visit `http://localhost:8000/admin` - should show Django admin login
2. **Frontend:** Visit `http://localhost:5173` - should show Kibali login page
3. **API:** Visit `http://localhost:8000/api/login/` - should show login endpoint
4. **Database:** `psql -U postgres -d kibali_db` - should connect successfully

All green? You're ready to use the system! 🎉
